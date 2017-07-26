"""
Savings
===============================================================================


"""
# import sys
# import os

# sys.path.insert(0, os.path.abspath('..'))

from cashflows.gtimeseries import TimeSeries, cashflow, interest_rate, verify_eq_time_range



def savings(deposits, nrate, initbal=0, noprint=True):
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

    >>> cflo = cashflow(const_value=[100] * 12, pyr=4)
    >>> nrate = interest_rate([10] * 12, pyr=4)
    >>> savings(deposits=cflo, nrate=nrate, initbal=0, noprint=False) # doctest: +NORMALIZE_WHITESPACE
    t      Beginning   Deposit    Earned    Ending
             Balance            Interest   Balance
    -----------------------------------------------
    (0, 0)      0.00    100.00      0.00    100.00
    (0, 1)    100.00    100.00      2.50    202.50
    (0, 2)    202.50    100.00      5.06    307.56
    (0, 3)    307.56    100.00      7.69    415.25
    (1, 0)    415.25    100.00     10.38    525.63
    (1, 1)    525.63    100.00     13.14    638.77
    (1, 2)    638.77    100.00     15.97    754.74
    (1, 3)    754.74    100.00     18.87    873.61
    (2, 0)    873.61    100.00     21.84    995.45
    (2, 1)    995.45    100.00     24.89   1120.34
    (2, 2)   1120.34    100.00     28.01   1248.35
    (2, 3)   1248.35    100.00     31.21   1379.56


    >>> cflo = cashflow(const_value=[100] * 5, spec=[(0, 0), (2, 0)])
    >>> nrate = interest_rate([0, 1, 2, 3, 4])
    >>> savings(deposits=cflo, nrate=nrate, initbal=1000, noprint=False) # doctest: +NORMALIZE_WHITESPACE
    t    Beginning   Deposit    Earned    Ending
           Balance            Interest   Balance
    ---------------------------------------------
    (0,)   1000.00      0.00      0.00   1000.00
    (1,)   1000.00    100.00     10.00   1110.00
    (2,)   1110.00      0.00     22.20   1132.20
    (3,)   1132.20    100.00     33.97   1266.17
    (4,)   1266.17    100.00     50.65   1416.81


    """
    verify_eq_time_range(deposits, nrate)

    begbal = deposits.copy()
    interest = deposits.copy()
    endbal = deposits.copy()

    for time, _ in enumerate(deposits):
        if time == 0:
            begbal[0] = initbal
            interest[0] = begbal[0] * nrate[0] / 100 / nrate.pyr
            endbal[0] = begbal[0] + deposits[0] + interest[0]
        else:
            begbal[time] = endbal[time - 1]
            interest[time] = begbal[time] * nrate[time] / 100 / nrate.pyr
            if deposits[time] < 0 and -deposits[time] > begbal[time] + interest[time]:
                deposits[time] = -(begbal[time] + interest[time])
            endbal[time] = begbal[time] + deposits[time] + interest[time]

    if noprint is True:
        return (interest, endbal)



    len_timeid = len(deposits.end.__repr__())
    len_number = max(len('{:1.2f}'.format(endbal[-1])), len('{:1.2f}'.format(begbal[0])), 9)

    fmt_timeid = '{:<' + '{:d}'.format(len_timeid) + 's}'
    fmt_number = ' {:' + '{:d}'.format(len_number) + '.2f}'
    fmt_header = ' {:>' + '{:d}'.format(len_number) + 's}'

    if deposits.pyr == 1:
        xmajor, = deposits.start
        xminor = 0
    else:
        xmajor, xminor = deposits.start

    txt = []
    header = fmt_timeid.format('t')
    header += fmt_header.format('Beginning')
    header += fmt_header.format('Deposit')
    header += fmt_header.format('Earned')
    header += fmt_header.format('Ending')
    txt.append(header)

    header = fmt_timeid.format('')
    header += fmt_header.format('Balance')
    header += fmt_header.format('')
    header += fmt_header.format('Interest')
    header += fmt_header.format('Balance')
    txt.append(header)

    txt.append('-' * len_timeid + '-----' + '-' * len_number * 4)


    for time, _ in enumerate(deposits):
        if deposits.pyr == 1:
            timeid = (xmajor,)
        else:
            timeid = (xmajor, xminor)
        fmt = fmt_timeid + fmt_number * 4
        txt.append(fmt.format(timeid.__repr__(),
                              begbal[time],
                              deposits[time],
                              interest[time],
                              endbal[time]))
        if deposits.pyr == 1:
            xmajor += 1
        else:
            xminor += 1
            if xminor == deposits.pyr:
                xminor = 0
                xmajor += 1

    print('\n'.join(txt))




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
