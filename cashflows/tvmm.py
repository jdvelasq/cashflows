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

from cashflows.common import _vars2list
from cashflows.rate import iconv


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
        return result.tolist()
    return result


    # nrate = nrate.tolist()
    #
    # if pval is None:
    #     pval = result
    # elif fval is None:
    #     fval = result
    # elif nper is None:
    #     nper = result
    # elif pmt is None:
    #     pmt = result
    # else:
    #     nrate = result
    #
    # params = _vars2list([pval, fval, nper, pmt, nrate])
    # pval = params[0]
    # fval = params[1]
    # nper = params[2]
    # pmt = params[3]
    # nrate = params[4]
    #
    # # raise ValueError(nrate.__repr__())
    #
    # erate, prate = iconv(nrate=nrate, pyr=pyr)
    #
    # table = pd.DataFrame({'pval' : pval,
    #                       'fval' : fval,
    #                       'due': due,
    #                       'nper':nper,
    #                       'pyr':pyr,
    #                       'nrate': nrate,
    #                       'erate': erate,
    #                       'prate': prate})
    #
    # if len(pmt) == 1:
    #     table['pmt'] = pmt
    # else:
    #     aux = []
    #     if isinstance(pmt, list):
    #         for item, _ in enumerate(pmt):
    #             aux.append(pmt[item])
    #         table['pmt'] = aux
    #
    #     # if isinstance(pmt, list):
    #     #     if due == 0:
    #     #         for item, _ in enumerate(pmt):
    #     #             aux.append(pmt[item][-1])
    #     #     else:
    #     #         for item, _ in enumerate(pmt):
    #     #             aux.append(pmt[item][0])
    #     #     table['pmt'] = aux
    #
    #
    #
    # table = table[['pval', 'fval', 'pmt', 'nper', 'pyr', 'nrate', 'erate', 'prate', 'due']]
    # # table = table.round(2)
    # return table




        # if due == 0:
        #     sdue = 'END'
        #     txtpmt = []
        #     for item, _ in enumerate(pval):
        #         txtpmt.append(pmt[item][-1])
        # else:
        #     sdue = 'BEG'
        #     txtpmt = []
        #     for item, _ in enumerate(pval):
        #         txtpmt.append(pmt[item][0])
        #
        #
        # maxlen = 5
        # for value1, value2, value3, value4 in zip(pval, fval, txtpmt, nper):
        #     maxlen = max(maxlen, len('{:1.2f}'.format(value1)))
        #     maxlen = max(maxlen, len('{:1.2f}'.format(value2)))
        #     maxlen = max(maxlen, len('{:1.2f}'.format(value3)))
        #     maxlen = max(maxlen, len('{:1.2f}'.format(value4)))
        #
        # len_aux = len('{:d}'.format(len(pval)))
        #
        # fmt_num = ' {:' + '{:d}'.format(maxlen) + '.2f}'
        # fmt_num = '{:<' + '{:d}'.format(len_aux) +  'd}' + fmt_num * 7 + ' {:3s}'
        # # fmt_shr = '{:' + '{:d}'.format(len_aux) + 's}'
        # fmt_hdr = ' {:>' + '{:d}'.format(maxlen) + 's}'
        # fmt_hdr = '{:' + '{:d}'.format(len_aux) + 's}' + fmt_hdr * 7 + ' due'
        #
        #
        # txt = fmt_hdr.format('#', 'pval', 'fval', 'pmt', 'nper', 'nrate', 'erate', 'prate')
        # print(txt)
        # print('-' * len_aux + '-' * maxlen * 7 + '-' * 7 + '----')
        # for item, _ in enumerate(pval):
        #     print(fmt_num.format(item,
        #                          pval[item],
        #                          fval[item],
        #                          txtpmt[item],
        #                          nper[item],
        #                          nrate[item],
        #                          erate[item],
        #                          prate[item],
        #                          sdue))


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
       Beg balance  Payment  Interest  Principal  Final balance
    0       100.00     0.00      0.00       0.00         100.00
    1       100.00   -26.38     10.00     -16.38          83.62
    2        83.62   -26.38      8.36     -18.02          65.60
    3        65.60   -26.38      6.56     -19.82          45.78
    4        45.78   -26.38      4.58     -21.80          23.98
    5        23.98   -26.38      2.40     -23.98           0.00

    >>> amortize(pval=-100, nrate=10, nper=5, fval=0) # doctest: +ELLIPSIS +NORMALIZE_WHITESPACE
       Beg balance  Payment  Interest  Principal  Final balance
    0      -100.00     0.00      0.00       0.00        -100.00
    1      -100.00    26.38    -10.00      16.38         -83.62
    2       -83.62    26.38     -8.36      18.02         -65.60
    3       -65.60    26.38     -6.56      19.82         -45.78
    4       -45.78    26.38     -4.58      21.80         -23.98
    5       -23.98    26.38     -2.40      23.98          -0.00

    >>> amortize(pval=100, nrate=10, nper=5, fval=0, due=1) # doctest: +ELLIPSIS +NORMALIZE_WHITESPACE
       Beg balance  Payment  Interest  Principal  Final balance
    0       100.00   -23.98      0.00     -23.98          76.02
    1        76.02   -23.98      7.60     -16.38          59.64
    2        59.64   -23.98      5.96     -18.02          41.62
    3        41.62   -23.98      4.16     -19.82          21.80
    4        21.80   -23.98      2.18     -21.80           0.00
    5         0.00     0.00      0.00       0.00           0.00

    >>> amortize(pval=-100, nrate=10, nper=5, fval=0, due=1) # doctest: +ELLIPSIS +NORMALIZE_WHITESPACE
       Beg balance  Payment  Interest  Principal  Final balance
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

    >>> table['Final balance']  # doctest: +ELLIPSIS
    0    100.00
    1     83.62
    2     65.60
    3     45.78
    4     23.98
    5      0.00
    Name: Final balance, dtype: float64



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

    table = pd.DataFrame({'Beg balance': begbal,
                          'Payment': pmt,
                          'Interest': ipmt,
                          'Principal': ppmt,
                          'Final balance': rembal})
    table = table[['Beg balance', 'Payment', 'Interest', 'Principal', 'Final balance']]
    table = table.round(2)

    return table
    # if asdataframe is True:
    #     return (ppmt, ipmt, pmt, rembal)
    #
    # txt = ['t      Beginning     Periodic     Interest    Principal        Final',
    #        '       Principal      Payment      Payment    Repayment    Principal',
    #        '          Amount       Amount                                 Amount',
    #        '--------------------------------------------------------------------']
    #
    # for time in range(nper + 1):
    #
    #     fmt = '{:<3d} {:12.2f} {:12.2f} {:12.2f} {:12.2f} {:12.2f}'
    #
    #
    #     txt.append(fmt.format(time,
    #                           begbal[time],
    #                           pmt[time],
    #                           ipmt[time],
    #                           ppmt[time],
    #                           rembal[time]))
    # print('\n'.join(txt))
    # return None

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


    Effective rate to nominal rate compounded monthly and monthly peridic rate.

    >>> iconv(erate=10, pyr=12) # doctest: +ELLIPSIS
    (9.56..., 0.79...)

    >>> iconv(prate=1, pyr=12) # doctest: +ELLIPSIS
    (12, 12.68...)

    >>> iconv(nrate=10, pyr=12) # doctest: +ELLIPSIS
    (10.47..., 0.83...)


    `iconv` accepts Python vectors.

    >>> iconv(erate=10, pyr=[3, 6, 12]) # doctest: +ELLIPSIS
    ([9.68..., 9.60..., 9.56...], [3.22..., 1.60..., 0.79...])

    >>> iconv(prate=1, pyr=[3, 6, 12]) # doctest: +ELLIPSIS
    ([3, 6, 12], [3.03..., 6.15..., 12.68...])

    >>> iconv(nrate=10, pyr=[3, 6, 12]) # doctest: +ELLIPSIS
    ([10.33..., 10.42..., 10.47...], [3.33..., 1.66..., 0.83...])

    >>> iconv(erate=[10, 12, 14], pyr=12) # doctest: +ELLIPSIS
    ([9.56..., 11.38..., 13.17...], [0.79..., 0.94..., 1.09...])

    >>> iconv(prate=[1, 2, 3], pyr=12) # doctest: +ELLIPSIS
    ([12, 24, 36], [12.68..., 26.82..., 42.57...])

    >>> iconv(nrate=[10, 12, 14], pyr=12) # doctest: +ELLIPSIS
    ([10.47..., 12.68..., 14.93...], [0.83..., 1.0, 1.16...])

    When a rate and the number of compounding periods (`pyr`) are vectors, they
    must have the same length. Computations are executed using the first rate
    with the first compounding and so on.

    >>> iconv(erate=[10, 12, 14], pyr=[3, 6, 12]) # doctest: +ELLIPSIS
    ([9.68..., 11.44..., 13.17...], [3.22..., 1.90..., 1.09...])

    >>> iconv(nrate=[10, 12, 14], pyr=[3, 6, 12]) # doctest: +ELLIPSIS
    ([10.33..., 12.61..., 14.93...], [3.33..., 2.0, 1.16...])

    >>> iconv(prate=[1, 2, 3], pyr=[3, 6, 12]) # doctest: +ELLIPSIS
    ([3, 12, 36], [3.03..., 12.61..., 42.57...])

    `iconv` accepts pandas.Series objects

    >>> erate, prate = iconv(nrate = interest_rate(const_value=12, start='2000-06', periods=12, freq='6M'))
    >>> prate # doctest: +NORMALIZE_WHITESPACE
    2000-06    6.0
    2000-12    6.0
    2001-06    6.0
    2001-12    6.0
    2002-06    6.0
    2002-12    6.0
    2003-06    6.0
    2003-12    6.0
    2004-06    6.0
    2004-12    6.0
    2005-06    6.0
    2005-12    6.0
    Freq: 6M, dtype: float64

    >>> erate # doctest: +NORMALIZE_WHITESPACE
    2000-06    12.36
    2000-12    12.36
    2001-06    12.36
    2001-12    12.36
    2002-06    12.36
    2002-12    12.36
    2003-06    12.36
    2003-12    12.36
    2004-06    12.36
    2004-12    12.36
    2005-06    12.36
    2005-12    12.36
    Freq: 6M, dtype: float64

    >>> erate, prate = iconv(nrate = interest_rate(const_value=12, start='2000-01', periods=12, freq='Q'))
    >>> prate # doctest: +NORMALIZE_WHITESPACE
    2000Q1    3.0
    2000Q2    3.0
    2000Q3    3.0
    2000Q4    3.0
    2001Q1    3.0
    2001Q2    3.0
    2001Q3    3.0
    2001Q4    3.0
    2002Q1    3.0
    2002Q2    3.0
    2002Q3    3.0
    2002Q4    3.0
    Freq: Q-DEC, dtype: float64

    >>> erate # doctest: +NORMALIZE_WHITESPACE
    2000Q1    12.550881
    2000Q2    12.550881
    2000Q3    12.550881
    2000Q4    12.550881
    2001Q1    12.550881
    2001Q2    12.550881
    2001Q3    12.550881
    2001Q4    12.550881
    2002Q1    12.550881
    2002Q2    12.550881
    2002Q3    12.550881
    2002Q4    12.550881
    Freq: Q-DEC, dtype: float64

    >>> nrate, prate = iconv(erate = erate)
    >>> nrate # doctest: +NORMALIZE_WHITESPACE
    2000Q1    12.0
    2000Q2    12.0
    2000Q3    12.0
    2000Q4    12.0
    2001Q1    12.0
    2001Q2    12.0
    2001Q3    12.0
    2001Q4    12.0
    2002Q1    12.0
    2002Q2    12.0
    2002Q3    12.0
    2002Q4    12.0
    Freq: Q-DEC, dtype: float64

    >>> prate # doctest: +NORMALIZE_WHITESPACE
    2000Q1    3.0
    2000Q2    3.0
    2000Q3    3.0
    2000Q4    3.0
    2001Q1    3.0
    2001Q2    3.0
    2001Q3    3.0
    2001Q4    3.0
    2002Q1    3.0
    2002Q2    3.0
    2002Q3    3.0
    2002Q4    3.0
    Freq: Q-DEC, dtype: float64

    >>> nrate, erate = iconv(prate = prate)
    >>> nrate # doctest: +NORMALIZE_WHITESPACE
    2000Q1    12.0
    2000Q2    12.0
    2000Q3    12.0
    2000Q4    12.0
    2001Q1    12.0
    2001Q2    12.0
    2001Q3    12.0
    2001Q4    12.0
    2002Q1    12.0
    2002Q2    12.0
    2002Q3    12.0
    2002Q4    12.0
    Freq: Q-DEC, dtype: float64

    >>> erate # doctest: +NORMALIZE_WHITESPACE
    2000Q1    12.550881
    2000Q2    12.550881
    2000Q3    12.550881
    2000Q4    12.550881
    2001Q1    12.550881
    2001Q2    12.550881
    2001Q3    12.550881
    2001Q4    12.550881
    2002Q1    12.550881
    2002Q2    12.550881
    2002Q3    12.550881
    2002Q4    12.550881
    Freq: Q-DEC, dtype: float64

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

    if nrate is not None:
        if isinstance(nrate, (int, float)):
            nrate = [nrate] * maxlen
        nrate = np.array(nrate)
        prate = nrate / pyr
        erate = 100 * (np.power(1 + prate/100, pyr) - 1)
        prate = prate.tolist()
        erate = erate.tolist()
        if maxlen == 1:
            prate = prate[0]
            erate = erate[0]
        return (erate, prate)

    if erate is not None:
        if isinstance(erate, (int, float)):
            erate = [erate] * maxlen
        erate = np.array(erate)
        prate = 100 * (np.power(1 + erate / 100, 1 / pyr) - 1)
        nrate = pyr * prate
        prate = prate.tolist()
        nrate = nrate.tolist()
        if maxlen == 1:
            prate = prate[0]
            nrate = nrate[0]
        return (nrate, prate)

    if prate is not None:
        if isinstance(prate, (int, float)):
            prate = [prate] * maxlen
        prate = np.array(prate)
        erate = 100 * (np.power(1 + prate / 100, pyr) - 1)
        nrate = pyr * prate
        erate = erate.tolist()
        nrate = nrate.tolist()
        if maxlen == 1:
            erate = erate[0]
            nrate = nrate[0]
        return (nrate, erate)


# def to_discount_factor(nrate=None, erate=None, prate=None, base_date=None):
#     """Returns a list of discount factors calculated as 1 / (1 + r)^(t - t0).
#
#     Args:
#         nrate (pandasSeries): Nominal interest rate per year.
#         nrate (pandasSeries): Effective interest rate per year.
#         prate (pandasSeries): Periodic interest rate.
#         base_date (string): basis time.
#
#     Returns:
#         pandas.Series of float values
#
#     Only one of the interest rates must be supplied for the computation.
#
#     >>> nrate = interest_rate(const_value=4, periods=10, start='2016Q1', freq='Q')
#     >>> erate, prate = iconv(nrate=nrate)
#     >>> to_discount_factor(nrate=nrate, base_date='2016Q3') # doctest: +ELLIPSIS
#     [1.0201, 1.01, 1.0, 0.990..., 0.980..., 0.970..., 0.960..., 0.951..., 0.942..., 0.932...]
#
#     >>> to_discount_factor(erate=erate, base_date='2016Q3') # doctest: +ELLIPSIS
#     [1.0201, 1.01, 1.0, 0.990..., 0.980..., 0.970..., 0.960..., 0.951..., 0.942..., 0.932...]
#
#     >>> to_discount_factor(prate=prate, base_date='2016Q3') # doctest: +ELLIPSIS
#     [1.0201, 1.01, 1.0, 0.990..., 0.980..., 0.970..., 0.960..., 0.951..., 0.942..., 0.932...]
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
#         pyr = getpyr(nrate)
#         prate = nrate.copy()
#         for i,_ in enumerate(nrate):
#             prate[i] = nrate[i] / pyr  # periodic rate
#
#     if erate is not None:
#         pyr = getpyr(erate)
#         prate = erate.copy()
#         for i,_ in enumerate(erate):
#             prate[i] = 100 * (np.power(1 + erate[i]/100, 1. / pyr) - 1) # periodic rate
#
#     pyr = getpyr(prate)
#
#     factor = [x/100 for x in prate]
#
#     for index, _ in enumerate(factor):
#         if index == 0:
#             factor[0] = 1 / (1 + factor[0])
#         else:
#             factor[index] = factor[index-1] / (1 + factor[index])
#
#     if isinstance(base_date, str):
#         base_date = pd.Period(base_date, freq=prate.axes[0].freq)
#         base_date = period2pos(prate.axes[0], base_date)
#
#     div = factor[base_date]
#     for index, _ in enumerate(factor):
#         factor[index] = factor[index] / div
#     return factor


# def to_compound_factor(nrate=None, erate=None, prate=None, base_date=0):
#     """Returns a list of compounding factors calculated as (1 + r)^(t - t0).
#
#     Args:
#         nrate (TimeSeries): Nominal interest rate per year.
#         nrate (TimeSeries): Effective interest rate per year.
#         prate (TimeSeries): Periodic interest rate.
#         base_date (int, tuple): basis time.
#
#     Returns:
#         Compound factor (list)
#
#
#     **Examples**
#
#     >>> nrate = interest_rate(const_value=4, start='2000', periods=10, freq='Q')
#     >>> erate, prate = iconv(nrate=nrate)
#     >>> to_compound_factor(prate=prate, base_date=2) # doctest: +ELLIPSIS
#     [0.980..., 0.990..., 1.0, 1.01, 1.0201, 1.030..., 1.040..., 1.051..., 1.061..., 1.072...]
#
#     >>> to_compound_factor(nrate=nrate, base_date=2) # doctest: +ELLIPSIS
#     [0.980..., 0.990..., 1.0, 1.01, 1.0201, 1.030..., 1.040..., 1.051..., 1.061..., 1.072...]
#
#     >>> to_compound_factor(erate=erate, base_date=2) # doctest: +ELLIPSIS
#     [0.980..., 0.990..., 1.0, 1.01, 1.0201, 1.030..., 1.040..., 1.051..., 1.061..., 1.072...]
#
#     """
#     factor = to_discount_factor(nrate=nrate, erate=erate, prate=prate, base_date=base_date)
#     for time, _ in enumerate(factor):
#         factor[time] = 1 / factor[time]
#     return factor



def equivalent_rate(nrate=None, erate=None, prate=None):
    """Returns the equivalent interest rate over a time period.

    Args:
        nrate (TimeSeries): Nominal interest rate per year.
        erate (TimeSeries): Effective interest rate per year.
        prate (TimeSeries): Periodic interest rate.

    Returns:
        float value.

    Only one of the interest rate must be supplied for the computation.

    >>> equivalent_rate(prate=interest_rate([10]*5, start='2000Q1', freq='Q')) # doctest: +ELLIPSIS
    10.0...


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

    if nrate is not None:
        value = nrate.tolist()
        factor = 1
        for element in value[1:]:
            factor *= (1 + element / 100 / nrate.pyr)
        return 100 * nrate.pyr * (factor**(1/(len(value) - 1)) - 1)

    if prate is not None:
        value = prate.tolist()
        factor = 1
        for element in value[1:]:
            factor *= (1 + element / 100)
        return 100  * (factor**(1/(len(value) - 1)) - 1)

    if erate is not None:
        value = erate.tolist()
        factor = 1
        for element in value[1:]:
            factor *= (1 + (numpy.power(1 + element/100, 1. / erate.pyr) - 1))
        return 100  * (factor**(1/(len(value) - 1)) - 1)



if __name__ == "__main__":
    import doctest
    doctest.testmod()
