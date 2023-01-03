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
        self._pvalue_limit = float(self._env_vars['PLIMIT'])
        self._outdir = self._env_vars['OUTPUTDIR']
        self._price_file = self._env_vars['PRICE_HISTORY_FILE']
        self._cointegration_file = self._env_vars['COINTEGRATION_FILE']
        self._backtest_file = self._env_vars['BACKTEST_FILE']
        self._zscore_file = self._env_vars['ZSCORE_FILE']

        self.zscore_list = []
        self.backtest_df = None

    #########################
    #   private methods     #
    #########################
    def _get_price_history(self) -> dict:
        """Get price history for a given derivative."""
        
        return utils.open_price_history(self._outdir, self._price_file)

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

    def _calculate_zscore(self, spread: list) -> list:
        """Calculate zscore."""

        df = pd.DataFrame(spread)

        window = int(self._env_vars['ZSCORE_WINDOW'])
        mean = df.rolling(center=False, window=window).mean()
        std = df.rolling(center=False, window=window).std()
        x = df.rolling(center=False, window=1).mean()
        
        df["zscore"] = (x - mean) / std
        df["zscore"] = df["zscore"].fillna(0)
        df["zscore"] = (spread - np.mean(spread)) / np.std(spread)

        zscore = df["zscore"].astype(float).values
        self.zscore_list.append(zscore)
        return zscore

    def _get_cointegration_for_pair(self, first_set: list, second_set: list) -> dict:
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

        # calculate zscore
        self._calculate_zscore(spread)

        # if pvalue is less than 0.05, we can reject the null hypothesis
        if pvalue < self._pvalue_limit and cointegration_value < critical_value:
            hot = True

        return {
                "hot": hot,
                "pvalue": round(pvalue, 3),
                "cointegration_value": cointegration_value,
                "critical_value": critical_value,
                "hedge_ratio": hedge_ratio,
                "zero_crossings": zero_crossings
                }


    def _save_backtest_data(self, coin1: str, coin2: str) -> None:
        """Save backtest data to file."""

        price_history = self._get_price_history()
        first_set = self._extract_close_prices(price_history[coin1])
        second_set = self._extract_close_prices(price_history[coin2])

        df = pd.DataFrame()
        df['symbol1'] = first_set
        df['symbol2'] = second_set
        df["spread"] = self._calculate_spread(first_set, second_set, self._calculate_hedge_ration(first_set, second_set))
        df["zscore"] = self._calculate_zscore(df["spread"])
        self.backtest_df = df

        utils.save_metrics(self.backtest_df, \
                    self._outdir, self._backtest_file)


    ###########################
    #      public methods     #
    ###########################

    def get_cointegration(self) -> dict:
        """Get and store price history for all available pairs."""

        if utils.file_exists(self._outdir, self._cointegration_file):
            return utils.open_cointegration(self._outdir, self._cointegration_file)

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

                    cointegration_dict = self._get_cointegration_for_pair(first_set, 
                                                                        second_set)

                    if cointegration_dict['hot'] == True:
                        utils.log_info(f'   ✅ Found a hot pair: {symbol1} and {symbol2}')
                        pairs_list.append(this_symbol)
                        cointegration_dict['symbol1'] = symbol1
                        cointegration_dict['symbol2'] = symbol2
                        results.append(cointegration_dict)
        
        utils.save_metrics(self.zscore_list, \
                    self._outdir, self._zscore_file)
        return utils.save_cointegration(results, 'zero_crossings', \
                    self._outdir, self._cointegration_file)


    def get_zscore(self) -> list:
        """Get z-score for a given window."""

        if utils.file_exists(self._outdir, self._zscore_file):
            return utils.metrics(self._outdir, self._zscore_file)
        
        else:   
            self.get_cointegration()
            return pd.DataFrame(self.zscore_list)


    def get_backtests(self, coin1: str, coin2: str) -> pd.DataFrame:
        """Run backtests for all pairs, based on spread and zscore."""

        if utils.file_exists(self._outdir, self._backtest_file):
            return utils.open_metrics(self._outdir, self._backtest_file)
        
        else:   
            self.get_cointegration()
            self._save_backtest_data(coin1, coin2)
            return self.backtest_df
