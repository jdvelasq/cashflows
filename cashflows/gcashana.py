"""

Net present value
===============================================================================


>>> marr = generic_rate([12]*5)
>>> cflo = generic_cashflow([100]*5, spec=(0, -200))
>>> timevalue(cflo=cflo, marr=marr) # doctest: +ELLIPSIS
103.73...


>>> timevalue(cflo=[cflo, cflo], marr=marr) # doctest: +ELLIPSIS
[103.73..., 103.73...]

>>> timevalue(cflo=cflo, marr=[marr, marr]) # doctest: +ELLIPSIS
[103.73..., 103.73...]

>>> timevalue(cflo=[cflo, cflo], marr=[marr, marr]) # doctest: +ELLIPSIS
[103.73..., 103.73...]

>>> timevalue(cflo=[cflo, cflo], marr=[marr, marr], base_date=[4, 4]) # doctest: +ELLIPSIS
[163.22..., 163.22...]



Net uniform series
===============================================================================

>>> marr = generic_rate([12]*5)
>>> cflo = generic_cashflow([100]*5, spec=(0, -200))
>>> net_uniform_series(cflo, marr) # doctest: +ELLIPSIS
116.18...


>>> net_uniform_series([cflo, cflo], marr) # doctest: +ELLIPSIS
[116.18..., 116.18...]

>>> net_uniform_series(cflo, [marr, marr]) # doctest: +ELLIPSIS
[116.18..., 116.18...]

>>> net_uniform_series([cflo, cflo], [marr, marr]) # doctest: +ELLIPSIS
[116.18..., 116.18...]

>>> net_uniform_series([cflo, cflo], [marr, marr], nper=5) # doctest: +ELLIPSIS
[28.77..., 28.77...]

>>> net_uniform_series([cflo, cflo], [marr, marr], nper=[5, 5]) # doctest: +ELLIPSIS
[28.77..., 28.77...]




Benefit-Cost ratio
===============================================================================

>>> marr = generic_rate([12]*5)
>>> cflo = generic_cashflow([100]*5, spec=(0, -200))
>>> benefit_cost_ratio(cflo, marr) # doctest: +ELLIPSIS
1.518...

>>> benefit_cost_ratio([cflo, cflo], marr) # doctest: +ELLIPSIS
[1.518..., 1.518...]

>>> benefit_cost_ratio(cflo, [marr, marr]) # doctest: +ELLIPSIS
[1.518..., 1.518...]

>>> benefit_cost_ratio([cflo, cflo], [marr, marr]) # doctest: +ELLIPSIS
[1.518..., 1.518...]

>>> benefit_cost_ratio([cflo, cflo], [marr, marr], [0, 0]) # doctest: +ELLIPSIS
[1.518..., 1.518...]




Internal Rate of Return
===============================================================================

>>> cflo = generic_cashflow([100]*5, spec=(0, -200))
>>> irr(cflo) # doctest: +ELLIPSIS
34.90...

Modified Internal Rate of Return
===============================================================================

>>> cflo = generic_cashflow([100]*5, spec=(0, -200))
>>> mirr(cflo) # doctest: +ELLIPSIS
18.92...


Description of the functions in this module
===============================================================================


"""

import numpy as np
from cashflows.gtimeseries import TimeSeries, generic_cashflow, generic_rate, verify_eq_time_range
from cashflows.gcashcomp import to_discount_factor, equivalent_rate, vars2list
from cashflows.basics import tvmm
# from cashflows.basics import amort



def timevalue(cflo, marr, base_date=0):
    """
    Computes the net value of a cashflow at time `base_date`.

    Args:
        cflo (TimeSeries, list of TimeSeries): cashflow.
        marr (TimeSeries): Minimum atractive interest rate.
        base_date (int, tuple): Time.

    Returns:
        net value (float, list of floats)

    >>> marr = generic_rate([12]*5)
    >>> cflo = generic_cashflow([100]*5, spec = (0, -200))
    >>> timevalue(cflo, marr) # doctest: +ELLIPSIS
    103.73...

    >>> timevalue(cflo, marr, 4) # doctest: +ELLIPSIS
    163.22...


    """
    params = vars2list([cflo, marr, base_date])
    cflo = params[0]
    marr = params[1]
    base_date = params[2]
    retval = []
    for xcflo, xmarr, xbase_date in zip(cflo, marr, base_date):
        if not isinstance(xcflo, TimeSeries):
            raise TypeError("`cflo` must be a TimeSeries")
        if not isinstance(xmarr, TimeSeries):
            raise TypeError("`marr` must be a TimeSeries")
        verify_eq_time_range(xcflo, xmarr)
        netval = 0
        factor = to_discount_factor(xmarr, xbase_date)
        for time, _ in enumerate(xcflo):
            netval += xcflo[time] * factor[time]
        retval.append(netval)
    if len(retval) == 1:
        return retval[0]
    return retval


def net_uniform_series(cflo, marr, nper=1):
    """Computes a net uniform series equivalent of a cashflow.

    Args:
        cflo (cashflow): cashflow.
        marr (TimeSeries): Minimum atractive interest rate.
        nper (int, list): number of equivalent payment periods.

    Returns:
        net uniform series (float)

    """
    params = vars2list([cflo, marr, nper])
    cflo = params[0]
    marr = params[1]
    nper = params[2]
    retval = []
    for xcflo, xmarr, xnper in zip(cflo, marr, nper):
        netval = timevalue(cflo=xcflo, marr=xmarr, base_date=0)
        erate = equivalent_rate(xmarr)
        retval.append(-tvmm(nrate=erate, nper=xnper, pval=netval, fval=0, pmt=None))
    if len(retval) == 1:
        return retval[0]
    return retval


def benefit_cost_ratio(cflo, marr, base_date=0):
    """
    Computes a benefit cost ratio at time `base_date` of a cashflow.

    Args:
        rate (int float, Rate): Minimum atractive interest rate.
        cashflow (cashflow, list): cashflow.
        base_date (int, list): Time.

    Returns:
        (float) net present value.

    """

    params = vars2list([marr, cflo, base_date])
    marr = params[0]
    cflo = params[1]
    base_date = params[2]

    retval = []
    for xmarr, xcflo, xbase_date in zip(marr, cflo, base_date):
        verify_eq_time_range(xcflo, xmarr)
        num = 0
        den = 0
        num = xcflo.copy()
        den = xcflo.copy()
        for time, _ in enumerate(xcflo):
            if xcflo[time] >= 0.0:
                den[time] = 0
            else:
                num[time] = 0
        retval.append(-timevalue(num, xmarr, xbase_date) / timevalue(den, xmarr, xbase_date))

    if len(retval) == 1:
        return retval[0]
    return retval



def irr(cflo):
    """Computes the internal rate of return.

    Args:
        cashflow (TimeSeries): cashflow.

    Returns:
        (float) net uniform series.

    """
    if isinstance(cflo, TimeSeries):
        cflo = [cflo]
    retval = []
    for xcflo in cflo:
        retval.append(100 * xcflo.pyr * np.irr(xcflo.tolist()))
    if len(retval) == 1:
        return retval[0]
    return retval

## modified internal rate of return
def mirr(cflo, finance_rate=0, reinvest_rate=0):
    """Computes the modified internal rate of return.

    Args:
        cashflow (list, cashflow): cashflow.
        finance_rate (float): rate applied to negative values of the cashflow
        reinvest_rate (float): rate applied to positive values of the cashflow

    Returns:
        (float) modified internal rate of return.

    """
    # negativos: finance_rate
    # positivos: reinvest_rate
    if isinstance(cflo, TimeSeries):
        cflo = [cflo]
    retval = []
    for xcflo in cflo:
        retval.append(100 * xcflo.pyr * np.mirr(xcflo.tolist(),
                                                finance_rate,
                                                reinvest_rate))

    if len(retval) == 1:
        return retval[0]
    return retval

def table(data):
    """Prints the list `data` as a table

    Args:
        data:
    """
    print(' #               Value')
    print('------------------------')
    #
    data = [round(element, 4) for element in data]

    for index, _ in enumerate(data):
        print(' {:<3d}    {:14.4f}'.format(index, data[index]))


if __name__ == "__main__":
    import doctest
    doctest.testmod()
