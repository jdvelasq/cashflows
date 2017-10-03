"""
Savings
===============================================================================


"""
# import sys
# import os

# sys.path.insert(0, os.path.abspath('..'))

import pandas as pd

from timeseries import cashflow, interest_rate, verify_period_range
from common import getpyr


def savings(deposits, nrate, initbal=0):
    """
    Computes the final balance for a savings account with arbitrary deposits and
    withdrawls and variable interset rate.

    Args:
        deposits (TimeSeries): deposits to the account.
        nrate (TimeSeries): nominal interest rate paid by the account.
        initbal (float): initial balance of the account.
        noprint (bool): prints summary report?

    Return:
        interest, end_balance (TimeSeries, TimeSeries)


    **Examples**

    >>> cflo = cashflow(const_value=[100]*12, start='2000Q1', freq='Q')
    >>> nrate = interest_rate([10]*12, start='2000Q1', freq='Q')
    >>> savings(deposits=cflo, nrate=nrate, initbal=0) # doctest: +NORMALIZE_WHITESPACE
            Beginning Balance  Deposits  Earned interest  Ending balance
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


    >>> cflo = cashflow(const_value=[0, 100, 0, 100, 100], start='2000Q1', freq='A')
    >>> nrate = interest_rate([0, 1, 2, 3, 4], start='2000Q1', freq='A')
    >>> savings(deposits=cflo, nrate=nrate, initbal=1000) # doctest: +NORMALIZE_WHITESPACE
          Beginning Balance  Deposits  Earned interest  Ending balance
    2000           1000.000       0.0          0.00000      1000.00000
    2001           1000.000     100.0         10.00000      1110.00000
    2002           1110.000       0.0         22.20000      1132.20000
    2003           1132.200     100.0         33.96600      1266.16600
    2004           1266.166     100.0         50.64664      1416.81264


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

    table = pd.DataFrame({'Beginning Balance' : begbal,
                          'Deposits' : deposits,
                          'Earned interest': interest,
                          'Ending balance': endbal })

    return table
    # if noprint is True:
    #     return (interest, endbal)



    # len_timeid = len(deposits.end.__repr__())
    # len_number = max(len('{:1.2f}'.format(endbal[-1])), len('{:1.2f}'.format(begbal[0])), 9)
    #
    # fmt_timeid = '{:<' + '{:d}'.format(len_timeid) + 's}'
    # fmt_number = ' {:' + '{:d}'.format(len_number) + '.2f}'
    # fmt_header = ' {:>' + '{:d}'.format(len_number) + 's}'
    #
    # if deposits.pyr == 1:
    #     xmajor, = deposits.start
    #     xminor = 0
    # else:
    #     xmajor, xminor = deposits.start
    #
    # txt = []
    # header = fmt_timeid.format('t')
    # header += fmt_header.format('Beginning')
    # header += fmt_header.format('Deposit')
    # header += fmt_header.format('Earned')
    # header += fmt_header.format('Ending')
    # txt.append(header)
    #
    # header = fmt_timeid.format('')
    # header += fmt_header.format('Balance')
    # header += fmt_header.format('')
    # header += fmt_header.format('Interest')
    # header += fmt_header.format('Balance')
    # txt.append(header)
    #
    # txt.append('-' * len_timeid + '-----' + '-' * len_number * 4)
    #
    #
    # for time, _ in enumerate(deposits):
    #     if deposits.pyr == 1:
    #         timeid = (xmajor,)
    #     else:
    #         timeid = (xmajor, xminor)
    #     fmt = fmt_timeid + fmt_number * 4
    #     txt.append(fmt.format(timeid.__repr__(),
    #                           begbal[time],
    #                           deposits[time],
    #                           interest[time],
    #                           endbal[time]))
    #     if deposits.pyr == 1:
    #         xmajor += 1
    #     else:
    #         xminor += 1
    #         if xminor == deposits.pyr:
    #             xminor = 0
    #             xmajor += 1
    #
    # print('\n'.join(txt))





    # verify_eq_time_range(deposits, nrate)
    #
    # begbal = deposits.copy()
    # interest = deposits.copy()
    # endbal = deposits.copy()
    #
    # for time, _ in enumerate(deposits):
    #     if time == 0:
    #         begbal[0] = initbal
    #         interest[0] = begbal[0] * nrate[0] / 100 / nrate.pyr
    #         endbal[0] = begbal[0] + deposits[0] + interest[0]
    #     else:
    #         begbal[time] = endbal[time - 1]
    #         interest[time] = begbal[time] * nrate[time] / 100 / nrate.pyr
    #         if deposits[time] < 0 and -deposits[time] > begbal[time] + interest[time]:
    #             deposits[time] = -(begbal[time] + interest[time])
    #         endbal[time] = begbal[time] + deposits[time] + interest[time]
    #
    # if noprint is True:
    #     return (interest, endbal)
    #
    #
    #
    # len_timeid = len(deposits.end.__repr__())
    # len_number = max(len('{:1.2f}'.format(endbal[-1])), len('{:1.2f}'.format(begbal[0])), 9)
    #
    # fmt_timeid = '{:<' + '{:d}'.format(len_timeid) + 's}'
    # fmt_number = ' {:' + '{:d}'.format(len_number) + '.2f}'
    # fmt_header = ' {:>' + '{:d}'.format(len_number) + 's}'
    #
    # if deposits.pyr == 1:
    #     xmajor, = deposits.start
    #     xminor = 0
    # else:
    #     xmajor, xminor = deposits.start
    #
    # txt = []
    # header = fmt_timeid.format('t')
    # header += fmt_header.format('Beginning')
    # header += fmt_header.format('Deposit')
    # header += fmt_header.format('Earned')
    # header += fmt_header.format('Ending')
    # txt.append(header)
    #
    # header = fmt_timeid.format('')
    # header += fmt_header.format('Balance')
    # header += fmt_header.format('')
    # header += fmt_header.format('Interest')
    # header += fmt_header.format('Balance')
    # txt.append(header)
    #
    # txt.append('-' * len_timeid + '-----' + '-' * len_number * 4)
    #
    #
    # for time, _ in enumerate(deposits):
    #     if deposits.pyr == 1:
    #         timeid = (xmajor,)
    #     else:
    #         timeid = (xmajor, xminor)
    #     fmt = fmt_timeid + fmt_number * 4
    #     txt.append(fmt.format(timeid.__repr__(),
    #                           begbal[time],
    #                           deposits[time],
    #                           interest[time],
    #                           endbal[time]))
    #     if deposits.pyr == 1:
    #         xmajor += 1
    #     else:
    #         xminor += 1
    #         if xminor == deposits.pyr:
    #             xminor = 0
    #             xmajor += 1
    #
    # print('\n'.join(txt))



# class Savings():
#     """Creates a Savings object.
#
#     Args:
#         deposits (Cashflow): Deposits to the account.
#         rate (float, Rate): Interest rate.
#         initbal (float): Initial balance of the account.
#
#     Returns:
#         An Savigs object.
#
#     Member functions can be used to extract information of the object.
#
#
#
#     """
#     def __init__(self, deposits, rate=0, initbal=0):
#         """
#         Args:
#             deposits (Cashflow): deposits to the account.
#             rate (float, Rate): interest rate paid by the account.
#             initbal (float): initial balance of the accout.
#
#         Return:
#             A `Savings` object.
#
#         """
#
#         if not isinstance(deposits, Cashflow):
#             raise ValueError('deposits must be a Cashflow instance')
#
#         nper = len(deposits)
#
#         if isinstance(rate, (int, float)):
#             rate = Rate(constValue=rate, nper=nper)
#
#
#         begbal = Cashflow(nper=nper, constValue=0)
#         interest = Cashflow(nper=nper, constValue=0)
#         endbal = Cashflow(nper=nper, constValue=0)
#
#         ##
#         ## balance calculation
#         ##
#         for time in range(nper):
#
#             if time == 0:
#                 #
#                 begbal[time] = initbal
#                 interest[time] = 0
#                 endbal[time] = begbal[time] + deposits[time] + interest[time]
#                 #
#             else:
#                 #
#                 begbal[time] = endbal[time - 1]
#                 interest[time] = begbal[time] * rate[time]
#
#                 if deposits[time] < 0 and -deposits[time] > begbal[time] + interest[time]:
#                     #
#                     deposits[time] = -(begbal[time] + interest[time])
#                     #
#
#                 endbal[time] = begbal[time] + deposits[time] + interest[time]
#                 #
#
#         self._begbal = begbal
#         self._deposits = deposits
#         self._interest = interest
#         self._endbal = endbal
#
#
#     ##
#     ## accounts
#     ##
#     def interest(self):
#         """Returns the earned interest as a Cashflow object."""
#         return self._interest.copy()
#
#     # def deposits(self):
#     #     return self._deposits.copy()
#
#     def begbal(self):
#         """Returns the balance at the begining of each compounding period as a
#         Cashflow object."""
#         return self._begbal.copy()
#
#     def endbal(self):
#         """Returns the balance at the ending of each compounding period as a
#         Cashflow object."""
#         return self._endbal.copy()
#
#     ##
#     ## conversion to generic cashflow object
#     ##
#     def to_cashflow(self):
#         """Converts the object to a equivalent cashflow."""
#         nper = len(self._interest.tolist())
#         cashflow = Cashflow(nper=nper)
#         #
#         for time in range(nper):
#             #
#             cashflow[time] = -self._deposits[time]
#             #
#         cashflow[0] = -self._endbal[0]
#         cashflow[-1] = cashflow[-1] + self._endbal[-1]
#         return cashflow
#
#
#
#     def __repr__(self):
#
#         txt = ['']
#         txt.append('')
#
#         txt.append('   t     Beginning      Deposit       Earned       Ending')
#         txt.append('           balance                  Interest      balance')
#         txt.append('------------------------------------------------------------')
#
#         for time in range(len(self._deposits)):
#
#             fmt = '  {:<3d} {:12.2f} {:12.2f} {:12.2f} {:12.2f}'
#             txt.append(fmt.format(time,
#                                   self._begbal[time],
#                                   self._deposits[time],
#                                   self._interest[time],
#                                   self._endbal[time]))
#
#         return '\n'.join(txt)

if __name__ == "__main__":
    import doctest
    doctest.testmod()
