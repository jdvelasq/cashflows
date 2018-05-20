"""
Loan analysis
==============================================================================

Overview
-------------------------------------------------------------------------------

Computes the amorization schedule for the following types of loans:

* ``fixed_rate_loan``: In this loan, the interest rate is fixed and the total
  payments are equal during the life of the loan.

* ``buydown_loan``: the interest rate changes during the life of the loan;
  the value of the payments are calculated using the current value of the
  interest rate. When the interest rate is constant during the life of the loan,
  the results are equals to the function ``fixed_rate_loan``.

* ``fixed_ppal_loan``: the payments to the principal are constant during the life
  of loan.

* ``bullet_loan``: the principal is payed at the end of the life of the loan.


Functions in this module
-------------------------------------------------------------------------------



"""

import numpy as np
import pandas as pd

from cashflows.analysis import *
from cashflows.tvmm import *
from cashflows.timeseries import *
from cashflows.common import *

##
## base class for computations
##
class Loan(pd.DataFrame):

    def __init__(self, life, amount, grace, nrate, dispoints=0, orgpoints=0,
                 data=None, index=None, columns=None, dtype=None, copy=False):
        super().__init__(data=data, index=index, columns=columns, dtype=dtype, copy=copy)
        self.life = life
        self.amount = amount
        self.grace = grace
        self.dispoints = dispoints
        self.orgpoints = orgpoints
        self.nrate = nrate

    def tocashflow(self, tax_rate=None):
        cflo = self.nrate.copy()
        cflo[:] = 0
        if tax_rate is None:
            tax_rate = cflo.copy()
            tax_rate[:] = 0
        #
        # descuenta todos los pagos adicionales
        #
        cflo[0] += self.amount
        cflo[0] -= self.amount * self.orgpoints / 100
        cflo[0] -= self.amount * self.dispoints / 100
        cflo[0] += self.amount * self.dispoints / 100 * tax_rate[0] / 100
        cflo -= self.Ppal_Payment
        cflo -= self.Int_Payment
        cflo += self.Int_Payment * tax_rate / 100
        return cflo

    def true_rate(self, tax_rate=None):
        cflo = self.tocashflow(tax_rate)
        return irr(cflo) * getpyr(cflo)


    def __str__(self):
        str = []
        str.append("Amount:             {:.2f}".format(self.amount))
        str.append("Total interest:     {:.2f}".format(sum(self.Int_Payment)))
        str.append("Total payment:      {:.2f}".format(sum(self.Tot_Payment)))
        str.append("Discount points:    {:.2f}".format(self.dispoints))
        str.append("Origination points: {:.2f}".format(self.orgpoints))
        str = '\n'.join(str) + '\n\n'
        str = str + super().__str__()
        return str



def fixed_ppal_loan(amount, nrate, grace=0, dispoints=0, orgpoints=0,
               prepmt=None, balloonpmt=None):
    """Loan with fixed principal payment.

    Args:
        amount (float): Loan amount.
        nrate (float, pandas.Series): nominal interest rate per year.
        grace (int): number of grace periiods without paying principal.
        dispoints (float): Discount points of the loan.
        orgpoints (float): Origination points of the loan.
        prepmt (pandas.Series): generic cashflow representing prepayments.
        balloonpmt (pandas.Series): generic cashflow representing balloon payments.


    Returns:
       A object of the class ``Loan``.

    **Examples**

    >>> nrate = interest_rate(const_value=[10]*11, start='2018Q1', freq='Q')
    >>> tax_rate = interest_rate(const_value=[35]*11, start='2018Q1', freq='Q')
    >>> fixed_ppal_loan(amount=1000, nrate=nrate, grace=0, dispoints=0, orgpoints=0,
    ...                prepmt=None, balloonpmt=None)  # doctest: +NORMALIZE_WHITESPACE
    Amount:             1000.00
    Total interest:     137.50
    Total payment:      1137.50
    Discount points:    0.00
    Origination points: 0.00
    <BLANKLINE>
            Beg_Ppal_Amount  Nom_Rate  Tot_Payment  Int_Payment  Ppal_Payment  \\
    2018Q1              0.0      10.0          0.0          0.0           0.0
    2018Q2           1000.0      10.0        125.0         25.0         100.0
    2018Q3            900.0      10.0        122.5         22.5         100.0
    2018Q4            800.0      10.0        120.0         20.0         100.0
    2019Q1            700.0      10.0        117.5         17.5         100.0
    2019Q2            600.0      10.0        115.0         15.0         100.0
    2019Q3            500.0      10.0        112.5         12.5         100.0
    2019Q4            400.0      10.0        110.0         10.0         100.0
    2020Q1            300.0      10.0        107.5          7.5         100.0
    2020Q2            200.0      10.0        105.0          5.0         100.0
    2020Q3            100.0      10.0        102.5          2.5         100.0
    <BLANKLINE>
            End_Ppal_Amount
    2018Q1           1000.0
    2018Q2            900.0
    2018Q3            800.0
    2018Q4            700.0
    2019Q1            600.0
    2019Q2            500.0
    2019Q3            400.0
    2019Q4            300.0
    2020Q1            200.0
    2020Q2            100.0
    2020Q3              0.0

    >>> fixed_ppal_loan(amount=1000, nrate=nrate, grace=2, dispoints=0, orgpoints=0,
    ...                prepmt=None, balloonpmt=None)  # doctest: +NORMALIZE_WHITESPACE
    Amount:             1000.00
    Total interest:     162.50
    Total payment:      1162.50
    Discount points:    0.00
    Origination points: 0.00
    <BLANKLINE>
            Beg_Ppal_Amount  Nom_Rate  Tot_Payment  Int_Payment  Ppal_Payment  \\
    2018Q1              0.0      10.0        0.000        0.000           0.0
    2018Q2           1000.0      10.0       25.000       25.000           0.0
    2018Q3           1000.0      10.0       25.000       25.000           0.0
    2018Q4           1000.0      10.0      150.000       25.000         125.0
    2019Q1            875.0      10.0      146.875       21.875         125.0
    2019Q2            750.0      10.0      143.750       18.750         125.0
    2019Q3            625.0      10.0      140.625       15.625         125.0
    2019Q4            500.0      10.0      137.500       12.500         125.0
    2020Q1            375.0      10.0      134.375        9.375         125.0
    2020Q2            250.0      10.0      131.250        6.250         125.0
    2020Q3            125.0      10.0      128.125        3.125         125.0
    <BLANKLINE>
            End_Ppal_Amount
    2018Q1           1000.0
    2018Q2           1000.0
    2018Q3           1000.0
    2018Q4            875.0
    2019Q1            750.0
    2019Q2            625.0
    2019Q3            500.0
    2019Q4            375.0
    2020Q1            250.0
    2020Q2            125.0
    2020Q3              0.0

    >>> pmt = cashflow(const_value=[0]*11, start='2018Q1', freq='Q')
    >>> pmt['2019Q4'] = 200
    >>> fixed_ppal_loan(amount=1000, nrate=nrate, grace=2, dispoints=0, orgpoints=0,
    ...                prepmt=pmt, balloonpmt=None)  # doctest: +NORMALIZE_WHITESPACE
    Amount:             1000.00
    Total interest:     149.38
    Total payment:      1149.38
    Discount points:    0.00
    Origination points: 0.00
    <BLANKLINE>
            Beg_Ppal_Amount  Nom_Rate  Tot_Payment  Int_Payment  Ppal_Payment  \\
    2018Q1              0.0      10.0        0.000        0.000           0.0
    2018Q2           1000.0      10.0       25.000       25.000           0.0
    2018Q3           1000.0      10.0       25.000       25.000           0.0
    2018Q4           1000.0      10.0      150.000       25.000         125.0
    2019Q1            875.0      10.0      146.875       21.875         125.0
    2019Q2            750.0      10.0      143.750       18.750         125.0
    2019Q3            625.0      10.0      140.625       15.625         125.0
    2019Q4            500.0      10.0      337.500       12.500         325.0
    2020Q1            175.0      10.0      129.375        4.375         125.0
    2020Q2             50.0      10.0       51.250        1.250          50.0
    2020Q3              0.0      10.0        0.000        0.000           0.0
    <BLANKLINE>
            End_Ppal_Amount
    2018Q1           1000.0
    2018Q2           1000.0
    2018Q3           1000.0
    2018Q4            875.0
    2019Q1            750.0
    2019Q2            625.0
    2019Q3            500.0
    2019Q4            175.0
    2020Q1             50.0
    2020Q2              0.0
    2020Q3              0.0

    >>> fixed_ppal_loan(amount=1000, nrate=nrate, grace=2, dispoints=0, orgpoints=0,
    ...                prepmt=None, balloonpmt=pmt)  # doctest: +NORMALIZE_WHITESPACE +ELLIPSIS
    Amount:             1000.00
    Total interest:     165.00
    Total payment:      1165.00
    Discount points:    0.00
    Origination points: 0.00
    <BLANKLINE>
            Beg_Ppal_Amount  Nom_Rate  Tot_Payment  Int_Payment  Ppal_Payment  \\
    2018Q1              0.0      10.0          0.0          0.0           0.0
    2018Q2           1000.0      10.0         25.0         25.0           0.0
    2018Q3           1000.0      10.0         25.0         25.0           0.0
    2018Q4           1000.0      10.0        125.0         25.0         100.0
    2019Q1            900.0      10.0        122.5         22.5         100.0
    2019Q2            800.0      10.0        120.0         20.0         100.0
    2019Q3            700.0      10.0        117.5         17.5         100.0
    2019Q4            600.0      10.0        315.0         15.0         300.0
    2020Q1            300.0      10.0        107.5          7.5         100.0
    2020Q2            200.0      10.0        105.0          5.0         100.0
    2020Q3            100.0      10.0        102.5          2.5         100.0
    <BLANKLINE>
            End_Ppal_Amount
    2018Q1           1000.0
    2018Q2           1000.0
    2018Q3           1000.0
    2018Q4            900.0
    2019Q1            800.0
    2019Q2            700.0
    2019Q3            600.0
    2019Q4            300.0
    2020Q1            200.0
    2020Q2            100.0
    2020Q3              0.0


    >>> x = fixed_ppal_loan(amount=1000, nrate=nrate, grace=2, dispoints=0, orgpoints=0,
    ...                     prepmt=None, balloonpmt=pmt)
    >>> x.true_rate() # doctest: +NORMALIZE_WHITESPACE +ELLIPSIS
    10.00...

    >>> x.true_rate(tax_rate) # doctest: +NORMALIZE_WHITESPACE +ELLIPSIS
    6.50...

    >>> x.tocashflow()
    2018Q1    1000.0
    2018Q2     -25.0
    2018Q3     -25.0
    2018Q4    -125.0
    2019Q1    -122.5
    2019Q2    -120.0
    2019Q3    -117.5
    2019Q4    -315.0
    2020Q1    -107.5
    2020Q2    -105.0
    2020Q3    -102.5
    Freq: Q-DEC, dtype: float64

    >>> x.tocashflow(tax_rate)
    2018Q1    1000.000
    2018Q2     -16.250
    2018Q3     -16.250
    2018Q4    -116.250
    2019Q1    -114.625
    2019Q2    -113.000
    2019Q3    -111.375
    2019Q4    -309.750
    2020Q1    -104.875
    2020Q2    -103.250
    2020Q3    -101.625
    Freq: Q-DEC, dtype: float64


    >>> x = fixed_ppal_loan(amount=1000, nrate=nrate, grace=2, dispoints=0, orgpoints=10,
    ...                     prepmt=None, balloonpmt=pmt)
    >>> x # doctest: +NORMALIZE_WHITESPACE +ELLIPSIS
    Amount:             1000.00
    Total interest:     165.00
    Total payment:      1265.00
    Discount points:    0.00
    Origination points: 10.00
    <BLANKLINE>
            Beg_Ppal_Amount  Nom_Rate  Tot_Payment  Int_Payment  Ppal_Payment  \\
    2018Q1              0.0      10.0        100.0          0.0           0.0
    2018Q2           1000.0      10.0         25.0         25.0           0.0
    2018Q3           1000.0      10.0         25.0         25.0           0.0
    2018Q4           1000.0      10.0        125.0         25.0         100.0
    2019Q1            900.0      10.0        122.5         22.5         100.0
    2019Q2            800.0      10.0        120.0         20.0         100.0
    2019Q3            700.0      10.0        117.5         17.5         100.0
    2019Q4            600.0      10.0        315.0         15.0         300.0
    2020Q1            300.0      10.0        107.5          7.5         100.0
    2020Q2            200.0      10.0        105.0          5.0         100.0
    2020Q3            100.0      10.0        102.5          2.5         100.0
    <BLANKLINE>
            End_Ppal_Amount
    2018Q1           1000.0
    2018Q2           1000.0
    2018Q3           1000.0
    2018Q4            900.0
    2019Q1            800.0
    2019Q2            700.0
    2019Q3            600.0
    2019Q4            300.0
    2020Q1            200.0
    2020Q2            100.0
    2020Q3              0.0

    >>> x.true_rate() # doctest: +NORMALIZE_WHITESPACE +ELLIPSIS
    17.1725...

    >>> x.tocashflow() # doctest: +NORMALIZE_WHITESPACE +ELLIPSIS
    2018Q1    900.0
    2018Q2    -25.0
    2018Q3    -25.0
    2018Q4   -125.0
    2019Q1   -122.5
    2019Q2   -120.0
    2019Q3   -117.5
    2019Q4   -315.0
    2020Q1   -107.5
    2020Q2   -105.0
    2020Q3   -102.5
    Freq: Q-DEC, dtype: float64

    >>> x.true_rate(tax_rate) # doctest: +NORMALIZE_WHITESPACE +ELLIPSIS
    13.4232...

    >>> x.tocashflow(tax_rate) # doctest: +NORMALIZE_WHITESPACE +ELLIPSIS
    2018Q1    900.000
    2018Q2    -16.250
    2018Q3    -16.250
    2018Q4   -116.250
    2019Q1   -114.625
    2019Q2   -113.000
    2019Q3   -111.375
    2019Q4   -309.750
    2020Q1   -104.875
    2020Q2   -103.250
    2020Q3   -101.625
    Freq: Q-DEC, dtype: float64



    """
    #pylint: disable-msg=too-many-arguments

    if not isinstance(nrate, pd.Series):
        TypeError('nrate must be a pandas.Series object.')

    if prepmt is None:
        prepmt = nrate.copy()
        prepmt[:] = 0
    else:
        verify_period_range([nrate, prepmt])

    if balloonpmt is None:
        balloonpmt = nrate.copy()
        balloonpmt[:] = 0
    else:
        verify_period_range([nrate, balloonpmt])

    # present value of the balloon payments
    balloonpv = sum(balloonpmt)

    life = len(nrate) - grace - 1

    begppalbal = nrate.copy()
    intpmt = nrate.copy()
    ppalpmt = nrate.copy()
    totpmt = nrate.copy()
    endppalbal = nrate.copy()

    begppalbal[:] = 0
    intpmt[:] = 0
    ppalpmt[:] = 0
    totpmt[:] = 0
    endppalbal[:] = 0

    pmt = (amount - balloonpv) / life # periodic ppal payment
    pyr = getpyr(nrate)

    # balance calculation
    for time in range(grace + life + 1):

        if time == 0:
            begppalbal[time] = 0
            endppalbal[time] = amount - prepmt[time]
            totpmt[time] = amount * (dispoints + orgpoints) / 100
            ### intpmt[time] = amount * dispoints / 100
        else:
            begppalbal[time] = endppalbal[time - 1]
            intpmt[time] = begppalbal[time] * nrate[time] / pyr / float(100)
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


    data = {'Beg_Ppal_Amount':begppalbal}
    result = Loan(life=life, amount=amount, grace=grace, nrate=nrate,
                  dispoints=dispoints, orgpoints=orgpoints,
                  data=data)
    result['Nom_Rate'] = nrate
    result['Tot_Payment'] = totpmt
    result['Int_Payment'] = intpmt
    result['Ppal_Payment'] = ppalpmt
    result['End_Ppal_Amount'] = endppalbal
    return result


def bullet_loan(amount, nrate, dispoints=0, orgpoints=0, prepmt=None):
    """
    In this type of loan, the principal is payed at the end for the life of the
    loan. Periodic payments correspond only to interests.

    Args:
        amount (float): Loan amount.
        nrate (float, pandas.Series): nominal interest rate per year.
        dispoints (float): Discount points of the loan.
        orgpoints (float): Origination points of the loan.
        prepmt (pandas.Series): generic cashflow representing prepayments.

    Returns:
       A object of the class ``Loan``.

    >>> nrate = interest_rate(const_value=[10]*11, start='2018Q1', freq='Q')
    >>> bullet_loan(amount=1000, nrate=nrate, dispoints=0, orgpoints=0, prepmt=None)  # doctest: +NORMALIZE_WHITESPACE
    Amount:             1000.00
    Total interest:     250.00
    Total payment:      1250.00
    Discount points:    0.00
    Origination points: 0.00
    <BLANKLINE>
            Beg_Ppal_Amount  Nom_Rate  Tot_Payment  Int_Payment  Ppal_Payment  \\
    2018Q1              0.0      10.0          0.0          0.0           0.0
    2018Q2           1000.0      10.0         25.0         25.0           0.0
    2018Q3           1000.0      10.0         25.0         25.0           0.0
    2018Q4           1000.0      10.0         25.0         25.0           0.0
    2019Q1           1000.0      10.0         25.0         25.0           0.0
    2019Q2           1000.0      10.0         25.0         25.0           0.0
    2019Q3           1000.0      10.0         25.0         25.0           0.0
    2019Q4           1000.0      10.0         25.0         25.0           0.0
    2020Q1           1000.0      10.0         25.0         25.0           0.0
    2020Q2           1000.0      10.0         25.0         25.0           0.0
    2020Q3           1000.0      10.0       1025.0         25.0        1000.0
    <BLANKLINE>
            End_Ppal_Amount
    2018Q1           1000.0
    2018Q2           1000.0
    2018Q3           1000.0
    2018Q4           1000.0
    2019Q1           1000.0
    2019Q2           1000.0
    2019Q3           1000.0
    2019Q4           1000.0
    2020Q1           1000.0
    2020Q2           1000.0
    2020Q3              0.0

    """
    if not isinstance(nrate, pd.Series):
        raise TypeError("nrate must be a pandas.Series object")

    balloonpmt = nrate.copy()
    balloonpmt[:] = 0
    balloonpmt[-1] = amount
    return fixed_ppal_loan(amount=amount, nrate=nrate, grace=0, dispoints=dispoints,
                           orgpoints=orgpoints, prepmt=prepmt, balloonpmt=balloonpmt)




def fixed_rate_loan(amount, nrate, life, start, freq='A', grace=0,
                    dispoints=0, orgpoints=0, prepmt=None, balloonpmt=None):
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
        prepmt (pandas.Series): generic cashflow representing prepayments.
        balloonpmt (pandas.Series): generic cashflow representing balloon payments.

    Returns:
       A object of the class ``Loan``.

    >>> pmt = cashflow(const_value=0, start='2016Q1', periods=11, freq='Q')
    >>> pmt['2017Q4'] = 200
    >>> fixed_rate_loan(amount=1000, nrate=10, life=10, start='2016Q1', freq='Q',
    ...                 grace=0, dispoints=0,
    ...                 orgpoints=0, prepmt=pmt, balloonpmt=None) # doctest: +NORMALIZE_WHITESPACE
    Amount:             1000.00
    Total interest:     129.68
    Total payment:      1129.68
    Discount points:    0.00
    Origination points: 0.00
    <BLANKLINE>
            Beg_Ppal_Amount  Nom_Rate  Tot_Payment  Int_Payment  Ppal_Payment  \\
    2016Q1      1000.000000      10.0     0.000000     0.000000      0.000000
    2016Q2      1000.000000      10.0   114.258763    25.000000     89.258763
    2016Q3       910.741237      10.0   114.258763    22.768531     91.490232
    2016Q4       819.251005      10.0   114.258763    20.481275     93.777488
    2017Q1       725.473517      10.0   114.258763    18.136838     96.121925
    2017Q2       629.351591      10.0   114.258763    15.733790     98.524973
    2017Q3       530.826618      10.0   114.258763    13.270665    100.988098
    2017Q4       429.838520      10.0   314.258763    10.745963    303.512800
    2018Q1       126.325720      10.0   114.258763     3.158143    111.100620
    2018Q2        15.225100      10.0    15.605727     0.380627     15.225100
    2018Q3         0.000000      10.0     0.000000     0.000000      0.000000
    <BLANKLINE>
            End_Ppal_Amount
    2016Q1      1000.000000
    2016Q2       910.741237
    2016Q3       819.251005
    2016Q4       725.473517
    2017Q1       629.351591
    2017Q2       530.826618
    2017Q3       429.838520
    2017Q4       126.325720
    2018Q1        15.225100
    2018Q2         0.000000
    2018Q3         0.000000

    """

    if not isinstance(float(nrate), float):
        TypeError('nrate must be a float.')

    nrate = interest_rate(const_value=nrate, start=start, periods=life+grace+1, freq=freq)

    if prepmt is None:
        prepmt = cashflow(const_value=0, start=start, periods=len(nrate), freq=freq)
    else:
        verify_period_range([nrate, prepmt])

    if balloonpmt is None:
        balloonpmt = nrate.copy()
        balloonpmt[:] = 0
    else:
        verify_period_range([nrate, balloonpmt])

    # present value of the balloon payments
    if balloonpmt is not None:
        balloonpv = timevalue(cflo=balloonpmt, prate=nrate, base_date=grace)
    else:
        balloonpv = 0

    pyr = getpyr(nrate)
    pmt = pvpmt(pmt=None, pval=-amount+balloonpv, nrate=nrate[0], nper=len(nrate)-1, pyr=pyr)
    pmts = nrate.copy()
    pmts[:] = 0
    for time in range(1, life + 1):
        pmts[grace + time] = pmt

    # balance
    begppalbal = nrate.copy()
    intpmt = nrate.copy()
    ppalpmt = nrate.copy()
    totpmt = nrate.copy()
    endppalbal = nrate.copy()

    begppalbal[:] = 0
    intpmt[:] = 0
    ppalpmt[:] = 0
    totpmt[:] = 0
    endppalbal[:] = 0

    # payments per period
    for time, _ in enumerate(totpmt):
        totpmt[time] = pmts[time] + balloonpmt[time] + prepmt[time]

    # balance calculation
    for time in range(grace + life + 1):

        if time == 0:
            begppalbal[0] = amount
            endppalbal[0] = amount
            totpmt[time] = amount * (dispoints + orgpoints) / 100
            ### intpmt[time] = amount * dispoints / 100
        else:
            begppalbal[time] = endppalbal[time - 1]
            if time <= grace:
                intpmt[time] = begppalbal[time] * nrate[time] / pyr / 100
                totpmt[time] = intpmt[time]
                endppalbal[time] = begppalbal[time]
            else:
                intpmt[time] = begppalbal[time] * nrate[time] / pyr / 100
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

    data = {'Beg_Ppal_Amount':begppalbal}
    result = Loan(life=life, amount=amount, grace=grace, nrate=nrate,
                  dispoints=dispoints, orgpoints=orgpoints,
                  data=data)
    result['Nom_Rate'] = nrate
    result['Tot_Payment'] = totpmt
    result['Int_Payment'] = intpmt
    result['Ppal_Payment'] = ppalpmt
    result['End_Ppal_Amount'] = endppalbal
    return result


def buydown_loan(amount, nrate, grace=0, dispoints=0, orgpoints=0, prepmt=None):
    """
    In this loan, the periodic payments are recalculated when there are changes
    in the value of the interest rate.

    Args:
        amount (float): Loan amount.
        nrate (float, pandas.Series): nominal interest rate per year.
        grace (int): numner of grace periods without paying the principal.
        dispoints (float): Discount points of the loan.
        orgpoints (float): Origination points of the loan.
        prepmt (pandas.Series): generic cashflow representing prepayments.


    Returns:
       A object of the class ``Loan``.

    >>> nrate = interest_rate(const_value=10, start='2016Q1', periods=11, freq='Q', chgpts={'2017Q2':20})
    >>> buydown_loan(amount=1000, nrate=nrate, dispoints=0, orgpoints=0, prepmt=None)  # doctest: +NORMALIZE_WHITESPACE
    Amount:             1000.00
    Total interest:     200.99
    Total payment:      1200.99
    Discount points:    0.00
    Origination points: 0.00
    <BLANKLINE>
            Beg_Ppal_Amount  Nom_Rate  Tot_Payment  Int_Payment  Ppal_Payment  \\
    2016Q1      1000.000000      10.0     0.000000     0.000000      0.000000
    2016Q2      1000.000000      10.0   114.258763    25.000000     89.258763
    2016Q3       910.741237      10.0   114.258763    22.768531     91.490232
    2016Q4       819.251005      10.0   114.258763    20.481275     93.777488
    2017Q1       725.473517      10.0   114.258763    18.136838     96.121925
    2017Q2       629.351591      20.0   123.993257    31.467580     92.525677
    2017Q3       536.825914      20.0   123.993257    26.841296     97.151961
    2017Q4       439.673952      20.0   123.993257    21.983698    102.009559
    2018Q1       337.664393      20.0   123.993257    16.883220    107.110037
    2018Q2       230.554356      20.0   123.993257    11.527718    112.465539
    2018Q3       118.088816      20.0   123.993257     5.904441    118.088816
    <BLANKLINE>
            End_Ppal_Amount
    2016Q1     1.000000e+03
    2016Q2     9.107412e+02
    2016Q3     8.192510e+02
    2016Q4     7.254735e+02
    2017Q1     6.293516e+02
    2017Q2     5.368259e+02
    2017Q3     4.396740e+02
    2017Q4     3.376644e+02
    2018Q1     2.305544e+02
    2018Q2     1.180888e+02
    2018Q3     1.136868e-13

    >>> pmt = cashflow(const_value=0, start='2016Q1', periods=11, freq='Q')
    >>> pmt['2017Q4'] = 200
    >>> buydown_loan(amount=1000, nrate=nrate, dispoints=0, orgpoints=0, prepmt=pmt)  # doctest: +NORMALIZE_WHITESPACE
    Amount:             1000.00
    Total interest:     180.67
    Total payment:      1180.67
    Discount points:    0.00
    Origination points: 0.00
    <BLANKLINE>
            Beg_Ppal_Amount  Nom_Rate  Tot_Payment  Int_Payment  Ppal_Payment  \\
    2016Q1      1000.000000      10.0     0.000000     0.000000      0.000000
    2016Q2      1000.000000      10.0   114.258763    25.000000     89.258763
    2016Q3       910.741237      10.0   114.258763    22.768531     91.490232
    2016Q4       819.251005      10.0   114.258763    20.481275     93.777488
    2017Q1       725.473517      10.0   114.258763    18.136838     96.121925
    2017Q2       629.351591      20.0   123.993257    31.467580     92.525677
    2017Q3       536.825914      20.0   123.993257    26.841296     97.151961
    2017Q4       439.673952      20.0   323.993257    21.983698    302.009559
    2018Q1       137.664393      20.0    50.551544     6.883220     43.668324
    2018Q2        93.996068      20.0    50.551544     4.699803     45.851741
    2018Q3        48.144328      20.0    50.551544     2.407216     48.144328
    <BLANKLINE>
            End_Ppal_Amount
    2016Q1     1.000000e+03
    2016Q2     9.107412e+02
    2016Q3     8.192510e+02
    2016Q4     7.254735e+02
    2017Q1     6.293516e+02
    2017Q2     5.368259e+02
    2017Q3     4.396740e+02
    2017Q4     1.376644e+02
    2018Q1     9.399607e+01
    2018Q2     4.814433e+01
    2018Q3     4.263256e-14

    """

    if not isinstance(nrate, pd.Series):
        TypeError('nrate must be a pandas.Series object.')

    if prepmt is None:
        prepmt = nrate.copy()
        prepmt[:] = 0
    else:
        verify_period_range([nrate, prepmt])

    life = len(nrate) - grace - 1

    begppalbal = nrate.copy()
    intpmt = nrate.copy()
    ppalpmt = nrate.copy()
    totpmt = nrate.copy()
    endppalbal = nrate.copy()

    begppalbal[:] = 0
    intpmt[:] = 0
    ppalpmt[:] = 0
    totpmt[:] = 0
    endppalbal[:] = 0


    ##
    ## balance calculation
    ##
    pyr = getpyr(nrate)
    for time in range(grace + life + 1):

        if time == 0:
            #
            begppalbal[time] = amount
            endppalbal[time] = amount
            totpmt[time] = amount * (dispoints + orgpoints) / 100
            ### intpmt[time] = amount * dispoints / 100
            #
        else:
            #
            # periodic payment per period
            #
            if time <= grace:

                begppalbal[time] = endppalbal[time - 1]
                intpmt[time] = begppalbal[time] * nrate[time] / pyr / 100
                totpmt[time] = intpmt[time]
                endppalbal[time] = begppalbal[time]

            else:

                pmt = -pvpmt(nrate=nrate[time], nper=grace+life-time+1,
                             pval=endppalbal[time-1], pmt=None, pyr=pyr)

                totpmt[time] = pmt + prepmt[time]

                # balance
                begppalbal[time] = endppalbal[time - 1]
                intpmt[time] = begppalbal[time] * nrate[time] / pyr / 100
                ppalpmt[time] = totpmt[time] - intpmt[time]
                endppalbal[time] = begppalbal[time] - ppalpmt[time]


    data = {'Beg_Ppal_Amount':begppalbal}
    result = Loan(life=life, amount=amount, grace=grace, nrate=nrate,
                  dispoints=dispoints, orgpoints=orgpoints,
                  data=data)
    result['Nom_Rate'] = nrate
    result['Tot_Payment'] = totpmt
    result['Int_Payment'] = intpmt
    result['Ppal_Payment'] = ppalpmt
    result['End_Ppal_Amount'] = endppalbal
    return result



if __name__ == "__main__":
    import doctest
    doctest.testmod()
