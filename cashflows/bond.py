"""
Bond Valuation
===============================================================================

This module computes the present value or the yield-to-maturity of of the
expected cashflow of a bond. Also,it is possible to make a sensibility analysis
for different values for the yield-to-maturity and one present value of
the bond.

"""

import numpy as np
import pandas as pd

# cashflows.
from cashflows.tvmm import tvmm

def bond(maturity_date=None, freq='A', face_value=None,
         coupon_rate=None, coupon_value=None, num_coupons=None, value=None, ytm=None):
    """

    Examples:

    >>> bond(face_value=1000, coupon_value=56, num_coupons=10, ytm=5.6) # doctest: +ELLIPSIS
    1000.0...

    >>> bond(face_value=1000, coupon_rate=5.6, num_coupons=10, value=1000) # doctest: +ELLIPSIS
    5.6...

    >>> bond(face_value=[1000, 1200, 1400], coupon_value=56, num_coupons=10, value=1000) # doctest: +ELLIPSIS +NORMALIZE_WHITESPACE
       Coupon_Rate  Coupon_Value  Face_Value  Num_Coupons  Value      YTM
    0     5.600000            56        1000           10   1000  5.60000
    1     4.666667            56        1200           10   1000  7.04451
    2     4.000000            56        1400           10   1000  8.31956


    >>> bond(face_value=1000, coupon_value=[56., 57, 58], num_coupons=10, value=1000) # doctest: +ELLIPSIS +NORMALIZE_WHITESPACE
       Coupon_Rate  Coupon_Value  Face_Value  Num_Coupons  Value  YTM
    0          5.6          56.0        1000           10   1000  5.6
    1          5.7          57.0        1000           10   1000  5.7
    2          5.8          58.0        1000           10   1000  5.8


    >>> bond(face_value=1000, coupon_rate=[5.6, 5.7, 5.8], num_coupons=10, value=1000) # doctest: +ELLIPSIS +NORMALIZE_WHITESPACE
       Coupon_Rate  Coupon_Value  Face_Value  Num_Coupons  Value  YTM
    0          5.6          56.0        1000           10   1000  5.6
    1          5.7          57.0        1000           10   1000  5.7
    2          5.8          58.0        1000           10   1000  5.8

    >>> bond(face_value=1000, coupon_rate=5.6, num_coupons=[10, 20, 30], value=1000) # doctest: +ELLIPSIS +NORMALIZE_WHITESPACE
       Coupon_Rate  Coupon_Value  Face_Value  Num_Coupons  Value  YTM
    0          5.6          56.0        1000           10   1000  5.6
    1          5.6          56.0        1000           20   1000  5.6
    2          5.6          56.0        1000           30   1000  5.6


    >>> bond(face_value=1000, coupon_rate=5.6, num_coupons=10, value=[800, 900, 1000]) # doctest: +ELLIPSIS +NORMALIZE_WHITESPACE
       Coupon_Rate  Coupon_Value  Face_Value  Num_Coupons  Value       YTM
    0          5.6          56.0        1000           10    800  8.671484
    1          5.6          56.0        1000           10    900  7.025450
    2          5.6          56.0        1000           10   1000  5.600000

    >>> bond(face_value=[1000, 1100, 1200], coupon_rate=5.6, num_coupons=10, value=[800, 900, 1000]) # doctest: +ELLIPSIS +NORMALIZE_WHITESPACE
       Coupon_Rate  Coupon_Value  Face_Value  Num_Coupons  Value        YTM
    0     5.600000          56.0        1000           10    800   8.671484
    1     5.600000          56.0        1000           10    900   7.025450
    2     5.600000          56.0        1000           10   1000   5.600000
    3     5.090909          56.0        1100           10    800   9.419301
    4     5.090909          56.0        1100           10    900   7.772838
    5     5.090909          56.0        1100           10   1000   6.346424
    6     4.666667          56.0        1200           10    800  10.119360
    7     4.666667          56.0        1200           10    900   8.472129
    8     4.666667          56.0        1200           10   1000   7.044510

    >>> bond(face_value=[1000, 1100, 1200], coupon_rate=[5.6, 5.7, 5.8], num_coupons=10, value=[800, 900, 1000]) # doctest: +ELLIPSIS +NORMALIZE_WHITESPACE
        Coupon_Rate  Coupon_Value  Face_Value  Num_Coupons  Value        YTM
    0      5.600000          56.0        1000           10    800   8.671484
    1      5.600000          56.0        1000           10    900   7.025450
    2      5.600000          56.0        1000           10   1000   5.600000
    3      5.700000          57.0        1000           10    800   8.787284
    4      5.700000          57.0        1000           10    900   7.132508
    5      5.700000          57.0        1000           10   1000   5.700000
    6      5.800000          58.0        1000           10    800   8.903126
    7      5.800000          58.0        1000           10    900   7.239584
    8      5.800000          58.0        1000           10   1000   5.800000
    9      5.090909          56.0        1100           10    800   9.419301
    10     5.090909          56.0        1100           10    900   7.772838
    11     5.090909          56.0        1100           10   1000   6.346424
    12     5.181818          57.0        1100           10    800   9.531367
    13     5.181818          57.0        1100           10    900   7.876353
    14     5.181818          57.0        1100           10   1000   6.443037
    15     5.272727          58.0        1100           10    800   9.643488
    16     5.272727          58.0        1100           10    900   7.979898
    17     5.272727          58.0        1100           10   1000   6.539664
    18     4.666667          56.0        1200           10    800  10.119360
    19     4.666667          56.0        1200           10    900   8.472129
    20     4.666667          56.0        1200           10   1000   7.044510
    21     4.750000          57.0        1200           10    800  10.228122
    22     4.750000          57.0        1200           10    900   8.572512
    23     4.750000          57.0        1200           10   1000   7.138133
    24     4.833333          58.0        1200           10    800  10.336951
    25     4.833333          58.0        1200           10    900   8.672936
    26     4.833333          58.0        1200           10   1000   7.231779

    >>> bond(face_value=1000, coupon_rate=5.6, num_coupons=10, value=1000, ytm=[5.1, 5.6, 6.1]) # doctest: +ELLIPSIS +NORMALIZE_WHITESPACE
       Basis_Value        Change  Coupon_Rate  Coupon_Value  Face_Value  \\
    0         1000  3.842187e+00          5.6          56.0        1000
    1         1000  1.136868e-14          5.6          56.0        1000
    2         1000 -3.662671e+00          5.6          56.0        1000
    <BLANKLINE>
       Num_Coupons        Value  YTM
    0           10  1038.421866  5.1
    1           10  1000.000000  5.6
    2           10   963.373290  6.1


    >>> bond(face_value=1000, coupon_rate=5.6, num_coupons=10, value=[1000, 1100], ytm=[5.1, 5.6, 6.1]) # doctest: +ELLIPSIS +NORMALIZE_WHITESPACE
       Basis_Value        Change  Coupon_Rate  Coupon_Value  Face_Value  \\
    0         1000  3.842187e+00          5.6          56.0        1000
    1         1000  1.136868e-14          5.6          56.0        1000
    2         1000 -3.662671e+00          5.6          56.0        1000
    3         1100 -5.598012e+00          5.6          56.0        1000
    4         1100 -9.090909e+00          5.6          56.0        1000
    5         1100 -1.242061e+01          5.6          56.0        1000
    <BLANKLINE>
       Num_Coupons        Value  YTM
    0           10  1038.421866  5.1
    1           10  1000.000000  5.6
    2           10   963.373290  6.1
    3           10  1038.421866  5.1
    4           10  1000.000000  5.6
    5           10   963.373290  6.1


>>> bond(face_value=1000, coupon_rate=5.6, num_coupons=[20], value=[1000, 1100], ytm=[5.6, 6.1]) # doctest: +ELLIPSIS +NORMALIZE_WHITESPACE
       Basis_Value     Change  Coupon_Rate  Coupon_Value  Face_Value  Num_Coupons  \
    0         1000   0.000000          5.6          56.0        1000           20
    1         1000  -5.688693          5.6          56.0        1000           20
    2         1100  -9.090909          5.6          56.0        1000           20
    3         1100 -14.262448          5.6          56.0        1000           20
    <BLANKLINE>
             Value  YTM
    0  1000.000000  5.6
    1   943.113073  6.1
    2  1000.000000  5.6
    3   943.113073  6.1


    """


    if coupon_rate is None and coupon_value is None:
        raise ValueError('coupon_rate or coupon_value must be specified')

    ## converts params to lists

    if coupon_rate is not None and not isinstance(coupon_rate, list):
            coupon_rate = [coupon_rate]

    if coupon_value is not None and not isinstance(coupon_value, list):
            coupon_value = [coupon_value]

    if not isinstance(num_coupons, list):
        num_coupons = [num_coupons]

    if not isinstance(face_value, list):
        face_value = [face_value]

    if not isinstance(num_coupons, list):
        num_coupons = [num_coupons]

    if ytm is not None and not isinstance(ytm, list):
        ytm = [ytm]

    if value is not None and not isinstance(value, list):
        value = [value]

    result = None
    counter = 0

    ## value is unknown
    if value is None:

        for xface_value in face_value:

            if coupon_value is None:
                coupon_value = [xrate * xface_value / 100 for xrate in coupon_rate]

            for xcoupon_value in coupon_value:
                for xnum_coupons in num_coupons:
                    for xytm in ytm:

                        xvalue = tvmm(pmt=xcoupon_value,
                                      fval=xface_value,
                                      nper=xnum_coupons,
                                      nrate=xytm,
                                      due=0, pyr=1)

                        xcoupon_rate = xcoupon_value / xface_value * 100.0

                        aux = pd.DataFrame({'Face_Value': xface_value,
                                            'Coupon_Value': xcoupon_value,
                                            'Coupon_Rate': xcoupon_rate,
                                            'Num_Coupons':xnum_coupons,
                                            'YTM':xytm,
                                            'Value': -xvalue},
                                            index = [counter])
                        counter += 1

                        if result is None:
                            result = aux
                        else:
                            result = result.append(aux, ignore_index=True)


        if len(result) == 1:
            return np.asscalar(result['Value'])
        return result

    ## ytm is unknown
    if ytm is None:

        for xface_value in face_value:

            if coupon_value is None:
                coupon_value = [xrate * xface_value / 100 for xrate in coupon_rate]

            for xcoupon_value in coupon_value:
                for xnum_coupons in num_coupons:
                    for xvalue in value:

                        xytm = tvmm(pmt=xcoupon_value,
                                     fval=xface_value,
                                     nper=xnum_coupons,
                                     pval=-xvalue,
                                     due=0, pyr=1)

                        xcoupon_rate = xcoupon_value / xface_value * 100.0

                        aux = pd.DataFrame({'Face_Value': xface_value,
                                            'Coupon_Value': xcoupon_value,
                                            'Coupon_Rate': xcoupon_rate,
                                            'Num_Coupons':xnum_coupons,
                                            'YTM':xytm,
                                            'Value': xvalue},
                                            index = [counter])

                        counter += 1

                        if result is None:
                            result = aux
                        else:
                            result = result.append(aux, ignore_index=True)

        if len(result) == 1:
            return np.asscalar(result['YTM'])
        return result



    #
    # value and ytm are not None
    # sensibility analysis
    #

    for basis_value in value:

        for xface_value in face_value:

            if coupon_value is None or coupon_rate is not None:
                coupon_value = [xrate * xface_value / 100 for xrate in coupon_rate]

            for xcoupon_value in coupon_value:
                for xnum_coupons in num_coupons:
                    for xytm in ytm:

                        xvalue = tvmm(pmt=xcoupon_value,
                                      fval=xface_value,
                                      nper=xnum_coupons,
                                      nrate=xytm,
                                      due=0, pyr=1)

                        xcoupon_rate = xcoupon_value / xface_value * 100.0

                        aux = pd.DataFrame({'Coupon_Value': xcoupon_value,
                                            'Coupon_Rate': xcoupon_rate,
                                            'Face_Value': xface_value,
                                            'Num_Coupons':xnum_coupons,
                                            'Basis_Value': basis_value,
                                            'YTM':xytm,
                                            'Value': -xvalue,
                                            'Change': 100 * (-xvalue-basis_value)/basis_value},
                                            index = [counter])

                        counter += 1

                        if result is None:
                            result = aux
                        else:
                            result = result.append(aux, ignore_index=True)


    return result










# def bond(face_value=None, coupon_rate=None, coupon_value=None, num_coupons=None,
#          value=None, ytm=None):
#     """
#
#     Evaluation of bond investments.
#
#     Args:
#        face_value (float): the bond's value-at-maturity.
#        coupon_rate (float): rate for calculate the coupon payment.
#        coupon_value (float): periodic payment.
#        num_coupons (int): number of couont payments before maturity.
#        value (float, list): present value of the bond
#        ytm (float, list): yield-to-maturity.
#
#
#     Returns:
#         None, a float value, or a list of float values:
#         * `value`: when `ytm` is specified.
#         * `ytm`:  when `value` is specified.
#         * `None`: when `ytm` and `value` are specified. Prints a sensibility table.
#
#     When `coupon_rate` is defined, `coupon_value` is calculated automaticly.
#
#
#     Examples:
#
#     >>> bond(face_value=1000, coupon_value=56, num_coupons=10, ytm=5.6) # doctest: +ELLIPSIS
#     1000.0...
#
#     >>> bond(face_value=1000, coupon_rate=5.6, num_coupons=10, value=1000) # doctest: +ELLIPSIS
#     5.6...
#
#
#     Also, it is possible to make sensibility analysis for bond's data. In the
#     following case, the present value of the bond is calculated for various
#     values of the yield-to-maturity.
#
#     >>> bond(face_value=1000, coupon_rate=5.6, num_coupons=10,
#     ... ytm=[4.0, 5.0, 5.6, 6.0, 7.0]) # doctest: +ELLIPSIS
#     [1129.77..., 1046.33..., 1000.0..., 970.55..., 901.66...]
#
#
#     And for different values:
#
#     >>> bond(face_value=1000, coupon_rate=5.6, num_coupons=10,
#     ... value=[900, 1000, 1100]) # doctest: +ELLIPSIS
#     [7.0..., 5.6..., 4.3...]
#
#     When values for the yield-to-maturity and one value for present value of
#     the bond are supplied, the function prints a report.
#
#     >>> bond(face_value=1000, coupon_rate=5.6, num_coupons=10,
#     ... ytm=[4.0, 5.0, 5.6, 6.0, 7.0], value=1000) # doctest: +ELLIPSIS +NORMALIZE_WHITESPACE
#     Bond valuation analysis
#     Reference price: 1000
#     Analysis:
#               Yield     Value Change
#                 (%)       ($)    (%)
#              ------------------------
#                4.00   1129.77  12.98
#                5.00   1046.33   4.63
#                5.60   1000.00   0.00
#                6.00    970.56  -2.94
#                7.00    901.67  -9.83
#
#
#     """
#
#
#     if coupon_rate is None and coupon_value is None:
#         raise ValueError('coupon_rate or coupon_value must be specified')
#
#     if coupon_rate is None:
#         coupon_rate = coupon_value / face_value
#
#     if coupon_value is None:
#         coupon_value = coupon_rate * face_value / 100
#
#     if value is None:
#         value = tvmm(pmt=coupon_value, fval=face_value,
#                      nper=num_coupons, nrate=ytm, due=0, pyr=1)
#         if isinstance(value, list):
#             value = [-x for x in value]
#         else:
#             value = -value
#         return value
#
#     if ytm is None:
#         if isinstance(value, list):
#             value = [-x for x in value]
#         else:
#             value = -value
#         return tvmm(pmt=coupon_value, fval=face_value, pval=value, nper=num_coupons, pyr=1)
#
#     #
#     # value and ytm are not None
#     # sensibility analysis
#     #
#
#     values = tvmm(pmt=coupon_value, fval=face_value,
#                   nper=num_coupons, nrate=ytm, due=0, pyr=1)
#     if isinstance(values, list):
#         values = [-x for x in values]
#     else:
#         values = -values
#
#     txt = ['Bond valuation analysis']
#     txt += ['Reference price: ' + value.__str__()]
#     txt += ['Analysis:']
#     txt += ['           Yield     Value Change']
#     txt += ['             (%)       ($)    (%)']
#     txt += ['          ------------------------']
#
#
#     if not isinstance(ytm, list):
#         ytm = [ytm]
#         values = [values]
#     for iytm, ivalue in zip(ytm, values):
#         fmt = '          {:6.2f} {:9.2f} {:6.2f}'
#         txt += [fmt.format(iytm, ivalue, 100 * (ivalue-value)/value)]
#
#     print('\n'.join(txt))




if __name__ == "__main__":
    import doctest
    doctest.testmod()
