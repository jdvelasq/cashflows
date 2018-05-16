"""
After tax cashflow calculation.
===============================================================================


"""


from cashflows.gtimeseries import *
from cashflows.common import _vars2list


def after_tax_cashflow(cflo, tax_rate):
    """
    The function `after_tax_cashflow` returns a new cashflow object for which the
    values are taxed. The specified tax rate is only appled to positive values
    in the cashflow. Negative values are reemplazed by a zero value. `cflo`
    and `tax_rate` must have the same length and time specification.


    Computes the after cashflow for a tax rate. Taxes are not computed
    for negative values in the cashflow.

    Args:
        cflo (TimeSeries): generic cashflow.
        tax_rate (TimeSeries): periodic income tax rate.

    Returns:
        TimeSeries objects with taxed values

    **Example***

    >>> cflo = cashflow(const_value=[100] * 5, spec=(0, -100))
    >>> tax_rate = interest_rate(const_value=[10] * 5)
    >>> after_tax_cashflow(cflo=cflo, tax_rate=tax_rate) # doctest: +NORMALIZE_WHITESPACE
    Time Series:
    Start = (0,)
    End = (4,)
    pyr = 1
    Data = (0,)           0.00
           (1,)-(4,) [4] 10.00

    """
    params = _vars2list([cflo, tax_rate])
    cflo = params[0]
    tax_rate = params[1]
    retval = []
    for xcflo, xtax_rate in zip(cflo, tax_rate):
        if not isinstance(xcflo, TimeSeries):
            raise TypeError("cashflow must be a TimeSeries")
        verify_eq_time_range(xcflo, xtax_rate)
        result = xcflo.copy()
        for time, _ in enumerate(xcflo):
            if result[time] > 0:
                result[time] *= xtax_rate[time] / 100
            else:
                result[time] = 0
        retval.append(result)
    if len(retval) == 1:
        return retval[0]
    return retval

if __name__ == "__main__":
    import doctest
    doctest.testmod()
