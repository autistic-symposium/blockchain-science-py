# -*- encoding: utf-8 -*-
# src/markets/bybit.py
# author: steinkirch
# Bybit API class.

import time
import asyncio 
import datetime
from pybit import HTTP
from pybit.spot import WebSocket as SpotWebSocket
from pybit.usdt_perpetual import WebSocket as LinearWebSocket
from pybit.inverse_perpetual import WebSocket as InverseWebSocket

import src.utils.os as utils

class BybitCex():

    def __init__(self, env_vars: dict, currency=None, ws=False, market=None):
    
        self._env_vars = env_vars
        self._currency = currency or 'USDT'
        self._is_websocket = ws
        self._market_type = market

        self._is_public = bool(env_vars['IS_PUBLIC'])
        self._is_test = bool(self._env_vars['IS_TESTNET'])
        self._timeframe = env_vars['TIMEFRAME']
        self._kline_limit = int(env_vars['KLINE_LIMIT'])
    
        self._api_key = None
        self._api_secret = None
        self._symbols_dict = None
        
        self._url = self._set_url()
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
            self._api_key = self._env_vars['BYBIT_API_KEY']
            self._api_secret = self._env_vars['BYBIT_API_SECRET']

        return self._env_vars['BYBIT_WS_PRIVATE'] \
                if self._is_websocket else self._env_vars['BYBIT_HTTP']

    def _start_bybit_session(self) -> object:
        """Start a bybit session."""
        
        if self._is_websocket:
            if self._is_public:
                if self._market_type == 'INVERSE':
                    return InverseWebSocket(test=self._is_test)
                elif self._market_type == 'SPOT':
                    return SpotWebSocket(test=self._is_test)
                elif self._market_type == 'LINEAR':
                    return LinearWebSocket(test=self._is_test)
            
            else:
                if self._market_type == 'INVERSE':
                    return InverseWebSocket(api_key=self._api_key, 
                                            api_secret=self._api_secret, 
                                            test=self._is_test)
                elif self._market_type == 'SPOT':
                    return SpotWebSocket(api_key=self._api_key, 
                                        api_secret=self._api_secret, 
                                        test=self._is_test)
                elif self._market_type == 'LINEAR':
                    return LinearWebSocket(api_key=self._api_key, 
                                            api_secret=self._api_secret, 
                                            test=self._is_test)
        else:
            return HTTP(self._url, 
                        self._api_key, 
                        self._api_secret)

    def _change_session(self, is_public: bool, ws=False) -> None:
        """Change session to private or public session."""

        self._is_websocket = ws
        self._is_public = is_public
        self._url = self._set_url()
        self._session = self._start_bybit_session()

    def _parse_symbols(self, coin: str) -> list:
        """Parse coin data for cex data"""

        result = []
        symbols = {}

        try:
            if 'ret_msg' in self._symbols_dict.keys() and \
                self._symbols_dict['ret_msg'] == 'OK':
                    symbols = self._symbols_dict['result']
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

        if self._timeframe == '60':
            from_time = datetime.datetime.now() - datetime.timedelta(hours=self._kline_limit)
        elif self._timeframe == 'D':
            from_time = datetime.datetime.now() - datetime.timedelta(days=self._kline_limit)
        elif self._timeframe == 'W':
            from_time = datetime.datetime.now() - datetime.timedelta(weeks=self._kline_limit)
        else:
            utils.exit_with_error(f'TIMEFRAME {self._timeframe} not supported.')
        
        return int(from_time.timestamp())

    def _get_price_klines(self, coin: str) -> dict:
        """Get price history for a given symbol."""

        from_time = self._get_timeframe()

        try:
            prices = self._session.query_mark_price_kline(
                    symbol=coin,
                    interval=self._timeframe,
                    from_time=from_time,
                    limit=self._kline_limit
                )

            utils.log_info(f'Retrieving k-lines for {coin}: {prices["result"]}')
            time.sleep(0.1)

            # make sure both series are the same length
            if len(prices['result']) == self._kline_limit:
                return prices['result']

            else:
                utils.log_error(f'Could not get k-lines for {coin}: {prices}')


        except Exception as e:
            utils.log_error(f'Could not get k-lines for {coin}: {e}')


    def _handle_orderbook_ws(self, msg: dict) -> None:
        """Handle orderbook data from websocket."""
        utils.pprint(msg['data'])

    def _get_side(self, direction: str) -> str:
        """Get side for order."""
            
        if direction.upper() == 'LONG':
            return 'Buy'
        elif direction.upper() == 'SHORT':
            return 'Sell'


    ########################################
    #    public methods                    #    
    #                public and stats      #
    ########################################

    def get_derivative_currency_info(self) -> list:
        """Get tradeable data for a given currency."""

        self._symbols_dict = self._symbols_dict or \
                                    self._session.query_symbol()
    
        return self._parse_symbols(self._currency)

    def get_price_history(self) -> dict:
        """Get and store price history for all available pairs."""

        price_history = {}
        coin_info = self.get_derivative_currency_info()

        for this_coin in coin_info:
            try:
                ticker = this_coin['name']
                this_price_history = self._get_price_klines(ticker)

                if this_price_history is not None:
                    price_history[ticker] = this_price_history

            except KeyError as e:
                utils.exit_with_error(f'Could not retrieve price history: {e}')

        return price_history  

    async def orderbook_ws(self, coin1: str, coin2: str, handling_func=None) -> None:
        """Connect to websocket for spot or inverse orderbook."""
        
        handling_func = handling_func or self._handle_orderbook_ws

        while True:

            if self._market_type == 'INVERSE':
                self._session.orderbook_25_stream(handling_func, [coin1, coin2])
                
            elif self._market_type == 'SPOT':
                self._session.trade_v1_stream(handling_func, [coin1, coin2])
                
            elif self._market_type == 'LINEAR':
                self._session.orderbook_25_stream(handling_func,[coin1, coin2])
            
            else:
                utils.exit_with_error(f"Can't connect to {self._market_type} orderbook ws.")

            await asyncio.sleep(10)

    def open_orderbook_ws(self, coin1: str, coin2: str) -> None:
        """Open websocket for spot, linear, or inverse orderbook."""
        
        asyncio.get_event_loop().run_until_complete(self.orderbook_ws(coin1, coin2))
            

    ########################################
    #    public methods                    #    
    #                        positions     #
    ########################################

    def set_leverage(self, ticker: str, is_isolated: bool, 
                           buy_leverage: int, sell_leverage: int) -> None:
        """Set leverage for a given ticker."""
        
        self._change_session(is_public=False)

        try:
            self._session.cross_isolated_margin_switch(
                symbol=ticker,
                is_isolated=is_isolated,
                buy_leverage=buy_leverage,
                sell_leverage=sell_leverage
            )
        except Exception as e:
            utils.log_error(f'Could not set leverage for {ticker}: {e}')
    
    def place_order(self, ticker: str, price: float, quantity: int, direction: str) -> dict:
        """Place an order for a given ticker."""

        side = self._get_side(direction)
        self._change_session(is_public=False)

        try:
            if self._env_vars['ORDER_TYPE'] == 'LIMIT':
                self._session.place_active_order(
                        symbol=ticker,
                        side=side,
                        order_type=self._env_vars['ORDER_TYPE'],
                        qty=quantity,
                        price=price,
                        time_in_force="PostOnly",
                        reduce_only=False,
                        close_on_trigger=False,
                        stop_loss=self._env_vars['STOP_LOSS'],
                    )
            elif self._env_vars['ORDER_TYPE'] == 'MARKET':
                self._session.place_active_order(
                        symbol=ticker,
                        side=side,
                        order_type=self._env_vars['ORDER_TYPE'],
                        qty=quantity,
                        time_in_force="PostOnly",
                        reduce_only=False,
                        close_on_trigger=False,
                        stop_loss=self._env_vars['STOP_LOSS'],
                    )
            
        except Exception as e:
            utils.log_error(f'Could not place order for {ticker}: {e}')
