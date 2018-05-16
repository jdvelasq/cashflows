"""
Currency conversion
===============================================================================

The function `currency_conversion` allows the user to convert an cashflow in a
currency to the equivalent flow in other currency using the specified
`exchange_rate`. In addition, it is possible to include the devaluation of the
foreign exchange rate.

"""

from cashflows.gtimeseries import *
from cashflows.common import _vars2list
from cashflows.rate import to_discount_factor, to_compound_factor


def currency_conversion(cflo, exchange_rate=1, devaluation=None, base_date=0):
    """Converts a cashflow of dollars to another currency.

    Args:
        cflo (TimeSeries): A cashflow.
        exchange_rate (float): Exchange rate at time `base_date`.
        devaluation (TimeSeries): Devaluation rate per compounding period.
        base_date (int): Time index for the `exchange_rate` in current dollars.

    Returns:
        A TimeSeries object.

    **Examples.**


    >>> cflo = cashflow(const_value=[100] * 5)
    >>> currency_conversion(cflo=cflo, exchange_rate=2) # doctest: +NORMALIZE_WHITESPACE
    Time Series:
    Start = (0,)
    End = (4,)
    pyr = 1
    Data = (0,)-(4,) [5] 200.00

    >>> currency_conversion(cflo=cflo, exchange_rate=2,
    ... devaluation=interest_rate(const_value=[5]*5), base_date=(2,)) # doctest: +NORMALIZE_WHITESPACE
    Time Series:
    Start = (0,)
    End = (4,)
    pyr = 1
    Data = (0,)   181.41
           (1,)   190.48
           (2,)   200.00
           (3,)   210.00
           (4,)   220.50


    >>> cflo = cashflow(const_value=[100] * 8, pyr=4)
    >>> currency_conversion(cflo=cflo,
    ...                     exchange_rate=2,
    ...                     devaluation=interest_rate([1]*8, pyr=4)) # doctest: +NORMALIZE_WHITESPACE
        Qtr0   Qtr1   Qtr2   Qtr3
    0 200.00 202.00 204.02 206.06
    1 208.12 210.20 212.30 214.43

    >>> cflo = cashflow(const_value=[100] * 5)
    >>> currency_conversion(cflo=[cflo, cflo], exchange_rate=2) # doctest: +NORMALIZE_WHITESPACE
    [Time Series:
    Start = (0,)
    End = (4,)
    pyr = 1
    Data = (0,)-(4,) [5] 200.00
    ,  Time Series:
    Start = (0,)
    End = (4,)
    pyr = 1
    Data = (0,)-(4,) [5] 200.00
    ]

    """
    params = _vars2list([cflo, exchange_rate, devaluation, base_date])
    cflo = params[0]
    exchange_rate = params[1]
    devaluation = params[2]
    base_date = params[3]
    retval = []
    for xcflo, xexchange_rate, xdevaluation, xbase_date in zip(cflo, exchange_rate, devaluation, base_date):
        if not isinstance(xcflo, TimeSeries):
            raise TypeError("`cashflow` must be a TimeSeries")
        if xdevaluation is None:
            result = xcflo.copy()
            for time, _ in enumerate(result):
                result[time] *= xexchange_rate
        else:
            if not isinstance(xdevaluation, TimeSeries):
                raise TypeError("`devaluation` must be a TimeSeries")
            verify_eq_time_range(xcflo, xdevaluation)
            factor = to_compound_factor(prate=xdevaluation, base_date=xbase_date)
            result = xcflo.copy()
            for time, _ in enumerate(result):
                result[time] *= xexchange_rate * factor[time]
        retval.append(result)
    if len(retval) == 1:
        return retval[0]
    return retval

if __name__ == "__main__":
    import doctest
    doctest.testmod()
