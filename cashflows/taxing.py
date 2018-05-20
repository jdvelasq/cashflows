"""
After tax cashflow calculation
===============================================================================

Overview
-------------------------------------------------------------------------------

The function ``after_tax_cashflow`` returns a new cashflow object for which the
values are taxed. The specified tax rate is only appled to positive values
in the cashflow. Negative values are reemplazed by a zero value.

Functions in this module
-------------------------------------------------------------------------------



"""

import pandas as pd

from cashflows.timeseries import *
from cashflows.common import *


def after_tax_cashflow(cflo, tax_rate):
    """Computes the after cashflow for a tax rate. Taxes are not computed
    for negative values in the cashflow.

    Args:
        cflo (pandas.Series): generic cashflow.
        tax_rate (pandas.Series): periodic income tax rate.

    Returns:
        Taxed values (`pandas.Series`)

    **Example***

    >>> cflo = cashflow(const_value=[-50] + [100] * 4, start='2010', freq='A')
    >>> tax_rate = interest_rate(const_value=[10] * 5, start='2010', freq='A')
    >>> after_tax_cashflow(cflo=cflo, tax_rate=tax_rate) # doctest: +NORMALIZE_WHITESPACE
    2010     0.0
    2011    10.0
    2012    10.0
    2013    10.0
    2014    10.0
    Freq: A-DEC, dtype: float64

    """
    if not isinstance(cflo, pd.Series):
        raise TypeError("cashflow must be a pandas.Series")
    if not isinstance(tax_rate, pd.Series):
        raise TypeError("tax_rate must be a pandas.Series")
    verify_period_range([cflo, tax_rate])
    result = cflo.copy()
    for time, _ in enumerate(cflo):
        if result[time] > 0:
            result[time] *= tax_rate[time] / 100
        else:
            result[time] = 0
    return result

    
if __name__ == "__main__":
    import doctest
    doctest.testmod()
