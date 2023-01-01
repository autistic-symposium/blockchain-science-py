# -*- encoding: utf-8 -*-
# src/buybit.py
# author: steinkirch
# buybit API methods.

import src.utils.os as utils
from pybit.inverse_perpetual import HTTP


class BuybitCex():
    """Methods for Buybit."""

    def __init__(self, env_vars):
        """Initialize Buybit class."""

        self._url = env_vars['BUYBIT_URL']
        self._session = self._start_buybit_session()

    #########################
    #   private methods     #
    #########################
    def _start_buybit_session(self) -> object:
        """Start a buybit session."""
        return HTTP(self._url)

    def _parse_symbols(self, symbols, coin) -> list:
        """Parse coin data for cex data"""

        result = []
        try:
            if symbols['ret_msg'] == 'OK':
                symbols = symbols['result']

            else:
                utils.exit_with_error(f'No data found for {coin}.')
            
            for symbol in symbols:
                if symbol['quote_currency'] == coin and symbol['status'] == 'Trading':
                    result.append(symbol)

        except KeyError as e:
            utils.exit_with_error(f'Could not retrive symbols for {coin}: {e}')

        return result
    

    ###########################
    #      public methods     #
    ###########################

    def get_coin_info(self, coin) -> list:
        """Get tradeable data for a given currency."""

        symbols = self._session.query_symbol()
        return self._parse_symbols(symbols, coin)


    