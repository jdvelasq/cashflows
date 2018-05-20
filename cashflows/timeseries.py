"""
Representation of Cashflows and Interest Rates
===============================================================================

Overview
-------------------------------------------------------------------------------

The functions in this module allow the user to create generic cashflows and
interest rates as `pandas.Series` objects under the following restrictions:

* Frequency of time series is restricted to the following values:
  `A`, `'BA'`, `'Q'`, `'BQ'`, `'M'`, `'BM'`, `'CBM'`, `'SM'`, `'6M'`, `'6BM'`
  and `'6CMB'`.
* Interest rates are represented as percentages (not as a fraction).
* Appropriate values must be supplied for the arguments used to create the
  timestamps of the time series.

Due to generic cashflows and interest rates are pandas.Series objects, all available
functions for manipulating and transforming pandas time series can be used with this package.


The ``cashflow`` function returns a `pandas.Series` object that represents a  generic
cashflow. The user must supply two of the following arguments ``start``, ``end``
and ``periods`` in order to create the corresponding timestamps for the time series.
The generic cashflow is set to the value specified by the argument ``const_value``.
In addition, when the value of the argument ``const_value`` is a list, only is
necessary to specify the ``start`` or the ``end`` dates.

For convenience of the user, point values of the time series can be changed using
the argument ``chgpts``.  In this case, the value passed to this argument is a
dictionary where the keys are valid dates and the values are the new values
specified for the generic cashflow in these dates.

The ``interest_rate`` function returns a `pandas.Series` object in the same way
as the ``cashflow`` function. The only difference is that the dictionary passed
to the argument ``chgpts`` specifies change points in the time series, where
the value of the interest rate changes for all points ahead.


Functions in this module
-----------------------------------------------------------------




"""

import numpy as np
import pandas as pd

def period2pos(index, date):
    x = [i for i, elem in enumerate(index) if elem == date]
    if x == []:
        raise ValueError('Date does not exists: ' + date.__repr__())
    return x[0]

def verify_period_range(x):
    if not isinstance(x, list):
        raise ValueError('Argument must be a list: ' + x.__repr__())
    if len(x) == 1:
        return
    for elem in x:
        if not isinstance(elem, pd.Series):
            raise ValueError('pandas.Series expected: ' + elem.__repr__())
        allTrue = all(x[0].axes[0] == elem.axes[0])
        if allTrue is False:
            raise ValueError('Series with different period_range')


def textplot(cflo):
    """Text plot of a generic cashflow.

    Args:
        cflo (pandas.Series): Generic cashflow.

    Returns:
        None.

    **Example**

    >>> cflo = cashflow(const_value=[-10, 5, 0, 20] * 3, start='2000Q1', freq='Q')
    >>> textplot(cflo)# doctest: +NORMALIZE_WHITESPACE
    time      value +------------------+------------------+
    2000Q1   -10.00           **********
    2000Q2     5.00                    *****
    2000Q3     0.00                    *
    2000Q4    20.00                    ********************
    2001Q1   -10.00           **********
    2001Q2     5.00                    *****
    2001Q3     0.00                    *
    2001Q4    20.00                    ********************
    2002Q1   -10.00           **********
    2002Q2     5.00                    *****
    2002Q3     0.00                    *
    2002Q4    20.00                    ********************

    """


    timeid = cflo.index.to_series().astype(str)


    len_timeid = len(timeid[-1].__repr__())
    fmt_timeid = '{:<' + '{:d}'.format(len_timeid) + 's}'

    len_number = 0
    for value in cflo:
        len_number = max(len_number, len('{:1.2f}'.format(value)))

    fmt_number = ' {:' + '{:d}'.format(len_number) + '.2f}'
    fmt_header = ' {:>' + '{:d}'.format(len_number) + 's}'

    # if cflo.pyr == 1:
    #     xmajor, = cflo.start
    #     xminor = 0
    # else:
    #     xmajor, xminor = cflo.start

    maxval = max(abs(cflo))
    width = 20

    txt = []
    txtrow = fmt_timeid.format("time") + fmt_header.format('value')
    txtrow += " +" + "-" * (width - 2) + "+" + "-" * (width - 2) + "+"
    txt.append(txtrow)

    for value, timeid in zip(cflo, cflo.index.to_series().astype(str)):

        # if cflo.pyr == 1:
        #     timeid = (xmajor,)
        # else:
        #     timeid = (xmajor, xminor)

        txtrow = fmt_timeid.format(timeid.__str__())
        txtrow += fmt_number.format(value)

        # fmt_row = "                    *                    "
        xlim = int(width * abs(value / maxval))
        if value < 0:
            txtrow += " " + " " * (width - xlim) + '*' * (xlim)
        elif value > 0:
            txtrow += " " + " " * (width - 1) + "*" * (xlim)
        else:
            txtrow += " " + " " * (width - 1) + '*'

        txt.append(txtrow)


    print('\n'.join(txt))




def cashflow(const_value=0, start=None, end=None, periods=None, freq='A', chgpts=None):
    """Returns a generic cashflow as a pandas.Series object.

    Args:
        const_value (number): constant value for all time series.
        start (string): Date as string using pandas convetion for dates.
        end (string):  Date as string using pandas convetion for dates.
        peridos (integer): Length of the time seriesself.
        freq (string): String indicating the period of time series. Valid values
                      are `'A'`, `'BA'`, `'Q'`, `'BQ'`, `'M'`, `'BM'`, `'CBM'`, `'SM'`, `'6M'`,
                      `'6BM'` and `'6CMB'`. See https://pandas.pydata.org/pandas-docs/stable/timeseries.html#timeseries-offset-aliases
        chgpts (dict): Dictionary indicating point changes in the values of the time series.

    Returns:
        A pandas time series object.


    **Examples**

    A quarterly cashflow with a constant value 1.0 beginning in 2000Q1 can be
    expressed as:

    >>> cashflow(const_value=1.0, start='2000Q1', periods=8, freq='Q') # doctest: +NORMALIZE_WHITESPACE
    2000Q1    1.0
    2000Q2    1.0
    2000Q3    1.0
    2000Q4    1.0
    2001Q1    1.0
    2001Q2    1.0
    2001Q3    1.0
    2001Q4    1.0
    Freq: Q-DEC, dtype: float64

    In the following example, the cashflow function returns a time series object
    using a list for the ``const_value`` and a timestamp for the parameter ``start``.

    >>> cashflow(const_value=[10]*10, start='2000Q1', freq='Q') # doctest: +NORMALIZE_WHITESPACE
    2000Q1    10.0
    2000Q2    10.0
    2000Q3    10.0
    2000Q4    10.0
    2001Q1    10.0
    2001Q2    10.0
    2001Q3    10.0
    2001Q4    10.0
    2002Q1    10.0
    2002Q2    10.0
    Freq: Q-DEC, dtype: float64

    The following example uses the operator ``[]`` to modify the value with
    index equal to 3

    >>> x = cashflow(const_value=[0, 1, 2, 3], start='2000Q1', freq='Q')
    >>> x[3] = 10
    >>> x  # doctest: +NORMALIZE_WHITESPACE
    2000Q1     0.0
    2000Q2     1.0
    2000Q3     2.0
    2000Q4    10.0
    Freq: Q-DEC, dtype: float64


    >>> x[3]  # doctest: +NORMALIZE_WHITESPACE
    10.0


    Indexes in the time series also can be specified using a valid timestamp.

    >>> x['2000Q4'] = 0
    >>> x # doctest: +NORMALIZE_WHITESPACE
    2000Q1    0.0
    2000Q2    1.0
    2000Q3    2.0
    2000Q4    0.0
    Freq: Q-DEC, dtype: float64

    >>> x['2000Q3']  # doctest: +NORMALIZE_WHITESPACE
    2.0

    The following example uses the member function ``cumsum()`` for computing
    the cumulative sum of the original time series.

    >>> cashflow(const_value=[0, 1, 2, 3, 4, 5], freq='Q', start='2000Q1').cumsum() # doctest: +NORMALIZE_WHITESPACE
    2000Q1     0.0
    2000Q2     1.0
    2000Q3     3.0
    2000Q4     6.0
    2001Q1    10.0
    2001Q2    15.0
    Freq: Q-DEC, dtype: float64

    In the next examples, a change point is specified using a dictionary. The key
    can be a integer or a valid timestamp.

    >>> cashflow(const_value=0, freq='Q', periods=6, start='2000Q1', chgpts={2:10}) # doctest: +NORMALIZE_WHITESPACE
    2000Q1     0.0
    2000Q2     0.0
    2000Q3    10.0
    2000Q4     0.0
    2001Q1     0.0
    2001Q2     0.0
    Freq: Q-DEC, dtype: float64

    >>> cashflow(const_value=0, freq='Q', periods=6, start='2000Q1', chgpts={'2000Q3':10}) # doctest: +NORMALIZE_WHITESPACE
    2000Q1     0.0
    2000Q2     0.0
    2000Q3    10.0
    2000Q4     0.0
    2001Q1     0.0
    2001Q2     0.0
    Freq: Q-DEC, dtype: float64


    """
    if freq not in ['A', 'BA', 'Q', 'BQ', 'M', 'BM', 'CBM', 'SM', '6M', '6BM', '6CMB']:
        msg = 'Invalid freq value:  ' + freq.__repr__()
        raise ValueError(msg)
    if isinstance(const_value, list):
        periods = len(const_value)
    prng = pd.period_range(start=start, end=end, periods=periods, freq=freq)
    periods = len(prng)
    if not isinstance(const_value, list):
        const_value = [const_value] * periods
    time_series = pd.Series(data=const_value, index=prng, dtype=np.float64)

    if isinstance(chgpts, dict):
        keys = sorted(chgpts.keys())
        for k in keys:
            if isinstance(k, int):
                x = time_series.axes[0][k]
            else:
                x = k
            time_series[x] = chgpts[k]

    return time_series


def interest_rate(const_value=0, start=None, end=None, periods=None, freq='A', chgpts=None):
    """Creates a time series object specified as a interest rate.

    Args:
        const_value (number): constant value for all time series.
        start (string): Date as string using pandas convetion for dates.
        end (string):  Date as string using pandas convetion for dates.
        peridos (integer): Length of the time seriesself.
        freq (string): String indicating the period of time series. Valid values
                      are `'A'`, `'BA'`, `'Q'`, `'BQ'`, `'M'`, `'BM'`, `'CBM'`, `'SM'`, `'6M'`,
                      `'6BM'` and `'6CMB'`. See https://pandas.pydata.org/pandas-docs/stable/timeseries.html#timeseries-offset-aliases
        chgpts (dict): Dictionary indicating point changes in the values of the time series.

    Returns:
        A pandas time series object.

    **Examples**

    In the following examples, the argument ``chgpts`` is used to specify chnages
    in the value of the interest rate. The keys in the dictionary can be integers
    or valid timestamps.

    >>> chgpts = {'2000Q4':10}
    >>> interest_rate(const_value=1, start='2000Q1', periods=8, freq='Q', chgpts=chgpts) # doctest: +NORMALIZE_WHITESPACE
    2000Q1     1.0
    2000Q2     1.0
    2000Q3     1.0
    2000Q4    10.0
    2001Q1    10.0
    2001Q2    10.0
    2001Q3    10.0
    2001Q4    10.0
    Freq: Q-DEC, dtype: float64

    >>> chgpts = {'2000Q4':10, '2001Q2':20}
    >>> interest_rate(const_value=1, start='2000Q1', periods=8, freq='Q', chgpts=chgpts) # doctest: +NORMALIZE_WHITESPACE
    2000Q1     1.0
    2000Q2     1.0
    2000Q3     1.0
    2000Q4    10.0
    2001Q1    10.0
    2001Q2    20.0
    2001Q3    20.0
    2001Q4    20.0
    Freq: Q-DEC, dtype: float64

    >>> chgpts = {3:10}
    >>> interest_rate(const_value=1, start='2000Q1', periods=8, freq='Q', chgpts=chgpts) # doctest: +NORMALIZE_WHITESPACE
    2000Q1     1.0
    2000Q2     1.0
    2000Q3     1.0
    2000Q4    10.0
    2001Q1    10.0
    2001Q2    10.0
    2001Q3    10.0
    2001Q4    10.0
    Freq: Q-DEC, dtype: float64

    >>> chgpts = {3:10, 6:20}
    >>> interest_rate(const_value=1, start='2000Q1', periods=8, freq='Q', chgpts=chgpts) # doctest: +NORMALIZE_WHITESPACE
    2000Q1     1.0
    2000Q2     1.0
    2000Q3     1.0
    2000Q4    10.0
    2001Q1    10.0
    2001Q2    10.0
    2001Q3    20.0
    2001Q4    20.0
    Freq: Q-DEC, dtype: float64

    The parameter ``const_value`` can be a list of numbers. In this case, only is
    necesary to specify the ``start`` or ``end`` arguments.

    >>> interest_rate(const_value=[10]*12, start='2000-1', freq='M')  # doctest: +NORMALIZE_WHITESPACE
    2000-01    10.0
    2000-02    10.0
    2000-03    10.0
    2000-04    10.0
    2000-05    10.0
    2000-06    10.0
    2000-07    10.0
    2000-08    10.0
    2000-09    10.0
    2000-10    10.0
    2000-11    10.0
    2000-12    10.0
    Freq: M, dtype: float64

    """
    time_series = cashflow(const_value=const_value, start=start, end=end, periods=periods, freq=freq)
    if isinstance(chgpts, dict):
        keys = sorted(chgpts.keys())
        for k in keys:
            if isinstance(k, int):
                x = time_series.axes[0][k]
            else:
                x = k
            for t in time_series.axes[0]:
                if t >= pd.Period(x, freq=freq):
                    time_series[t] = chgpts[k]
    return time_series

if __name__ == "__main__":
    import doctest
    doctest.testmod()
