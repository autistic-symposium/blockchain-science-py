# -*- encoding: utf-8 -*-
# src/cexes.py
# cexex API methods.

import datetime
from pybit.inverse_perpetual import HTTP

from src.utils import save_output, create_dir, format_path


#########################
#   Methods for Buybit  #
#########################

def start_buybit_session(url) -> object:
    return HTTP(url)


def query_symbols_pybit(session) -> dict:
    """Query tradeable symbols for pybit cex."""
    return session.query_symbol()


def parse_symbols_pybit(symbols, quote_currency) -> list:
    """Parse results from querying pybit for symbols."""
    
    result = []
    try:
        if symbols['ret_msg'] =='OK':
            symbols = symbols['result']

            for symbol in symbols:
                if symbol['quote_currency'] == quote_currency \
                                    and symbol['status'] == 'Trading':
                    result.append(symbol)

    except KeyError as e:
        print(f'Could not retrive symbols for {quote_currency}: {e}')

    return result


def get_price_klines_pybit(session, symbol, specs) -> dict:
    """Get historical prices."""

    from_time, interval = get_start_time(specs['timeframe'], specs['kline_limit'])

    print(interval)

    try:
        prices = session.query_mark_price_kline(
                symbol = symbol,
                interval = interval,
                limit = specs['kline_limit'],
                from_time = from_time
            )
        if len(prices['result']) == specs['kline_limit']:
            return prices['result']

    except Exception as e:
        print(f'Could not get klines for {symbol}: {e}')


################################
#   General public methods     #
###############################

def get_tradeable_symbols(session, quote_currency) -> list:
    """Get symbols that are tradeable."""

    symbols = query_symbols_pybit(session) 
    return parse_symbols_pybit(symbols, quote_currency)


def get_start_time(timeframe, kline_limit) -> int:
    """Get start times and timeframes."""

    from_time = 0
    if timeframe == 'D':
        from_time = datetime.datetime.now() - \
                            datetime.timedelta(days=kline_limit)
    if timeframe == 60:
        time_start_date = datetime.datetime.now() - \
                            datetime.timedelta(hours=kline_limit)
    else:
        print(f'Time frame not supported:{timeframe}')
    
    return int(from_time.timestamp()), timeframe


def get_price_history(session, symbols, specs) -> dict:
    """Get and store price histry for all available pairs."""

    price_history_dict = {}

    for symbol in symbols:

        symbol_name = symbol['name']
        price_history = get_price_klines_pybit(session, symbol_name, specs)

        if price_history is not None:
            price_history_dict[symbol_name] = price_history

    return price_history_dict  


def save_price_history(price_history_dict, outdir, outfile) -> None:
    """Handle saving the results for price history."""

    create_dir(outdir) 
    destination = format_path(outdir, outfile)
    save_output(destination, price_history_dict)

