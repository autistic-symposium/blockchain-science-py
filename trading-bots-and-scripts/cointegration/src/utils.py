# -*- encoding: utf-8 -*-
# src/util.py
# Util methods.

import os
import json
from pathlib import Path
from dotenv import load_dotenv
from pprint import PrettyPrinter


def save_output(destination, data) -> None:
    """Save data to a destination in disk."""

    try:
        with open(destination, 'w', encoding='utf-8') as outfile:
            json.dump(data, outfile, indent=4)

    except (IOError, TypeError) as e:
        print(f'Could not save {destination}: {e}')


def create_dir(result_dir) -> None:
    """Check whether a directory exists and create it if needed."""

    try:
        if not os.path.isdir(result_dir):
            os.mkdir(result_dir)

    except OSError as e:
        print(f'Could not create {result_dir}: {e}')


def open_json(filepath) -> dict:
    """Load and parse a file."""

    try:
        with open(filepath, 'r', encoding='utf-8') as infile:
            return json.load(infile)

    except (IOError, FileNotFoundError, TypeError) as e:
        print(f'Failed to parse: "{filepath}": {e}')



def format_path(dir_path, filename) -> str:
    """Format a OS full filepath."""

    return os.path.join(dir_path, filename)


def pprint(data, indent=None) -> None:
    """Print dicts and data in a suitable format"""

    print()
    indent = indent or 4
    pp = PrettyPrinter(indent=indent)
    pp.pprint(data)
    print()


def load_config() -> dict:
    """Load and set environment variables."""

    env_file = Path('.') / '.env'
    if not os.path.isfile(env_file):
        print('Please create an .env file')

    env_vars = {}
    load_dotenv(env_file)

    try:
        env_vars['PYBIT_API_URL'] = os.getenv("PYBIT_API_URL")
        env_vars['API_KEY'] = os.getenv("API_KEY")
        env_vars['API_SECRET'] = os.getenv("API_SECRET")
        env_vars['ZSCORE_WINDOW'] = os.getenv("ZSCORE_WINDOW")
        env_vars['KLINE_LIMIT'] = os.getenv("KLINE_LIMIT")
        env_vars['TIMEFRAME'] = os.getenv("TIMEFRAME")
        env_vars['PRICE_HISTORY_FILE'] = os.getenv("PRICE_HISTORY_FILE")
        env_vars['BACKTEST_FILE'] = os.getenv("BACKTEST_FILE")
        env_vars['OUTPUTDIR'] = os.getenv("OUTPUTDIR")
        env_vars['WS_PRIVATE_URL'] = os.getenv("WS_PRIVATE_URL")
        env_vars['WS_PUBLIC_URL'] = os.getenv("WS_PUBLIC_URL")
        env_vars['TOKEN1'] = os.getenv("TOKEN1")
        env_vars['TOKEN2'] = os.getenv("TOKEN2")
        env_vars['API_URL'] = os.getenv("API_URL")
        env_vars['API_KEY'] = os.getenv("API_KEY")
        env_vars['API_SECRET'] = os.getenv("API_SECRET")
        env_vars['SIGNAL_POSTIVE'] = os.getenv("SIGNAL_POSTIVE")
        env_vars['SIGNAL_NEGATIVE'] = os.getenv("SIGNAL_NEGATIVE")
        env_vars['ROUDING_TOKEN1'] = os.getenv("ROUDING_TOKEN1")
        env_vars['ROUNDING_TOKEN2'] = os.getenv("ROUNDING_TOKEN2")
        env_vars['QTY_TOKEN1'] = os.getenv("SIGNAL_NQTY_TOKEN1EGATIVE")
        env_vars['QTY_TOKEN2'] = os.getenv("QTY_TOKEN2")
        env_vars['MASS_LOSS_USDT'] = os.getenv("MASS_LOSS_USDT")                
        env_vars['LIMIT_ORDER_BASIS'] = os.getenv("LIMIT_ORDER_BASIS")      
        env_vars['TRADEABLE_CAPITAL'] = os.getenv("TRADEABLE_CAPITAL")      
        env_vars['MAX_TRADES_PER_SIGNAL'] = os.getenv("MAX_TRADES_PER_SIGNAL")      
        env_vars['STOP_LOSS_FAIL_SAFE'] = os.getenv("STOP_LOSS_FAIL_SAFE")      
        env_vars['HALTING_TRADE'] = os.getenv("HALTING_TRADE")   
        env_vars['SIGNAL_TRIGGER_THRESH'] = os.getenv("SIGNAL_TRIGGER_THRESH")   
        
        return env_vars

    except KeyError as e:
        print(f'Cannot extract env variables: {e}. Exiting.')

