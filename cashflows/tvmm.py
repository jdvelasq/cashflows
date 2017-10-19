"""
Time value of money models
===============================================================================

This module contains functions for computing the time value of the money.

* ``pvfv``: computes the missing value in the equation
  ``fval = pval * (1 + rate) ** nper``, that represents the following
  cashflow.

.. image:: ./images/pvfv.png
    :width: 350px
    :align: center

* ``pvpmt``: computes the missing value (`pmt`, `pval`, `nper`, `nrate`) in a
  model relating a present value and
  a finite sequence of payments made at the end of the period (payments
  in arrears, or ordinary annuities), as indicated in the following cashflow
  diagram:

.. image:: ./images/pvpmt.png
    :width: 350px
    :align: center

* ``pmtfv``: computes the missing value (`pmt`, `fval`, `nper`, `nrate`) in a
  model relating a finite sequence  of payments in advance (annuities due)
  and a future value, as indicated in the following diagram:

.. image:: ./images/pmtfv.png
    :width: 350px
    :align: center

* ``tvmm``: computes the missing value (`pmt`, `fval`, `pval, `nper`, `nrate`)
  in a model relating a finite sequence  of payments made at the beginning or at
  the end of the period, a present value, a future value, and an interest rate,
  as indicated in the following diagram:

.. image:: ./images/tvmm.png
    :width: 650px
    :align: center


"""

import numpy as np
import pandas as pd

# cashflows.
from cashflows.common import _vars2list



def tvmm(pval=None, fval=None, pmt=None, nrate=None, nper=None, due=0, pyr=1):
    """Computes present and future values, periodic payments, nominal interest
    rate or number of periods.

    Args:
        pval (float, list): Present value.
        fval (float, list): Future value.
        pmt (float, list): Periodic payment.
        nrate (float, list): Nominal interest rate per year.
        nper (int, list): Number of compounding periods.
        due (int): When payments are due.
        pyr (int, list): number of periods per year.


    Returns:
        Argument set to None in the function call.

    Effective interest rate per period is calculated as `nrate` / `pyr`.


    **Examples.**

    In this example shows how to find different values for a loan of 5000, with a
    monthly payment of 130 at the end of the month, a life of 48 periods, and a
    interest rate of 0.94 per month (equivalent to 11.32% nominal)

    * Periodic payment:

    >>> pmt = tvmm(pval=5000, nrate=11.32/12, nper=48, fval=0)
    >>> pmt # doctest: +ELLIPSIS
    -130.00...

    * Future value:

    >>> tvmm(pval=5000, nrate=11.32/12, nper=48, pmt=pmt) # doctest: +ELLIPSIS
    -0.0...

    * Present value:

    >>> tvmm(nrate=11.32/12, nper=48, pmt=pmt, fval = 0.0) # doctest: +ELLIPSIS
    5000...

    * Rate:

    >>> tvmm(pval=5000, nper=48, pmt=pmt, fval = 0.0) # doctest: +ELLIPSIS
    0.94...

    * Number of periods:

    >>> tvmm(pval=5000, nrate=11.32/12, pmt=pmt, fval=0.0) # doctest: +ELLIPSIS
    48.0...

    * Periodic paymnts:

    >>> tvmm(pval=5000, nrate=11.32, nper=48, fval=0, pyr=12) # doctest: +ELLIPSIS
    -130.00...

    * Nominal rate:

    >>> tvmm(pval=5000, nper=48, pmt=pmt, fval = 0.0, pyr=12) # doctest: +ELLIPSIS
    11.32...

    * Vectors of data:

    >>> tvmm(pval=[5000, 4000, 3000], nper=48, pmt=pmt, fval = 0.0, pyr=12) # doctest: +ELLIPSIS
    0    11.320000
    1    23.818359
    2    42.045544
    dtype: float64


    """

    #pylint: disable=too-many-arguments
    #pylint: disable=too-many-branches

    numnone = 0
    numnone += 1 if pval is None else 0
    numnone += 1 if fval is None else 0
    numnone += 1 if nper is None else 0
    numnone += 1 if pmt is None else 0
    numnone += 1 if nrate is None else 0

    if numnone > 1:
        raise ValueError('One of the params must be set to None')

    if numnone == 0:
        pmt = None

    if pmt == 0.0:
        pmt = 0.0000001

    nrate = np.array(nrate)

    if pval is None:
        result = np.pv(rate=nrate/100/pyr, nper=nper, fv=fval, pmt=pmt, when=due)
    elif fval is None:
        result = np.fv(rate=nrate/100/pyr, nper=nper, pv=pval, pmt=pmt, when=due)
    elif nper is None:
        result = np.nper(rate=nrate/100/pyr, pv=pval, fv=fval, pmt=pmt, when=due)
    elif pmt is None:
        result = np.pmt(rate=nrate/100/pyr, nper=nper, pv=pval, fv=fval, when=due)
    else:
        result = np.rate(pv=pval, nper=nper, fv=fval, pmt=pmt, when=due) * 100 * pyr


    if isinstance(result, np.ndarray):
        return pd.Series(result)
    return result



def pvfv(pval=None, fval=None, nrate=None, nper=None, pyr=1):
    """Computes the missing argument (set to None) in the function call.

    Args:
        pval (float, list): Present value.
        fval (float, list): Future value.
        nrate (float, list): Nominal interest rate per year.
        nper (int, list): Number of compounding periods.
        pyr (int, list): number of periods per year.

    Returns:
        The value of the parameter set to None in the function call.

    Effective interest rate per period is calculated as `nrate` / `pyr`.

    """
    result = tvmm(pval=pval, fval=fval, pmt=0, nrate=nrate, nper=nper, due=0, pyr=pyr)
    # if asdataframe == True:
    #     result = result.drop('pmt', 1)
    #     result = result.drop('due', 1)
    #     result = result.drop('prate', 1)
    #     result = result.drop('erate', 1)
    return result


def pmtfv(pmt=None, fval=None, nrate=None, nper=None, pyr=1):
    """CComputes the missing argument (set to None) in the function call.

    Args:
        pmt (float, list): Periodic payment.
        fval (float, list): Future value.
        nrate (float, list): Nominal rate per year.
        nper (int, list): Number of compounding periods.
        pyr (int, list): number of periods per year.

    Returns:
        The value of the parameter set to None in the function call.

    Effective interest rate per period is calculated as `nrate` / `pyr`.

    """
    result = tvmm(pval=0, fval=fval, pmt=pmt, nrate=nrate, nper=nper, due=1, pyr=pyr)
    # if asdataframe == True:
    #     result = result.drop('pval', 1)
    #     result = result.drop('due', 1)
    #     result = result.drop('prate', 1)
    #     result = result.drop('erate', 1)
    return result


def pvpmt(pmt=None, pval=None, nrate=None, nper=None, pyr=1):
    """Computes the missing argument (set to None) in the function call.

    Args:
        pmt (float, list): Periodic payment.
        pval (float, list): Present value.
        nrate (float, list): Nominal interest rate per year.
        nper (int, list): Number of compounding periods.
        pyr (int, list): number of periods per year.

    Returns:
        The value of the parameter set to None in the function call.

    Effective interest rate per period is calculated as `nrate` / `pyr`.

    """
    result = tvmm(pval=pval, fval=0, pmt=pmt, nrate=nrate, nper=nper, due=0, pyr=pyr)
    # if asdataframe is True:
    #     result = result.drop('fval', 1)
    #     result = result.drop('due', 1)
    #     result = result.drop('prate', 1)
    #     result = result.drop('erate', 1)
    return result


def amortize(pval=None, fval=None, pmt=None, nrate=None, nper=None, due=0, pyr=1):
    """Amortization schedule of a loan.

    Args:
        pval (float): present value.
        fval (float): Future value.
        pmt (float): periodic payment per period.
        nrate (float): nominal interest rate per year.
        nper (int): total number of compounding periods.
        due (int): When payments are due.
        pyr (int, list): number of periods per year.

    Returns:
        A pandas.DataFrame


    **Examples.**

    >>> pmt = tvmm(pval=100, nrate=10, nper=5, fval=0) # doctest: +ELLIPSIS
    >>> table = amortize(pval=100, nrate=10, nper=5, fval=0)
    >>> table # doctest: +NORMALIZE_WHITESPACE
       Beg_Balance  Payment  Interest  Principal  Final_Balance
    0       100.00     0.00      0.00       0.00         100.00
    1       100.00   -26.38     10.00     -16.38          83.62
    2        83.62   -26.38      8.36     -18.02          65.60
    3        65.60   -26.38      6.56     -19.82          45.78
    4        45.78   -26.38      4.58     -21.80          23.98
    5        23.98   -26.38      2.40     -23.98           0.00

    >>> amortize(pval=-100, nrate=10, nper=5, fval=0) # doctest: +ELLIPSIS +NORMALIZE_WHITESPACE
       Beg_Balance  Payment  Interest  Principal  Final_Balance
    0      -100.00     0.00      0.00       0.00        -100.00
    1      -100.00    26.38    -10.00      16.38         -83.62
    2       -83.62    26.38     -8.36      18.02         -65.60
    3       -65.60    26.38     -6.56      19.82         -45.78
    4       -45.78    26.38     -4.58      21.80         -23.98
    5       -23.98    26.38     -2.40      23.98          -0.00

    >>> amortize(pval=100, nrate=10, nper=5, fval=0, due=1) # doctest: +ELLIPSIS +NORMALIZE_WHITESPACE
       Beg_Balance  Payment  Interest  Principal  Final_Balance
    0       100.00   -23.98      0.00     -23.98          76.02
    1        76.02   -23.98      7.60     -16.38          59.64
    2        59.64   -23.98      5.96     -18.02          41.62
    3        41.62   -23.98      4.16     -19.82          21.80
    4        21.80   -23.98      2.18     -21.80           0.00
    5         0.00     0.00      0.00       0.00           0.00

    >>> amortize(pval=-100, nrate=10, nper=5, fval=0, due=1) # doctest: +ELLIPSIS +NORMALIZE_WHITESPACE
       Beg_Balance  Payment  Interest  Principal  Final_Balance
    0      -100.00    23.98      0.00      23.98         -76.02
    1       -76.02    23.98     -7.60      16.38         -59.64
    2       -59.64    23.98     -5.96      18.02         -41.62
    3       -41.62    23.98     -4.16      19.82         -21.80
    4       -21.80    23.98     -2.18      21.80          -0.00
    5        -0.00     0.00     -0.00      -0.00          -0.00



    >>> table = amortize(pval=100, nrate=10, nper=5, fval=0) # doctest: +ELLIPSIS
    >>> table['Interest']  # doctest: +ELLIPSIS
    0     0.00
    1    10.00
    2     8.36
    3     6.56
    4     4.58
    5     2.40
    Name: Interest, dtype: float64

    >>> table['Payment']  # doctest: +ELLIPSIS
    0     0.00
    1   -26.38
    2   -26.38
    3   -26.38
    4   -26.38
    5   -26.38
    Name: Payment, dtype: float64

    >>> table['Final_Balance']  # doctest: +ELLIPSIS
    0    100.00
    1     83.62
    2     65.60
    3     45.78
    4     23.98
    5      0.00
    Name: Final_Balance, dtype: float64



    """

    #pylint: disable=too-many-arguments


    numnone = 0
    numnone += 1 if pval is None else 0
    numnone += 1 if fval is None else 0
    numnone += 1 if nper is None else 0
    numnone += 1 if pmt is None else 0
    numnone += 1 if nrate is None else 0


    if numnone > 1:
        raise ValueError('One of the params must be set to None')

    if numnone == 0:
        pmt = None

    if pmt == 0.0:
        pmt = 0.0000001

    if pval is None:
        pval = tvmm(fval=fval, pmt=pmt, nrate=nrate, nper=nper, due=due, pyr=pyr)
    elif fval is None:
        fval = tvmm(pval=pval, pmt=pmt, nrate=nrate, nper=nper, due=due, pyr=pyr)
    elif nper is None:
        nper = tvmm(pval=pval, fval=fval, pmt=pmt, nrate=nrate, due=due, pyr=pyr)
    elif pmt is None:
        pmt = tvmm(pval=pval, fval=fval, nrate=nrate, nper=nper, due=due, pyr=pyr)
    else:
        nrate = tvmm(pval=pval, fval=fval, pmt=pmt, nper=nper, due=due, pyr=pyr)

    erate = nrate / pyr / 100

    if int(nper) != nper:
        nper = int(nper + 0.9)

    # variable definition
    begbal = [0] * (nper + 1)
    ipmt = [0] * (nper + 1)
    ppmt = [0] * (nper + 1)
    rembal = [0] * (nper + 1)

    # calcula el pmt periodico
    pmt = [pmt] * (nper + 1)

    if due == 0:  # vencido
        pmt[0] = 0

    if due == 1:  # anticipado
        pmt[nper] = 0

    begbal[0] = pval


    for period in range(nper + 1):

        if period == 0:
            rembal[0] = begbal[0] + pmt[0]
            ppmt[0] = + pmt[0]
        else:
            begbal[period] = rembal[period-1]
            ipmt[period] = begbal[period] * erate
            ppmt[period] = pmt[period] + ipmt[period]
            rembal[period] = begbal[period] + ppmt[period]

    table = pd.DataFrame({'Beg_Balance': begbal,
                          'Payment': pmt,
                          'Interest': ipmt,
                          'Principal': ppmt,
                          'Final_Balance': rembal})
    table = table[['Beg_Balance', 'Payment', 'Interest', 'Principal', 'Final_Balance']]
    table = table.round(2)

    return table

def iconv(nrate=None, erate=None, prate=None, pyr=1):
    """The function `iconv` computes the conversion among periodic, nominal
    and effective interest rates. Only an interest rate (periodic, nominal or
    effective) must be specified and the other two are computed. The periodic
    rate is the rate used in each compounding period. The effective rate is
    the equivalent rate that produces the same interest earnings that a periodic
    rate when there is P compounding periods in a year. The nominal rate is
    defined as the annual rate computed as P times the periodic rate.

    Args:
        nrate (float, list, TimeSeries): nominal interest rate per year.
        erate (float, list, TimeSeries): effective interest rate per year.
        prate (float, list, TimeSeries): periodic rate
        pyr (int, list): number of compounding periods per year

    Returns:
        A tuple:
        * (**nrate**, **prate**): when **erate** is specified.
        * (**erate**, **prate**): when **nrate** is specified.
        * (**nrate**, **erate**): when **prate** is specified.









    `iconv` accepts Python vectors.







    When a rate and the number of compounding periods (`pyr`) are vectors, they
    must have the same length. Computations are executed using the first rate
    with the first compounding and so on.





    """

    numnone = 0
    if nrate is None:
        numnone += 1
    if erate is None:
        numnone += 1
    if prate is None:
        numnone += 1
    if numnone != 2:
        raise ValueError('Two of the rates must be set to `None`')


    if isinstance(nrate, pd.Series):
        pyr = getpyr(nrate)
        erate = nrate.copy()
        prate = nrate.copy()
        for index in range(len(nrate)):
            prate[index] = nrate[index] / pyr
            erate[index] = 100 * (np.power(1 + prate[index]/100, pyr) - 1)
        return (erate, prate)

    if isinstance(erate, pd.Series):
        pyr = getpyr(erate)
        nrate = erate.copy()
        prate = erate.copy()
        for index in range(len(erate)):
            prate[index] = 100 * (np.power(1 + erate[index]/100, 1. / pyr) - 1)
            nrate[index] = pyr * prate[index]
        return (nrate, prate)

    if isinstance(prate, pd.Series):
        pyr = getpyr(prate)
        erate = prate.copy()
        nrate = prate.copy()
        for index in range(len(prate)):
            nrate[index] = prate[index] * pyr
            erate[index] = 100 * (np.power(1 + prate[index]/100, pyr) - 1)
        return (nrate, erate)

    if isinstance(nrate, list) and isinstance(pyr, list) and len(nrate) != len(pyr):
        raise ValueError('List must have the same length')
    if isinstance(erate, list) and isinstance(pyr, list) and len(erate) != len(pyr):
        raise ValueError('List must have the same length')
    if isinstance(prate, list) and isinstance(pyr, list) and len(prate) != len(pyr):
        raise ValueError('List must have the same length')

    maxlen = 1
    if isinstance(nrate, list):
        maxlen = max(maxlen, len(nrate))
    if isinstance(erate, list):
        maxlen = max(maxlen, len(erate))
    if isinstance(prate, list):
        maxlen = max(maxlen, len(prate))
    if isinstance(pyr, list):
        maxlen = max(maxlen, len(pyr))

    if isinstance(pyr, (int, float)):
        pyr = [pyr] * maxlen
    pyr = np.array(pyr)









# def equivalent_rate(nrate=None, erate=None, prate=None):
#     """Returns the equivalent interest rate over a time period.
#
#     Args:
#         nrate (TimeSeries): Nominal interest rate per year.
#         erate (TimeSeries): Effective interest rate per year.
#         prate (TimeSeries): Periodic interest rate.
#
#     Returns:
#         float value.
#
#     Only one of the interest rate must be supplied for the computation.
#
#     >>> equivalent_rate(prate=interest_rate([10]*5, start='2000Q1', freq='Q')) # doctest: +ELLIPSIS
#     10.0...
#
#
#     """
#     numnone = 0
#     if nrate is None:
#         numnone += 1
#     if erate is None:
#         numnone += 1
#     if prate is None:
#         numnone += 1
#     if numnone != 2:
#         raise ValueError('Two of the rates must be set to `None`')
#
#     if nrate is not None:
#         value = nrate.tolist()
#         factor = 1
#         for element in value[1:]:
#             factor *= (1 + element / 100 / nrate.pyr)
#         return 100 * nrate.pyr * (factor**(1/(len(value) - 1)) - 1)
#
#     if prate is not None:
#         value = prate.tolist()
#         factor = 1
#         for element in value[1:]:
#             factor *= (1 + element / 100)
#         return 100  * (factor**(1/(len(value) - 1)) - 1)
#
#     if erate is not None:
#         value = erate.tolist()
#         factor = 1
#         for element in value[1:]:
#             factor *= (1 + (numpy.power(1 + element/100, 1. / erate.pyr) - 1))
#         return 100  * (factor**(1/(len(value) - 1)) - 1)



if __name__ == "__main__":
    import doctest
    doctest.testmod()
