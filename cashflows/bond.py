"""
Bond Valuation
===============================================================================

This module computes the present value or the yield-to-maturity of of the
expected cashflow of a bond. Also,it is possible to make a sensibility analysis
for different values for the yield-to-maturity and one present value of
the bond.

"""

from cashflows.tvmm import tvmm

def bond(face_value=None, coupon_rate=None, coupon_value=None, num_coupons=None,
         value=None, ytm=None):
    """

    Evaluation of bond investments.

    Args:
       face_value (float): the bond's value-at-maturity.
       coupon_rate (float): rate for calculate the coupon payment.
       coupon_value (float): periodic payment.
       num_coupons (int): number of couont payments before maturity.
       value (float, list): present value of the bond
       ytm (float, list): yield-to-maturity.


    Returns:
        None, a float value, or a list of float values:
        * `value`: when `ytm` is specified.
        * `ytm`:  when `value` is specified.
        * `None`: when `ytm` and `value` are specified. Prints a sensibility table.

    When `coupon_rate` is defined, `coupon_value` is calculated automaticly.


    Examples:

    >>> bond(face_value=1000, coupon_value=56, num_coupons=10, ytm=5.6) # doctest: +ELLIPSIS
    1000.0...

    >>> bond(face_value=1000, coupon_rate=5.6, num_coupons=10, value=1000) # doctest: +ELLIPSIS
    5.6...


    Also, it is possible to make sensibility analysis for bond's data. In the
    following case, the present value of the bond is calculated for various
    values of the yield-to-maturity.

    >>> bond(face_value=1000, coupon_rate=5.6, num_coupons=10,
    ... ytm=[4.0, 5.0, 5.6, 6.0, 7.0]) # doctest: +ELLIPSIS
    [1129.77..., 1046.33..., 1000.0..., 970.55..., 901.66...]


    And for different values:

    >>> bond(face_value=1000, coupon_rate=5.6, num_coupons=10,
    ... value=[900, 1000, 1100]) # doctest: +ELLIPSIS
    [7.0..., 5.6..., 4.3...]

    When values for the yield-to-maturity and one value for present value of
    the bond are supplied, the function prints a report.

    >>> bond(face_value=1000, coupon_rate=5.6, num_coupons=10,
    ... ytm=[4.0, 5.0, 5.6, 6.0, 7.0], value=1000) # doctest: +ELLIPSIS +NORMALIZE_WHITESPACE
    Bond valuation analysis
    Reference price: 1000
    Analysis:
              Yield     Value Change
                (%)       ($)    (%)
             ------------------------
               4.00   1129.77  12.98
               5.00   1046.33   4.63
               5.60   1000.00   0.00
               6.00    970.56  -2.94
               7.00    901.67  -9.83


    """


    if coupon_rate is None and coupon_value is None:
        raise ValueError('coupon_rate or coupon_value must be specified')

    if coupon_rate is None:
        coupon_rate = coupon_value / face_value

    if coupon_value is None:
        coupon_value = coupon_rate * face_value / 100

    if value is None:
        value = tvmm(pmt=coupon_value, fval=face_value,
                     nper=num_coupons, nrate=ytm, due=0, pyr=1)
        if isinstance(value, list):
            value = [-x for x in value]
        else:
            value = -value
        return value

    if ytm is None:
        if isinstance(value, list):
            value = [-x for x in value]
        else:
            value = -value
        return tvmm(pmt=coupon_value, fval=face_value, pval=value, nper=num_coupons, pyr=1)

    #
    # value and ytm are not None
    # sensibility analysis
    #

    values = tvmm(pmt=coupon_value, fval=face_value,
                  nper=num_coupons, nrate=ytm, due=0, pyr=1)
    if isinstance(values, list):
        values = [-x for x in values]
    else:
        values = -values

    txt = ['Bond valuation analysis']
    txt += ['Reference price: ' + value.__str__()]
    txt += ['Analysis:']
    txt += ['           Yield     Value Change']
    txt += ['             (%)       ($)    (%)']
    txt += ['          ------------------------']


    if not isinstance(ytm, list):
        ytm = [ytm]
        values = [values]
    for iytm, ivalue in zip(ytm, values):
        fmt = '          {:6.2f} {:9.2f} {:6.2f}'
        txt += [fmt.format(iytm, ivalue, 100 * (ivalue-value)/value)]

    print('\n'.join(txt))




if __name__ == "__main__":
    import doctest
    doctest.testmod()
