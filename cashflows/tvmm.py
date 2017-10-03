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
from common import _vars2list
from rate import iconv


def tvmm(pval=None, fval=None, pmt=None, nrate=None, nper=None, due=0, pyr=1, noprint=True):
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
        noprint (bool): prints enhanced output


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

    >>> tvmm(pval=5000, nrate=11.32, nper=48, fval=0, pyr=12, noprint=False) # doctest: +ELLIPSIS
       pval  fval     pmt  nper  pyr  nrate  erate  prate  due
    0  5000     0 -130.01    48   12  11.32  11.93   0.94    0

    >>> tvmm(pval=[5, 500, 5], nrate=11.32, nper=48, fval=0, pyr=12, noprint=False) # doctest: +ELLIPSIS
       pval  fval   pmt  nper  pyr  nrate  erate  prate  due
    0     5     0 -0.13    48   12  11.32  11.93   0.94    0
    1   500     0 -0.13    48   12  11.32  11.93   0.94    0
    2     5     0 -0.13    48   12  11.32  11.93   0.94    0


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

    if noprint is True:
        if isinstance(result, np.ndarray):
            return result.tolist()
        return result


    nrate = nrate.tolist()

    if pval is None:
        pval = result
    elif fval is None:
        fval = result
    elif nper is None:
        nper = result
    elif pmt is None:
        pmt = result
    else:
        nrate = result

    params = _vars2list([pval, fval, nper, pmt, nrate])
    pval = params[0]
    fval = params[1]
    nper = params[2]
    pmt = params[3]
    nrate = params[4]

    # raise ValueError(nrate.__repr__())

    erate, prate = iconv(nrate=nrate, pyr=pyr)

    table = pd.DataFrame({'pval' : pval,
                          'fval' : fval,
                          'due': due,
                          'nper':nper,
                          'pyr':pyr,
                          'nrate': nrate,
                          'erate': erate,
                          'prate': prate})

    if len(pmt) == 1:
        table['pmt'] = pmt
    else:
        aux = []
        if isinstance(pmt, list):
            if due == 0:
                for item, _ in enumerate(pmt):
                    aux.append(pmt[item][-1])
            else:
                for item, _ in enumerate(pmt):
                    aux.append(pmt[item][0])
            table['pmt'] = aux



    table = table[['pval', 'fval', 'pmt', 'nper', 'pyr', 'nrate', 'erate', 'prate', 'due']]
    table = table.round(2)
    return table




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


def pvfv(pval=None, fval=None, nrate=None, nper=None, pyr=1, noprint=True):
    """Computes the missing argument (set to None) in the function call.

    Args:
        pval (float, list): Present value.
        fval (float, list): Future value.
        nrate (float, list): Nominal interest rate per year.
        nper (int, list): Number of compounding periods.
        pyr (int, list): number of periods per year.
        noprint (bool): prints enhanced output

    Returns:
        The value of the parameter set to None in the function call.

    Effective interest rate per period is calculated as `nrate` / `pyr`.

    """
    return tvmm(pval=pval, fval=fval, pmt=0, nrate=nrate, nper=nper, due=0, pyr=pyr, noprint=noprint)


def pmtfv(pmt=None, fval=None, nrate=None, nper=None, pyr=1, noprint=True):
    """CComputes the missing argument (set to None) in the function call.

    Args:
        pmt (float, list): Periodic payment.
        fval (float, list): Future value.
        nrate (float, list): Nominal rate per year.
        nper (int, list): Number of compounding periods.
        pyr (int, list): number of periods per year.
        noprint (bool): prints enhanced output

    Returns:
        The value of the parameter set to None in the function call.

    Effective interest rate per period is calculated as `nrate` / `pyr`.

    """
    return tvmm(pval=0, fval=fval, pmt=pmt, nrate=nrate, nper=nper, due=1, pyr=pyr, noprint=noprint)


def pvpmt(pmt=None, pval=None, nrate=None, nper=None, pyr=1, noprint=True):
    """Computes the missing argument (set to None) in the function call.

    Args:
        pmt (float, list): Periodic payment.
        pval (float, list): Present value.
        nrate (float, list): Nominal interest rate per year.
        nper (int, list): Number of compounding periods.
        pyr (int, list): number of periods per year.
        noprint (bool): prints enhanced output

    Returns:
        The value of the parameter set to None in the function call.

    Effective interest rate per period is calculated as `nrate` / `pyr`.

    """
    return tvmm(pval=pval, fval=0, pmt=pmt, nrate=nrate, nper=nper, due=0, pyr=pyr, noprint=noprint)


def amortize(pval=None, fval=None, pmt=None, nrate=None, nper=None, due=0, pyr=1, noprint=True):
    """Amortization schedule of a loan.

    Args:
        pval (float): present value.
        fval (float): Future value.
        pmt (float): periodic payment per period.
        nrate (float): nominal interest rate per year.
        nper (int): total number of compounding periods.
        due (int): When payments are due.
        pyr (int, list): number of periods per year.
        noprint (bool): prints enhanced output

    Returns:
        A tuple: (principal, interest, payment, balance)


    **Examples.**

    >>> pmt = tvmm(pval=100, nrate=10, nper=5, fval=0) # doctest: +ELLIPSIS
    >>> table = amortize(pval=100, nrate=10, nper=5, fval=0, noprint=False)
    >>> table # doctest: +NORMALIZE_WHITESPACE
       Beg balance  Payment  Interest  Principal  Final balance
    0       100.00     0.00      0.00       0.00         100.00
    1       100.00   -26.38     10.00     -16.38          83.62
    2        83.62   -26.38      8.36     -18.02          65.60
    3        65.60   -26.38      6.56     -19.82          45.78
    4        45.78   -26.38      4.58     -21.80          23.98
    5        23.98   -26.38      2.40     -23.98           0.00

    >>> amortize(pval=-100, nrate=10, nper=5, fval=0, noprint=False) # doctest: +ELLIPSIS +NORMALIZE_WHITESPACE
       Beg balance  Payment  Interest  Principal  Final balance
    0      -100.00     0.00      0.00       0.00        -100.00
    1      -100.00    26.38    -10.00      16.38         -83.62
    2       -83.62    26.38     -8.36      18.02         -65.60
    3       -65.60    26.38     -6.56      19.82         -45.78
    4       -45.78    26.38     -4.58      21.80         -23.98
    5       -23.98    26.38     -2.40      23.98          -0.00

    >>> amortize(pval=100, nrate=10, nper=5, fval=0, due=1, noprint=False) # doctest: +ELLIPSIS +NORMALIZE_WHITESPACE
       Beg balance  Payment  Interest  Principal  Final balance
    0       100.00   -23.98      0.00     -23.98          76.02
    1        76.02   -23.98      7.60     -16.38          59.64
    2        59.64   -23.98      5.96     -18.02          41.62
    3        41.62   -23.98      4.16     -19.82          21.80
    4        21.80   -23.98      2.18     -21.80           0.00
    5         0.00     0.00      0.00       0.00           0.00

    >>> amortize(pval=-100, nrate=10, nper=5, fval=0, due=1, noprint=False) # doctest: +ELLIPSIS +NORMALIZE_WHITESPACE
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
    # if noprint is True:
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



if __name__ == "__main__":
    import doctest
    doctest.testmod()
