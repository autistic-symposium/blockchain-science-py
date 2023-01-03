# -*- encoding: utf-8 -*-
# src/strategies/cointegration.py
# author: steinkirch
# Cointegration class.


import math
import pandas as pd
import numpy as np
import statsmodels.api as sm
from statsmodels.tsa.stattools import coint

import src.utils.os as utils

class Cointegrator:

    def __init__(self, env_vars: dict):
        self._env_vars = env_vars
        self._pvalue = float(self._env_vars['PLIMIT'])


    #########################
    #   private methods     #
    #########################
    def _get_price_history(self) -> dict:
        """Get price history for a given derivative."""
        
        return utils.open_price_history(self._env_vars['OUTPUTDIR'],
                                        self._env_vars['PRICE_HISTORY_FILE'])

    def _extract_close_prices(self, prices_list: list) -> list:
        """Extract all close prices info into a list."""

        close_prices = []

        for prices in prices_list:
            try:
                if not math.isnan(prices["close"]):
                    close_prices.append(prices["close"])
            except KeyError:
                print(f'Could not find close price for {prices}')

        return close_prices

    def _calculate_spread(self, first_set: list, second_set: list, hedge_ratio: float) -> list:
        """Calculate spread."""

        return pd.Series(first_set) - (pd.Series(second_set) * hedge_ratio)

    def _calculate_hedge_ration(self, first_set: list, second_set: list) -> float:
        """Calculate hedge ratio."""

        model = sm.OLS(first_set, second_set)
        return model.fit().params[0]

    def _calculate_cointegration(self, first_set: list, second_set: list) -> dict:
        """Calculate co-integration for two tokens."""

        hot = False
        
        # calculate cointegration
        cointegration = coint(first_set, second_set)
        cointegration_value = cointegration[0]
        pvalue = cointegration[1]
        critical_value = cointegration[2][1]
        
        # calculate hedge ratio
        hedge_ratio = self._calculate_hedge_ration(first_set, second_set)
        
        # calculate spread
        spread = self._calculate_spread(first_set, second_set, hedge_ratio)
        zero_crossings = len(np.where(np.diff(np.sign(spread)))[0])

        # if pvalue is less than 0.05, we can reject the null hypothesis
        if pvalue < self._pvalue and cointegration_value < critical_value:
            hot = True

        return {
                "hot": hot,
                "pvalue": round(pvalue, 3),
                "cointegration_value": cointegration_value,
                "critical_value": critical_value,
                "hedge_ratio": hedge_ratio,
                "zero_crossings": zero_crossings
                }


    ###########################
    #      public methods     #
    ###########################

    def get_cointegration(self) -> dict:
        """Get and store price history for all available pairs."""

        results = []        
        pairs_list = []
        price_history = self._get_price_history()

        for symbol1 in price_history.keys():
            utils.log_info(f'Calculating cointegration for {symbol1}...')

            for symbol2 in price_history.keys():
                if symbol1 != symbol2:

                    this_symbol = "".join(sorted([symbol1, symbol2]))
                    if this_symbol in pairs_list:
                        break

                    first_set = self._extract_close_prices(price_history[symbol1])
                    second_set = self._extract_close_prices(price_history[symbol2])

                    cointegration_dict = self._calculate_cointegration(first_set, second_set)

                    if cointegration_dict['hot'] == True:
                        utils.log_info(f'   ✅ Found a hot pair: {symbol1} and {symbol2}')
                        pairs_list.append(this_symbol)
                        cointegration_dict['symbol1'] = symbol1
                        cointegration_dict['symbol2'] = symbol2
                        results.append(cointegration_dict)
        
        return utils.save_cointegration(results, 'zero_crossings', \
                    self._env_vars['OUTPUTDIR'], self._env_vars['COINTEGRATION_FILE'])


    def get_zscore(self) -> list:
        """Get zscore for a given window."""
        pass

