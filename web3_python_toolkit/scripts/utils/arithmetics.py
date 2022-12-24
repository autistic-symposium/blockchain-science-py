# -*- encoding: utf-8 -*-
# arithmetics.py
# This class implements math methods used by the other classes.
# author: steinkirch


from decimal import Decimal, getcontext
from utils.strings import log_error


def div(dividend, divisor) -> Decimal:
    """Return higher precision division."""

    if divisor == 0:
        log_error('Found a zero division error. Returning 0.')
        return 0
    return to_decimal(dividend) / to_decimal(divisor)


def to_decimal(value, precision=None) -> Decimal:
    """Return Decimal value for higher (defined) precision."""

    precision = precision or 22
    getcontext().prec = precision
    return Decimal(value)
