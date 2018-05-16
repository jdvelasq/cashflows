"""
Constant dollar transformations
===============================================================================

The function `const2curr` computes the equivalent generic cashflow in current
dollars from a generic cashflow in constant dollars of the date given by
`base_date`. `inflation` is the inflation rate per compounding period.
`curr2const` computes the inverse transformation.

"""


from cashflows.gtimeseries import TimeSeries, cashflow, interest_rate, verify_eq_time_range, _timeid2index
from cashflows.common import _vars2list
from cashflows.rate import to_compound_factor, to_discount_factor


def const2curr(cflo, inflation, base_date=0):
    """Converts a cashflow of constant dollars to current dollars
    of the time `base_date`.

    Args:
        cflo (TimeSeries): A cashflow.
        inflation (TimeSeries): Inflation rate per compounding period.
        base_date (int, tuple): base date.

    Returns:
        A cashflow in current money (TimeSeries)


    **Examples.**

    >>> const2curr(cflo=cashflow(const_value=[100] * 5),
    ... inflation=interest_rate(const_value=[10, 10, 20, 20, 20])) # doctest: +NORMALIZE_WHITESPACE
    Time Series:
    Start = (0,)
    End = (4,)
    pyr = 1
    Data = (0,)   100.00
           (1,)   110.00
           (2,)   132.00
           (3,)   158.40
           (4,)   190.08


    >>> const2curr(cflo=cashflow(const_value=[100] * 5),
    ... inflation=interest_rate(const_value=[10, 10, 20, 20, 20]), base_date=4) # doctest: +NORMALIZE_WHITESPACE
    Time Series:
    Start = (0,)
    End = (4,)
    pyr = 1
    Data = (0,)    52.61
           (1,)    57.87
           (2,)    69.44
           (3,)    83.33
           (4,)   100.00


    >>> const2curr(cflo=cashflow(const_value=[100] * 8, pyr=4),
    ... inflation=interest_rate(const_value=1, nper=8, pyr=4)) # doctest: +NORMALIZE_WHITESPACE
        Qtr0   Qtr1   Qtr2   Qtr3
    0 100.00 101.00 102.01 103.03
    1 104.06 105.10 106.15 107.21


    """
    params = _vars2list([cflo, inflation, base_date])
    cflo = params[0]
    inflation = params[1]
    base_date = params[2]
    retval = []
    for xcflo, xinflation, xbase_date in zip(cflo, inflation, base_date):
        if not isinstance(xcflo, TimeSeries):
            raise TypeError("cflo must be a TimeSeries object")
        if not isinstance(xinflation, TimeSeries):
            raise TypeError("inflation must be a TimeSeries object")
        verify_eq_time_range(xcflo, xinflation)
        factor = to_compound_factor(prate=xinflation, base_date=xbase_date)
        result = xcflo.copy()
        for time, _ in enumerate(result):
            result[time] *= factor[time]
        retval.append(result)
    if len(retval) == 1:
        return retval[0]
    return retval



def curr2const(cflo, inflation, base_date=0):
    """Converts a cashflow of current dollars to constant dollars of
    the date `base_date`.

    Args:
        cflo (list, Cashflow): A cashflow.
        inflation_rate (float, Rate): Inflation rate per compounding period.
        base_date (int): base time..

    Returns:
        A cashflow in constant dollars

    >>> curr2const(cflo=cashflow(const_value=[100] * 5),
    ... inflation=interest_rate(const_value=[10, 10, 20, 20, 20])) # doctest: +NORMALIZE_WHITESPACE
    Time Series:
    Start = (0,)
    End = (4,)
    pyr = 1
    Data = (0,)   100.00
           (1,)    90.91
           (2,)    75.76
           (3,)    63.13
           (4,)    52.61


    >>> curr2const(cflo=cashflow(const_value=[100] * 5),
    ... inflation=interest_rate(const_value=[10, 10, 20, 20, 20]), base_date=4) # doctest: +NORMALIZE_WHITESPACE
    Time Series:
    Start = (0,)
    End = (4,)
    pyr = 1
    Data = (0,)   190.08
           (1,)   172.80
           (2,)   144.00
           (3,)   120.00
           (4,)   100.00

    >>> curr2const(cflo=cashflow(const_value=[100] * 8, pyr=4),
    ... inflation=interest_rate(const_value=1, nper=8, pyr=4)) # doctest: +NORMALIZE_WHITESPACE
        Qtr0   Qtr1   Qtr2   Qtr3
    0 100.00  99.01  98.03  97.06
    1  96.10  95.15  94.20  93.27

    """
    params = _vars2list([cflo, inflation, base_date])
    cflo = params[0]
    inflation = params[1]
    base_date = params[2]
    retval = []
    for xcflo, xinflation, xbase_date in zip(cflo, inflation, base_date):
        if not isinstance(xcflo, TimeSeries):
            raise TypeError("cflo must be a TimeSeries object")
        if not isinstance(xinflation, TimeSeries):
            raise TypeError("inflation must be a TimeSeries object")
        verify_eq_time_range(xcflo, xinflation)
        factor = to_discount_factor(prate=xinflation, base_date=xbase_date)
        result = xcflo.copy()
        for time, _ in enumerate(result):
            result[time] *= factor[time]
        retval.append(result)
    if len(retval) == 1:
        return retval[0]
    return retval



if __name__ == "__main__":
    import doctest
    doctest.testmod()
