# -*- encoding: utf-8 -*-
# arithmetics.py
# This class implements math methods used by the other classes.

import scipy

from decimal import Decimal, getcontext
from src.util.strings import log_error


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


def invert_equation(equation) -> object:
    """Invert the sign of an equation represented by a function object."""
    return lambda x: - equation(x)


def nelder_mead_simplex_optimization(equation, boundary_max, x0=None) -> float:
    """
        Run a simple form of the Nelder-Mead optimization solver,
        that minimizes a scalar function of one or more variables.
    """

    # If initial guess (x0) is None, set it to the middle.
    x0 = x0 or int(div(boundary_max, 2))

    # Optimize to find a min of the negative of the original equation.
    lambda_equation = invert_equation(equation)

    # Run Nelder-Mead solver.
    solution_for_max = scipy.optimize.fmin(lambda_equation, x0, disp=False)

    try:
        return int(to_decimal(solution_for_max[0]))
    except (ValueError, KeyError) as e:
        log_error(f'Could not find a optimization solution: {e}. Returning 0.')
        return 0