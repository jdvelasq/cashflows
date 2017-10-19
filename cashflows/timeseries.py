
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
    """Text plot of a cashflow.

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




def cashflow(const_value=0, start=None, end=None, periods=None, freq='A'):
    """Returns a generic cashflow as a pandas.Series object.

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

    >>> x['2000Q4'] = 0
    >>> x # doctest: +NORMALIZE_WHITESPACE
    2000Q1    0.0
    2000Q2    1.0
    2000Q3    2.0
    2000Q4    0.0
    Freq: Q-DEC, dtype: float64

    >>> x['2000Q3']  # doctest: +NORMALIZE_WHITESPACE
    2.0

    >>> cashflow(const_value=[0, 1, 2, 3, 4, 5], freq='Q', start='2000Q1').cumsum() # doctest: +NORMALIZE_WHITESPACE
    2000Q1     0.0
    2000Q2     1.0
    2000Q3     3.0
    2000Q4     6.0
    2001Q1    10.0
    2001Q2    15.0
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
    return time_series


def interest_rate(const_value=0, start=None, end=None, periods=None, freq='A', chgpts=None):
    """Creates a time series object specified as a interest rate.

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



#### esto ya no
# class xTimeSeries(pd.Series):
#
#     def __init__(self, start=None, end=None, nper=None, freq='A'):
#         """Creates a generic time series.
#
#         >>> xTimeSeries(start="2001", nper=10) # doctest: +NORMALIZE_WHITESPACE
#         Time Series:
#           Start = 2001-12-31
#           End   = 2010-12-31
#           pyr   = 1
#           Data  = 2001-12-31 0.0
#                   2002-12-31 0.0
#                   2003-12-31 0.0
#                   2004-12-31 0.0
#                   2005-12-31 0.0
#                   2006-12-31 0.0
#                   2007-12-31 0.0
#                   2008-12-31 0.0
#                   2009-12-31 0.0
#                   2010-12-31 0.0
#
#         # >>> xTimeSeries(end="2010", nper=10) # doctest: +NORMALIZE_WHITESPACE
#         # Time Series:
#         # Start = (2001,)
#         # End = (2010,)
#         # pyr = 1
#         # Data = (2001,)-(2010,) [10] 0.00
#         #
#         # >>> xTimeSeries(start="2000", end="2002") # doctest: +NORMALIZE_WHITESPACE
#         # Time Series:
#         # Start = (2000,)
#         # End = (2002,)
#         # pyr = 1
#         # Data = (2000,)-(2002,) [3] 0.00
#         #
#         # >>> xTimeSeries(start="2000", end="2002", nper=3) # doctest: +NORMALIZE_WHITESPACE
#         # Time Series:
#         # Start = (2000,)
#         # End = (2002,)
#         # pyr = 1
#         # Data = (2000,)-(2002,) [3] 0.00
#         #
#         # >>> xTimeSeries(start="2000Q1", nper=4, freq='Q') # doctest: +NORMALIZE_WHITESPACE
#         # Time Series:
#         # Start = (2000,)
#         # End = (2002,)
#         # pyr = 1
#         # Data = (2000,)-(2002,) [3] 0.00
#
#
#         """
#
#         pyr = None
#
#         if freq in ['A', 'BA']:
#             pyr = 1
#
#         if freq in ['Q', 'BQ']:
#             pyr = 4
#
#         if freq in ['M', 'BM', 'CBM']:
#             pyr = 12
#
#         if freq in ['SM']:
#             pyr = 24
#
#
#         if pyr is None:
#             msg = 'Invalid freq value:  ' + freq.__repr__()
#             raise ValueError(msg)
#
#         # print(start)
#         # print(end)
#         # print(nper)
#         # print(freq)
#
#         index = pd.date_range(start=start, end=end, periods=nper, freq=freq)
#         nper = len(index)
#         super().__init__(data=[0.0] * nper, index=index)
#         self.start = index[0]
#         self.end = index[-1]
#         self.pyr = pyr
#         self.freq = freq
#
#         # self.name = ''
#         #self.nper = nper
#
#         #self.start = index[1]
#         #self.end = index[-1]
#         #self.pyr = pyr
#         #self.freq = freq
#         # self.data = pd.Series([[0] * nper])
#
#
#
#     def __repr__(self):
#         """Print the time series."""
#
#
#
#         txt = ['Time Series:']
#         txt += ['  Start = {:s}'.format(pd.to_datetime(self.start).strftime('%Y-%m-%d').__str__())]
#         txt += ['  End   = {:s}'.format(pd.to_datetime(self.end).strftime('%Y-%m-%d').__str__())]
#         txt += ['  pyr   = {:s}'.format(self.pyr.__repr__())]
#
#         x = pd.to_datetime(self.index[0]).strftime('%Y-%m-%d').__str__()
#
#
#         txt += ['  Data  = ' + x + ' ' + self.values[0].__str__()]
#         for (t, v)  in zip(self.index[1:], self.values[1:]):
#             x = pd.to_datetime(t).strftime('%Y-%m-%d').__str__()
#             txt += ['          ' + x + ' ' + v.__str__()]
#         txt = '\n'.join(txt) + '\n'
#         return txt
#
#
# # to_datetime(df[['year', 'month', 'day']])
# #         return(super().__repr__())
#
# #        if self.pyr in [4, 7, 12]:
# #            return self.__repr4712__()
# #
#
#         #
#         # if self.pyr == 1:
#         #     imajor, = self.start
#         #     iminor = 0
#         # else:
#         #     imajor, iminor = self.start
#         #
#         # txt_date = []
#         # txt_freq = []
#         # txt_val = []
#         #
#         # period = 0
#         # while period < len(self.data):
#         #
#         #     freq = 1
#         #     if self.pyr == 1:
#         #         beg_date = end_date = (imajor,)
#         #     else:
#         #         beg_date = end_date = (imajor, iminor)
#         #
#         #     while period + freq < len(self.data) and \
#         #           self.data[period] == self.data[period + freq]:
#         #         freq += 1
#         #         iminor += 1
#         #         if iminor >= self.pyr:
#         #             iminor = 0
#         #             imajor += 1
#         #
#         #         if self.pyr == 1:
#         #             end_date = (imajor,)
#         #         else:
#         #             end_date = (imajor, iminor)
#         #
#         #     iminor += 1
#         #     if iminor >= self.pyr:
#         #         iminor = 0
#         #         imajor += 1
#         #
#         #     if freq == 1:
#         #
#         # #                iminor += 1
#         # #                if iminor >= self.pyr:
#         # #                    iminor = 0
#         # #                    imajor += 1
#         #
#         #         txt_date += ['{:s}'.format(beg_date.__str__())]
#         #         txt_freq += [' ']
#         #         txt_val += ['{:1.2f}'.format(self.data[period])]
#         #     else:
#         #         fmt = '{:s}-{:s}'
#         #         txt_date += [fmt.format(beg_date.__str__(), end_date.__str__())]
#         #         txt_freq += ['[{:d}]'.format(freq)]
#         #         txt_val += ['{:1.2f}'.format(self.data[period])]
#         #
#         #
#         #
#         #     period += freq
#         #
#         # max_date = max_freq = max_val = 0
#         # for index, _ in enumerate(txt_date):
#         #     max_date = max(max_date, len(txt_date[index]))
#         #     max_freq = max(max_freq, len(txt_freq[index]))
#         #     max_val = max(max_val, len(txt_val[index]))
#         #
#         # fmt = ' {:' + '{:d}'.format(max_date) + 's} '
#         # fmt += '{:' + '{:d}'.format(max_freq) + 's} '
#         # fmt += '{:>' + '{:d}'.format(max_val) + 's} '
#         #
#         #
#         # for index, _ in enumerate(txt_date):
#         #     if index == 0:
#         #         txt += ['Data =' + fmt.format(txt_date[index], txt_freq[index], txt_val[index])]
#         #     else:
#         #         txt += ['      ' +fmt.format(txt_date[index], txt_freq[index], txt_val[index])]
#         #
#         # return '\n'.join(txt)+'\n'
#         #
#         #
#         # def __repr4712__(self):
#         # """ Prints as table with quarters, days or months.
#         #
#         # # >>> TimeSeries(start=(1, 0), pyr=4) # doctest: +NORMALIZE_WHITESPACE
#         # #   Qtr0 Qtr1 Qtr2 Qtr3
#         # # 1 0.00
#         #
#         # # >>> TimeSeries(start=(1, 1), pyr=7) # doctest: +NORMALIZE_WHITESPACE
#         # #   Mon  Tue  Wed  Thu  Fri  Sat  Sun
#         # # 1 0.00
#         #
#         # # >>> TimeSeries(start=(1, 1), pyr=12)  # doctest: +NORMALIZE_WHITESPACE
#         # #    Jan  Feb  Mar  Apr  May  Jun  Jul  Aug  Sep  Oct  Nov  Dec
#         # # 1 0.00
#         #
#         #
#         # """
#         # smajor, sminor = self.start
#         # emajor, eminor = self.end
#         #
#         # imajor = smajor
#         # iminor = 0
#         # iper = 0
#         #
#         # maxlen = 0
#         # for data in self.data:
#         #     maxlen = max(maxlen, len('{:.2f}'.format(data)))
#         #
#         # maxlen = maxlen - 3
#         #
#         # fmt_major = '{:<' + '{:<d}'.format(len(emajor.__str__())) + 'd}'
#         # fmt_minor = ' {:>' + '{:d}'.format(maxlen+3) + '.2f}'
#         # fmt_void = ' ' * (4+len(max(self.data).__str__()))
#         # fmt_head = ' {:>' + '{:d}'.format(maxlen+3) + 's}'
#         #
#         # sline = ' ' * len(emajor.__str__())
#         # if self.pyr == 4:
#         #     names = ['Qtr0', 'Qtr1', 'Qtr2', 'Qtr3']
#         # elif self.pyr == 7:
#         #     names = calendar.day_abbr
#         # else:
#         #     names = calendar.month_abbr[1:13]
#         #
#         # for index in range(self.pyr):
#         #     sline += fmt_head.format(names[index])
#         # txt = [sline]
#         # sline = ''
#         #
#         # sline = fmt_major.format(imajor)
#         #
#         # is_ok = True
#         #
#         # while is_ok is True:
#         #
#         #     if imajor == smajor and iminor < sminor:
#         #         sline += fmt_void
#         #     else:
#         #         sline += fmt_minor.format(self.data[iper])
#         #         iper += 1
#         #
#         #     if  imajor == emajor and iminor == eminor:
#         #         is_ok = False
#         #
#         #     iminor += 1
#         #     if iminor >= self.pyr:
#         #         iminor = 0
#         #         imajor += 1
#         #         txt.append(sline)
#         #         if is_ok is True:
#         #             sline = fmt_major.format(imajor)
#         #         else:
#         #             sline = ''
#         #
#         # txt.append(sline)
#         # return '\n'.join(txt)
#         #
#         #
#         #
#         # def __getitem__(self, key):
#         # """gets the item
#         #
#         #
#         #
#         # """
#         # if isinstance(key, tuple):
#         #     key = _timeid2index(timeid=key, basis=self.start, pyr=self.pyr)
#         # return self.data[key]
#         #
#         # def __setitem__(self, key, value):
#         #
#         # if isinstance(key, tuple):
#         #     key = _timeid2index(timeid=key, basis=self.start, pyr=self.pyr)
#         # self.data[key] = value
#         #
#         # def __len__(self):
#         #     return len(self.data)
#         #
#         # def __iter__(self):
#         #     return self.data.__iter__()
#         #
#         # def __next__(self):
#         # return self.data.__next__()
#         #
#         #
#         # def tolist(self):
#         # """Returns the values as a list"""
#         # return [x for x in self.data]
#         #
#         # def copy(self):
#         # """returns a copy of the time series"""
#         # result = TimeSeries(start=self.start, end=self.end, nper=len(self.data), pyr=self.pyr)
#         # result.data = [value for value in self.data]
#         # return result
#         #
#         #
#         # def cumsum(self):
#         # """returns the cumulative sum of the time series"""
#         # result = TimeSeries(start=self.start, end=self.end, nper=len(self.data), pyr=self.pyr)
#         # result.data = [value for value in self.data]
#         # for index in range(1, len(self.data)):
#         #     result.data[index] += result.data[index - 1]
#         # return result
#         #
#         # #
#         # # mathematical operations
#         # #
#         #
#         # def __abs__(self):
#         # """Returns a new time series computed by applying the `abs` funtion
#         # to the elements of the original time series.
#         #
#         # >>> abs(cashflow(const_value=[-10]*4, pyr=4)) # doctest: +NORMALIZE_WHITESPACE
#         #    Qtr0  Qtr1  Qtr2  Qtr3
#         # 0 10.00 10.00 10.00 10.00
#         #
#         # """
#         # result = self.copy()
#         # for time, _ in enumerate(result.data):
#         #     result[time] = abs(self[time])
#         # return result
#         #
#         # def __add__(self, other):
#         # """Addition
#         #
#         # >>> cashflow(const_value=[1]*4, pyr=4) + cashflow(const_value=[2]*4, pyr=4) # doctest: +NORMALIZE_WHITESPACE
#         #   Qtr0 Qtr1 Qtr2 Qtr3
#         # 0 3.00 3.00 3.00 3.00
#         #
#         # """
#         # if isinstance(other, (int, float)):
#         #     other = [other] * len(self)
#         # else:
#         #     verify_eq_time_range(self, other)
#         # result = self.copy()
#         # for index, _ in enumerate(result.data):
#         #     result[index] += other[index]
#         # return result
#         #
#         #
#         # def __floordiv__(self, other):
#         # """floordiv
#         #
#         # >>> cashflow(const_value=[6]*4, pyr=4) // cashflow(const_value=[4]*4, pyr=4) # doctest: +NORMALIZE_WHITESPACE
#         #   Qtr0 Qtr1 Qtr2 Qtr3
#         # 0 1.00 1.00 1.00 1.00
#         #
#         # """
#         # if isinstance(other, (int, float)):
#         #     other = [other] * len(self)
#         # else:
#         #     verify_eq_time_range(self, other)
#         # result = self.copy()
#         # for index, _ in enumerate(result.data):
#         #     result[index] //= other[index]
#         # return result
#         #
#         #
#         # def __mod__(self, other):
#         # """
#         #
#         # >>> cashflow( const_value=[6]*4, pyr=4) % cashflow( const_value=[4]*4, pyr=4) # doctest: +NORMALIZE_WHITESPACE
#         #   Qtr0 Qtr1 Qtr2 Qtr3
#         # 0 2.00 2.00 2.00 2.00
#         #
#         #
#         # """
#         # if isinstance(other, (int, float)):
#         #     other = [other] * len(self)
#         # else:
#         #     verify_eq_time_range(self, other)
#         # result = self.copy()
#         # for index, _ in enumerate(result.data):
#         #     result[index] %= other[index]
#         # return result
#         #
#         #
#         # def __mul__(self, other):
#         # """multiplication
#         #
#         # >>> cashflow( const_value=[2]*4, pyr=4) * cashflow( const_value=[3]*4, pyr=4) # doctest: +NORMALIZE_WHITESPACE
#         #   Qtr0 Qtr1 Qtr2 Qtr3
#         # 0 6.00 6.00 6.00 6.00
#         #
#         # """
#         # if isinstance(other, (int, float)):
#         #     other = [other] * len(self)
#         # else:
#         #     verify_eq_time_range(self, other)
#         # result = self.copy()
#         # for index, _ in enumerate(result.data):
#         #     result[index] *= other[index]
#         # return result
#         #
#         #
#         # def __sub__(self, other):
#         # """Substraction
#         #
#         # >>> cashflow( const_value=[6]*4, pyr=4) - cashflow( const_value=[4]*4, pyr=4) # doctest: +NORMALIZE_WHITESPACE
#         #   Qtr0 Qtr1 Qtr2 Qtr3
#         # 0 2.00 2.00 2.00 2.00
#         #
#         # """
#         # if isinstance(other, (int, float)):
#         #     other = [other] * len(self)
#         # else:
#         #     verify_eq_time_range(self, other)
#         # result = self.copy()
#         # for index, _ in enumerate(result.data):
#         #     result[index] -= other[index]
#         # return result
#         #
#         #
#         # def __truediv__(self, other):
#         # """
#         #
#         # >>> cashflow(const_value=[6]*4, pyr=4) / cashflow(const_value=[4]*4, pyr=4) # doctest: +NORMALIZE_WHITESPACE
#         #   Qtr0 Qtr1 Qtr2 Qtr3
#         # 0 1.50 1.50 1.50 1.50
#         #
#         # """
#         # if isinstance(other, (int, float)):
#         #     other = [other] * len(self)
#         # else:
#         #     verify_eq_time_range(self, other)
#         # result = self.copy()
#         # for index, _ in enumerate(result.data):
#         #     result[index] /= other[index]
#         # return result
#         #
#         # def __radd__(self, other):
#         # """Reverse add function"""
#         # if other == 0:
#         #     return self
#         # else:
#         #     return self.__add__(other)
#         #
#         #
#         #
#         # #
#         # # operations over sequences
#         # #
#         #
#         # # def append(self, other):
#         # #     """
#         # #
#         # #     # >>> x = TimeSeries(data=[10]*10, start=(2001,))
#         # #     # >>> y = TimeSeries(data=[20]*10, start=(2001,))
#         # #     # >>> x.append(y)
#         # #     # >>> x # doctest: +NORMALIZE_WHITESPACE
#         # #     # Time Series:
#         # #     # Start = (2001,)
#         # #     # End = (2020,)
#         # #     # pyr = 1
#         # #     # Data = (2001,)-(2020,) [20] 10.00
#         # #
#         # #     """
#         # #     if self.pyr != other.pyr:
#         # #         raise ValueError("time series must have the same pyr")
#         # #
#         # #     self.data.extend([x for x in other.data])
#         # #     self.nper = len(self.data)
#         # #     self.end = _float2timeid(_timeid2float(self.start, self.pyr) + (self.nper - 1)/self.pyr, self.pyr)
#         #
#         #
#         #
#         #
#         # #
#         # # inplace operators
#         # #
#         # def __iadd__(self, other):
#         # """
#         #
#         #
#         # >>> x = cashflow( const_value=[2]*4, pyr=4)
#         # >>> x += cashflow( const_value=[3]*4, pyr=4)
#         # >>> x # doctest: +NORMALIZE_WHITESPACE
#         #   Qtr0 Qtr1 Qtr2 Qtr3
#         # 0 5.00 5.00 5.00 5.00
#         #
#         # """
#         # if isinstance(other, (int, float)):
#         #     other = [other] * len(self)
#         # else:
#         #     verify_eq_time_range(self, other)
#         # for index, _ in enumerate(self.data):
#         #     self[index] += other[index]
#         # return self
#         #
#         #
#         #
#         # # def __iconcat__(self, other):
#         # #     """
#         # #     """
#         # #     if self.pyr != other.pyr:
#         # #         raise ValueError("time series must have the same pyr")
#         # #     self.data += other.data
#         # #     self.nper = len(self.data)
#         # #     self.end = _float2timeid(_timeid2float(self.start, self.pyr) + (self.nper - 1)/self.pyr, self.pyr)
#         #
#         # def __ifloordiv__(self, other):
#         # """
#         #
#         # >>> x = cashflow( const_value=[6]*4, pyr=4)
#         # >>> x //= cashflow( const_value=[4]*4, pyr=4)
#         # >>> x # doctest: +NORMALIZE_WHITESPACE
#         #   Qtr0 Qtr1 Qtr2 Qtr3
#         # 0 1.00 1.00 1.00 1.00
#         #
#         # """
#         # if isinstance(other, (int, float)):
#         #     other = [other] * len(self)
#         # else:
#         #     verify_eq_time_range(self, other)
#         # for index, _ in enumerate(self.data):
#         #     self[index] //= other[index]
#         # return self
#         #
#         #
#         #
#         # def __imod__(self, other):
#         # """
#         #
#         # >>> x = cashflow( const_value=[6]*4, pyr=4)
#         # >>> x %= cashflow( const_value=[4]*4, pyr=4)
#         # >>> x # doctest: +NORMALIZE_WHITESPACE
#         #   Qtr0 Qtr1 Qtr2 Qtr3
#         # 0 2.00 2.00 2.00 2.00
#         #
#         # """
#         # if isinstance(other, (int, float)):
#         #     other = [other] * len(self)
#         # else:
#         #     verify_eq_time_range(self, other)
#         # for index, _ in enumerate(self.data):
#         #     self[index] %= other[index]
#         # return self
#         #
#         #
#         #
#         # def __imul__(self, other):
#         # """
#         # >>> x = cashflow( const_value=[2]*4, pyr=4)
#         # >>> x *= cashflow( const_value=[3]*4, pyr=4)
#         # >>> x # doctest: +NORMALIZE_WHITESPACE
#         #   Qtr0 Qtr1 Qtr2 Qtr3
#         # 0 6.00 6.00 6.00 6.00
#         #
#         # """
#         # if isinstance(other, (int, float)):
#         #     other = [other] * len(self)
#         # else:
#         #     verify_eq_time_range(self, other)
#         # for index, _ in enumerate(self.data):
#         #     self[index] *= other[index]
#         # return self
#         #
#         #
#         # def __isub__(self, other):
#         # """
#         #
#         # >>> x = cashflow( const_value=[6]*4, pyr=4)
#         # >>> x -= cashflow( const_value=[4]*4, pyr=4)
#         # >>> x # doctest: +NORMALIZE_WHITESPACE
#         #   Qtr0 Qtr1 Qtr2 Qtr3
#         # 0 2.00 2.00 2.00 2.00
#         #
#         # """
#         # if isinstance(other, (int, float)):
#         #     other = [other] * len(self)
#         # else:
#         #     verify_eq_time_range(self, other)
#         # for index, _ in enumerate(self.data):
#         #     self[index] -= other[index]
#         # return self
#         #
#         #
#         # def __itruediv__(self, other):
#         # """
#         #
#         # >>> x = cashflow( const_value=[6]*4, pyr=4)
#         # >>> x /= cashflow( const_value=[4]*4, pyr=4)
#         # >>> x # doctest: +NORMALIZE_WHITESPACE
#         #   Qtr0 Qtr1 Qtr2 Qtr3
#         # 0 1.50 1.50 1.50 1.50
#         #
#         # """
#         # if isinstance(other, (int, float)):
#         #     other = [other] * len(self)
#         # else:
#         #     verify_eq_time_range(self, other)
#         # for index, _ in enumerate(self.data):
#         #     self[index] /= other[index]
#         # return self
#         #
#         #
#         #
#         #
#         # # def window(self, left=None, right=None):
#         # #     """Returns a sublist"""
#         # #     if left is None:
#         # #         left = 0
#         # #     if right is None:
#         # #         right = len(self.data)
#         # #     return [self.data[t] for t in range(left, right + 1)]
#         #
#         # # def extend(self, left=0, right=0):
#         # #     """extendes the list"""
#         # #     self.data = [0] * left + self.data + [0] * right
#         # #     return self
#         #
#
#
#
# # M - month end frequency
# # SM semi month
# # BM bussines month frequency
# # Q quarters









if __name__ == "__main__":
    import doctest
    doctest.testmod()
