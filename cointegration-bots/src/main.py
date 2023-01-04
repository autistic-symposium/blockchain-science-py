#!/usr/bin/env python3
# -*- encoding: utf-8 -*-
# src/main.py
# author: steinkirch
# Entry point for cointbot.


import argparse

import src.utils.os as utils
import src.utils.plots as plots
from src.markets.bybit import BybitCex
from src.bots.bot1 import BbBotOne
from src.strategies.cointegration import Cointegrator


def run_menu() -> argparse.ArgumentParser:
    """Run the menu for this module."""

    parser = argparse.ArgumentParser(description='🏭 cointbot 🪙')
    parser.add_argument('-c', dest='coin', nargs=1,
                        help='Get derivatives data for a derivative currency. \
                            Example: cointbot -d usdt')
    parser.add_argument('-p', dest='price', nargs=1,
                        help='Save price history for a derivative currency. \
                            Example: cointbot -p usdt')
    parser.add_argument('-i', dest='cointegration', nargs=1,
                        help='Get cointegration history data for a derivative \
                            currency. Example: cointbot -i usdt')
    parser.add_argument('-z', dest='zscore',nargs=1,
                        help='Get z-core signal for a cointegrated pair and a \
                            derivative currency. Example: cointbot -z usdt')
    parser.add_argument('-t', dest='test', nargs=2, 
                        help='Generate backtests for a cointegrated pair and a \
                            derivative currency. Example: cointbot -t ethusdt btcusdt')
    parser.add_argument('-n', dest='network', nargs=3, 
                        help='Test websockets for orderbooks, for either inverse, \
                            linear, or spot market, for a cointegrated pair. \
                            Example: cointbot -n ethusd btcusd inverse')
    parser.add_argument('-b', dest='bot', nargs=1, 
                        help='Deploy a trading bot using the cointegrated strategy, \
                            from a options of possible market and pairs strategy. \
                            Example: cointbot -b 1')

    return parser


def run() -> None:
    """Entry point for this module."""

    parser = run_menu()
    args = parser.parse_args()
    
    env_vars = utils.load_config()
    cex = env_vars['CEX'].upper()


    ##########################################
    #     Get derivative currency info       #
    ##########################################
    if args.coin:
        currency = args.coin[0].upper()

        if cex == 'BYBIT':
            b = BybitCex(env_vars, currency)
            info = b.get_derivative_currency_info()

            if info:
                utils.pprint(info)
            else:
                utils.exit_with_error(f'No data found for {currency}.')
        else:
            utils.exit_with_error(f'CEX not supported: {cex}')


    ############################
    #     Get price history    #
    ############################
    elif args.price:
        currency = args.price[0].upper()

        if cex == 'BYBIT':
            b = BybitCex(env_vars, currency)
            info = b.get_price_history()

            if info:
                outfile = env_vars['PRICE_HISTORY_FILE'].format(currency)
                outdir = env_vars['OUTPUTDIR']
                utils.save_price_history(info, outdir, outfile)
            else:
                utils.exit_with_error(f'Could not retrieve price history for {currency}')

        else:
            utils.exit_with_error(f'CEX not supported: {cex}')


    ############################
    #     Get cointegration    #
    ############################
    elif args.cointegration:
        currency = args.cointegration[0].upper()

        if cex == 'BYBIT':
            s = Cointegrator(env_vars, currency)
            info = s.get_cointegration()

            if not info.empty:
                utils.log_info(info)
            else:
                utils.exit_with_error(f'No data found for {currency}.')

        else:
            utils.exit_with_error(f'CEX not supported: {cex}')


    ############################
    #     Get zscore           #
    ############################
    elif args.zscore:
        currency = args.zscore[0].upper()

        if cex == 'BYBIT':
            s = Cointegrator(env_vars, currency)
            info = s.get_zscore()

            if not info.empty:
                utils.log_info(info)
            else:
                utils.exit_with_error(f'No data found for {currency}.')

        else:
            utils.exit_with_error(f'CEX not supported: {cex}')


    ############################
    #     Get backtests        #
    ############################
    elif args.test:
        coin1 = args.test[0].upper()
        coin2 = args.test[1].upper()

        if cex == 'BYBIT':
            s = Cointegrator(env_vars)
            info = s.get_backtests(coin1, coin2)

            if not info.empty:
                utils.log_info(info)
                plots.plot_cointegrated_pair(info, coin1, coin2, env_vars)
            else:
                utils.exit_with_error(f'Could not get backtests for {cex}.')

        else:
            utils.exit_with_error(f'CEX not supported: {cex}')


    ############################
    #     Test network         #
    ############################
    elif args.network:
        coin1 = args.network[0].upper()
        coin2 = args.network[1].upper()
        market = args.network[2].upper()

        if market not in ['INVERSE', 'LINEAR', 'SPOT']:
            utils.exit_with_error(f'Market not supported: {market}')

        if cex == 'BYBIT':
            b = BybitCex(env_vars, ws=True, market=market)
            b.open_orderbook_ws(coin1, coin2)
            
        else:
            utils.exit_with_error(f'CEX not supported: {cex}')


    ############################
    #     Deploy bot           #
    ############################
    elif args.bot:
        bot_number = args.bot[0].upper()
    
        if cex == 'BYBIT':

            if bot_number == '1':
                b = BbBotOne(env_vars)
                success = b.run()
                if not success:
                    utils.exit_with_error(f'Could not deploy bot for {cex}.')
            
            else:
                utils.exit_with_error(f'Bot number not yet supported: {bot_number}')

        else:
            utils.exit_with_error(f'CEX not supported: {cex}')


    ############################
    #    Any invalid option    #
    ############################
    else:
        parser.print_help()


if __name__ == "__main__":
    run() 