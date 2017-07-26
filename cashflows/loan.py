"""
Loan analysis
==============================================================================

Computes the amorization schedule for the followint types of loans:

* ``fixed_rate_loan``: In this loan, the interest rate is fixed and the total
  payments are equal during the life of the loan.

* ``buydown_loan``: the interest rate changes during the life of the loan;
  the value of the payments are calculated using the current value of the
  interest rate. When the interest rate is constant during the life of the loan,
  the results are equals to the function ``fixed_rate_loan``.

* ``fixed_ppal_loan``: the payments to the principal are constant during the life
  of loan.

* ``bullet_loan``: the principal is payed at the end of the life of the loan.

"""


from cashflows.analysis import timevalue, irr
from cashflows.gtimeseries import TimeSeries, cashflow, interest_rate, verify_eq_time_range
from cashflows.gtimeseries import repr_table
from cashflows.tvmm import pvpmt

##
## base class for computations
##
class Loan():
    """
    Class for representing loans
    """

    # pylint: disable=too-many-instance-attributes

    def __init__(self):
        """
        """
        self.life = self.intpmt = self.endppalbal = self.begppalbal = None
        self.amount = self.grace = self.totpmt = None



    def to_cashflow(self, tax_rate=0):
        """Converts the loan to the equivalent cashflow.

        For the conversion, origination points are considered as exogenous costs
        and they are not taking in to account in the computation. In oposition,
        discount points are considered as prepaid interest and included in the
        cashflow.

        When tax_rate is different from zero, tax benefits are considered."""


        if isinstance(tax_rate, (int, float)):
            tax_rate = interest_rate(const_value = [tax_rate] * (self.life + self.grace + 1))

        cflo = cashflow(const_value= [0] * (self.grace + self.life + 1))

        ##
        ## payments per period
        ##
        for time in range(self.grace + self.life + 1):
            if time == 0:
                cflo[0] = self.amount
            cflo[time] += -self.totpmt[time] + self.intpmt[time] * tax_rate[time] / 100

        return cflo

    def true_rate(self, tax_rate=0):
        """Computes the true interest rate for the loan.

        For the computation, the loan is converted to the equivalent cashflow,
        taking in to account the following aspects:

        * Origination points are considered as non deducible costs and they \
        are ignored in the computation.

        * Discount points are prepaid interest and they are considered as \
        deducibles in the computation.

        * When `tax_rate` is different from zero, the After-Tax true interest \
        rate is calculated. This is, only the (1 - `tax_rate`) of paid interests \
        (including discount points) are used in the computation.

        """
        return irr(self.to_cashflow(tax_rate))



    def __repr__(self):

        return repr_table(cols=[self.begppalbal,
                                self.nrate,
                                self.totpmt,
                                self.intpmt,
                                self.ppalpmt,
                                self.endppalbal],
                       header=[['Beg.', 'Per.', 'Total', 'Int.', 'Ppal', 'Ending'],
                               ['Ppal', 'Rate', 'Pmt', 'Pmt', 'Pmt', 'Ppal']])

#    def x__repr__(self):
#        txt = ['']
#        txt.append('  t          Beginning  Periodic      Total     Interest    Principal       Ending')
#        txt.append('             Principal  Rate     Payment      Payment      Payment    Principal')
#        txt.append('--------------------------------------------------------------------------')
#
#        for time in range(self.grace + self.life + 1):
#            fmt = ' {:3d}       {:12.2f} {:12.2f} {:12.2f} {:12.2f} {:12.2f}'
#            txt.append(fmt.format(time,
#                                  self.begppalbal[time],
#                                  self.totpmt[time],
#                                  self.intpmt[time],
#                                  self.ppalpmt[time],
#                                  self.endppalbal[time]))
#        return '\n'.join(txt)

    def interest(self):
        """Returns the interest paid as a Cashflow object."""
        return Cashflow(constValue=self.intpmt.tolist())

    def begbal(self):
        """Returns the balance at the begining of each period as
        a Cashflow object."""
        return Cashflow(constValue=self.begppalbal.tolist())

    def endbal(self):
        """Returns the balance at the ending of each period as
        a Cashflow object."""
        return Cashflow(constValue=self.endppalbal.tolist())

    def ppalpmt(self):
        """Returns the principal payment for each period as
        a Cashflow object."""
        return Cashflow(constValue=self.ppalpmt.tolist())



def fixed_rate_loan(amount, nrate, life, start, pyr=1, grace=0, dispoints=0,
                    orgpoints=0, prepmt=None, balloonpmt=None):
    """Fixed rate loan.

    Args:
        amount (float): Loan amount.
        nrate (float): nominal interest rate per year.
        life (float): life of the loan.
        start (int, tuple): init period for the loan.
        pyr (int): number of compounding periods per year.
        grace (int): number of periods of grace (without payment of the principal)
        dispoints (float): Discount points of the loan.
        orgpoints (float): Origination points of the loan.
        prepmt (TimeSeries): generic cashflow representing prepayments.
        balloonpmt (TimeSeries): generic cashflow representing balloon payments.

    Returns:
       A object of the class ``Loan``.

    >>> pmt = cashflow(const_value=0, nper = 11, pyr=4, spec=((1, 3), 200))
    >>> fixed_rate_loan(amount=1000, nrate=10, life=10, start=None, pyr=4, grace=0, dispoints=0,
    ...                 orgpoints=0, prepmt=pmt, balloonpmt=None)
    t         Beg.    Per.   Total    Int.    Ppal  Ending
              Ppal    Rate     Pmt     Pmt     Pmt    Ppal
    ------------------------------------------------------
    (0, 0) 1000.00   10.00    0.00    0.00    0.00 1000.00
    (0, 1) 1000.00   10.00  114.26   25.00   89.26  910.74
    (0, 2)  910.74   10.00  114.26   22.77   91.49  819.25
    (0, 3)  819.25   10.00  114.26   20.48   93.78  725.47
    (1, 0)  725.47   10.00  114.26   18.14   96.12  629.35
    (1, 1)  629.35   10.00  114.26   15.73   98.52  530.83
    (1, 2)  530.83   10.00  114.26   13.27  100.99  429.84
    (1, 3)  429.84   10.00  314.26   10.75  303.51  126.33
    (2, 0)  126.33   10.00  114.26    3.16  111.10   15.23
    (2, 1)   15.23   10.00   15.61    0.38   15.23    0.00
    (2, 2)    0.00   10.00    0.00    0.00    0.00    0.00

    """
    if not isinstance(float(nrate), float):
        TypeError('nrate must be a float.')

    nrate = interest_rate(const_value=nrate, start=start, nper=life+grace+1, pyr=pyr)

    if prepmt is None:
        prepmt = cashflow(start=nrate.start, end=nrate.end, pyr=nrate.pyr)
    else:
        verify_eq_time_range(nrate, prepmt)

    if balloonpmt is None:
        balloonpmt = cashflow(start=nrate.start, end=nrate.end, pyr=nrate.pyr)
    else:
        verify_eq_time_range(nrate, balloonpmt)

    # present value of the balloon payments
    if balloonpmt is not None:
        balloonpv = timevalue(cflo=balloonpmt, prate=nrate, base_date=grace)
    else:
        balloonpv = 0

    pmt = pvpmt(pmt=None, pval=-amount+balloonpv, nrate=nrate[0], nper=len(nrate)-1, pyr=nrate.pyr)
    pmts = cashflow(start=nrate.start, end=nrate.end, pyr=nrate.pyr)
    for time in range(1, life + 1):
        pmts[grace + time] = pmt

    # balance
    begppalbal = TimeSeries(start=nrate.start, end=nrate.end, pyr=nrate.pyr)
    intpmt = TimeSeries(start=nrate.start, end=nrate.end, pyr=nrate.pyr)
    ppalpmt = TimeSeries(start=nrate.start, end=nrate.end, pyr=nrate.pyr)
    totpmt = TimeSeries(start=nrate.start, end=nrate.end, pyr=nrate.pyr)
    endppalbal = TimeSeries(start=nrate.start, end=nrate.end, pyr=nrate.pyr)

    # payments per period
    for time, _ in enumerate(totpmt):
        totpmt[time] = pmts[time] + balloonpmt[time] + prepmt[time]

    # balance calculation
    for time in range(grace + life + 1):

        if time == 0:
            begppalbal[0] = amount
            endppalbal[0] = amount
            totpmt[time] = amount * (dispoints + orgpoints)
            intpmt[time] = amount * dispoints
        else:
            begppalbal[time] = endppalbal[time - 1]
            if time <= grace:
                intpmt[time] = begppalbal[time] * nrate[time] / nrate.pyr / 100
                totpmt[time] = intpmt[time]
                endppalbal[time] = begppalbal[time]
            else:
                intpmt[time] = begppalbal[time] * nrate[time] / nrate.pyr / 100
                ppalpmt[time] = totpmt[time] - intpmt[time]
                if ppalpmt[time] < 0:
                    capint = - ppalpmt[time]
                    ppalpmt[time] = 0
                else:
                    capint = 0
                endppalbal[time] = begppalbal[time] - ppalpmt[time] + capint
                if endppalbal[time] < 0:
                    totpmt[time] = begppalbal[time] + intpmt[time]
                    ppalpmt[time] = begppalbal[time]
                    endppalbal[time] = begppalbal[time] - ppalpmt[time]
                    pmts[time] = 0
                    prepmt[time] = 0

    result = Loan()
    result.life = life
    result.nrate = nrate
    result.grace = grace
    result.amount = amount
    result.begppalbal = begppalbal
    result.totpmt = totpmt
    result.intpmt = intpmt
    result.ppalpmt = ppalpmt
    result.endppalbal = endppalbal

    return result


def buydown_loan(amount, nrate, grace=0, dispoints=0, orgpoints=0, prepmt=None):
    """
    In this loan, the periodic payments are recalculated when there are changes
    in the value of the interest rate.

    Args:
        amount (float): Loan amount.
        nrate (float, TimeSeries): nominal interest rate per year.
        grace (int): numner of grace periods without paying the principal.
        dispoints (float): Discount points of the loan.
        orgpoints (float): Origination points of the loan.
        prepmt (TimeSeries): generic cashflow representing prepayments.


    Returns:
       A object of the class ``Loan``.

    >>> nrate = interest_rate(const_value=10, nper=11, pyr=4, spec=(5, 20))
    >>> buydown_loan(amount=1000, nrate=nrate, dispoints=0, orgpoints=0, prepmt=None)  # doctest: +NORMALIZE_WHITESPACE
    t         Beg.    Per.   Total    Int.    Ppal  Ending
              Ppal    Rate     Pmt     Pmt     Pmt    Ppal
    ------------------------------------------------------
    (0, 0) 1000.00   10.00    0.00    0.00    0.00 1000.00
    (0, 1) 1000.00   10.00  114.26   25.00   89.26  910.74
    (0, 2)  910.74   10.00  114.26   22.77   91.49  819.25
    (0, 3)  819.25   10.00  114.26   20.48   93.78  725.47
    (1, 0)  725.47   10.00  114.26   18.14   96.12  629.35
    (1, 1)  629.35   20.00  123.99   31.47   92.53  536.83
    (1, 2)  536.83   20.00  123.99   26.84   97.15  439.67
    (1, 3)  439.67   20.00  123.99   21.98  102.01  337.66
    (2, 0)  337.66   20.00  123.99   16.88  107.11  230.55
    (2, 1)  230.55   20.00  123.99   11.53  112.47  118.09
    (2, 2)  118.09   20.00  123.99    5.90  118.09    0.00


    >>> pmt = cashflow(const_value=0, nper = 11, pyr=4, spec=((1, 3), 200))
    >>> buydown_loan(amount=1000, nrate=nrate, dispoints=0, orgpoints=0, prepmt=pmt)  # doctest: +NORMALIZE_WHITESPACE
    t         Beg.    Per.   Total    Int.    Ppal  Ending
              Ppal    Rate     Pmt     Pmt     Pmt    Ppal
    ------------------------------------------------------
    (0, 0) 1000.00   10.00    0.00    0.00    0.00 1000.00
    (0, 1) 1000.00   10.00  114.26   25.00   89.26  910.74
    (0, 2)  910.74   10.00  114.26   22.77   91.49  819.25
    (0, 3)  819.25   10.00  114.26   20.48   93.78  725.47
    (1, 0)  725.47   10.00  114.26   18.14   96.12  629.35
    (1, 1)  629.35   20.00  123.99   31.47   92.53  536.83
    (1, 2)  536.83   20.00  123.99   26.84   97.15  439.67
    (1, 3)  439.67   20.00  323.99   21.98  302.01  137.66
    (2, 0)  137.66   20.00   50.55    6.88   43.67   94.00
    (2, 1)   94.00   20.00   50.55    4.70   45.85   48.14
    (2, 2)   48.14   20.00   50.55    2.41   48.14    0.00


    """

    if not isinstance(nrate, TimeSeries):
        TypeError('nrate must be a TimeSeries object.')

    if prepmt is None:
        prepmt = cashflow(start=nrate.start, end=nrate.end, pyr=nrate.pyr)
    else:
        verify_eq_time_range(nrate, prepmt)

    life = len(nrate) - grace - 1

    begppalbal = TimeSeries(start=nrate.start, end=nrate.end, pyr=nrate.pyr)
    intpmt = TimeSeries(start=nrate.start, end=nrate.end, pyr=nrate.pyr)
    ppalpmt = TimeSeries(start=nrate.start, end=nrate.end, pyr=nrate.pyr)
    totpmt = TimeSeries(start=nrate.start, end=nrate.end, pyr=nrate.pyr)
    endppalbal = TimeSeries(start=nrate.start, end=nrate.end, pyr=nrate.pyr)

    if prepmt is None:
        prepmt = cashflow(start=nrate.start, end=nrate.end, pyr=nrate.pyr)
    else:
        verify_eq_time_range(nrate, prepmt)

    ##
    ## balance calculation
    ##
    for time in range(grace + life + 1):

        if time == 0:
            #
            begppalbal[time] = amount
            endppalbal[time] = amount
            totpmt[time] = amount * (dispoints + orgpoints)
            intpmt[time] = amount * dispoints
            #
        else:
            #
            # periodic payment per period
            #
            if time <= grace:

                begppalbal[time] = endppalbal[time - 1]
                intpmt[time] = begppalbal[time] * nrate[time] / nrate.pyr / 100
                totpmt[time] = intpmt[time]
                endppalbal[time] = begppalbal[time]

            else:

                pmt = -pvpmt(nrate=nrate[time], nper=grace+life-time+1,
                             pval=endppalbal[time-1], pmt=None, pyr=nrate.pyr)

                totpmt[time] = pmt + prepmt[time]

                # balance
                begppalbal[time] = endppalbal[time - 1]
                intpmt[time] = begppalbal[time] * nrate[time] / nrate.pyr / 100
                ppalpmt[time] = totpmt[time] - intpmt[time]
                endppalbal[time] = begppalbal[time] - ppalpmt[time]


    ## resuls
    result = Loan()
    result.nrate = nrate
    result.life = life
    result.grace = grace
    result.amount = amount
    result.begppalbal = begppalbal
    result.totpmt = totpmt
    result.intpmt = intpmt
    result.ppalpmt = ppalpmt
    result.endppalbal = endppalbal

    return result



def fixed_ppal_loan(amount, nrate, grace=0, dispoints=0, orgpoints=0,
               prepmt=None, balloonpmt=None):
    """Loan with fixed principal payment.

    Args:
        amount (float): Loan amount.
        nrate (float, TimeSeries): nominal interest rate per year.
        grace (int): number of grace periiods without paying principal.
        dispoints (float): Discount points of the loan.
        orgpoints (float): Origination points of the loan.
        prepmt (TimeSeries): generic cashflow representing prepayments.
        balloonpmt (TimeSeries): generic cashflow representing balloon payments.


    Returns:
       A object of the class ``Loan``.

    >>> nrate = interest_rate(const_value=10, nper=11, pyr=4)
    >>> fixed_ppal_loan(amount=1000, nrate=nrate, grace=0, dispoints=0, orgpoints=0,
    ...                prepmt=None, balloonpmt=None)  # doctest: +NORMALIZE_WHITESPACE
    t         Beg.    Per.   Total    Int.    Ppal  Ending
              Ppal    Rate     Pmt     Pmt     Pmt    Ppal
    ------------------------------------------------------
    (0, 0)    0.00   10.00    0.00    0.00    0.00 1000.00
    (0, 1) 1000.00   10.00  125.00   25.00  100.00  900.00
    (0, 2)  900.00   10.00  122.50   22.50  100.00  800.00
    (0, 3)  800.00   10.00  120.00   20.00  100.00  700.00
    (1, 0)  700.00   10.00  117.50   17.50  100.00  600.00
    (1, 1)  600.00   10.00  115.00   15.00  100.00  500.00
    (1, 2)  500.00   10.00  112.50   12.50  100.00  400.00
    (1, 3)  400.00   10.00  110.00   10.00  100.00  300.00
    (2, 0)  300.00   10.00  107.50    7.50  100.00  200.00
    (2, 1)  200.00   10.00  105.00    5.00  100.00  100.00
    (2, 2)  100.00   10.00  102.50    2.50  100.00    0.00


    >>> fixed_ppal_loan(amount=1000, nrate=nrate, grace=2, dispoints=0, orgpoints=0,
    ...                prepmt=None, balloonpmt=None)  # doctest: +NORMALIZE_WHITESPACE
    t         Beg.    Per.   Total    Int.    Ppal  Ending
              Ppal    Rate     Pmt     Pmt     Pmt    Ppal
    ------------------------------------------------------
    (0, 0)    0.00   10.00    0.00    0.00    0.00 1000.00
    (0, 1) 1000.00   10.00   25.00   25.00    0.00 1000.00
    (0, 2) 1000.00   10.00   25.00   25.00    0.00 1000.00
    (0, 3) 1000.00   10.00  150.00   25.00  125.00  875.00
    (1, 0)  875.00   10.00  146.88   21.88  125.00  750.00
    (1, 1)  750.00   10.00  143.75   18.75  125.00  625.00
    (1, 2)  625.00   10.00  140.62   15.62  125.00  500.00
    (1, 3)  500.00   10.00  137.50   12.50  125.00  375.00
    (2, 0)  375.00   10.00  134.38    9.38  125.00  250.00
    (2, 1)  250.00   10.00  131.25    6.25  125.00  125.00
    (2, 2)  125.00   10.00  128.12    3.12  125.00    0.00

    >>> pmt = cashflow(const_value=0, nper = 11, pyr=4, spec=((1, 3), 200))
    >>> fixed_ppal_loan(amount=1000, nrate=nrate, grace=2, dispoints=0, orgpoints=0,
    ...                prepmt=pmt, balloonpmt=None)  # doctest: +NORMALIZE_WHITESPACE
    t         Beg.    Per.   Total    Int.    Ppal  Ending
              Ppal    Rate     Pmt     Pmt     Pmt    Ppal
    ------------------------------------------------------
    (0, 0)    0.00   10.00    0.00    0.00    0.00 1000.00
    (0, 1) 1000.00   10.00   25.00   25.00    0.00 1000.00
    (0, 2) 1000.00   10.00   25.00   25.00    0.00 1000.00
    (0, 3) 1000.00   10.00  150.00   25.00  125.00  875.00
    (1, 0)  875.00   10.00  146.88   21.88  125.00  750.00
    (1, 1)  750.00   10.00  143.75   18.75  125.00  625.00
    (1, 2)  625.00   10.00  140.62   15.62  125.00  500.00
    (1, 3)  500.00   10.00  337.50   12.50  325.00  175.00
    (2, 0)  175.00   10.00  129.38    4.38  125.00   50.00
    (2, 1)   50.00   10.00   51.25    1.25   50.00    0.00
    (2, 2)    0.00   10.00    0.00    0.00    0.00    0.00

    >>> pmt = cashflow(const_value=0, nper = 11, pyr=4, spec=((1, 3), 200))
    >>> fixed_ppal_loan(amount=1000, nrate=nrate, grace=2, dispoints=0, orgpoints=0,
    ...                prepmt=None, balloonpmt=pmt)  # doctest: +NORMALIZE_WHITESPACE
    t         Beg.    Per.   Total    Int.    Ppal  Ending
              Ppal    Rate     Pmt     Pmt     Pmt    Ppal
    ------------------------------------------------------
    (0, 0)    0.00   10.00    0.00    0.00    0.00 1000.00
    (0, 1) 1000.00   10.00   25.00   25.00    0.00 1000.00
    (0, 2) 1000.00   10.00   25.00   25.00    0.00 1000.00
    (0, 3) 1000.00   10.00  125.00   25.00  100.00  900.00
    (1, 0)  900.00   10.00  122.50   22.50  100.00  800.00
    (1, 1)  800.00   10.00  120.00   20.00  100.00  700.00
    (1, 2)  700.00   10.00  117.50   17.50  100.00  600.00
    (1, 3)  600.00   10.00  315.00   15.00  300.00  300.00
    (2, 0)  300.00   10.00  107.50    7.50  100.00  200.00
    (2, 1)  200.00   10.00  105.00    5.00  100.00  100.00
    (2, 2)  100.00   10.00  102.50    2.50  100.00    0.00

    """
    #pylint: disable-msg=too-many-arguments

    if not isinstance(nrate, TimeSeries):
        TypeError('nrate must be a TimeSeries object.')

    if prepmt is None:
        prepmt = cashflow(start=nrate.start, end=nrate.end, pyr=nrate.pyr)
    else:
        verify_eq_time_range(nrate, prepmt)

    if balloonpmt is None:
        balloonpmt = cashflow(start=nrate.start, end=nrate.end, pyr=nrate.pyr)
    else:
        verify_eq_time_range(nrate, balloonpmt)

    # present value of the balloon payments
    balloonpv = sum(balloonpmt)

    life = len(nrate) - grace - 1

    begppalbal = TimeSeries(start=nrate.start, end=nrate.end, pyr=nrate.pyr)
    intpmt = TimeSeries(start=nrate.start, end=nrate.end, pyr=nrate.pyr)
    ppalpmt = TimeSeries(start=nrate.start, end=nrate.end, pyr=nrate.pyr)
    totpmt = TimeSeries(start=nrate.start, end=nrate.end, pyr=nrate.pyr)
    endppalbal = TimeSeries(start=nrate.start, end=nrate.end, pyr=nrate.pyr)

    pmt = (amount - balloonpv) / life # periodic ppal payment

    # balance calculation
    for time in range(grace + life + 1):

        if time == 0:
            begppalbal[time] = 0
            endppalbal[time] = amount - prepmt[time]
            totpmt[time] = amount * (dispoints + orgpoints)
            intpmt[time] = amount * dispoints
        else:
            begppalbal[time] = endppalbal[time - 1]
            intpmt[time] = begppalbal[time] * nrate[time] / nrate.pyr / float(100)
            if time <= grace:
                ppalpmt[time] = prepmt[time] + balloonpmt[time]
            else:
                ppalpmt[time] = pmt + prepmt[time] + balloonpmt[time]
            totpmt[time] = intpmt[time] + ppalpmt[time]
            endppalbal[time] = begppalbal[time] - ppalpmt[time]

            if endppalbal[time] < 0:
                totpmt[time] = begppalbal[time] + intpmt[time]
                ppalpmt[time] = begppalbal[time]
                endppalbal[time] = begppalbal[time] - ppalpmt[time]
                prepmt[time] = 0
                pmt = 0



    ## resuls
    result = Loan()
    result.life = life
    result.nrate = nrate
    result.grace = grace
    result.amount = amount
    result.begppalbal = begppalbal
    result.totpmt = totpmt
    result.intpmt = intpmt
    result.ppalpmt = ppalpmt
    result.endppalbal = endppalbal

    return result


def bullet_loan(amount, nrate, dispoints=0, orgpoints=0, prepmt=None):
    """
    In this type of loan, the principal is payed at the end for the life of the
    loan. Periodic payments correspond only to interests.

    Args:
        amount (float): Loan amount.
        nrate (float, TimeSeries): nominal interest rate per year.
        dispoints (float): Discount points of the loan.
        orgpoints (float): Origination points of the loan.
        prepmt (TimeSeries): generic cashflow representing prepayments.

    Returns:
       A object of the class ``Loan``.

    >>> nrate = interest_rate(const_value=10, nper=11, pyr=4)
    >>> bullet_loan(amount=1000, nrate=nrate, dispoints=0, orgpoints=0, prepmt=None)  # doctest: +NORMALIZE_WHITESPACE
    t         Beg.    Per.   Total    Int.    Ppal  Ending
              Ppal    Rate     Pmt     Pmt     Pmt    Ppal
    ------------------------------------------------------
    (0, 0)    0.00   10.00    0.00    0.00    0.00 1000.00
    (0, 1) 1000.00   10.00   25.00   25.00    0.00 1000.00
    (0, 2) 1000.00   10.00   25.00   25.00    0.00 1000.00
    (0, 3) 1000.00   10.00   25.00   25.00    0.00 1000.00
    (1, 0) 1000.00   10.00   25.00   25.00    0.00 1000.00
    (1, 1) 1000.00   10.00   25.00   25.00    0.00 1000.00
    (1, 2) 1000.00   10.00   25.00   25.00    0.00 1000.00
    (1, 3) 1000.00   10.00   25.00   25.00    0.00 1000.00
    (2, 0) 1000.00   10.00   25.00   25.00    0.00 1000.00
    (2, 1) 1000.00   10.00   25.00   25.00    0.00 1000.00
    (2, 2) 1000.00   10.00 1025.00   25.00 1000.00    0.00


    """
    balloonpmt = cashflow(const_value=0, start=nrate.start, end=nrate.end, pyr=nrate.pyr)
    balloonpmt[-1] = amount
    return fixed_ppal_loan(amount=amount, nrate=nrate, grace=0, dispoints=dispoints,
                           orgpoints=orgpoints, prepmt=prepmt, balloonpmt=balloonpmt)
