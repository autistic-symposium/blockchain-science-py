
# -*- encoding: utf-8 -*-
# src/stats.py
# Statistics API methods.

from utils import open_json


def plot_cointegrated_pairs(price_history_file, token1, token2) -> None:
    """Load a dict of cointegrated pairs and plot the data."""
    
    cointegrated_pairs = get_cointegrated_pairs(price_history_file) 
    plot_pair_trends(cointegrated_pairs)


def get_cointegrated_pairs(price_history_pair) -> dict:
    """Load price history json and return the data."""
    return open_json(price_history_pair)


def plot_pair_trends(cointegrated_pairs):
    print('aaa')