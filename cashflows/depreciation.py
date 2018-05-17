"""
Asset depreciation
===============================================================================

"""


from cashflows.gtimeseries import TimeSeries, cashflow, interest_rate, verify_eq_time_range

def print_depr(depr, adepr, costs, begbook, endbook):
    """Prints a depreciation table

    Args:
       cost (int, float): Initial cost of the asset
       depr (list): Depreciation per period
       adepr (list): Accumulated depreciation per period
       begbook (list): Beginning book value
       endbook (list): Ending book value

    Returns:
       None

    """


    len_timeid = len(costs.end.__repr__())
    len_number = max(len('{:1.2f}'.format(max(begbook))), 7)

    fmt_timeid = '{:<' + '{:d}'.format(len_timeid) + 's}'
    fmt_number = ' {:' + '{:d}'.format(len_number) + '.2f}'
    fmt_header = ' {:>' + '{:d}'.format(len_number) + 's}'

    if costs.pyr == 1:
        xmajor, = costs.start
        xminor = 0
    else:
        xmajor, xminor = costs.start

    txt = []
    header = fmt_timeid.format('t')
    header += fmt_header.format('Beg.')
    header += fmt_header.format('Cost')
    header += fmt_header.format('Depre.')
    header += fmt_header.format('Accum.')
    header += fmt_header.format('End.')
    txt.append(header)

    header = fmt_timeid.format('')
    header += fmt_header.format('Book')
    header += fmt_header.format('')
    header += fmt_header.format('')
    header += fmt_header.format('Depre.')
    header += fmt_header.format('Book')
    txt.append(header)

    header = fmt_timeid.format('')
    header += fmt_header.format('Value')
    header += fmt_header.format('')
    header += fmt_header.format('')
    header += fmt_header.format('')
    header += fmt_header.format('Value')
    txt.append(header)

    txt.append('-' * len_timeid + '-----' + '-' * len_number * 5)


    for time, _ in enumerate(costs):
        if costs.pyr == 1:
            timeid = (xmajor,)
        else:
            timeid = (xmajor, xminor)
        fmt = fmt_timeid + fmt_number * 5
        txt.append(fmt.format(timeid.__repr__(),
                              begbook[time],
                              costs[time],
                              depr[time],
                              adepr[time],
                              endbook[time]))
        if costs.pyr == 1:
            xmajor += 1
        else:
            xminor += 1
            if xminor == costs.pyr:
                xminor = 0
                xmajor += 1

    print('\n'.join(txt))



def depreciation_sl(costs, life, salvalue=None, delay=None, noprint=True):
    """Computes the depreciation of an asset using straight line depreciation
    method.

    Args:
        cost (TimeSeries): the cost per period of the assets.
        life (TimeSeries): number of depreciation periods for the asset.
        salvalue(TimeSeries): salvage value as a percentage of cost.
        noprint (bool): when True, the procedure prints a depreciation table.

    Returns:
        depreciation, accum_depreciation (TimeSeries, TimeSeries).


    **Examples.**

    >>> costs1 = cashflow(const_value=0, nper=16, spec=(0, 1000), pyr=4)
    >>> costs2 = cashflow(const_value=0, nper=16, spec=[(0, 1000), (8, 1000)], pyr=4)
    >>> life1 = cashflow(const_value=0, nper=16, spec=(0, 4), pyr=4)
    >>> life2 = cashflow(const_value=0, nper=16, spec=[(0, 4), (8, 4)], pyr=4)
    >>> delay12 = cashflow(const_value=0, nper=16, spec=(0, 2), pyr=4)
    >>> delay22 = cashflow(const_value=0, nper=16, spec=[(0, 2), (8, 2)], pyr=4)
    >>> depreciation_sl(costs=costs1, life=life1) # doctest: +NORMALIZE_WHITESPACE
        Qtr0   Qtr1   Qtr2   Qtr3
    0   0.00 250.00 250.00 250.00
    1 250.00   0.00   0.00   0.00
    2   0.00   0.00   0.00   0.00
    3   0.00   0.00   0.00   0.00

    >>> depreciation_sl(costs=costs1, life=life1, delay=delay12) # doctest: +NORMALIZE_WHITESPACE
        Qtr0   Qtr1   Qtr2   Qtr3
    0   0.00   0.00   0.00 250.00
    1 250.00 250.00 250.00   0.00
    2   0.00   0.00   0.00   0.00
    3   0.00   0.00   0.00   0.00

    >>> depreciation_sl(costs=costs2, life=life2) # doctest: +NORMALIZE_WHITESPACE
        Qtr0   Qtr1   Qtr2   Qtr3
    0   0.00 250.00 250.00 250.00
    1 250.00   0.00   0.00   0.00
    2   0.00 250.00 250.00 250.00
    3 250.00   0.00   0.00   0.00


    >>> depreciation_sl(costs=costs2, life=life2, delay=delay22) # doctest: +NORMALIZE_WHITESPACE
        Qtr0   Qtr1   Qtr2   Qtr3
    0   0.00   0.00   0.00 250.00
    1 250.00 250.00 250.00   0.00
    2   0.00   0.00   0.00 250.00
    3 250.00 250.00 250.00   0.00

    >>> depreciation_sl(costs=costs2, life=life2, delay=delay22, noprint=False) # doctest: +NORMALIZE_WHITESPACE
    t         Beg.    Cost  Depre.  Accum.    End.
              Book                  Depre.    Book
             Value                           Value
    ----------------------------------------------
    (0, 0)    0.00 1000.00    0.00    0.00 1000.00
    (0, 1) 1000.00    0.00    0.00    0.00 1000.00
    (0, 2) 1000.00    0.00    0.00    0.00 1000.00
    (0, 3) 1000.00    0.00  250.00  250.00  750.00
    (1, 0)  750.00    0.00  250.00  500.00  500.00
    (1, 1)  500.00    0.00  250.00  750.00  250.00
    (1, 2)  250.00    0.00  250.00 1000.00    0.00
    (1, 3)    0.00    0.00    0.00 1000.00    0.00
    (2, 0)    0.00 1000.00    0.00 1000.00 1000.00
    (2, 1) 1000.00    0.00    0.00 1000.00 1000.00
    (2, 2) 1000.00    0.00    0.00 1000.00 1000.00
    (2, 3) 1000.00    0.00  250.00 1250.00  750.00
    (3, 0)  750.00    0.00  250.00 1500.00  500.00
    (3, 1)  500.00    0.00  250.00 1750.00  250.00
    (3, 2)  250.00    0.00  250.00 2000.00    0.00
    (3, 3)    0.00    0.00    0.00 2000.00    0.00


    """
    verify_eq_time_range(costs, life)
    if salvalue is not None:
        verify_eq_time_range(costs, salvalue)
    else:
        salvalue = [0] * len(costs)
    if delay is not None:
        verify_eq_time_range(costs, delay)
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
        xdepr = [(costs[index] * (100 - salvalue[index]) / 100) / life[index]] * life[index]
        for time in range(life[index]):
            if index + time + delay[index] + 1 < len(costs):
                depr[index + time + delay[index] + 1] += xdepr[time]
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

    if noprint is True:
        retval = costs.copy()
        for index, _ in enumerate(costs):
            retval[index] = depr[index]
        return retval

    print_depr(depr, adepr, costs, begbook, endbook)


def depreciation_soyd(costs, life, salvalue=None, delay=None, noprint=True):
    """Computes the depreciation of an asset using the sum-of-year's-digits
    method.

    Args:
        cost (TimeSeries): the cost per period of the assets.
        life (TimeSeries): number of depreciation periods for the asset.
        salvalue(TimeSeries): salvage value as a percentage of cost.
        noprint (bool): when True, the procedure prints a depreciation table.

    Returns:
        A tuple (dep, accum) of lists (tuple): depreciation per period and accumulated depreciation per period


    **Examples.**


    >>> costs1 = cashflow(const_value=0, nper=16, spec=(0, 1000), pyr=4)
    >>> costs2 = cashflow(const_value=0, nper=16, spec=[(0, 1000), (8, 1000)], pyr=4)
    >>> life1 = cashflow(const_value=0, nper=16, spec=(0, 4), pyr=4)
    >>> life2 = cashflow(const_value=0, nper=16, spec=[(0, 4), (8, 4)], pyr=4)
    >>> delay12 = cashflow(const_value=0, nper=16, spec=(0, 2), pyr=4)
    >>> delay22 = cashflow(const_value=0, nper=16, spec=[(0, 2), (8, 2)], pyr=4)
    >>> depreciation_soyd(costs=costs1, life=life1) # doctest: +NORMALIZE_WHITESPACE
        Qtr0   Qtr1   Qtr2   Qtr3
    0   0.00 400.00 300.00 200.00
    1 100.00   0.00   0.00   0.00
    2   0.00   0.00   0.00   0.00
    3   0.00   0.00   0.00   0.00

    >>> depreciation_soyd(costs=costs1, life=life1, delay=delay12) # doctest: +NORMALIZE_WHITESPACE
        Qtr0   Qtr1   Qtr2   Qtr3
    0   0.00   0.00   0.00 400.00
    1 300.00 200.00 100.00   0.00
    2   0.00   0.00   0.00   0.00
    3   0.00   0.00   0.00   0.00

    >>> depreciation_soyd(costs=costs2, life=life2) # doctest: +NORMALIZE_WHITESPACE
        Qtr0   Qtr1   Qtr2   Qtr3
    0   0.00 400.00 300.00 200.00
    1 100.00   0.00   0.00   0.00
    2   0.00 400.00 300.00 200.00
    3 100.00   0.00   0.00   0.00


    >>> depreciation_soyd(costs=costs2, life=life2, delay=delay22) # doctest: +NORMALIZE_WHITESPACE
        Qtr0   Qtr1   Qtr2   Qtr3
    0   0.00   0.00   0.00 400.00
    1 300.00 200.00 100.00   0.00
    2   0.00   0.00   0.00 400.00
    3 300.00 200.00 100.00   0.00

    >>> depreciation_soyd(costs=costs2, life=life2, delay=delay22, noprint=False) # doctest: +NORMALIZE_WHITESPACE
    t         Beg.    Cost  Depre.  Accum.    End.
              Book                  Depre.    Book
             Value                           Value
    ----------------------------------------------
    (0, 0)    0.00 1000.00    0.00    0.00 1000.00
    (0, 1) 1000.00    0.00    0.00    0.00 1000.00
    (0, 2) 1000.00    0.00    0.00    0.00 1000.00
    (0, 3) 1000.00    0.00  400.00  400.00  600.00
    (1, 0)  600.00    0.00  300.00  700.00  300.00
    (1, 1)  300.00    0.00  200.00  900.00  100.00
    (1, 2)  100.00    0.00  100.00 1000.00    0.00
    (1, 3)    0.00    0.00    0.00 1000.00    0.00
    (2, 0)    0.00 1000.00    0.00 1000.00 1000.00
    (2, 1) 1000.00    0.00    0.00 1000.00 1000.00
    (2, 2) 1000.00    0.00    0.00 1000.00 1000.00
    (2, 3) 1000.00    0.00  400.00 1400.00  600.00
    (3, 0)  600.00    0.00  300.00 1700.00  300.00
    (3, 1)  300.00    0.00  200.00 1900.00  100.00
    (3, 2)  100.00    0.00  100.00 2000.00    0.00
    (3, 3)    0.00    0.00    0.00 2000.00    0.00


    """
    verify_eq_time_range(costs, life)
    if salvalue is not None:
        verify_eq_time_range(costs, salvalue)
    else:
        salvalue = [0] * len(costs)
    if delay is not None:
        verify_eq_time_range(costs, delay)
    else:
        delay = [0] * len(costs)

    depr = [0] * len(costs)
    adepr = [0] * len(costs)
    begbook = [0] * len(costs)
    endbook = [0] * len(costs)

    for index, _ in enumerate(costs):
        sumdig = life[index] * (life[index] + 1) / 2
        xdepr = [(costs[index] * (100 - salvalue[index]) / 100) * (life[index] - time) / sumdig for time in range(life[index])]
        for time in range(life[index]):
            if index + time + delay[index] + 1 < len(costs):
                depr[index + time + delay[index] + 1] += xdepr[time]
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

    if noprint is True:
        retval = costs.copy()
        for index, _ in enumerate(costs):
            retval[index] = depr[index]
        return retval

    print_depr(depr, adepr, costs, begbook, endbook)



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


    >>> costs1 = cashflow(const_value=0, nper=16, spec=(0, 1000), pyr=4)
    >>> costs2 = cashflow(const_value=0, nper=16, spec=[(0, 1000), (8, 1000)], pyr=4)
    >>> life1 = cashflow(const_value=0, nper=16, spec=(0, 4), pyr=4)
    >>> life2 = cashflow(const_value=0, nper=16, spec=[(0, 4), (8, 4)], pyr=4)
    >>> delay12 = cashflow(const_value=0, nper=16, spec=(0, 2), pyr=4)
    >>> delay22 = cashflow(const_value=0, nper=16, spec=[(0, 2), (8, 2)], pyr=4)
    >>> depreciation_db(costs=costs1, life=life1, factor=1.5, convert_to_sl=False) # doctest: +NORMALIZE_WHITESPACE
        Qtr0   Qtr1   Qtr2   Qtr3
    0   0.00 375.00 234.38 146.48
    1  91.55   0.00   0.00   0.00
    2   0.00   0.00   0.00   0.00
    3   0.00   0.00   0.00   0.00

    >>> depreciation_db(costs=costs1, life=life1, factor=1.5, convert_to_sl=False, noprint=False) # doctest: +NORMALIZE_WHITESPACE
    t         Beg.    Cost  Depre.  Accum.    End.
              Book                  Depre.    Book
             Value                           Value
    ----------------------------------------------
    (0, 0)    0.00 1000.00    0.00    0.00 1000.00
    (0, 1) 1000.00    0.00  375.00  375.00  625.00
    (0, 2)  625.00    0.00  234.38  609.38  390.62
    (0, 3)  390.62    0.00  146.48  755.86  244.14
    (1, 0)  244.14    0.00   91.55  847.41  152.59
    (1, 1)  152.59    0.00    0.00  847.41  152.59
    (1, 2)  152.59    0.00    0.00  847.41  152.59
    (1, 3)  152.59    0.00    0.00  847.41  152.59
    (2, 0)  152.59    0.00    0.00  847.41  152.59
    (2, 1)  152.59    0.00    0.00  847.41  152.59
    (2, 2)  152.59    0.00    0.00  847.41  152.59
    (2, 3)  152.59    0.00    0.00  847.41  152.59
    (3, 0)  152.59    0.00    0.00  847.41  152.59
    (3, 1)  152.59    0.00    0.00  847.41  152.59
    (3, 2)  152.59    0.00    0.00  847.41  152.59
    (3, 3)  152.59    0.00    0.00  847.41  152.59

    >>> depreciation_db(costs=costs1, life=life1, delay=delay12, factor=1.5, convert_to_sl=False) # doctest: +NORMALIZE_WHITESPACE
        Qtr0   Qtr1   Qtr2   Qtr3
    0   0.00   0.00   0.00 375.00
    1 234.38 146.48  91.55   0.00
    2   0.00   0.00   0.00   0.00
    3   0.00   0.00   0.00   0.00

    >>> depreciation_db(costs=costs2, life=life2, factor=1.5, convert_to_sl=False) # doctest: +NORMALIZE_WHITESPACE
        Qtr0   Qtr1   Qtr2   Qtr3
    0   0.00 375.00 234.38 146.48
    1  91.55   0.00   0.00   0.00
    2   0.00 375.00 234.38 146.48
    3  91.55   0.00   0.00   0.00

    >>> depreciation_db(costs=costs2, life=life2, delay=delay22, factor=1.5, convert_to_sl=False) # doctest: +NORMALIZE_WHITESPACE
        Qtr0   Qtr1   Qtr2   Qtr3
    0   0.00   0.00   0.00 375.00
    1 234.38 146.48  91.55   0.00
    2   0.00   0.00   0.00 375.00
    3 234.38 146.48  91.55   0.00

    >>> depreciation_db(costs=costs2, life=life2, delay=delay22, factor=1.5, convert_to_sl=False, noprint=False) # doctest: +NORMALIZE_WHITESPACE
    t         Beg.    Cost  Depre.  Accum.    End.
              Book                  Depre.    Book
             Value                           Value
    ----------------------------------------------
    (0, 0)    0.00 1000.00    0.00    0.00 1000.00
    (0, 1) 1000.00    0.00    0.00    0.00 1000.00
    (0, 2) 1000.00    0.00    0.00    0.00 1000.00
    (0, 3) 1000.00    0.00  375.00  375.00  625.00
    (1, 0)  625.00    0.00  234.38  609.38  390.62
    (1, 1)  390.62    0.00  146.48  755.86  244.14
    (1, 2)  244.14    0.00   91.55  847.41  152.59
    (1, 3)  152.59    0.00    0.00  847.41  152.59
    (2, 0)  152.59 1000.00    0.00  847.41 1152.59
    (2, 1) 1152.59    0.00    0.00  847.41 1152.59
    (2, 2) 1152.59    0.00    0.00  847.41 1152.59
    (2, 3) 1152.59    0.00  375.00 1222.41  777.59
    (3, 0)  777.59    0.00  234.38 1456.79  543.21
    (3, 1)  543.21    0.00  146.48 1603.27  396.73
    (3, 2)  396.73    0.00   91.55 1694.82  305.18
    (3, 3)  305.18    0.00    0.00 1694.82  305.18


    """

    verify_eq_time_range(costs, life)
    if salvalue is not None:
        verify_eq_time_range(costs, salvalue)
    else:
        salvalue = [0] * len(costs)
    if delay is not None:
        verify_eq_time_range(costs, delay)
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
        xdepr = [0] * life[index]

        sl_depr = (costs[index] - salvalue[index]) / life[index]

        for time in range(life[index]):
            xdepr[time] = rem_cost * xfactor
            if convert_to_sl is True and xdepr[time] < sl_depr:
                xdepr[time] = sl_depr
            rem_cost -= xdepr[time]
            if rem_cost < salvalue[index]:
                rem_cost += xdepr[time]
                xdepr[time] = rem_cost - salvalue[index]
                rem_cost = salvalue[index]

        for time in range(life[index]):
            if index + time + delay[index] + 1 < len(costs):
                depr[index + time + delay[index] + 1] += xdepr[time]
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

    if noprint is True:
        retval = costs.copy()
        for index, _ in enumerate(costs):
            retval[index] = depr[index]
        return retval

    print_depr(depr, adepr, costs, begbook, endbook)





if __name__ == "__main__":
    import doctest
    doctest.testmod()
