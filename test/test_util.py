from unittest import TestCase
from util import *

class TestUtil(TestCase):
    def test_linear(self):
        self.assertAlmostEqual(linear(0, 1, 0.5), 0.5)
        self.assertAlmostEqual(
            linear([0, 0], [1, 1], 0.7), [0.7, 0.7]
        )
        self.assertAlmostEqual(linear(-2, 2, 0.5), 0)

    def test_linear_2D(self):
        lin = linear([521, 799], [795, 987], 0.2)
        self.assertIsInstance(lin, list)
        self.assertAlmostEqual(lin[0], 575.8)
        self.assertAlmostEqual(lin[1], 836.6)