"""
Constant dollar transformations
===============================================================================

The function `const2curr` computes the equivalent generic cashflow in current
dollars from a generic cashflow in constant dollars of the date given by
`base_date`. `inflation` is the inflation rate per compounding period.
`curr2const` computes the inverse transformation.

"""
import pandas as pd

# cashflows.
from cashflows.timeseries import cashflow, interest_rate, verify_period_range
from cashflows.rate import to_compound_factor, to_discount_factor
from cashflows.common import _vars2list


def const2curr(cflo, inflation, base_date=0):
    """Converts a cashflow of constant dollars to current dollars
    of the time `base_date`.

    Args:
        cflo (pandas.Series): A cashflow.
        inflation (pandas.Series): Inflation rate per compounding period.
        base_date (int, str): base date.

    Returns:
        A cashflow in current money (pandas.Series)


    **Examples.**

    >>> cflo=cashflow(const_value=[100] * 5, start='2000', freq='A')
    >>> inflation=interest_rate(const_value=[10, 10, 20, 20, 20], start='2000', freq='A')
    >>> const2curr(cflo=cflo, inflation=inflation) # doctest: +NORMALIZE_WHITESPACE
    2000    100.00
    2001    110.00
    2002    132.00
    2003    158.40
    2004    190.08
    Freq: A-DEC, dtype: float64

    >>> const2curr(cflo=cflo, inflation=inflation, base_date=0) # doctest: +NORMALIZE_WHITESPACE
    2000    100.00
    2001    110.00
    2002    132.00
    2003    158.40
    2004    190.08
    Freq: A-DEC, dtype: float64

    >>> const2curr(cflo=cflo, inflation=inflation, base_date='2000') # doctest: +NORMALIZE_WHITESPACE
    2000    100.00
    2001    110.00
    2002    132.00
    2003    158.40
    2004    190.08
    Freq: A-DEC, dtype: float64

    >>> const2curr(cflo=cflo, inflation=inflation, base_date=4) # doctest: +NORMALIZE_WHITESPACE
    2000     52.609428
    2001     57.870370
    2002     69.444444
    2003     83.333333
    2004    100.000000
    Freq: A-DEC, dtype: float64

    >>> const2curr(cflo=cflo, inflation=inflation, base_date='2004') # doctest: +NORMALIZE_WHITESPACE
    2000     52.609428
    2001     57.870370
    2002     69.444444
    2003     83.333333
    2004    100.000000
    Freq: A-DEC, dtype: float64


    """
    if not isinstance(cflo, pd.Series):
        raise TypeError("cflo must be a TimeSeries object")
    if not isinstance(inflation, pd.Series):
        raise TypeError("inflation must be a TimeSeries object")
    verify_period_range([cflo, inflation])
    factor = to_compound_factor(prate=inflation, base_date=base_date)
    result = cflo.copy()
    for time, _ in enumerate(result):
        result[time] *= factor[time]
    return result


    # if not isinstance(cflo, pd.Series):
    #     raise TypeError("cflo must be a TimeSeries object")
    # if not isinstance(inflation, pd.Series):
    #     raise TypeError("inflation must be a TimeSeries object")
    # if not isinstance(base_date, list):
    #     base_date = [base_date]
    # verify_period_range([cflo, inflation])
    # index = cflo.index.copy().to_series().astype(str)
    # retval = None
    # for xbase_date in base_date:
    #     factor = to_compound_factor(prate=inflation, base_date=xbase_date)
    #     result = cflo.copy()
    #     for time, _ in enumerate(result):
    #         result[time] *= factor[time]
    #     if isinstance(xbase_date, str):
    #         current_date = xbase_date
    #     else:
    #         current_date = index[xbase_date]
    #     if retval is None:
    #         retval = {current_date:result}
    #     else:
    #         retval[current_date] = result
    # retval = pd.DataFrame(retval)
    # if len(retval.columns) == 1:
    #     return retval[retval.columns[0]]
    # return retval



    ##
    ## version inicial
    ##

    # params = _vars2list([cflo, inflation, base_date])
    # cflo = params[0]
    # inflation = params[1]
    # base_date = params[2]
    # retval = []
    # for xcflo, xinflation, xbase_date in zip(cflo, inflation, base_date):
    #     if not isinstance(xcflo, pd.Series):
    #         raise TypeError("cflo must be a TimeSeries object")
    #     if not isinstance(xinflation, pd.Series):
    #         raise TypeError("inflation must be a TimeSeries object")
    #     verify_period_range([xcflo, xinflation])
    #     factor = to_compound_factor(prate=xinflation, base_date=xbase_date)
    #     result = xcflo.copy()
    #     for time, _ in enumerate(result):
    #         result[time] *= factor[time]
    #     retval.append(result)
    # if len(retval) == 1:
    #     return retval[0]
    # return retval



def curr2const(cflo, inflation, base_date=0):
    """Converts a cashflow of current dollars to constant dollars of
    the date `base_date`.

    Args:
        cflo (list, Cashflow): A cashflow.
        inflation_rate (float, Rate): Inflation rate per compounding period.
        base_date (int): base time..

    Returns:
        A cashflow in constant dollars

    >>> cflo = cashflow(const_value=[100] * 5, start='2015', freq='A')
    >>> inflation = interest_rate(const_value=[10, 10, 20, 20, 20], start='2015', freq='A')
    >>> curr2const(cflo=cflo, inflation=inflation) # doctest: +NORMALIZE_WHITESPACE
    2015    100.000000
    2016     90.909091
    2017     75.757576
    2018     63.131313
    2019     52.609428
    Freq: A-DEC, dtype: float64

    >>> curr2const(cflo=cflo, inflation=inflation, base_date=4) # doctest: +NORMALIZE_WHITESPACE
    2015    190.08
    2016    172.80
    2017    144.00
    2018    120.00
    2019    100.00
    Freq: A-DEC, dtype: float64

    >>> curr2const(cflo=cflo, inflation=inflation, base_date='2017') # doctest: +NORMALIZE_WHITESPACE
    2015    132.000000
    2016    120.000000
    2017    100.000000
    2018     83.333333
    2019     69.444444
    Freq: A-DEC, dtype: float64

    """
    if not isinstance(cflo, pd.Series):
        raise TypeError("cflo must be a TimeSeries object")
    if not isinstance(inflation, pd.Series):
        raise TypeError("inflation must be a TimeSeries object")
    verify_period_range([cflo, inflation])
    factor = to_discount_factor(prate=inflation, base_date=base_date)
    result = cflo.copy()
    for time, _ in enumerate(result):
        result[time] *= factor[time]
    return result


    # if not isinstance(cflo, pd.Series):
    #     raise TypeError("cflo must be a TimeSeries object")
    # if not isinstance(inflation, pd.Series):
    #     raise TypeError("inflation must be a TimeSeries object")
    # if not isinstance(base_date, list):
    #     base_date = [base_date]
    # verify_period_range([cflo, inflation])
    # index = cflo.index.copy().to_series().astype(str)
    # retval = None
    # for xbase_date in base_date:
    #     factor = to_discount_factor(prate=inflation, base_date=xbase_date)
    #     result = cflo.copy()
    #     for time, _ in enumerate(result):
    #         result[time] *= factor[time]
    #     if isinstance(xbase_date, str):
    #         current_date = xbase_date
    #     else:
    #         current_date = index[xbase_date]
    #     if retval is None:
    #         retval = {current_date:result}
    #     else:
    #         retval[current_date] = result
    # retval = pd.DataFrame(retval)
    # if len(retval.columns) == 1:
    #     return retval[retval.columns[0]]
    # return retval



    ##
    ## version inicial
    ##



    # params = _vars2list([cflo, inflation, base_date])
    # cflo = params[0]
    # inflation = params[1]
    # base_date = params[2]
    # retval = []
    # for xcflo, xinflation, xbase_date in zip(cflo, inflation, base_date):
    #     if not isinstance(xcflo, pd.Series):
    #         raise TypeError("cflo must be a TimeSeries object")
    #     if not isinstance(xinflation, pd.Series):
    #         raise TypeError("inflation must be a TimeSeries object")
    #     verify_period_range([xcflo, xinflation])
    #     factor = to_discount_factor(prate=xinflation, base_date=xbase_date)
    #     result = xcflo.copy()
    #     for time, _ in enumerate(result):
    #         result[time] *= factor[time]
    #     retval.append(result)
    # if len(retval) == 1:
    #     return retval[0]
    # return retval



if __name__ == "__main__":
    import doctest
    doctest.testmod()
