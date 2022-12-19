#!/usr/bin/env python3
# -*- encoding: utf-8 -*-
# src/main.py
# author: steinkirch
# Entry point for cointbot.

import argparse

from src.bot import run_bot
from src.utils import load_config, pprint
from src.stats import plot_cointegrated_pairs, save_backtest, get_pair_trends, get_percentage_changes
from src.cexes import start_buybit_session, get_tradeable_symbols, get_price_history, save_price_history


def run_menu() -> argparse.ArgumentParser:

    parser = argparse.ArgumentParser(description='🏭 cointbot 🪙')
    parser.add_argument('-s', dest='symbols', nargs=2,
                        help='Get tradeable symbols for CEX and QUOTE CURRENCY. \
                            Example: cointbot buybit usdt')
    parser.add_argument('-p', dest='price', nargs=2,
                        help='Get price history for CEX and QUOTE CURRENCY. \
                            Example: cointbot buybit usdt')
    parser.add_argument('-i', dest='pairs', nargs=3,
                        help='Get cointegration for a pair of tokens \
                            Example: cointbot <price history file.json> maticusdt stxusdt')
    parser.add_argument('-b', dest='bot', help='Start bot')
    return parser


def run() -> None:
    """Entry point for this module."""

    parser = run_menu()
    args = parser.parse_args()

    env_vars = load_config()
    url = env_vars['PYBIT_API_URL']
    

    ############################
    #     Get symbol list      #
    ############################
    if args.symbols:
        cex = args.symbols[0].upper()
        quote_currency = args.symbols[1].upper()

        if cex == 'BUYBIT':
            session = start_buybit_session(url)
            pprint(get_tradeable_symbols(session, quote_currency))
        else:
            print(f'CEX not supoorted: {cex}')


    ############################
    #     Get price list      #
    ############################
    elif args.price:
        cex = args.price[0].upper()
        quote_currency = args.price[1].upper()

        timeframe = env_vars['TIMEFRAME']
        kline_limit = int(env_vars['KLINE_LIMIT'])
        prices_outfile = env_vars['PRICE_HISTORY_FILE']

        if cex == 'BUYBIT':
            session = start_buybit_session(url)
            symbols = get_tradeable_symbols(session, quote_currency)
            specs = {
                'timeframe': timeframe,
                'kline_limit': kline_limit
            }
            price_history = get_price_history(session, symbols, specs)

            if price_history:
                save_price_history(price_history, outdir, prices_outfile)
                pprint(price_history)
            else:
                print(f'Could not retrieve any price history for {cex}')
        else:
            print(f'CEX not supoorted: {cex}')


    ############################
    #  Get a cointegrated pair #
    ############################
    elif args.pairs:
        price_history_file = args.pairs[0]
        token1 = args.pairs[1].upper()
        token2 = args.pairs[2].upper()

        outdir = env_vars['OUTPUTDIR']
        backtest_outfile = env_vars['BACKTEST_FILE']
        z_score_window = int(env_vars['ZSCORE_WINDOW'])

        print(backtest_outfile)

        data = get_pair_trends(price_history_file, token1, token2, z_score_window)
        save_backtest(data, backtest_outfile, outdir)
        
        data = get_percentage_changes(data)
        plot_cointegrated_pairs(data)


    ############################
    #        Start bot         #
    ############################
    elif args.bot:
        run_bot()

    ############################
    #    Any invalid option    #
    ############################
    else:
        parser.print_help()


if __name__ == "__main__":
    run() 
