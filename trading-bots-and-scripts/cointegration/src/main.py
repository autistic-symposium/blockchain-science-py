#!/usr/bin/env python3
# -*- encoding: utf-8 -*-
# src/main.py
# author: steinkirch
# Entry point for cointbot.


import asyncio
import argparse

import src.utils.os as util
import src.bots.bybit as bbbot
import src.utils.plots as plots
from src.markets.bybit import BybitCex
from src.strategies.cointegration import Cointegrator


def run_menu() -> argparse.ArgumentParser:
    """Run the menu for this module."""

    parser = argparse.ArgumentParser(description='🏭 cointbot 🪙')
    parser.add_argument('-c', dest='coin', nargs=1,
                        help='Get derivatives data for a given currency. \
                            Example: cointbot -d usdt')
    parser.add_argument('-p', dest='price', nargs=1,
                        help='Save price history for a derivative. \
                            Example: cointbot -p usdt')
    parser.add_argument('-i', dest='cointegration', action='store_true',
                        help='Get cointegration history data. \
                            Example: cointbot -i')
    parser.add_argument('-z', dest='zscore', action='store_true',
                        help='Get latest z-core signal. \
                            Example: cointbot -z')
    parser.add_argument('-t', dest='test', nargs=2, help='Generate backtests. \
                            Example: cointbot -t ethusdt btcusdt')
    parser.add_argument('-n', dest='network', nargs=3, help='Test websockets for orderbooks, \
                            for either inverse or spot markets. \
                            Example: cointbot -n ethusdt btcusdt spot')
    parser.add_argument('-b', dest='bot', action='store_true', help='Deploy trading bot. \
                            Example: cointbot -b')

    return parser


def run() -> None:
    """Entry point for this module."""

    parser = run_menu()
    args = parser.parse_args()
    
    env_vars = util.load_config()
    cex = env_vars['CEX'].upper()


    ############################
    #     Get coin info        #
    ############################
    if args.coin:
        coin = args.coin[0].upper()

        if cex == 'BYBIT':
            b = BybitCex(env_vars)
            coin_info = b.get_coin_info(coin)

            if coin_info:
                util.pprint(coin_info)
            else:
                util.exit_with_error(f'No data found for {coin}.')
        else:
            util.exit_with_error(f'CEX not supported: {cex}')

    ############################
    #     Get price history    #
    ############################
    elif args.price:
        coin = args.price[0].upper()

        if cex == 'BYBIT':
            b = BybitCex(env_vars)
            price_history = b.get_price_history(coin)

            if price_history:
                prices_outfile = env_vars['PRICE_HISTORY_FILE']
                outdir = env_vars['OUTPUTDIR']
                util.save_price_history(price_history, outdir, prices_outfile)
            else:
                util.exit_with_error(f'Could not retrieve price history for {coin}')

        else:
            util.exit_with_error(f'CEX not supported: {cex}')

    ############################
    #     Get cointegration    #
    ############################
    elif args.cointegration:

        if cex == 'BYBIT':
            s = Cointegrator(env_vars)
            cointegration = s.get_cointegration()

            if not cointegration.empty:
                print(cointegration)
            else:
                util.exit_with_error(f'No cointegration data found for {cex}.')

        else:
            util.exit_with_error(f'CEX not supported: {cex}')


    ############################
    #     Get zscore           #
    ############################
    elif args.zscore:

        if cex == 'BYBIT':
            s = Cointegrator(env_vars)
            zscore = s.get_zscore()

            if not zscore.empty:
                print(zscore)
            else:
                util.exit_with_error(f'No z-score data found for {cex}.')

        else:
            util.exit_with_error(f'CEX not supported: {cex}')


    ############################
    #     Get backtests        #
    ############################
    elif args.test:
        coin1 = args.test[0].upper()
        coin2 = args.test[1].upper()

        if cex == 'BYBIT':
            s = Cointegrator(env_vars)
            backtests_results = s.get_backtests(coin1, coin2)

            if not backtests_results.empty:
                print(backtests_results)
                plots.plot_cointegrated_pair(backtests_results, coin1, coin2, env_vars)
            else:
                util.exit_with_error(f'Could not get backtests for {cex}.')

        else:
            util.exit_with_error(f'CEX not supported: {cex}')


    ############################
    #     Test network         #
    ############################
    elif args.network:
        coin1 = args.network[0].upper()
        coin2 = args.network[1].upper()
        market = args.network[2].upper()


        if cex == 'BYBIT':
            
            if market == "SPOT":
                b = BybitCex(env_vars, ws=True, inverse=False)
                asyncio.get_event_loop().run_until_complete(b.orderbook_ws(coin1, coin2))

            elif market == "INVERSE":
                b = BybitCex(env_vars, ws=True, inverse=True)
                asyncio.get_event_loop().run_until_complete(b.orderbook_ws(coin1, coin2))
            
            else:
                util.exit_with_error(f'Market not supported: {market}')

        else:
            util.exit_with_error(f'CEX not supported: {cex}')


    ############################
    #     Deploy bot           #
    ############################
    elif args.bot:

        if cex == 'BYBIT':
            bot_results = bbbot.run_bot()

            if bot_results:
                print(bot_results)
            else:
                util.exit_with_error(f'Could not deploy bot for {cex}.')

        else:
            util.exit_with_error(f'CEX not supported: {cex}')


    ############################
    #    Any invalid option    #
    ############################
    else:
        parser.print_help()


if __name__ == "__main__":
    run() 