
# -*- encoding: utf-8 -*-
# src/stats.py
# author: steinkirch
# Statistics API methods.

import math
import numpy as np
import pandas as pd
import statsmodels.api as sm
import matplotlib.pyplot as plt

from src.utils import open_json, format_path, create_dir


def get_pair_trends(price_history_file, token1, token2, z_score_window) -> None:
    """Plot prices and trends."""

    cointegrated_pairs = get_cointegrated_pairs(price_history_file)
    prices_token1, prices_token2 = 0, 0

    for token, data in cointegrated_pairs.items():
        if token == token1:
            prices_token1 = extract_close_prices(data, 'close')
        elif token == token2:
            prices_token2 = extract_close_prices(data, 'close')
    
    if prices_token1 == 0 or prices_token2 == 0:
        print(f'Could not retrieve prices for {token1}, {token2}')

    cointegration_data = calculate_cointegration(prices_token1, prices_token2, z_score_window)
    
    return {
        'spread': cointegration_data['spread'],
        'zscore': cointegration_data['zscore'],
        'prices_token1': prices_token1,
        'prices_token2': prices_token2,
        'token1': token1,
        'token2': token2
    }


def extract_close_prices(prices, key):
    """Extract all close prices info into a list."""

    close_prices = []
    for price_values in prices:
        if not math.isnan(price_values[key]):
            close_prices.append(float(price_values[key]))

    return close_prices


def get_cointegrated_pairs(price_history_pair) -> dict:
    """Load price history json and return the data."""
    return open_json(price_history_pair)


def calculate_cointegration(series1, series2, z_score_window) -> dict:
    """Calculate co-integration for two tokens."""

    model = sm.OLS(series1, series2).fit()
    hedge_ratio = model.params[0]
    spread = calculate_spread(series1, series2, hedge_ratio)
    zscore = calculate_zscore(spread, z_score_window)
    
    return {
        'hedge_ratio': round(hedge_ratio, 2),
        'spread': len(np.where(np.diff(np.sign(spread)))[0]),
        'zscore': zscore,
        'spread': spread
    }


def calculate_spread(series1, series2, hedge_ratio) -> float:

    return pd.Series(series1) - (pd.Series(series2) * hedge_ratio)


def calculate_zscore(spread, z_score_window) -> float:

    df = pd.DataFrame(spread)

    mean = df.rolling(center=False, window=z_score_window).mean()
    std = df.rolling(center=False, window=z_score_window).std()

    x = df.rolling(center=False, window=1).mean()
    df['ZSCORE'] = (x - mean) / std

    return df['ZSCORE'].astype(float).values


def save_backtest(data, backtest_outfile, outdir) -> None:
    
    df_2 = pd.DataFrame()
    df_2[data['token1']] = data['prices_token1']
    df_2[data['token2']] = data['prices_token2']
    df_2['Spread'] = data['spread']
    df_2['ZScore'] = data['zscore']

    create_dir(outdir) 
    destination = format_path(outdir, backtest_outfile)
    df_2.to_csv(destination)

    print(f'Saved backtest data at {destination}')


def get_percentage_changes(data) -> None:

    token1 = data['token1']
    token2 = data['token2']

    df = pd.DataFrame(columns=[token1, token2])
    
    df[token1] = data['prices_token1']
    df[token2] = data['prices_token2']

    df[f'{token1}_pct'] = df[token1] / data['prices_token1'][0]
    df[f'{token2}_pct'] = df[token2] / data['prices_token2'][0]

    series_1 = df[f'{token1}_pct'].astype(float).values
    series_2 = df[f'{token2}_pct'].astype(float).values

    data['series1'] = series1
    data['series2'] = series2

    return data


def plot_cointegrated_pairs(data) -> None:
    
    fig, axis = plt.subplots(3, figsize=(16, 8))
    fig.suptitle(f"Price + Spread - {data['token1']} vs {data['token2']}")

    axis[0].plot(data['series1'])
    axis[0].plot(data['series2'])
    axis[1].plot(data['spread'])
    axis[2].plot(data['zscore'])

    plt.show()


