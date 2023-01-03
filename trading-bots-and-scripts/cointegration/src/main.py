#!/usr/bin/env python3
# -*- encoding: utf-8 -*-
# src/main.py
# author: steinkirch
# Entry point for cointbot.

import argparse

import src.utils.os as utils
from src.markets.buybit import BuybitCex


def run_menu() -> argparse.ArgumentParser:
    """Run the menu for this module."""

    parser = argparse.ArgumentParser(description='🏭 cointbot 🪙')
    parser.add_argument('-d', dest='derivatives', nargs=1,
                        help='Get data for a derivative. \
                            Example: cointbot -d usdt')
    parser.add_argument('-p', dest='price', nargs=1,
                        help='Save price history for a derivative. \
                            Example: cointbot -p usdt')
    parser.add_argument('-i', dest='pairs', nargs=2,
                        help='Get cointegration for a pair of assets. \
                            Example: cointbot -i ethusdt btcusdt')
    parser.add_argument('-z', dest='zscore', nargs=2,
                        help='Get latest z-core signal for a pair of assets. \
                            Example: cointbot -z ethusdt btcusdt')
    parser.add_argument('-t', dest='test', help='Run backtests. \
                            Example: cointbot -t')
    parser.add_argument('-b', dest='bot', help='Deploy and start bot. \
                            Example: cointbot -b')
    return parser


def run() -> None:
    """Entry point for this module."""

    parser = run_menu()
    args = parser.parse_args()
    
    env_vars = utils.load_config()
    cex = env_vars['CEX'].upper()


    ############################
    #     Get coin info        #
    ############################
    if args.derivatives:
        coin = args.derivatives[0].upper()

        if cex == 'BUYBIT':
            b = BuybitCex(env_vars)
            coin_info = b.get_coin_info(coin)
            if coin_info:
                utils.pprint(coin_info)
            else:
                utils.exit_with_error(f'No data found for {coin}.')

        elif cex == 'BINANCE':
            # TODO: implement binance
            coin_info = {}
        elif cex == 'BITMEX':
            # TODO: implement bitmex
            pass
        else:
            utils.exit_with_error(f'CEX not supoorted: {cex}')

    ############################
    #     Get price list      #
    ############################
    elif args.price:
        coin = args.price[0].upper()

        if cex == 'BUYBIT':
            b = BuybitCex(env_vars)
            price_history = b.get_price_history(coin)

            if price_history:
                prices_outfile = env_vars['PRICE_HISTORY_FILE']
                outdir = env_vars['OUTPUTDIR']

                utils.save_price_history(price_history, outdir, prices_outfile)
                utils.pprint(price_history)
    
            else:
                utils.exit_with_error(f'Could not retrieve price history for {cex}')
        
        elif cex == 'BINANCE':
            pass
    
        elif cex == 'BITMEX':
            pass

        else:
            utils.exit_with_error(f'CEX not supported: {cex}')


    ############################
    #    Any invalid option    #
    ############################
    else:
        parser.print_help()


if __name__ == "__main__":
    run() 
