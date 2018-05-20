"""
Asset depreciation
===============================================================================

Overview
-------------------------------------------------------------------------------

This module implements the following functions to compute the depreciation of an
asset:

* ``depreciation_sl``: Computes the depreciation of an asset using straight line
  depreciation method.
* ``depreciation_soyd``: Computes the depreciation of an asset using the
  sum-of-year's-digits method.
* ``depreciation_db``: Computes the depreciation of an asset using the declining
  balance method.


Functions in this module
-----------------------------------------------------------------

"""


import pandas as pd

from cashflows.timeseries import *


def depreciation_sl(costs, life, salvalue=None):
    """Computes the depreciation of an asset using straight line depreciation
    method.

    Args:
        costs (pandas.Series): the cost per period of the assets.
        life (pandas.Series): number of depreciation periods for the asset.
        salvalue (pandas.Series): salvage value as a percentage of cost.

    Returns:
        Returns a pandas DataFrame with the computations.


    **Examples.**

    >>> costs = cashflow(const_value=0, periods=16, start='2000Q1', freq='Q')
    >>> costs[0] = 1000
    >>> life = cashflow(const_value=0, periods=16, start='2000Q1', freq='Q')
    >>> life[0] = 4
    >>> depreciation_sl(costs=costs, life=life) # doctest: +NORMALIZE_WHITESPACE
               Beg_Book   Depr  Accum_Depr  End_Book
       2000Q1    1000.0  250.0       250.0     750.0
       2000Q2     750.0  250.0       500.0     500.0
       2000Q3     500.0  250.0       750.0     250.0
       2000Q4     250.0  250.0      1000.0       0.0
       2001Q1       0.0    0.0      1000.0       0.0
       2001Q2       0.0    0.0      1000.0       0.0
       2001Q3       0.0    0.0      1000.0       0.0
       2001Q4       0.0    0.0      1000.0       0.0
       2002Q1       0.0    0.0      1000.0       0.0
       2002Q2       0.0    0.0      1000.0       0.0
       2002Q3       0.0    0.0      1000.0       0.0
       2002Q4       0.0    0.0      1000.0       0.0
       2003Q1       0.0    0.0      1000.0       0.0
       2003Q2       0.0    0.0      1000.0       0.0
       2003Q3       0.0    0.0      1000.0       0.0
       2003Q4       0.0    0.0      1000.0       0.0


    >>> costs = cashflow(const_value=0, periods=16, start='2000Q1', freq='Q')
    >>> costs[0] = 1000
    >>> costs[8] = 1000
    >>> life = cashflow(const_value=0, periods=16, start='2000Q1', freq='Q')
    >>> life[0] = 4
    >>> life[8] = 4
    >>> depreciation_sl(costs=costs, life=life) # doctest: +NORMALIZE_WHITESPACE
               Beg_Book   Depr  Accum_Depr  End_Book
       2000Q1    1000.0  250.0       250.0     750.0
       2000Q2     750.0  250.0       500.0     500.0
       2000Q3     500.0  250.0       750.0     250.0
       2000Q4     250.0  250.0      1000.0       0.0
       2001Q1       0.0    0.0      1000.0       0.0
       2001Q2       0.0    0.0      1000.0       0.0
       2001Q3       0.0    0.0      1000.0       0.0
       2001Q4       0.0    0.0      1000.0       0.0
       2002Q1    1000.0  250.0      1250.0     750.0
       2002Q2     750.0  250.0      1500.0     500.0
       2002Q3     500.0  250.0      1750.0     250.0
       2002Q4     250.0  250.0      2000.0       0.0
       2003Q1       0.0    0.0      2000.0       0.0
       2003Q2       0.0    0.0      2000.0       0.0
       2003Q3       0.0    0.0      2000.0       0.0
       2003Q4       0.0    0.0      2000.0       0.0




    """
    verify_period_range([costs, life])
    if salvalue is not None:
        verify_period_range([costs, salvalue])
    else:
        salvalue = [0] * len(costs)

    depr = costs.copy()
    adepr = costs.copy()
    begbook = costs.copy()
    endbook = costs.copy()

    depr[:] = 0
    adepr[:] = 0
    begbook[:] = 0
    endbook[:] = 0

    for index, _ in enumerate(costs):
        if costs[index] == 0:
            continue
        xdepr = [(costs[index] * (100 - salvalue[index]) / 100) / int(life[index])] * int(life[index])
        for time in range(int(life[index])):
            if index + time  < len(costs):
                depr[index + time] += xdepr[time]
            else:
                break

    for time, _ in enumerate(depr):
        if time > 0:
            adepr[time] = adepr[time - 1] + depr[time]
        else:
            adepr[time] = depr[time]

    for time, _ in enumerate(depr):
        if time > 0:
            begbook[time] = endbook[time - 1] + costs[time]
        else:
            begbook[0] = costs[0]
        endbook[time] = begbook[time] - depr[time]

    table = pd.DataFrame({'Beg_Book': begbook,
                          'Depr': depr,
                          'Accum_Depr': adepr,
                          'End_Book': endbook})

    table = table[['Beg_Book', 'Depr', 'Accum_Depr', 'End_Book']]
    table = table.round(2)
    return table



def depreciation_soyd(costs, life, salvalue=None):
    """Computes the depreciation of an asset using the sum-of-year's-digits
    method.

    Args:
        costs (pandas.Series): the cost per period of the assets.
        life (pandas.Series): number of depreciation periods for the asset.
        salvalue (pandas.Series): salvage value as a percentage of cost.

    Returns:
        Returns a pandas DataFrame with the computations.


    **Examples.**

    >>> costs = cashflow(const_value=0, periods=16, start='2000Q1', freq='Q')
    >>> costs[0] = 1000
    >>> life = cashflow(const_value=0, periods=16, start='2000Q1', freq='Q')
    >>> life[0] = 4
    >>> depreciation_soyd(costs=costs, life=life) # doctest: +NORMALIZE_WHITESPACE
               Beg_Book   Depr  Accum_Depr  End_Book
       2000Q1    1000.0  400.0       400.0     600.0
       2000Q2     600.0  300.0       700.0     300.0
       2000Q3     300.0  200.0       900.0     100.0
       2000Q4     100.0  100.0      1000.0       0.0
       2001Q1       0.0    0.0      1000.0       0.0
       2001Q2       0.0    0.0      1000.0       0.0
       2001Q3       0.0    0.0      1000.0       0.0
       2001Q4       0.0    0.0      1000.0       0.0
       2002Q1       0.0    0.0      1000.0       0.0
       2002Q2       0.0    0.0      1000.0       0.0
       2002Q3       0.0    0.0      1000.0       0.0
       2002Q4       0.0    0.0      1000.0       0.0
       2003Q1       0.0    0.0      1000.0       0.0
       2003Q2       0.0    0.0      1000.0       0.0
       2003Q3       0.0    0.0      1000.0       0.0
       2003Q4       0.0    0.0      1000.0       0.0


    >>> costs = cashflow(const_value=0, periods=16, start='2000Q1', freq='Q')
    >>> costs[0] = 1000
    >>> costs[8] = 1000
    >>> life = cashflow(const_value=0, periods=16, start='2000Q1', freq='Q')
    >>> life[0] = 4
    >>> life[8] = 4
    >>> depreciation_soyd(costs=costs, life=life) # doctest: +NORMALIZE_WHITESPACE
               Beg_Book   Depr  Accum_Depr  End_Book
       2000Q1    1000.0  400.0       400.0     600.0
       2000Q2     600.0  300.0       700.0     300.0
       2000Q3     300.0  200.0       900.0     100.0
       2000Q4     100.0  100.0      1000.0       0.0
       2001Q1       0.0    0.0      1000.0       0.0
       2001Q2       0.0    0.0      1000.0       0.0
       2001Q3       0.0    0.0      1000.0       0.0
       2001Q4       0.0    0.0      1000.0       0.0
       2002Q1    1000.0  400.0      1400.0     600.0
       2002Q2     600.0  300.0      1700.0     300.0
       2002Q3     300.0  200.0      1900.0     100.0
       2002Q4     100.0  100.0      2000.0       0.0
       2003Q1       0.0    0.0      2000.0       0.0
       2003Q2       0.0    0.0      2000.0       0.0
       2003Q3       0.0    0.0      2000.0       0.0
       2003Q4       0.0    0.0      2000.0       0.0


    """
    verify_period_range([costs, life])
    if salvalue is not None:
        verify_period_range([costs, salvalue])
    else:
        salvalue = [0] * len(costs)

    depr = costs.copy()
    adepr = costs.copy()
    begbook = costs.copy()
    endbook = costs.copy()

    depr[:] = 0
    adepr[:] = 0
    begbook[:] = 0
    endbook[:] = 0

    for index, _ in enumerate(costs):
        sumdig = life[index] * (life[index] + 1) / 2
        xdepr = [(costs[index] * (100 - salvalue[index]) / 100) * (int(life[index]) - time) / sumdig for time in range(int(life[index]))]
        for time in range(int(life[index])):
            if index + time < len(costs):
                depr[index + time] += xdepr[time]
            else:
                break

    for time, _ in enumerate(depr):
        if time > 0:
            adepr[time] = adepr[time - 1] + depr[time]
        else:
            adepr[time] = depr[time]

    for time, _ in enumerate(depr):
        if time > 0:
            begbook[time] = endbook[time - 1] + costs[time]
        else:
            begbook[0] = costs[0]
        endbook[time] = begbook[time] - depr[time]

    table = pd.DataFrame({'Beg_Book': begbook,
                          'Depr': depr,
                          'Accum_Depr': adepr,
                          'End_Book': endbook})

    table = table[['Beg_Book', 'Depr', 'Accum_Depr', 'End_Book']]
    table = table.round(2)
    return table




def depreciation_db(costs, life, salvalue=None, factor=1, convert_to_sl=True, delay=None, noprint=True):
    """Computes the depreciation of an asset using the declining balance
    method.

    Args:
        costs (pandas.Series): the cost per period of the assets.
        life (pandas.Series): number of depreciation periods for the asset.
        salvalue (pandas.Series): salvage value as a percentage of cost.
        factor (float): acelerating factor for depreciation.
        convert_to_sl (bool): converts to straight line method?
        noprint (bool): when True, the procedure prints a depreciation table.

    Returns:
        Returns a pandas DataFrame with the computations.


    **Examples.**

    >>> costs = cashflow(const_value=0, periods=16, start='2000Q1', freq='Q')
    >>> costs[0] = 1000
    >>> life = cashflow(const_value=0, periods=16, start='2000Q1', freq='Q')
    >>> life[0] = 4
    >>> depreciation_db(costs=costs, life=life, factor=1.5, convert_to_sl=False) # doctest: +NORMALIZE_WHITESPACE
            Beg_Book    Depr  Accum_Depr  End_Book
    2000Q1   1000.00  375.00      375.00    625.00
    2000Q2    625.00  234.38      609.38    390.62
    2000Q3    390.62  146.48      755.86    244.14
    2000Q4    244.14   91.55      847.41    152.59
    2001Q1    152.59    0.00      847.41    152.59
    2001Q2    152.59    0.00      847.41    152.59
    2001Q3    152.59    0.00      847.41    152.59
    2001Q4    152.59    0.00      847.41    152.59
    2002Q1    152.59    0.00      847.41    152.59
    2002Q2    152.59    0.00      847.41    152.59
    2002Q3    152.59    0.00      847.41    152.59
    2002Q4    152.59    0.00      847.41    152.59
    2003Q1    152.59    0.00      847.41    152.59
    2003Q2    152.59    0.00      847.41    152.59
    2003Q3    152.59    0.00      847.41    152.59
    2003Q4    152.59    0.00      847.41    152.59

    >>> costs = cashflow(const_value=0, periods=16, start='2000Q1', freq='Q')
    >>> costs[0] = 1000
    >>> costs[8] = 1000
    >>> life = cashflow(const_value=0, periods=16, start='2000Q1', freq='Q')
    >>> life[0] = 4
    >>> life[8] = 4
    >>> depreciation_db(costs=costs, life=life, factor=1.5, convert_to_sl=False) # doctest: +NORMALIZE_WHITESPACE
            Beg_Book    Depr  Accum_Depr  End_Book
    2000Q1   1000.00  375.00      375.00    625.00
    2000Q2    625.00  234.38      609.38    390.62
    2000Q3    390.62  146.48      755.86    244.14
    2000Q4    244.14   91.55      847.41    152.59
    2001Q1    152.59    0.00      847.41    152.59
    2001Q2    152.59    0.00      847.41    152.59
    2001Q3    152.59    0.00      847.41    152.59
    2001Q4    152.59    0.00      847.41    152.59
    2002Q1   1152.59  375.00     1222.41    777.59
    2002Q2    777.59  234.38     1456.79    543.21
    2002Q3    543.21  146.48     1603.27    396.73
    2002Q4    396.73   91.55     1694.82    305.18
    2003Q1    305.18    0.00     1694.82    305.18
    2003Q2    305.18    0.00     1694.82    305.18
    2003Q3    305.18    0.00     1694.82    305.18
    2003Q4    305.18    0.00     1694.82    305.18


    """

    verify_period_range([costs, life])
    if salvalue is not None:
        verify_period_range([costs, salvalue])
    else:
        salvalue = [0] * len(costs)
    if delay is not None:
        verify_period_range([costs, delay])
    else:
        delay = [0] * len(costs)
    if not isinstance(factor, (int, float)):
        raise TypeError('Invalid type for `factor`')
    if not isinstance(convert_to_sl, bool):
        raise TypeError('Invalid type for `convert_to_sl`')

    depr = costs.copy()
    adepr = costs.copy()
    begbook = costs.copy()
    endbook = costs.copy()

    depr[:] = 0
    adepr[:] = 0
    begbook[:] = 0
    endbook[:] = 0
    for index, _ in enumerate(costs):

        if costs[index] == 0:
            continue

        xfactor = factor / life[index]

        rem_cost = costs[index]
        xdepr = [0] * int(life[index])

        sl_depr = (costs[index] - salvalue[index]) / life[index]

        for time in range(int(life[index])):
            xdepr[time] = rem_cost * xfactor
            if convert_to_sl is True and xdepr[time] < sl_depr:
                xdepr[time] = sl_depr
            rem_cost -= xdepr[time]
            if rem_cost < salvalue[index]:
                rem_cost += xdepr[time]
                xdepr[time] = rem_cost - salvalue[index]
                rem_cost = salvalue[index]

        for time in range(int(life[index])):
            if index + time  < len(costs):
                depr[index + time] += xdepr[time]
            else:
                break

    for time, _ in enumerate(depr):
        if time > 0:
            adepr[time] = adepr[time - 1] + depr[time]
        else:
            adepr[0] = depr[0]

    for time, _ in enumerate(depr):
        if time > 0:
            begbook[time] = endbook[time - 1] + costs[time]
        else:
            begbook[0] = costs[0]
        endbook[time] = begbook[time] - depr[time]

    table = pd.DataFrame({'Beg_Book': begbook,
                          'Depr': depr,
                          'Accum_Depr': adepr,
                          'End_Book': endbook})

    table = table[['Beg_Book', 'Depr', 'Accum_Depr', 'End_Book']]
    table = table.round(2)
    return table




if __name__ == "__main__":
    import doctest
    doctest.testmod()
