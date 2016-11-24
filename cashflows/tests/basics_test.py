"""Time Value of Money Models

"""

# import os
# import sys
import unittest
import numpy as np

from cashflows.basics import iconv

# from cashflows.basics import compound


class BasicsTestCase(unittest.TestCase):
    """Testing basic financial calculations"""
    pass
    #def setUp(self):
    #    self.tvm = Widget('The widget')

    #def tearDown(self):
    #    self.widget.dispose()

    # def test_compound_simple(self):
    #     """Test compound calculations over numbers"""
    #     pval = -729.88
    #     rate = 0.065
    #     fval = 1000.0
    #     nper = 5
    #     self.assertAlmostEqual(tvmm(pval=pval, nomrate=rate, nper=5),
    #                            fval, delta=0.01)
    #     self.assertAlmostEqual(tvmm(fval=fval, nomrate=rate, nper=5),
    #                            pval, delta=0.01)
    #     self.assertAlmostEqual(tvmm(pval=pval, fval=fval, nper=5),
    #                            rate, delta=0.01)
    #     self.assertAlmostEqual(tvmm(pval=pval, nomrate=rate, fval=fval),
    #                            nper, delta=0.01)


class RateProc_TestCase(unittest.TestCase):
    """Test of rate conversions"""

    def test_rate1(self):
        # data
        nrate = [float(12)] * 3
        erate = [100*((1.01)**12-1)] * 3
        prate = [float(1)] * 3

        # case 1
        (xnrate, xprate) = iconv(erate=erate, pyr=12)
        np.testing.assert_almost_equal(xnrate, nrate)
        np.testing.assert_almost_equal(xprate, prate)

        # case 2
        (xerate, xprate) = iconv(nrate=nrate, pyr=12)
        np.testing.assert_almost_equal(xerate, erate)
        np.testing.assert_almost_equal(xprate, prate)

        # case 3
        (xnrate, xerate) = iconv(prate=prate, pyr=12)
        np.testing.assert_almost_equal(xnrate, nrate)
        np.testing.assert_almost_equal(xerate, erate)




if __name__ == '__main__':
    unittest.main()
