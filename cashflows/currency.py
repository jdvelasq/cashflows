"""
Currency conversion
===============================================================================

Overview
-------------------------------------------------------------------------------

The function ``currency_conversion`` allows the user to convert an cashflow in a
currency to the equivalent cashflow in other currency using the specified
``exchange_rate``. In addition, it is possible to include the devaluation of the
foreign exchange rate.


Functions in this module
-------------------------------------------------------------------------------


"""

import pandas

# cashflows.
from cashflows.timeseries import *
from cashflows.common import _vars2list
from cashflows.rate import to_discount_factor, to_compound_factor


def currency_conversion(cflo, exchange_rate=1, devaluation=None, base_date=0):
    """Converts a cashflow of dollars to another currency.

    Args:
        cflo (pandas.Series): Generic cashflow.
        exchange_rate (float): Exchange rate at time `base_date`.
        devaluation (pandas.Series): Devaluation rate per compounding period.
        base_date (int): Time index for the `exchange_rate` in current dollars.

    Returns:
        A TimeSeries object.

    **Examples.**


    >>> cflo = cashflow(const_value=[100] * 5, start='2015', freq='A')
    >>> devaluation = interest_rate(const_value=[5]*5, start='2015', freq='A')
    >>> currency_conversion(cflo=cflo, exchange_rate=2) # doctest: +NORMALIZE_WHITESPACE
    2015    200.0
    2016    200.0
    2017    200.0
    2018    200.0
    2019    200.0
    Freq: A-DEC, dtype: float64

    >>> currency_conversion(cflo=cflo, exchange_rate=2, devaluation=devaluation) # doctest: +NORMALIZE_WHITESPACE
    2015    200.00000
    2016    210.00000
    2017    220.50000
    2018    231.52500
    2019    243.10125
    Freq: A-DEC, dtype: float64

    >>> currency_conversion(cflo=cflo, exchange_rate=2,
    ... devaluation=devaluation, base_date='2017') # doctest: +NORMALIZE_WHITESPACE
    2015    181.405896
    2016    190.476190
    2017    200.000000
    2018    210.000000
    2019    220.500000
    Freq: A-DEC, dtype: float64

    """
    if not isinstance(cflo, pandas.Series):
        raise TypeError("`cashflow` must be a pandas.Series object")
    result = cflo.copy()
    if devaluation is None:
        for time, _ in enumerate(result):
            result[time] *= exchange_rate
    else:
        if not isinstance(devaluation, pandas.Series):
            raise TypeError("`devaluation` must be a pandas.Series object")
        verify_period_range([cflo, devaluation])
        factor = to_compound_factor(prate=devaluation, base_date=base_date)
        for time, _ in enumerate(result):
            result[time] *= exchange_rate * factor[time]
    return result



if __name__ == "__main__":
    import doctest
    doctest.testmod()
