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


    # create figure and axis
    figure, axis = plt.subplots(3, figsize=(20, 20))

    # plot title
    figure.suptitle(
        f"Cointegration (timeframe: {env_vars['TIMEFRAME']})",
        fontsize=30,
        fontweight='bold',
        family='monospace',
    )

    # plot series
    axis[0].plot(series1, color='red', label=f'{coin1}', linewidth=2)
    axis[0].plot(series2, color='blue', label=f'{coin2}', linewidth=2)
    axis[0].grid(color="grey", axis="y", linestyle="dotted", linewidth=0.5)
    axis[0].set_title(
        f'Price series for {coin1} vs. {coin2} ', 
        fontweight='bold',
        fontsize=18,
        pad=5,
        loc="left",
    )
    axis[0].set_xlabel(
        'k-line data', 
        fontweight ='bold',
        fontsize=12,
    )


    # plot spread
    axis[1].plot(data['spread'], color='green', linewidth=3)
    axis[1].grid(color="grey", axis="y", linestyle="dotted", linewidth=0.5)
    axis[1].set_title(
        'Spread (first set - second set * hedge ratio)', 
        fontweight='bold',
        fontsize=18,
        pad=5,
        loc="left",
    )
    axis[1].set_xlabel(
        'k-line data', 
        fontweight ='bold',
        fontsize=12,
    )
    axis[1].set_ylabel(
        'k-line data', 
        fontweight ='bold',
        fontsize=12,
    )

    # plot z-score
    axis[2].plot(data['zscore'], color='magenta', linewidth=3)
    axis[2].grid(color="grey", axis="y", linestyle="dotted", linewidth=0.5)
    axis[2].set_title(
        'Z-score', 
        fontweight='bold',
        fontsize=18,
        pad=5,
        loc="left",
    )
    axis[2].set_xlabel(
        'k-line data', 
        fontweight ='bold',
        fontsize=12,
    )
    axis[2].set_ylabel(
        'standard deviations', 
        fontweight ='bold',
        fontsize=12,
    )

    # save plot
    plot_name = f"{coin1}_{coin2}_{env_vars['TIMEFRAME']}_cointegration.png"
    plot_filename = utils.format_path(env_vars['OUTPUTDIR'], plot_name)
    plt.savefig(plot_filename)
    utils.log_info(f"Saving plot to {plot_filename}")
