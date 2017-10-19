"""
Savings
===============================================================================


"""
# import sys
# import os

# sys.path.insert(0, os.path.abspath('..'))

import pandas as pd

#cashflows.
from cashflows.timeseries import cashflow, interest_rate, verify_period_range
from cashflows.common import getpyr


def savings(deposits, nrate, initbal=0):
    """
    Computes the final balance for a savings account with arbitrary deposits and
    withdrawls and variable interset rate.

    Args:
        deposits (TimeSeries): deposits to the account.
        nrate (TimeSeries): nominal interest rate paid by the account.
        initbal (float): initial balance of the account.

    Return:
        A pandas.DataFrame.


    **Examples**

    >>> cflo = cashflow(const_value=[100]*12, start='2000Q1', freq='Q')
    >>> nrate = interest_rate([10]*12, start='2000Q1', freq='Q')
    >>> savings(deposits=cflo, nrate=nrate, initbal=0) # doctest: +NORMALIZE_WHITESPACE
            Beginning_Balance  Deposits  Earned_Interest  Ending_Balance  \\
    2000Q1           0.000000     100.0         0.000000      100.000000
    2000Q2         100.000000     100.0         2.500000      202.500000
    2000Q3         202.500000     100.0         5.062500      307.562500
    2000Q4         307.562500     100.0         7.689063      415.251562
    2001Q1         415.251562     100.0        10.381289      525.632852
    2001Q2         525.632852     100.0        13.140821      638.773673
    2001Q3         638.773673     100.0        15.969342      754.743015
    2001Q4         754.743015     100.0        18.868575      873.611590
    2002Q1         873.611590     100.0        21.840290      995.451880
    2002Q2         995.451880     100.0        24.886297     1120.338177
    2002Q3        1120.338177     100.0        28.008454     1248.346631
    2002Q4        1248.346631     100.0        31.208666     1379.555297
    <BLANKLINE>
            Nominal_Rate
    2000Q1          10.0
    2000Q2          10.0
    2000Q3          10.0
    2000Q4          10.0
    2001Q1          10.0
    2001Q2          10.0
    2001Q3          10.0
    2001Q4          10.0
    2002Q1          10.0
    2002Q2          10.0
    2002Q3          10.0
    2002Q4          10.0

    >>> cflo = cashflow(const_value=[0, 100, 0, 100, 100], start='2000Q1', freq='A')
    >>> nrate = interest_rate([0, 1, 2, 3, 4], start='2000Q1', freq='A')
    >>> savings(deposits=cflo, nrate=nrate, initbal=1000) # doctest: +NORMALIZE_WHITESPACE
          Beginning_Balance  Deposits  Earned_Interest  Ending_Balance  \\
    2000           1000.000       0.0          0.00000      1000.00000
    2001           1000.000     100.0         10.00000      1110.00000
    2002           1110.000       0.0         22.20000      1132.20000
    2003           1132.200     100.0         33.96600      1266.16600
    2004           1266.166     100.0         50.64664      1416.81264
    <BLANKLINE>
          Nominal_Rate
    2000           0.0
    2001           1.0
    2002           2.0
    2003           3.0
    2004           4.0

    """
    verify_period_range([deposits, nrate])

    begbal = deposits.copy()
    interest = deposits.copy()
    endbal = deposits.copy()
    pyr = getpyr(deposits)

    for time, _ in enumerate(deposits):
        if time == 0:
            begbal[0] = initbal
            interest[0] = begbal[0] * nrate[0] / 100 / pyr
            endbal[0] = begbal[0] + deposits[0] + interest[0]
        else:
            begbal[time] = endbal[time - 1]
            interest[time] = begbal[time] * nrate[time] / 100 / pyr
            if deposits[time] < 0 and -deposits[time] > begbal[time] + interest[time]:
                deposits[time] = -(begbal[time] + interest[time])
            endbal[time] = begbal[time] + deposits[time] + interest[time]

    table = pd.DataFrame({'Beginning_Balance' : begbal,
                          'Deposits' : deposits,
                          'Nominal_Rate':nrate,
                          'Earned_Interest': interest,
                          'Ending_Balance': endbal })

    return table


if __name__ == "__main__":
    import doctest
    doctest.testmod()
