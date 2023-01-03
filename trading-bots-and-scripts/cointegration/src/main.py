#!/usr/bin/env python3
# -*- encoding: utf-8 -*-
# src/main.py
# author: steinkirch
# Entry point for cointbot.

import argparse

import src.utils.os as util
import src.utils.bot as bot
import src.utils.backtesting as test
from src.markets.buybit import BuybitCex
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
    parser.add_argument('-t', dest='test', action='store_true', help='Run backtests. \
                            Example: cointbot -t')
    parser.add_argument('-b', dest='bot', action='store_true', help='Deploy and start bot. \
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

        if cex == 'BUYBIT':
            b = BuybitCex(env_vars)
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

        if cex == 'BUYBIT':
            b = BuybitCex(env_vars)
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

        if cex == 'BUYBIT':
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

        if cex == 'BUYBIT':
            s = Cointegrator(env_vars)
            zscore = s.get_zscore()

            if zscore:
                print(zscore)
            else:
                util.exit_with_error(f'No z-score data found for {cex}.')

        else:
            util.exit_with_error(f'CEX not supported: {cex}')


    ############################
    #     Run backtests        #
    ############################
    elif args.test:

        if cex == 'BUYBIT':
            backtests_results = test.run_backtests()

            if backtests_results:
                util.pprint(backtests_results)
    
            else:
                util.exit_with_error(f'Could not run backtests for {cex}.')

        else:
            util.exit_with_error(f'CEX not supported: {cex}')


    ############################
    #     Deploy bot           #
    ############################
    elif args.bot:

        if cex == 'BUYBIT':
            bot_results = bot.run_bot()

            if bot_results:
                util.pprint(bot_results)
    
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
