#!/usr/bin/env python3
# -*- encoding: utf-8 -*-
# src/main.py
# author: steinkirch
# Entry point for cointbot.

import argparse

import src.utils.os as utils
from src.cexes.buybit import BuybitCex


def run_menu() -> argparse.ArgumentParser:
    """Run the menu for this module."""

    parser = argparse.ArgumentParser(description='🏭 cointbot 🪙')
    parser.add_argument('-c', dest='coin', nargs=1,
                        help='Get data for a currency (coin). \
                            Example: cointbot usdt')
    parser.add_argument('-p', dest='price', nargs=1,
                        help='Get price history for CEX and QUOTE CURRENCY. \
                            Example: cointbot usdt')
    parser.add_argument('-i', dest='pairs', nargs=3,
                        help='Get cointegration for a pair of tokens \
                            Example: cointbot <price history file.json> maticusdt stxusdt')
    parser.add_argument('-b', dest='bot', help='Start bot')
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
    if args.coin:
        coin = args.coin[0].upper()

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
    #    Any invalid option    #
    ############################
    else:
        parser.print_help()


if __name__ == "__main__":
    run() 
