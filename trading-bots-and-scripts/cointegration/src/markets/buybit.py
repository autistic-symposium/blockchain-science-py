# -*- encoding: utf-8 -*-
# src/buybit.py
# author: steinkirch
# buybit API methods.

import datetime
import src.utils.os as utils
from pybit.inverse_perpetual import HTTP


class BuybitCex():
    """Methods for Buybit."""

    def __init__(self, env_vars):
        """Initialize Buybit class."""

        self._url = env_vars['BUYBIT_URL']
        self.timeframe = env_vars['TIMEFRAME']
        self.kline_limit = int(env_vars['KLINE_LIMIT'])

        self._symbols_dict = None
        self._session = self._start_buybit_session()

    #########################
    #   private methods     #
    #########################
    def _start_buybit_session(self) -> object:
        """Start a buybit session."""
        return HTTP(self._url)

    def _parse_symbols(self, coin) -> list:
        """Parse coin data for cex data"""

        result = []
        symbols = {}

        try:
            if self.symbols_dict['ret_msg'] == 'OK':
                symbols = self.symbols_dict['result']

            else:
                utils.exit_with_error(f'No data found for {coin}.')
            
            for symbol in symbols:
                if symbol['quote_currency'] == coin and symbol['status'] == 'Trading':
                    result.append(symbol)

        except KeyError as e:
            utils.exit_with_error(f'Could not retrieve symbols for {coin}: {e}')

        return result
    

    def _get_start_time(self) -> int:
        """
           Get start time for k-lines, also known as a candlestick chart.
           This is a chart marked with the opening price, closing price, 
           highest price, and lowest price to reflect price changes.
        """

        from_time = 0
        
        if self.timeframe == 'D':
            from_time = datetime.datetime.now() - \
                        datetime.timedelta(days=self.kline_limit)
        elif self.timeframe == '60':
            from_time = datetime.datetime.now() - \
                        datetime.timedelta(hours=self.kline_limit)
        
        else:
            utils.exit_with_error(f'Time frame not implemented:{self.timeframe}')
        
        return int(from_time.timestamp())


    def _get_price_klines(self, ticker) -> dict:
        """
           Get price history for a given symbol.
           https://bybit-exchange.github.io/docs/futuresV2/inverse/#t-markpricekline
        """

        from_time = self._get_start_time()

        try:
            prices = self._session.query_mark_price_kline(
                    symbol = ticker,
                    interval = self.timeframe,
                    from_time = from_time,
                    limit = self.kline_limit
                )
            if len(prices['result']) == self.kline_limit:
                return prices['result']

        except Exception as e:
            utils.log_error(f'Could not get klines for {ticker}: {e}')



    ###########################
    #      public methods     #
    ###########################

    def get_coin_info(self, coin) -> list:
        """Get tradeable data for a given currency."""

        if self._symbols_dict is None:
            self.symbols_dict = self._session.query_symbol()
    
        return self._parse_symbols(coin)


    def get_price_history(self, coin) -> dict:
        """Get and store price history for all available pairs."""

        price_history_dict = {}
        coin_info = self.get_coin_info(coin)

        for this_coin in coin_info:
            utils.pprint(this_coin)
        

            try:
                ticker = this_coin['name']
                price_history = self._get_price_klines(ticker)

                if price_history is not None:
                    price_history_dict[ticker] = price_history

            except KeyError as e:
                utils.exit_with_error(f'Could not retrieve price history for {coin}: {e}')

        return price_history_dict  
    
