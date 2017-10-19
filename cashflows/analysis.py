"""
Analysis of cashflows
===============================================================================

This module implements the following functions for financial analysis of
cashflows:

* ``timevalue``: computes the equivalent net value of a cashflow in a specified
  time moment.

* ``net_uniform_series``: computes the periodic equivalent net value of a
  cashflow for a specified number of payments.

* ``benefit_cost_ratio``: computes the benefit cost ratio of a cashflow using
  a periodic interest rate for discounting the cashflow.

* ``irr``:  calculates the periodic internal rate of return of a cashflow.

* ``mirr``:  calculates the periodic modified internal rate of return of a
  cashflow.

* ``list_as_table``: prints a list as a table. This function is useful for
  comparing financial indicators for different alternatives.

"""

import numpy as np
import pandas as pd

# cashflows.
from cashflows.timeseries import *
from cashflows.rate import *
from cashflows.common import _vars2list
from cashflows.tvmm import tvmm
# from cashflows.utilityfun import exp_utility_fun, log_utility_fun, sqrt_utility_fun




def irr(cflo):
    """Computes the internal rate of return of a generic cashflow as a periodic
    interest rate.

    Args:
        cflo (Series): Generic cashflow.

    Returns:
        Float or list of floats.

    **Examples.**

    >>> cflo = cashflow([-200] + [100]*4, start='2000Q1', freq='Q')
    >>> irr(cflo) # doctest: +ELLIPSIS
    34.90...

    >>> irr([cflo, cflo]) # doctest: +ELLIPSIS
    0    34.90...
    1    34.90...
    dtype: float64

    """
    # if isinstance(cflo, pd.Series):
    #     cflo = [cflo]
    # retval = []
    # freq = []
    # for xcflo in cflo:
    #     retval.append(100 * np.irr(xcflo.tolist()))
    #     freq.append(xcflo.index.freq.__repr__())
    # if len(retval) == 1:
    #     return retval[0]
    # daux = {'<YearEnd: month=12>':'A',
    #         '<BusinessYearEnd: month=12>':'BA',
    #         '<QuarterEnd: startingMonth=12>':'Q',
    #         '<BusinessQuarterEnd: startingMonth=12>':'BQ',
    #         '<MonthEnd>':'M',
    #         '<BusinessMonthEnd>':'BM',
    #         '<CustomBusinessMonthEnd>':'CBM',
    #         '<SemiMonthEnd: day_of_month=15>':'SM',
    #         '<6 * MonthEnds>':'6M',
    #         '<6 * BusinessMonthEnds>':'6BM',
    #         '<6 * CustomBusinessMonthEnds>':'6CBM'}
    # freq = [daux[i] for i in freq]
    # retval = pd.DataFrame({'IRR':retval, 'Freq':freq})
    # return retval


    if isinstance(cflo, pd.Series):
        cflo = [cflo]
    retval = pd.Series([0] * len(cflo), dtype=np.float64)
    for index, xcflo in enumerate(cflo):
        retval[index] = (100 * np.irr(xcflo))
    if len(retval) == 1:
        return retval[0]
    return retval

## modified internal rate of return
def mirr(cflo, finance_rate=0, reinvest_rate=0):
    """Computes the modified internal rate of return of a generic cashflow
    as a periodic interest rate.

    Args:
        cflo (list, cashflow): Generic cashflow.
        finance_rate (float): Periodic interest rate applied to negative values of the cashflow.
        reinvest_rate (float): Periodic interest rate applied to positive values of the cashflow.

    Returns:
        Float or list of floats.

    **Examples.**

    >>> cflo = cashflow([-200] + [100]*4, start='2000Q1', freq='Q')
    >>> mirr(cflo) # doctest: +ELLIPSIS
    18.92...

    >>> mirr([cflo, cflo]) # doctest: +ELLIPSIS
    0    18.920712
    1    18.920712
    dtype: float64


    """
    # negativos: finance_rate
    # positivos: reinvest_rate
    if isinstance(cflo, pd.Series):
        cflo = [cflo]
    retval = pd.Series([0] * len(cflo), dtype=np.float64)
    for index, xcflo in enumerate(cflo):
        retval[index] = (100 *  np.mirr(xcflo,
                                        finance_rate,
                                        reinvest_rate))

    if len(retval) == 1:
        return retval[0]
    return retval

def timevalue(cflo, prate, base_date=0, utility=None):
    """
    Computes the equivalent net value of a generic cashflow at time `base_date`
    using the periodic interest rate `prate`.  If `base_date` is 0, `timevalue`
    computes the net present value of the
    cashflow. If `base_date` is the index of the last element of `cflo`,
    this function computes the equivalent future value.


    Args:
        cflo (TimeSeries, list of TimeSeries): Generic cashflow.
        prate (TimeSeries): Periodic interest rate.
        base_date (int, tuple): Time.
        utility (function): Utility function.

    Returns:
        Float or list of floats.

    **Examples.**


    >>> cflo = cashflow([-732.54] + [100]*8, start='2000Q1', freq='Q')
    >>> prate = interest_rate([2]*9, start='2000Q1', freq='Q')
    >>> timevalue(cflo, prate) # doctest: +ELLIPSIS
    0.00...


    >>> prate = interest_rate([12]*5, start='2000Q1', freq='Q')
    >>> cflo = cashflow([-200]+[100]*4, start='2000Q1', freq='Q')
    >>> timevalue(cflo, prate) # doctest: +ELLIPSIS
    103.73...

    >>> timevalue(cflo, prate, 4) # doctest: +ELLIPSIS
    163.22...


    >>> prate = interest_rate([12]*5, start='2000Q1', freq='Q')
    >>> cflo = cashflow([-200] + [100]*4, start='2000Q1', freq='Q')
    >>> timevalue(cflo=cflo, prate=prate) # doctest: +ELLIPSIS
    103.73...

    >>> timevalue(cflo=[cflo, cflo], prate=prate) # doctest: +ELLIPSIS
    0    103.734935
    1    103.734935
    dtype: float64


    """

    if isinstance(cflo, pd.Series):
        cflo = [cflo]
    if not isinstance(prate, pd.Series):
        raise TypeError("`prate` must be a pandas.Series")
    verify_period_range(cflo + [prate])
    retval = pd.Series([0] * len(cflo), dtype=np.float64)
    factor = to_discount_factor(prate=prate, base_date=base_date)
    for index, xcflo in enumerate(cflo):
        netval = 0
        for time, _ in enumerate(xcflo):
            netval += xcflo[time] * factor[time]
        retval[index] = netval
    if len(retval) == 1:
        return retval[0]
    return retval


    # params = _vars2list([cflo, prate, base_date])
    # cflo = params[0]
    # prate = params[1]
    # base_date = params[2]
    # retval = []
    # for xcflo, xprate, xbase_date in zip(cflo, prate, base_date):
    #     if not isinstance(xcflo, pd.Series):
    #         raise TypeError("`cflo` must be a pandas.Series")
    #     if not isinstance(xprate, pd.Series):
    #         raise TypeError("`prate` must be a pandas.Series")
    #     verify_period_range([xcflo, xprate])
    #     netval = 0
    #     factor = to_discount_factor(prate=xprate, base_date=xbase_date)
    #     for time, _ in enumerate(xcflo):
    #         if utility is None:
    #             xcflo_aux = xcflo[time]
    #         else:
    #             xcflo_aux = utility(xcflo[time])
    #         netval += xcflo_aux * factor[time]
    #     if utility is not None:
    #         netval = utility(netval, inverse=True)
    #     retval.append(netval)
    # if len(retval) == 1:
    #     return retval[0]
    # return retval



def net_uniform_series(cflo, prate, nper=1):
    """Computes a net uniform series equivalent of a cashflow. This is,
    a fixed periodic payment during `nper` periods that is equivalent
    to the cashflow `cflo` at the periodic interest rate `prate`.

    Args:
        cflo (cashflow): Generic cashflow.
        prate (TimeSeries): Periodic interest rate.
        nper (int, list): Number of equivalent payment periods.

    Returns:
        Float or list of floats.

    **Examples.**

    >>> prate = interest_rate([2]*9, start='2000Q1', freq='Q')
    >>> cflo = cashflow([-732.54] + [100]*8, start='2000Q1', freq='Q')
    >>> net_uniform_series(cflo, prate) # doctest: +ELLIPSIS
    0.00...

    >>> prate = interest_rate([12]*5, start='2000Q1', freq='Q')
    >>> cflo = cashflow([-200] + [100]*4, start='2000Q1', freq='Q')
    >>> net_uniform_series(cflo, prate) # doctest: +ELLIPSIS
    116.18...

    >>> net_uniform_series([cflo, cflo], prate) # doctest: +ELLIPSIS
    0    116.183127
    1    116.183127
    dtype: float64



    """

    if isinstance(cflo, pd.Series):
        cflo = [cflo]
    if not isinstance(prate, pd.Series):
        raise TypeError("`prate` must be a pandas.Series")
    verify_period_range(cflo + [prate])
    retval = pd.Series([0] * len(cflo), dtype=np.float64)
    erate = equivalent_rate(prate=prate)
    for index, xcflo in enumerate(cflo):
        netval = timevalue(cflo=xcflo, prate=prate, base_date=0)
        retval[index] = (-tvmm(nrate=erate, nper=nper, pval=netval, fval=0, pmt=None))
    if len(retval) == 1:
        return retval[0]
    return retval



    # params = _vars2list([cflo, prate, nper])
    # cflo = params[0]
    # prate = params[1]
    # nper = params[2]
    # retval = []
    # for xcflo, xprate, xnper in zip(cflo, prate, nper):
    #     netval = timevalue(cflo=xcflo, prate=xprate, base_date=0)
    #     erate = equivalent_rate(prate=xprate)
    #     retval.append(-tvmm(nrate=erate, nper=xnper, pval=netval, fval=0, pmt=None))
    # if len(retval) == 1:
    #     return retval[0]
    # return retval


def benefit_cost_ratio(cflo, prate, base_date=0):
    """
    Computes a benefit cost ratio at time `base_date` of a discounted cashflow
    using the periodic interest rate `prate`.

    Args:
        prate (int float, Rate): Periodic interest rate.
        cflo (cashflow, list): Generic cashflow.
        base_date (int, list): Time.

    Returns:
        Float or list of floats.

    **Examples.**

    >>> prate = interest_rate([2]*9, start='2000Q1', freq='Q')
    >>> cflo = cashflow([-717.01] + [100]*8, start='2000Q1', freq='Q')
    >>> benefit_cost_ratio(cflo, prate) # doctest: +ELLIPSIS
    1.02...

    >>> prate = interest_rate([12]*5, start='2000Q1', freq='Q')
    >>> cflo = cashflow([-200] + [100]*4, start='2000Q1', freq='Q')
    >>> benefit_cost_ratio(cflo, prate) # doctest: +ELLIPSIS
    1.518...

    >>> benefit_cost_ratio([cflo, cflo], prate) # doctest: +ELLIPSIS
    0    1.518675
    1    1.518675
    dtype: float64


    """

    if isinstance(cflo, pd.Series):
        cflo = [cflo]
    if not isinstance(prate, pd.Series):
        raise TypeError("`prate` must be a pandas.Series")
    verify_period_range(cflo + [prate])
    retval = pd.Series([0] * len(cflo), dtype=np.float64)
    for index, xcflo in enumerate(cflo):
        num = 0
        den = 0
        num = xcflo.copy()
        den = xcflo.copy()
        for time, _ in enumerate(xcflo):
            if xcflo[time] >= 0.0:
                den[time] = 0
            else:
                num[time] = 0
        retval[index] = -timevalue(num, prate, base_date) / timevalue(den, prate, base_date)
    if len(retval) == 1:
        return retval[0]
    return retval



    # params = _vars2list([prate, cflo, base_date])
    # prate = params[0]
    # cflo = params[1]
    # base_date = params[2]
    #
    # retval = []
    # for xprate, xcflo, xbase_date in zip(prate, cflo, base_date):
    #     verify_period_range([xcflo, xprate])
    #     num = 0
    #     den = 0
    #     num = xcflo.copy()
    #     den = xcflo.copy()
    #     for time, _ in enumerate(xcflo):
    #         if xcflo[time] >= 0.0:
    #             den[time] = 0
    #         else:
    #             num[time] = 0
    #     retval.append(-timevalue(num, xprate, xbase_date) / timevalue(den, xprate, xbase_date))
    #
    # if len(retval) == 1:
    #     return retval[0]
    # return retval





##-------------------




#
#
#
# def list_as_table(data):
#     """Prints the list `data` as a table. This function is used to produce a
#     human-readable format of a table for comparing financial indicators.
#
#     Args:
#         data (list): List of numeric values.
#
#     Returns:
#         None
#
#     **Example.**
#
#     >>> list_as_table(data=[1, 2, 3, 4]) # doctest: +ELLIPSIS +NORMALIZE_WHITESPACE
#      #               Value
#     ------------------------
#      0              1.0000
#      1              2.0000
#      2              3.0000
#      3              4.0000
#
#
#     >>> prate = interest_rate([12]*5)
#     >>> cflo = cashflow([-200] + [100]*4)
#     >>> list_as_table(timevalue(cflo=[cflo, cflo, cflo], prate=prate)) # doctest: +NORMALIZE_WHITESPACE
#      #               Value
#     ------------------------
#      0            103.7349
#      1            103.7349
#      2            103.7349
#
#     """
#     print(' #               Value')
#     print('------------------------')
#     #
#     data = [round(element, 4) for element in data]
#
#     for index, _ in enumerate(data):
#         print(' {:<3d}    {:14.4f}'.format(index, data[index]))


if __name__ == "__main__":
    import doctest
    doctest.testmod()
