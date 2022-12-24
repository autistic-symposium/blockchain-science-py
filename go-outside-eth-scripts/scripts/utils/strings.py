# -*- encoding: utf-8 -*-
# This class implements string methods used by the other classes.
# author: steinkirch

from pprint import PrettyPrinter

from src.util.os import log_error
from src.util.arithmetics import to_decimal


def to_decimal_str(value) -> str:
    """Format a reserve amount to a suitable string."""

    return str(to_decimal(value))


def to_wei_str(value, decimals=None) -> str:
    """Parse an order string to wei value."""

    decimals = decimals or 18
    try:
        return str(value)[:-decimals] + '_' + str(value)[-decimals:]
    except ValueError as e:
        log_error(f'Cannot convert to wei: {e}')


def to_solution(value) -> str:
    """Format decimal wei with an underscore for easier reading."""

    return to_wei_str(to_decimal_str(value))


def pprint(data, indent=None) -> None:
    """Print dicts and data in a suitable format"""

    print()
    indent = indent or 4
    pp = PrettyPrinter(indent=indent)
    pp.pprint(data)
    print()
