"""
Project cashflow computation
===============================================================================

"""

# from cashflows.gtimeseries import *
# from cashflows.taxing import *
#
# def prjcashflow(totrev, invest, totexp, totint, ppal, tax_rate, depreciation, salvalue):
#     """Computes the net cashflow of a investment project.
#
#     Args:
#       totrev (TimeSeries): Total revenue.
#       invest (TimeSeries): Total investment costs
#       totexp (TimeSeries): Total expenses
#       totint (TimeSeries): Total payment interests
#       tax_rate (TimeSeries): Tax rate per period
#       ppal (TimeSeries): Principal payments
#       depreciation (TimeSeries): Total depreciation per period.
#       salvalue (TimeSeries): Salvament value per period as percentage.
#
#     Returns:
#       Project cashflow (TimeSeries)
#
#
#     **Example**
#
#     >>> totrev       = cashflow(const_value=[200, 100, 100, 100, 100, 100])
#     >>> invest       = cashflow(const_value=[400,   0,   0,   0,   0,   0])
#     >>> totexp       = cashflow(const_value=[  0,  30,  30,  30,  30,  30])
#     >>> totint       = cashflow(const_value=[  0,   5,   5,   5,   5,   5])
#     >>> tax_rate     = cashflow(const_value=[  0,  30,  30,  30,  30,  30])
#     >>> ppal         = cashflow(const_value=[  0,  30,  30,  30,  30,  30])
#     >>> depreciation = cashflow(const_value=[  0,  15,  15,  15,  15,  15])
#     >>> salvalue     = cashflow(const_value=[  0,   0,   0,   0,   0,  50])
#     >>> prjcashflow(totrev, invest, totexp, totint, ppal, tax_rate, depreciation, salvalue) # doctest: +NORMALIZE_WHITESPACE
#     (Time Series:
#     Start = (0,)
#     End = (5,)
#     pyr = 1
#     Data = (0,)           0.00
#            (1,)-(5,) [5] 15.00
#     , Time Series:
#     Start = (0,)
#     End = (5,)
#     pyr = 1
#     Data = (0,)          -200.00
#     (1,)-(5,) [5]   20.00
#        )
#
#     """
#
#     if not isinstance(totrev, TimeSeries):
#         raise TypeError("totrev must be a TimeSeries object")
#
#     if not isinstance(invest, TimeSeries):
#         raise TypeError("invest must be a TimeSeries object")
#
#     if not isinstance(totexp, TimeSeries):
#         raise TypeError("totexp must be a TimeSeries object")
#
#     if not isinstance(totint, TimeSeries):
#         raise TypeError("totexp must be a TimeSeries object")
#
#     if not isinstance(tax_rate, TimeSeries):
#         raise TypeError("tax_rate must be a TimeSeries object")
#
#     if not isinstance(ppal, TimeSeries):
#         raise TypeError("ppal must be a TimeSeries object")
#
#     if not isinstance(depreciation, TimeSeries):
#         raise TypeError("depreciation must be a TimeSeries object")
#
#     if not isinstance(salvalue, TimeSeries):
#         raise TypeError("salvalue must be a TimeSeries object")
#
#     verify_eq_time_range(totrev, invest)
#     verify_eq_time_range(totrev, totexp)
#     verify_eq_time_range(totrev, tax_rate)
#     verify_eq_time_range(totrev, totint)
#     verify_eq_time_range(totrev, salvalue)
#     verify_eq_time_range(totrev, ppal)
#
#
#     cflo = totrev - invest - totexp - totint - depreciation + invest * salvalue
#
#     taxes = after_tax_cashflow(cflo = cflo, tax_rate = tax_rate)
#
#     before_tax_cflo = cflo + depreciation - ppal
#     after_tax_cflo = before_tax_cflo - taxes
#
#     return (taxes, after_tax_cflo)
