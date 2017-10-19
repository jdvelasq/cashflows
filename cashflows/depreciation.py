"""
Asset depreciation
===============================================================================

"""


# from cashflows.gtimeseries import TimeSeries, cashflow, interest_rate, verify_eq_time_range


import pandas as pd

#
from cashflows.timeseries import cashflow, interest_rate, verify_period_range


def depreciation_sl(costs, life, salvalue=None, delay=None):
    """Computes the depreciation of an asset using straight line depreciation
    method.

    Args:
        cost (TimeSeries): the cost per period of the assets.
        life (TimeSeries): number of depreciation periods for the asset.
        salvalue(TimeSeries): salvage value as a percentage of cost.

    Returns:
        depreciation, accum_depreciation (TimeSeries, TimeSeries).


    **Examples.**

    >>> costs = cashflow(const_value=0, periods=16, start='2000Q1', freq='Q')
    >>> costs[0] = 1000
    >>> life = cashflow(const_value=0, periods=16, start='2000Q1', freq='Q')
    >>> life[0] = 4
    >>> depreciation_sl(costs=costs, life=life) # doctest: +NORMALIZE_WHITESPACE
            Beg book   Costs   Depr  Accum depr  End book
    2000Q1       0.0  1000.0    0.0         0.0    1000.0
    2000Q2    1000.0     0.0  250.0       250.0     750.0
    2000Q3     750.0     0.0  250.0       500.0     500.0
    2000Q4     500.0     0.0  250.0       750.0     250.0
    2001Q1     250.0     0.0  250.0      1000.0       0.0
    2001Q2       0.0     0.0    0.0      1000.0       0.0
    2001Q3       0.0     0.0    0.0      1000.0       0.0
    2001Q4       0.0     0.0    0.0      1000.0       0.0
    2002Q1       0.0     0.0    0.0      1000.0       0.0
    2002Q2       0.0     0.0    0.0      1000.0       0.0
    2002Q3       0.0     0.0    0.0      1000.0       0.0
    2002Q4       0.0     0.0    0.0      1000.0       0.0
    2003Q1       0.0     0.0    0.0      1000.0       0.0
    2003Q2       0.0     0.0    0.0      1000.0       0.0
    2003Q3       0.0     0.0    0.0      1000.0       0.0
    2003Q4       0.0     0.0    0.0      1000.0       0.0

    >>> delay = cashflow(const_value=0, start='2000Q1', periods=16, freq='Q')
    >>> delay[0] = 2
    >>> depreciation_sl(costs=costs, life=life, delay=delay) # doctest: +NORMALIZE_WHITESPACE
            Beg book   Costs   Depr  Accum depr  End book
    2000Q1       0.0  1000.0    0.0         0.0    1000.0
    2000Q2    1000.0     0.0    0.0         0.0    1000.0
    2000Q3    1000.0     0.0    0.0         0.0    1000.0
    2000Q4    1000.0     0.0  250.0       250.0     750.0
    2001Q1     750.0     0.0  250.0       500.0     500.0
    2001Q2     500.0     0.0  250.0       750.0     250.0
    2001Q3     250.0     0.0  250.0      1000.0       0.0
    2001Q4       0.0     0.0    0.0      1000.0       0.0
    2002Q1       0.0     0.0    0.0      1000.0       0.0
    2002Q2       0.0     0.0    0.0      1000.0       0.0
    2002Q3       0.0     0.0    0.0      1000.0       0.0
    2002Q4       0.0     0.0    0.0      1000.0       0.0
    2003Q1       0.0     0.0    0.0      1000.0       0.0
    2003Q2       0.0     0.0    0.0      1000.0       0.0
    2003Q3       0.0     0.0    0.0      1000.0       0.0
    2003Q4       0.0     0.0    0.0      1000.0       0.0

    >>> costs = cashflow(const_value=0, periods=16, start='2000Q1', freq='Q')
    >>> costs[0] = 1000
    >>> costs[8] = 1000
    >>> life = cashflow(const_value=0, periods=16, start='2000Q1', freq='Q')
    >>> life[0] = 4
    >>> life[8] = 4
    >>> depreciation_sl(costs=costs, life=life) # doctest: +NORMALIZE_WHITESPACE
            Beg book   Costs   Depr  Accum depr  End book
    2000Q1       0.0  1000.0    0.0         0.0    1000.0
    2000Q2    1000.0     0.0  250.0       250.0     750.0
    2000Q3     750.0     0.0  250.0       500.0     500.0
    2000Q4     500.0     0.0  250.0       750.0     250.0
    2001Q1     250.0     0.0  250.0      1000.0       0.0
    2001Q2       0.0     0.0    0.0      1000.0       0.0
    2001Q3       0.0     0.0    0.0      1000.0       0.0
    2001Q4       0.0     0.0    0.0      1000.0       0.0
    2002Q1       0.0  1000.0    0.0      1000.0    1000.0
    2002Q2    1000.0     0.0  250.0      1250.0     750.0
    2002Q3     750.0     0.0  250.0      1500.0     500.0
    2002Q4     500.0     0.0  250.0      1750.0     250.0
    2003Q1     250.0     0.0  250.0      2000.0       0.0
    2003Q2       0.0     0.0    0.0      2000.0       0.0
    2003Q3       0.0     0.0    0.0      2000.0       0.0
    2003Q4       0.0     0.0    0.0      2000.0       0.0

    >>> delay = cashflow(const_value=0, periods=16, start='2000Q1', freq='Q')
    >>> delay[0] = 2
    >>> delay[8] = 2
    >>> depreciation_sl(costs=costs, life=life, delay=delay) # doctest: +NORMALIZE_WHITESPACE
            Beg book   Costs   Depr  Accum depr  End book
    2000Q1       0.0  1000.0    0.0         0.0    1000.0
    2000Q2    1000.0     0.0    0.0         0.0    1000.0
    2000Q3    1000.0     0.0    0.0         0.0    1000.0
    2000Q4    1000.0     0.0  250.0       250.0     750.0
    2001Q1     750.0     0.0  250.0       500.0     500.0
    2001Q2     500.0     0.0  250.0       750.0     250.0
    2001Q3     250.0     0.0  250.0      1000.0       0.0
    2001Q4       0.0     0.0    0.0      1000.0       0.0
    2002Q1       0.0  1000.0    0.0      1000.0    1000.0
    2002Q2    1000.0     0.0    0.0      1000.0    1000.0
    2002Q3    1000.0     0.0    0.0      1000.0    1000.0
    2002Q4    1000.0     0.0  250.0      1250.0     750.0
    2003Q1     750.0     0.0  250.0      1500.0     500.0
    2003Q2     500.0     0.0  250.0      1750.0     250.0
    2003Q3     250.0     0.0  250.0      2000.0       0.0
    2003Q4       0.0     0.0    0.0      2000.0       0.0




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

    depr = [0] * len(costs)
    adepr = [0] * len(costs)
    begbook = [0] * len(costs)
    endbook = [0] * len(costs)

    for index, _ in enumerate(costs):
        if costs[index] == 0:
            continue
        if delay[index] == 0:
            ValueError('Depreciation with delay 0')
        xdepr = [(costs[index] * (100 - salvalue[index]) / 100) / int(life[index])] * int(life[index])
        for time in range(int(life[index])):
            if index + time + delay[index] + 1 < len(costs):
                depr[index + time + int(delay[index]) + 1] += xdepr[time]
            else:
                break

    for time, _ in enumerate(depr):
        if time > 0:
            adepr[time] = adepr[time - 1] + depr[time]
        else:
            adepr[time] = depr[time]

    for time, _ in enumerate(depr):
        if time > 0:
            begbook[time] = endbook[time - 1]
        endbook[time] = begbook[time] - depr[time] + costs[time]



    table = pd.DataFrame({'Beg book': begbook,
                          'Costs': costs,
                          'Depr': depr,
                          'Accum depr': adepr,
                          'End book': endbook})

    table = table[['Beg book', 'Costs', 'Depr', 'Accum depr', 'End book']]
    table = table.round(2)
    return table


    #
    #
    # if noprint is True:
    #     retval = costs.copy()
    #     for index, _ in enumerate(costs):
    #         retval[index] = depr[index]
    #     return retval
    #
    # print_depr(depr, adepr, costs, begbook, endbook)


def depreciation_soyd(costs, life, salvalue=None, delay=None):
    """Computes the depreciation of an asset using the sum-of-year's-digits
    method.

    Args:
        cost (TimeSeries): the cost per period of the assets.
        life (TimeSeries): number of depreciation periods for the asset.
        salvalue(TimeSeries): salvage value as a percentage of cost.

    Returns:
        A tuple (dep, accum) of lists (tuple): depreciation per period and accumulated depreciation per period


    **Examples.**

    >>> costs = cashflow(const_value=0, periods=16, start='2000Q1', freq='Q')
    >>> costs[0] = 1000
    >>> life = cashflow(const_value=0, periods=16, start='2000Q1', freq='Q')
    >>> life[0] = 4
    >>> depreciation_soyd(costs=costs, life=life) # doctest: +NORMALIZE_WHITESPACE
            Beg book   Costs   Depr  Accum depr  End book
    2000Q1       0.0  1000.0    0.0         0.0    1000.0
    2000Q2    1000.0     0.0  400.0       400.0     600.0
    2000Q3     600.0     0.0  300.0       700.0     300.0
    2000Q4     300.0     0.0  200.0       900.0     100.0
    2001Q1     100.0     0.0  100.0      1000.0       0.0
    2001Q2       0.0     0.0    0.0      1000.0       0.0
    2001Q3       0.0     0.0    0.0      1000.0       0.0
    2001Q4       0.0     0.0    0.0      1000.0       0.0
    2002Q1       0.0     0.0    0.0      1000.0       0.0
    2002Q2       0.0     0.0    0.0      1000.0       0.0
    2002Q3       0.0     0.0    0.0      1000.0       0.0
    2002Q4       0.0     0.0    0.0      1000.0       0.0
    2003Q1       0.0     0.0    0.0      1000.0       0.0
    2003Q2       0.0     0.0    0.0      1000.0       0.0
    2003Q3       0.0     0.0    0.0      1000.0       0.0
    2003Q4       0.0     0.0    0.0      1000.0       0.0

    >>> delay = cashflow(const_value=0, periods=16, start='2000Q1', freq='Q')
    >>> delay[0] = 2
    >>> depreciation_soyd(costs=costs, life=life, delay=delay) # doctest: +NORMALIZE_WHITESPACE
            Beg book   Costs   Depr  Accum depr  End book
    2000Q1       0.0  1000.0    0.0         0.0    1000.0
    2000Q2    1000.0     0.0    0.0         0.0    1000.0
    2000Q3    1000.0     0.0    0.0         0.0    1000.0
    2000Q4    1000.0     0.0  400.0       400.0     600.0
    2001Q1     600.0     0.0  300.0       700.0     300.0
    2001Q2     300.0     0.0  200.0       900.0     100.0
    2001Q3     100.0     0.0  100.0      1000.0       0.0
    2001Q4       0.0     0.0    0.0      1000.0       0.0
    2002Q1       0.0     0.0    0.0      1000.0       0.0
    2002Q2       0.0     0.0    0.0      1000.0       0.0
    2002Q3       0.0     0.0    0.0      1000.0       0.0
    2002Q4       0.0     0.0    0.0      1000.0       0.0
    2003Q1       0.0     0.0    0.0      1000.0       0.0
    2003Q2       0.0     0.0    0.0      1000.0       0.0
    2003Q3       0.0     0.0    0.0      1000.0       0.0
    2003Q4       0.0     0.0    0.0      1000.0       0.0

    >>> costs = cashflow(const_value=0, periods=16, start='2000Q1', freq='Q')
    >>> costs[0] = 1000
    >>> costs[8] = 1000
    >>> life = cashflow(const_value=0, periods=16, start='2000Q1', freq='Q')
    >>> life[0] = 4
    >>> life[8] = 4
    >>> depreciation_soyd(costs=costs, life=life) # doctest: +NORMALIZE_WHITESPACE
            Beg book   Costs   Depr  Accum depr  End book
    2000Q1       0.0  1000.0    0.0         0.0    1000.0
    2000Q2    1000.0     0.0  400.0       400.0     600.0
    2000Q3     600.0     0.0  300.0       700.0     300.0
    2000Q4     300.0     0.0  200.0       900.0     100.0
    2001Q1     100.0     0.0  100.0      1000.0       0.0
    2001Q2       0.0     0.0    0.0      1000.0       0.0
    2001Q3       0.0     0.0    0.0      1000.0       0.0
    2001Q4       0.0     0.0    0.0      1000.0       0.0
    2002Q1       0.0  1000.0    0.0      1000.0    1000.0
    2002Q2    1000.0     0.0  400.0      1400.0     600.0
    2002Q3     600.0     0.0  300.0      1700.0     300.0
    2002Q4     300.0     0.0  200.0      1900.0     100.0
    2003Q1     100.0     0.0  100.0      2000.0       0.0
    2003Q2       0.0     0.0    0.0      2000.0       0.0
    2003Q3       0.0     0.0    0.0      2000.0       0.0
    2003Q4       0.0     0.0    0.0      2000.0       0.0

    >>> delay = cashflow(const_value=0, periods=16, start='2000Q1', freq='Q')
    >>> delay[0] = 2
    >>> delay[8] = 2
    >>> depreciation_soyd(costs=costs, life=life, delay=delay) # doctest: +NORMALIZE_WHITESPACE
            Beg book   Costs   Depr  Accum depr  End book
    2000Q1       0.0  1000.0    0.0         0.0    1000.0
    2000Q2    1000.0     0.0    0.0         0.0    1000.0
    2000Q3    1000.0     0.0    0.0         0.0    1000.0
    2000Q4    1000.0     0.0  400.0       400.0     600.0
    2001Q1     600.0     0.0  300.0       700.0     300.0
    2001Q2     300.0     0.0  200.0       900.0     100.0
    2001Q3     100.0     0.0  100.0      1000.0       0.0
    2001Q4       0.0     0.0    0.0      1000.0       0.0
    2002Q1       0.0  1000.0    0.0      1000.0    1000.0
    2002Q2    1000.0     0.0    0.0      1000.0    1000.0
    2002Q3    1000.0     0.0    0.0      1000.0    1000.0
    2002Q4    1000.0     0.0  400.0      1400.0     600.0
    2003Q1     600.0     0.0  300.0      1700.0     300.0
    2003Q2     300.0     0.0  200.0      1900.0     100.0
    2003Q3     100.0     0.0  100.0      2000.0       0.0
    2003Q4       0.0     0.0    0.0      2000.0       0.0




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

    depr = [0] * len(costs)
    adepr = [0] * len(costs)
    begbook = [0] * len(costs)
    endbook = [0] * len(costs)

    for index, _ in enumerate(costs):
        sumdig = life[index] * (life[index] + 1) / 2
        xdepr = [(costs[index] * (100 - salvalue[index]) / 100) * (int(life[index]) - time) / sumdig for time in range(int(life[index]))]
        for time in range(int(life[index])):
            if index + time + delay[index] + 1 < len(costs):
                depr[index + time + int(delay[index]) + 1] += xdepr[time]
            else:
                break

    for time, _ in enumerate(depr):
        if time > 0:
            adepr[time] = adepr[time - 1] + depr[time]
        else:
            adepr[time] = depr[time]

    for time, _ in enumerate(depr):
        if time > 0:
            begbook[time] = endbook[time - 1]
        endbook[time] = begbook[time] - depr[time] + costs[time]


    table = pd.DataFrame({'Beg book': begbook,
                          'Costs': costs,
                          'Depr': depr,
                          'Accum depr': adepr,
                          'End book': endbook})
    table = table[['Beg book', 'Costs', 'Depr', 'Accum depr', 'End book']]
    table = table.round(2)
    return table

    # if noprint is True:
    #     retval = costs.copy()
    #     for index, _ in enumerate(costs):
    #         retval[index] = depr[index]
    #     return retval
    #
    # print_depr(depr, adepr, costs, begbook, endbook)



def depreciation_db(costs, life, salvalue=None, factor=1, convert_to_sl=True, delay=None, noprint=True):
    """Computes the depreciation of an asset using the declining balance
    method.

    Args:
        cost (TimeSeries): the cost per period of the assets.
        life (TimeSeries): number of depreciation periods for the asset.
        salvalue(TimeSeries): salvage value as a percentage of cost.
        factor (float): acelerating factor for depreciation.
        convert_to_sl (bool): converts to straight line method?
        noprint (bool): when True, the procedure prints a depreciation table.

    Returns:
        A tuple (dep, accum) of lists (tuple): depreciation per period and accumulated depreciation per period


    **Examples.**

    >>> costs = cashflow(const_value=0, periods=16, start='2000Q1', freq='Q')
    >>> costs[0] = 1000
    >>> life = cashflow(const_value=0, periods=16, start='2000Q1', freq='Q')
    >>> life[0] = 4
    >>> depreciation_db(costs=costs, life=life, factor=1.5, convert_to_sl=False) # doctest: +NORMALIZE_WHITESPACE
            Beg book   Costs    Depr  Accum depr  End book
    2000Q1      0.00  1000.0    0.00        0.00   1000.00
    2000Q2   1000.00     0.0  375.00      375.00    625.00
    2000Q3    625.00     0.0  234.38      609.38    390.62
    2000Q4    390.62     0.0  146.48      755.86    244.14
    2001Q1    244.14     0.0   91.55      847.41    152.59
    2001Q2    152.59     0.0    0.00      847.41    152.59
    2001Q3    152.59     0.0    0.00      847.41    152.59
    2001Q4    152.59     0.0    0.00      847.41    152.59
    2002Q1    152.59     0.0    0.00      847.41    152.59
    2002Q2    152.59     0.0    0.00      847.41    152.59
    2002Q3    152.59     0.0    0.00      847.41    152.59
    2002Q4    152.59     0.0    0.00      847.41    152.59
    2003Q1    152.59     0.0    0.00      847.41    152.59
    2003Q2    152.59     0.0    0.00      847.41    152.59
    2003Q3    152.59     0.0    0.00      847.41    152.59
    2003Q4    152.59     0.0    0.00      847.41    152.59

    >>> delay = cashflow(const_value=0, periods=16, start='2000Q1', freq='Q')
    >>> delay[0] = 2
    >>> depreciation_db(costs=costs, life=life, delay=delay, factor=1.5, convert_to_sl=False) # doctest: +NORMALIZE_WHITESPACE
            Beg book   Costs    Depr  Accum depr  End book
    2000Q1      0.00  1000.0    0.00        0.00   1000.00
    2000Q2   1000.00     0.0    0.00        0.00   1000.00
    2000Q3   1000.00     0.0    0.00        0.00   1000.00
    2000Q4   1000.00     0.0  375.00      375.00    625.00
    2001Q1    625.00     0.0  234.38      609.38    390.62
    2001Q2    390.62     0.0  146.48      755.86    244.14
    2001Q3    244.14     0.0   91.55      847.41    152.59
    2001Q4    152.59     0.0    0.00      847.41    152.59
    2002Q1    152.59     0.0    0.00      847.41    152.59
    2002Q2    152.59     0.0    0.00      847.41    152.59
    2002Q3    152.59     0.0    0.00      847.41    152.59
    2002Q4    152.59     0.0    0.00      847.41    152.59
    2003Q1    152.59     0.0    0.00      847.41    152.59
    2003Q2    152.59     0.0    0.00      847.41    152.59
    2003Q3    152.59     0.0    0.00      847.41    152.59
    2003Q4    152.59     0.0    0.00      847.41    152.59


    >>> costs = cashflow(const_value=0, periods=16, start='2000Q1', freq='Q')
    >>> costs[0] = 1000
    >>> costs[8] = 1000
    >>> life = cashflow(const_value=0, periods=16, start='2000Q1', freq='Q')
    >>> life[0] = 4
    >>> life[8] = 4
    >>> depreciation_db(costs=costs, life=life, factor=1.5, convert_to_sl=False) # doctest: +NORMALIZE_WHITESPACE
            Beg book   Costs    Depr  Accum depr  End book
    2000Q1      0.00  1000.0    0.00        0.00   1000.00
    2000Q2   1000.00     0.0  375.00      375.00    625.00
    2000Q3    625.00     0.0  234.38      609.38    390.62
    2000Q4    390.62     0.0  146.48      755.86    244.14
    2001Q1    244.14     0.0   91.55      847.41    152.59
    2001Q2    152.59     0.0    0.00      847.41    152.59
    2001Q3    152.59     0.0    0.00      847.41    152.59
    2001Q4    152.59     0.0    0.00      847.41    152.59
    2002Q1    152.59  1000.0    0.00      847.41   1152.59
    2002Q2   1152.59     0.0  375.00     1222.41    777.59
    2002Q3    777.59     0.0  234.38     1456.79    543.21
    2002Q4    543.21     0.0  146.48     1603.27    396.73
    2003Q1    396.73     0.0   91.55     1694.82    305.18
    2003Q2    305.18     0.0    0.00     1694.82    305.18
    2003Q3    305.18     0.0    0.00     1694.82    305.18
    2003Q4    305.18     0.0    0.00     1694.82    305.18

    >>> delay = cashflow(const_value=0, periods=16, start='2000Q1', freq='Q')
    >>> delay[0] = 2
    >>> delay[8] = 2
    >>> depreciation_db(costs=costs, life=life, delay=delay, factor=1.5, convert_to_sl=False) # doctest: +NORMALIZE_WHITESPACE
            Beg book   Costs    Depr  Accum depr  End book
    2000Q1      0.00  1000.0    0.00        0.00   1000.00
    2000Q2   1000.00     0.0    0.00        0.00   1000.00
    2000Q3   1000.00     0.0    0.00        0.00   1000.00
    2000Q4   1000.00     0.0  375.00      375.00    625.00
    2001Q1    625.00     0.0  234.38      609.38    390.62
    2001Q2    390.62     0.0  146.48      755.86    244.14
    2001Q3    244.14     0.0   91.55      847.41    152.59
    2001Q4    152.59     0.0    0.00      847.41    152.59
    2002Q1    152.59  1000.0    0.00      847.41   1152.59
    2002Q2   1152.59     0.0    0.00      847.41   1152.59
    2002Q3   1152.59     0.0    0.00      847.41   1152.59
    2002Q4   1152.59     0.0  375.00     1222.41    777.59
    2003Q1    777.59     0.0  234.38     1456.79    543.21
    2003Q2    543.21     0.0  146.48     1603.27    396.73
    2003Q3    396.73     0.0   91.55     1694.82    305.18
    2003Q4    305.18     0.0    0.00     1694.82    305.18

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

    depr = [0] * len(costs)
    adepr = [0] * len(costs)
    begbook = [0] * len(costs)
    endbook = [0] * len(costs)

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
            if index + time + delay[index] + 1 < len(costs):
                depr[index + time + int(delay[index]) + 1] += xdepr[time]
            else:
                break

    for time, _ in enumerate(depr):
        if time > 0:
            adepr[time] = adepr[time - 1] + depr[time]
        else:
            adepr[time] = depr[time]

    for time, _ in enumerate(depr):
        if time > 0:
            begbook[time] = endbook[time - 1]
        endbook[time] = begbook[time] - depr[time] + costs[time]

    table = pd.DataFrame({'Beg book': begbook,
                          'Costs': costs,
                          'Depr': depr,
                          'Accum depr': adepr,
                          'End book': endbook})

    table = table[['Beg book', 'Costs', 'Depr', 'Accum depr', 'End book']]
    table = table.round(2)
    return table


    # if noprint is True:
    #     retval = costs.copy()
    #     for index, _ in enumerate(costs):
    #         retval[index] = depr[index]
    #     return retval
    #
    # print_depr(depr, adepr, costs, begbook, endbook)





if __name__ == "__main__":
    import doctest
    doctest.testmod()


# def print_depr(depr, adepr, costs, begbook, endbook):
#     """Prints a depreciation table
#
#     Args:
#        cost (int, float): Initial cost of the asset
#        depr (list): Depreciation per period
#        adepr (list): Accumulated depreciation per period
#        begbook (list): Beginning book value
#        endbook (list): Ending book value
#
#     Returns:
#        None
#
#     """
#
#
#     len_timeid = len(costs.end.__repr__())
#     len_number = max(len('{:1.2f}'.format(max(begbook))), 7)
#
#     fmt_timeid = '{:<' + '{:d}'.format(len_timeid) + 's}'
#     fmt_number = ' {:' + '{:d}'.format(len_number) + '.2f}'
#     fmt_header = ' {:>' + '{:d}'.format(len_number) + 's}'
#
#     if costs.pyr == 1:
#         xmajor, = costs.start
#         xminor = 0
#     else:
#         xmajor, xminor = costs.start
#
#     txt = []
#     header = fmt_timeid.format('t')
#     header += fmt_header.format('Beg.')
#     header += fmt_header.format('Cost')
#     header += fmt_header.format('Depre.')
#     header += fmt_header.format('Accum.')
#     header += fmt_header.format('End.')
#     txt.append(header)
#
#     header = fmt_timeid.format('')
#     header += fmt_header.format('Book')
#     header += fmt_header.format('')
#     header += fmt_header.format('')
#     header += fmt_header.format('Depre.')
#     header += fmt_header.format('Book')
#     txt.append(header)
#
#     header = fmt_timeid.format('')
#     header += fmt_header.format('Value')
#     header += fmt_header.format('')
#     header += fmt_header.format('')
#     header += fmt_header.format('')
#     header += fmt_header.format('Value')
#     txt.append(header)
#
#     txt.append('-' * len_timeid + '-----' + '-' * len_number * 5)
#
#
#     for time, _ in enumerate(costs):
#         if costs.pyr == 1:
#             timeid = (xmajor,)
#         else:
#             timeid = (xmajor, xminor)
#         fmt = fmt_timeid + fmt_number * 5
#         txt.append(fmt.format(timeid.__repr__(),
#                               begbook[time],
#                               costs[time],
#                               depr[time],
#                               adepr[time],
#                               endbook[time]))
#         if costs.pyr == 1:
#             xmajor += 1
#         else:
#             xminor += 1
#             if xminor == costs.pyr:
#                 xminor = 0
#                 xmajor += 1
#
#     print('\n'.join(txt))
