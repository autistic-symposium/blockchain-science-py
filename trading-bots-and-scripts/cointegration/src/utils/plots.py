# -*- encoding: utf-8 -*-
# src/utils/plots.py
# author: steinkirch
# Methods to plot data.


import matplotlib.pyplot as plt
import src.utils.os as utils


def plot_cointegrated_pair(data: dict, coin1: str, coin2: str, env_vars: dict) -> None:
    """Plot cointegrated pairs."""

    series1 = data[f'{coin1}_perc'].astype(float).values
    series2 = data[f'{coin2}_perc'].astype(float).values

    fig, axis = plt.subplots(3, figsize=(16, 8))
    fig.suptitle(f"{coin1} / {coin2}: Cointegration Analysis")

    axis[0].plot(series1)
    axis[0].plot(series2)
    axis[1].plot(data['spread'])
    axis[1].set_title('Spread')
    axis[2].plot(data['zscore'])
    axis[2].set_title('Z-Score')

    plot_name = f"{coin1}_{coin2}_cointegration.png"
    plot_filename = utils.format_path(env_vars['OUTPUTDIR'], plot_name)
    utils.log_info(f"Saving plot to {plot_filename}")

    plt.savefig(plot_filename)
