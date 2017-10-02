"""
Interest rate transformations
===============================================================================


"""

import numpy as np
import pandas as pd
from timeseries import *
from common import getpyr


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

    `iconv` accepts TimeSeries objects

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
    >>> erate, prate = iconv(nrate=nrate)
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
    >>> erate, prate = iconv(nrate=nrate)
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
