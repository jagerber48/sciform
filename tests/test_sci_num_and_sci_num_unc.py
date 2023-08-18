import unittest

from sciform import SciNum, SciNumUnc


class TestSciNumAndSciNumUnc(unittest.TestCase):
    def test_sci_num_repr(self):
        self.assertEqual(repr(SciNum(123.456)), 'SciNum(123.456)')

    def test_sci_num_unc_repr(self):
        self.assertEqual(
            repr(SciNumUnc(123.456, 0.0000023)),
            'SciNumUnc(123.456, 0.0000023)')
