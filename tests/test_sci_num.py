import unittest

from sciform import SciNum


class TestSciNum(unittest.TestCase):
    def test_sci_num_repr(self):
        self.assertEqual(repr(SciNum(123.456)), "SciNum(123.456)")

    def test_sci_num_unc_repr(self):
        self.assertEqual(
            repr(SciNum(123.456, 0.0000023)),
            "SciNum(123.456, 0.0000023)",
        )

    def test_double_uncertainty_input(self):
        self.assertRaises(
            ValueError,
            SciNum,
            "1 +/- 2",
            2,
        )
