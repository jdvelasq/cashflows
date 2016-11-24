"""
Tutorial
===============================================================================

Depreciation using the Straight Line Method
-------------------------------------------------------------------------------

>>> costs = generic_cashflow(const_value=0, nper=12, spec=(0, 1000), pyr=4)
>>> life = generic_cashflow(const_value=0, nper=12, spec=(0, 4), pyr=4)
>>> delay2 = generic_cashflow(const_value=0, nper=12, spec=(0, 2), pyr=4)

>>> depreciation_sl(costs=costs, life=life) # doctest: +NORMALIZE_WHITESPACE
    Qtr0   Qtr1   Qtr2   Qtr3
0   0.00 250.00 250.00 250.00
1 250.00   0.00   0.00   0.00
2   0.00   0.00   0.00   0.00

>>> depreciation_sl(costs=costs, life=life, delay=delay2) # doctest: +NORMALIZE_WHITESPACE
    Qtr0   Qtr1   Qtr2   Qtr3
0   0.00   0.00 250.00 250.00
1 250.00 250.00   0.00   0.00
2   0.00   0.00   0.00   0.00

>>> depreciation_soyd(costs=costs, life=life) # doctest: +NORMALIZE_WHITESPACE
    Qtr0   Qtr1   Qtr2   Qtr3
0   0.00 396.00 297.00 198.00
1  99.00   0.00   0.00   0.00
2   0.00   0.00   0.00   0.00

>>> depreciation_soyd(costs=costs, life=life, delay=delay2) # doctest: +NORMALIZE_WHITESPACE
    Qtr0   Qtr1   Qtr2   Qtr3
0   0.00   0.00 396.00 297.00
1 198.00  99.00   0.00   0.00
2   0.00   0.00   0.00   0.00

>>> depreciation_db(costs=costs, life=life, factor=1.5) # doctest: +NORMALIZE_WHITESPACE
    Qtr0   Qtr1   Qtr2   Qtr3
0   0.00 375.00 250.00 250.00
1 125.00   0.00   0.00   0.00
2   0.00   0.00   0.00   0.00

>>> depreciation_db(costs=costs, life=life, factor=1.5, delay=delay2) # doctest: +NORMALIZE_WHITESPACE
    Qtr0   Qtr1   Qtr2   Qtr3
0   0.00   0.00 375.00 250.00
1 250.00 125.00   0.00   0.00
2   0.00   0.00   0.00   0.00




Depreciation using the Sum-of-years Digits Method
-------------------------------------------------------------------------------






Depreciation using the Declining Balance Method
-------------------------------------------------------------------------------




















Description of the functions in this module
===============================================================================


"""


from cashflows.gtimeseries import TimeSeries, generic_cashflow, generic_rate, verify_eq_time_range

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
    header += fmt_header.format('Begin')
    header += fmt_header.format('Cost')
    header += fmt_header.format('Deprec')
    header += fmt_header.format('Accum')
    header += fmt_header.format('Ending')
    txt.append(header)

    header = fmt_timeid.format('')
    header += fmt_header.format('Book')
    header += fmt_header.format('')
    header += fmt_header.format('')
    header += fmt_header.format('Deprec')
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

    """
    verify_eq_time_range(costs, life)
    if salvalue is not None:
        verify_eq_time_range(costs, salvalue)
    else:
        salvalue = [0] * len(costs)
    if delay is not None:
        verify_eq_time_range(costs, delay)
    else:
        delay = [1] * len(costs)

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
            if index + time + delay[index] < len(costs):
                depr[index + time + delay[index]] += xdepr[time]
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
        if time < len(costs):
            begbook[time] += costs[time]
        endbook[time] = begbook[time] - depr[time]

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

    """
    verify_eq_time_range(costs, life)
    if salvalue is not None:
        verify_eq_time_range(costs, salvalue)
    else:
        salvalue = [1] * len(costs)
    if delay is not None:
        verify_eq_time_range(costs, delay)
    else:
        delay = [1] * len(costs)

    depr = [0] * len(costs)
    adepr = [0] * len(costs)
    begbook = [0] * len(costs)
    endbook = [0] * len(costs)

    for index, _ in enumerate(costs):
        sumdig = life[index] * (life[index] + 1) / 2
        xdepr = [(costs[index] * (100 - salvalue[index]) / 100) * (life[index] - time) / sumdig for time in range(life[index])]
        for time in range(life[index]):
            if index + time + delay[index] < len(costs):
                depr[index + time + delay[index]] += xdepr[time]
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
        if time < len(costs):
            begbook[time] += costs[time]
        endbook[time] = begbook[time] - depr[time]

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
        ccost (TimeSeries): the cost per period of the assets.
        life (TimeSeries): number of depreciation periods for the asset.
        salvalue(TimeSeries): salvage value as a percentage of cost.
        factor (float): acelerating factor for depreciation.
        convert_to_sl (bool): converts to straight line method?
        noprint (bool): when True, the procedure prints a depreciation table.

    Returns:
        A tuple (dep, accum) of lists (tuple): depreciation per period and accumulated depreciation per period


    """

    verify_eq_time_range(costs, life)
    if salvalue is not None:
        verify_eq_time_range(costs, salvalue)
    else:
        salvalue = [0] * len(costs)
    if delay is not None:
        verify_eq_time_range(costs, delay)
    else:
        delay = [1] * len(costs)
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
            if index + time + delay[index] < len(costs):
                depr[index + time + delay[index]] += xdepr[time]
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
        if time < len(costs):
            begbook[time] += costs[time]
        endbook[time] = begbook[time] - depr[time]

    if noprint is True:
        retval = costs.copy()
        for index, _ in enumerate(costs):
            retval[index] = depr[index]
        return retval

    print_depr(depr, adepr, costs, begbook, endbook)





if __name__ == "__main__":
    import doctest
    doctest.testmod()
