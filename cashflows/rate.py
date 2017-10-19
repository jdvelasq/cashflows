"""
Interest rate transformations
===============================================================================


"""

import numpy as np
import pandas as pd

# cashflows.
from cashflows.timeseries import *
from cashflows.common import getpyr

def effrate(nrate=None, prate=None, pyr=1):
    """

    >>> effrate(prate=1, pyr=12) # doctest: +ELLIPSIS
    12.68...

    >>> effrate(nrate=10, pyr=12) # doctest: +ELLIPSIS
    10.4713...

    >>> effrate(prate=1, pyr=[3, 6, 12]) # doctest: +ELLIPSIS
    0     3.030100
    1     6.152015
    2    12.682503
    dtype: float64

    >>> effrate(nrate=10, pyr=[3, 6, 12]) # doctest: +ELLIPSIS
    0    10.337037
    1    10.426042
    2    10.471307
    dtype: float64

    >>> effrate(prate=[1, 2, 3], pyr=12) # doctest: +ELLIPSIS
    0    12.682503
    1    26.824179
    2    42.576089
    dtype: float64

    >>> effrate(nrate=[10, 12, 14], pyr=12) # doctest: +ELLIPSIS
    0    10.471307
    1    12.682503
    2    14.934203
    dtype: float64

    When a rate and the number of compounding periods (`pyr`) are vectors, they
    must have the same length. Computations are executed using the first rate
    with the first compounding and so on.

    >>> effrate(nrate=[10, 12, 14], pyr=[3, 6, 12]) # doctest: +ELLIPSIS
    0    10.337037
    1    12.616242
    2    14.934203
    dtype: float64

    >>> effrate(prate=[1, 2, 3], pyr=[3, 6, 12]) # doctest: +ELLIPSIS
    0     3.030100
    1    12.616242
    2    42.576089
    dtype: float64


    >>> nrate = interest_rate(const_value=12, start='2000-06', periods=12, freq='6M')
    >>> prate = perrate(nrate=nrate)
    >>> effrate(nrate = nrate) # doctest: +NORMALIZE_WHITESPACE
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

    >>> effrate(prate = prate) # doctest: +NORMALIZE_WHITESPACE
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

    """
    numnone = 0
    if nrate is None:
        numnone += 1
    if prate is None:
        numnone += 1
    if numnone != 1:
        raise ValueError('One of the rates must be set to `None`')

    if isinstance(nrate, pd.Series):
        pyr = getpyr(nrate)
        erate = nrate.copy()
        for index in range(len(nrate)):
            erate[index] = 100 * (np.power(1 + nrate[index]/100/pyr, pyr) - 1)
        return erate

    if isinstance(prate, pd.Series):
        pyr = getpyr(prate)
        erate = prate.copy()
        for index in range(len(prate)):
            erate[index] = 100 * (np.power(1 + prate[index]/100, pyr) - 1)
        return erate

    if nrate is not None:
        ##
        ##
        maxlen = 1
        if isinstance(nrate, (list, type(np.array), type(pd.Series))):
            maxlen = max(maxlen, len(nrate))
        if isinstance(pyr, (list, type(np.array), type(pd.Series))):
            maxlen = max(maxlen, len(pyr))
        #
        if isinstance(nrate, (int, float)):
            nrate = [nrate] * maxlen
        nrate = pd.Series(nrate, dtype=np.float64)
        if isinstance(pyr, (int, float)):
            pyr = [pyr] * maxlen
        pyr = pd.Series(pyr)
        #
        if len(nrate) != len(pyr):
            raise ValueError('Lists must have the same length')
        ##
        ##
        prate = nrate / pyr
        erate = 100 * (np.power(1 + prate/100, pyr) - 1)
        if maxlen == 1:
            erate = erate[0]
        return erate


    if prate is not None:
        ##
        ##
        maxlen = 1
        if isinstance(prate, (list, type(np.array), type(pd.Series))):
            maxlen = max(maxlen, len(prate))
        if isinstance(pyr, (list, type(np.array), type(pd.Series))):
            maxlen = max(maxlen, len(pyr))
        #
        if isinstance(prate, (int, float)):
            prate = [prate] * maxlen
        prate = pd.Series(prate, dtype=np.float64)
        if isinstance(pyr, (int, float)):
            pyr = [pyr] * maxlen
        pyr = pd.Series(pyr)
        #
        if len(prate) != len(pyr):
            raise ValueError('Lists must have the same length')
        ##
        ##
        erate = 100 * (np.power(1 + prate / 100, pyr) - 1)
        if maxlen == 1:
            erate = erate[0]
        return erate




def nomrate(erate=None, prate=None, pyr=1):
    """

    >>> nomrate(prate=1, pyr=12) # doctest: +ELLIPSIS
    12.0

    >>> nomrate(erate=10, pyr=[3, 6, 12]) # doctest: +ELLIPSIS
    0    9.684035
    1    9.607121
    2    9.568969
    dtype: float64

    >>> nomrate(erate=10, pyr=12) # doctest: +ELLIPSIS
    9.5689...

    >>> nomrate(prate=1, pyr=[3, 6, 12]) # doctest: +ELLIPSIS
    0     3.0
    1     6.0
    2    12.0
    dtype: float64

    >>> nomrate(erate=[10, 12, 14], pyr=12) # doctest: +ELLIPSIS
    0     9.568969
    1    11.386552
    2    13.174622
    dtype: float64

    >>> nomrate(prate=[1, 2, 3], pyr=12) # doctest: +ELLIPSIS
    0    12.0
    1    24.0
    2    36.0
    dtype: float64

    When a rate and the number of compounding periods (`pyr`) are vectors, they
    must have the same length. Computations are executed using the first rate
    with the first compounding and so on.

    >>> nomrate(erate=[10, 12, 14], pyr=[3, 6, 12]) # doctest: +ELLIPSIS
    0     9.684035
    1    11.440574
    2    13.174622
    dtype: float64

    >>> nomrate(prate=[1, 2, 3], pyr=[3, 6, 12]) # doctest: +ELLIPSIS
    0     3.0
    1    12.0
    2    36.0
    dtype: float64

    >>> prate = interest_rate(const_value=6.00, start='2000-06', periods=12, freq='6M')
    >>> erate = effrate(prate=prate)
    >>> nomrate(erate=erate)
    2000-06    12.0
    2000-12    12.0
    2001-06    12.0
    2001-12    12.0
    2002-06    12.0
    2002-12    12.0
    2003-06    12.0
    2003-12    12.0
    2004-06    12.0
    2004-12    12.0
    2005-06    12.0
    2005-12    12.0
    Freq: 6M, dtype: float64


    >>> nomrate(prate=prate)
    2000-06    12.0
    2000-12    12.0
    2001-06    12.0
    2001-12    12.0
    2002-06    12.0
    2002-12    12.0
    2003-06    12.0
    2003-12    12.0
    2004-06    12.0
    2004-12    12.0
    2005-06    12.0
    2005-12    12.0
    Freq: 6M, dtype: float64


    """
    numnone = 0
    if erate is None:
        numnone += 1
    if prate is None:
        numnone += 1
    if numnone != 1:
        raise ValueError('One of the rates must be set to `None`')

    if isinstance(erate, pd.Series):
        pyr = getpyr(erate)
        nrate = erate.copy()
        for index in range(len(erate)):
            nrate[index] = 100 * pyr * (np.power(1 + erate[index]/100, 1. / pyr) - 1)
        return nrate

    if isinstance(prate, pd.Series):
        pyr = getpyr(prate)
        nrate = prate.copy()
        for index in range(len(prate)):
            nrate[index] = prate[index] * pyr
        return nrate


    if erate is not None:
        ##
        ##
        maxlen = 1
        if isinstance(erate, (list, type(np.array), type(pd.Series))):
            maxlen = max(maxlen, len(erate))
        if isinstance(pyr, (list, type(np.array), type(pd.Series))):
            maxlen = max(maxlen, len(pyr))
        #
        if isinstance(erate, (int, float)):
            erate = [erate] * maxlen
        erate = pd.Series(erate, dtype=np.float64)
        #
        if isinstance(pyr, (int, float)):
            pyr = [pyr] * maxlen
        pyr = pd.Series(pyr)
        #
        if len(erate) != len(pyr):
            raise ValueError('Lists must have the same length')
        ##
        ##
        prate = 100 * (np.power(1 + erate / 100, 1 / pyr) - 1)
        nrate = pyr * prate
        if maxlen == 1:
            nrate = nrate[0]
        return nrate

    if prate is not None:
        ##
        ##
        maxlen = 1
        if isinstance(prate, (list, type(np.array), type(pd.Series))):
            maxlen = max(maxlen, len(prate))
        if isinstance(pyr, (list, type(np.array), type(pd.Series))):
            maxlen = max(maxlen, len(pyr))
        #
        if isinstance(prate, (int, float)):
            prate = [prate] * maxlen
        prate = pd.Series(prate, dtype=np.float64)
        if isinstance(pyr, (int, float)):
            pyr = [pyr] * maxlen
        pyr = pd.Series(pyr)
        #
        if len(prate) != len(pyr):
            raise ValueError('Lists must have the same length')
        ##
        ##
        nrate = pyr * prate
        if maxlen == 1:
            nrate = nrate[0]
        return nrate


def perrate(nrate=None, erate=None, pyr=1):
    """

    >>> perrate(nrate=10, pyr=12) # doctest: +ELLIPSIS
    0.8333...

    >>> perrate(erate=10, pyr=12) # doctest: +ELLIPSIS
    0.7974...

    >>> perrate(erate=10, pyr=[3, 6, 12]) # doctest: +ELLIPSIS
    0    3.228012
    1    1.601187
    2    0.797414
    dtype: float64

    >>> perrate(nrate=10, pyr=[3, 6, 12]) # doctest: +ELLIPSIS
    0    3.333333
    1    1.666667
    2    0.833333
    dtype: float64

    >>> perrate(erate=[10, 12, 14], pyr=12) # doctest: +ELLIPSIS
    0    0.797414
    1    0.948879
    2    1.097885
    dtype: float64

    >>> perrate(nrate=[10, 12, 14], pyr=12) # doctest: +ELLIPSIS
    0    0.833333
    1    1.000000
    2    1.166667
    dtype: float64

    When a rate and the number of compounding periods (`pyr`) are vectors, they
    must have the same length. Computations are executed using the first rate
    with the first compounding and so on.

    >>> perrate(erate=[10, 12, 14], pyr=[3, 6, 12]) # doctest: +ELLIPSIS
    0    3.228012
    1    1.906762
    2    1.097885
    dtype: float64

    >>> perrate(nrate=[10, 12, 14], pyr=[3, 6, 12]) # doctest: +ELLIPSIS
    0    3.333333
    1    2.000000
    2    1.166667
    dtype: float64


    >>> nrate = interest_rate(const_value=12.0,  start='2000-06', periods=12, freq='6M')
    >>> erate = effrate(nrate=nrate)
    >>> perrate(erate=erate) # doctest: +NORMALIZE_WHITESPACE
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

    >>> perrate(nrate=nrate) # doctest: +NORMALIZE_WHITESPACE
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


    """
    numnone = 0
    if nrate is None:
        numnone += 1
    if erate is None:
        numnone += 1
    if numnone != 1:
        raise ValueError('One of the rates must be set to `None`')

    if isinstance(nrate, pd.Series):
        pyr = getpyr(nrate)
        prate = nrate.copy()
        for index in range(len(nrate)):
            prate[index] = nrate[index] / pyr
        return prate

    if isinstance(erate, pd.Series):
        pyr = getpyr(erate)
        prate = erate.copy()
        for index in range(len(erate)):
            prate[index] = 100 * (np.power(1 + erate[index]/100, 1. / pyr) - 1)
        return prate

    if nrate is not None:
        ##
        ##
        maxlen = 1
        if isinstance(nrate, (list, type(np.array), type(pd.Series))):
            maxlen = max(maxlen, len(nrate))
        if isinstance(pyr, (list, type(np.array), type(pd.Series))):
            maxlen = max(maxlen, len(pyr))
        #
        if isinstance(nrate, (int, float)):
            nrate = [nrate] * maxlen
        nrate = pd.Series(nrate, dtype=np.float64)
        if isinstance(pyr, (int, float)):
            pyr = [pyr] * maxlen
        pyr = pd.Series(pyr)
        #
        if len(nrate) != len(pyr):
            raise ValueError('Lists must have the same length')
        ##
        ##
        prate = nrate / pyr
        if maxlen == 1:
            prate = prate[0]
        return prate

    if erate is not None:
        ##
        ##
        maxlen = 1
        if isinstance(erate, (list, type(np.array), type(pd.Series))):
            maxlen = max(maxlen, len(erate))
        if isinstance(pyr, (list, type(np.array), type(pd.Series))):
            maxlen = max(maxlen, len(pyr))
        #
        if isinstance(erate, (int, float)):
            erate = [erate] * maxlen
        erate = pd.Series(erate, dtype=np.float64)
        #
        if isinstance(pyr, (int, float)):
            pyr = [pyr] * maxlen
        pyr = pd.Series(pyr)
        #
        if len(erate) != len(pyr):
            raise ValueError('Lists must have the same length')
        ##
        ##
        prate = 100 * (np.power(1 + erate / 100, 1 / pyr) - 1)
        if maxlen == 1:
            prate = prate[0]
        return prate





def to_discount_factor(nrate=None, erate=None, prate=None, base_date=None):
    """Returns a list of discount factors calculated as 1 / (1 + r)^(t - t0).

    Args:
        nrate (pandasSeries): Nominal interest rate per year.
        nrate (pandasSeries): Effective interest rate per year.
        prate (pandasSeries): Periodic interest rate.
        base_date (string): basis time.

    Returns:
        pandas.Series of float values

    Only one of the interest rates must be supplied for the computation.

    >>> nrate = interest_rate(const_value=4, periods=10, start='2016Q1', freq='Q')
    >>> erate = effrate(nrate=nrate)
    >>> prate = perrate(nrate=nrate)
    >>> to_discount_factor(nrate=nrate, base_date='2016Q3') # doctest: +ELLIPSIS
    [1.0201, 1.01, 1.0, 0.990..., 0.980..., 0.970..., 0.960..., 0.951..., 0.942..., 0.932...]

    >>> to_discount_factor(erate=erate, base_date='2016Q3') # doctest: +ELLIPSIS
    [1.0201, 1.01, 1.0, 0.990..., 0.980..., 0.970..., 0.960..., 0.951..., 0.942..., 0.932...]

    >>> to_discount_factor(prate=prate, base_date='2016Q3') # doctest: +ELLIPSIS
    [1.0201, 1.01, 1.0, 0.990..., 0.980..., 0.970..., 0.960..., 0.951..., 0.942..., 0.932...]
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
        pyr = getpyr(nrate)
        prate = nrate.copy()
        for i,_ in enumerate(nrate):
            prate[i] = nrate[i] / pyr  # periodic rate

    if erate is not None:
        pyr = getpyr(erate)
        prate = erate.copy()
        for i,_ in enumerate(erate):
            prate[i] = 100 * (np.power(1 + erate[i]/100, 1. / pyr) - 1) # periodic rate

    pyr = getpyr(prate)

    factor = [x/100 for x in prate]

    for index, _ in enumerate(factor):
        if index == 0:
            factor[0] = 1 / (1 + factor[0])
        else:
            factor[index] = factor[index-1] / (1 + factor[index])

    if isinstance(base_date, str):
        base_date = pd.Period(base_date, freq=prate.axes[0].freq)
        base_date = period2pos(prate.axes[0], base_date)

    div = factor[base_date]
    for index, _ in enumerate(factor):
        factor[index] = factor[index] / div
    return factor


def to_compound_factor(nrate=None, erate=None, prate=None, base_date=0):
    """Returns a list of compounding factors calculated as (1 + r)^(t - t0).

    Args:
        nrate (TimeSeries): Nominal interest rate per year.
        nrate (TimeSeries): Effective interest rate per year.
        prate (TimeSeries): Periodic interest rate.
        base_date (int, tuple): basis time.

    Returns:
        Compound factor (list)


    **Examples**

    >>> nrate = interest_rate(const_value=4, start='2000', periods=10, freq='Q')
    >>> erate = effrate(nrate=nrate)
    >>> prate = perrate(nrate=nrate)
    >>> to_compound_factor(prate=prate, base_date=2) # doctest: +ELLIPSIS
    [0.980..., 0.990..., 1.0, 1.01, 1.0201, 1.030..., 1.040..., 1.051..., 1.061..., 1.072...]

    >>> to_compound_factor(nrate=nrate, base_date=2) # doctest: +ELLIPSIS
    [0.980..., 0.990..., 1.0, 1.01, 1.0201, 1.030..., 1.040..., 1.051..., 1.061..., 1.072...]

    >>> to_compound_factor(erate=erate, base_date=2) # doctest: +ELLIPSIS
    [0.980..., 0.990..., 1.0, 1.01, 1.0201, 1.030..., 1.040..., 1.051..., 1.061..., 1.072...]

    """
    factor = to_discount_factor(nrate=nrate, erate=erate, prate=prate, base_date=base_date)
    for time, _ in enumerate(factor):
        factor[time] = 1 / factor[time]
    return factor



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
        pyr = getpyr(nrate)
        factor = 1
        for element in nrate[1:]:
            factor *= (1 + element / 100 / pyr)
        return 100 * pyr * (factor**(1/(len(nrate) - 1)) - 1)

    if prate is not None:
        pyr = getpyr(prate)
        factor = 1
        for element in prate[1:]:
            factor *= (1 + element / 100)
        return 100  * (factor**(1/(len(prate) - 1)) - 1)

    if erate is not None:
        pyr = getpyr(erate)
        factor = 1
        for element in erate[1:]:
            factor *= (1 + (numpy.power(1 + element/100, 1. / pyr) - 1))
        return 100  * (factor**(1/(len(value) - 1)) - 1)



if __name__ == "__main__":
    import doctest
    doctest.testmod()
