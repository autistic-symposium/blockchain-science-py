# -*- encoding: utf-8 -*-
# src/markets/bybit.py
# author: steinkirch
# bybit API methods.

import time
import asyncio 
import datetime
import src.utils.os as utils
from pybit import HTTP
from pybit.inverse_perpetual import WebSocket as InverseWebSocket
from pybit.spot import WebSocket as SpotWebSocket

class BybitCex():
    """Methods for Bybit."""

    def __init__(self, env_vars: dict, ws=False, inverse=False):
        """Initialize Bybit class."""

        self._env_vars = env_vars
        self._is_websocket = ws
        self._is_inverse = inverse
        self._is_public = bool(env_vars['IS_PUBLIC'])
        self._url = self._set_url()
        self._api_key = None
        self._api_secret = None
        
        self.timeframe = env_vars['TIMEFRAME']
        self.kline_limit = int(env_vars['KLINE_LIMIT'])

        self._symbols_dict = None
        self._session = self._start_bybit_session()

    #########################
    #   private methods     #
    #########################
    def _set_url(self) -> None:
        """Set the URL for the API."""
        
        if self._is_public:
            if self._is_websocket:
                return self._env_vars['BYBIT_WS_PUBLIC']
            else:
                return self._env_vars['BYBIT_HTTP_PUBLIC']
        else:  
            self._api_key = self._env_vars['BYBIT_API_KEY']
            self._api_secret = self._env_vars['BYBIT_SECRET_KEY']

            if self._is_websocket:
                return self._env_vars['BYBIT_WS_PRIVATE'] 
            else:
                return self._env_vars['BYBIT_HTTP_PRIVATE']

    def _start_bybit_session(self) -> object:
        """Start a bybit session."""
        
        if self._is_websocket:
            if self._is_public and self._is_inverse:
                return InverseWebSocket(
                        test=bool(self._env_vars['IS_TESTNET']))
            elif self._is_public and not self._is_inverse:
                return SpotWebSocket(
                            test=bool(self._env_vars['IS_TESTNET']))
            elif not self._is_public and self._is_inverse:
                return InverseWebSocket(
                        test=bool(self._env_vars['IS_TESTNET']),
                        api_key=self._api_key, 
                        api_secret=self._api_secret)
            else:
                return SpotWebSocket(
                        test=bool(self._env_vars['IS_TESTNET']),
                        api_key=self._api_key, 
                        api_secret=self._api_secret)
        else:
            return HTTP(self._url, 
                        self.api_key, 
                        self.api_secret)

    def _parse_symbols(self, coin: str) -> list:
        """Parse coin data for cex data"""

        result = []
        symbols = {}

        try:
            if 'ret_msg' in self.symbols_dict.keys() and \
                self.symbols_dict['ret_msg'] == 'OK':
                    symbols = self.symbols_dict['result']
            else:
                utils.exit_with_error(f'No data found for {coin}.')
            
            for symbol in symbols:
                if symbol['quote_currency'] == coin and \
                        symbol['status'] == 'Trading':
                    result.append(symbol)

        except KeyError as e:
            utils.exit_with_error(f'Could not retrieve symbols for {coin}: {e}')

        return result

    def _get_timeframe(self) -> int:
        """
           Get start time for k-lines, also known as a candlestick chart.
           This is a chart marked with the opening price, closing price, 
           highest price, and lowest price to reflect price changes.
        """

        from_time = 0

        if self.timeframe == 'D':
            from_time = datetime.datetime.now() - datetime.timedelta(days=self.kline_limit)
        elif self.timeframe == '60':
            from_time = datetime.datetime.now() - datetime.timedelta(hours=self.kline_limit)
        
        else:
            utils.exit_with_error(f'Time frame not implemented:{self.timeframe}')
        
        return int(from_time.timestamp())

    def _get_price_klines(self, coin: str) -> dict:
        """
           Get price history for a given symbol.
           https://bybit-exchange.github.io/docs/futuresV2/linear/#t-markpricekline
        """

        from_time = self._get_timeframe()

        try:
            prices = self._session.query_mark_price_kline(
                    symbol=coin,
                    interval=self.timeframe,
                    from_time=from_time,
                    limit=self.kline_limit
                )

            utils.log_info(f'Retrieving k-lines for {coin}')
            
            time.sleep(0.1)

            if len(prices['result']) == self.kline_limit:
                return prices['result']

        except Exception as e:
            utils.log_error(f'Could not get k-lines for {coin}: {e}')

    def _handle_orderbook_ws(self, msg: dict) -> None:
        """Handle orderbook data from websocket."""
        utils.log_info(msg)
        orderbook_data = msg['data']


    ###########################
    #      public methods     #
    ###########################

    def get_coin_info(self, coin: str) -> list:
        """Get tradeable data for a given currency."""

        if self._symbols_dict is None:
            self.symbols_dict = self._session.query_symbol()
    
        return self._parse_symbols(coin)

    def get_price_history(self, coin: str) -> dict:
        """Get and store price history for all available pairs."""

        price_history_dict = {}
        coin_info = self.get_coin_info(coin)

        for this_coin in coin_info:
            try:
                ticker = this_coin['name']
                price_history = self._get_price_klines(ticker)

                if price_history is not None:
                    price_history_dict[ticker] = price_history

            except KeyError as e:
                utils.exit_with_error(f'Could not retrieve price history for {coin}: {e}')

        return price_history_dict  

    async def orderbook_ws(self, coin1: str, coin2: str) -> None:
        """Connect to websocket for spot or inverse orderbook."""

        while True:
            if self._is_inverse:
                self._session.orderbook_25_stream(
                    self._handle_orderbook_ws, 
                    [coin1, coin2])
            else:
                self._session.depth_v2_stream(
                    self._handle_orderbook_ws, 
                    [coin1, coin2])

            await asyncio.sleep(300)
