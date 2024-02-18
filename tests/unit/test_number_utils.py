import unittest
from decimal import Decimal

from sciform.format_utils import numbers


class TestNumberUtils(unittest.TestCase):
    def test_get_top_dec_place(self):
        cases = [
            (Decimal("1e-20"), -20),
            (Decimal("1e-06"), -6),
            (Decimal("1e-05"), -5),
            (Decimal("1e-04"), -4),
            (Decimal("1e-03"), -3),
            (Decimal("1e-02"), -2),
            (Decimal("1e-01"), -1),
            (Decimal("1e00"), 0),
            (Decimal("1e+01"), 1),
            (Decimal("1e+02"), 2),
            (Decimal("1e+03"), 3),
            (Decimal("1e+04"), 4),
            (Decimal("1e+05"), 5),
            (Decimal("1e+06"), 6),
            (Decimal("1e+20"), 20),
        ]

        for number, expected_output in cases:
            actual_output = numbers.get_top_dec_place(number)
            with self.subTest(
                number=number,
                expected_output=expected_output,
                actual_output=actual_output,
            ):
                self.assertEqual(
                    expected_output,
                    actual_output,
                )

    def test_get_bottom_dec_place(self):
        cases = [
            (Decimal("10000000.0000001"), -7),
            (Decimal("10000000.0000010"), -6),
            (Decimal("10000000.0000100"), -5),
            (Decimal("10000000.0001000"), -4),
            (Decimal("10000000.0010000"), -3),
            (Decimal("10000000.0100000"), -2),
            (Decimal("10000000.1000000"), -1),
            (Decimal("10000001.0000000"), 0),
            (Decimal("10000010.0000000"), +1),
            (Decimal("10000100.0000000"), +2),
            (Decimal("10001000.0000000"), +3),
            (Decimal("10010000.0000000"), +4),
            (Decimal("10100000.0000000"), +5),
            (Decimal("11000000.0000000"), +6),
            (Decimal("10000000.0000000"), +7),
            (Decimal("1.000001"), -6),
            (Decimal("1.00001"), -5),
            (Decimal("1.0001"), -4),
            (Decimal("1.001"), -3),
            (Decimal("1.01"), -2),
            (Decimal("1.1"), -1),
            (Decimal("1"), 0),
            (Decimal("1000001E+1"), +1),
            (Decimal("100001E+2"), +2),
            (Decimal("10001E+3"), +3),
            (Decimal("1001E+4"), +4),
            (Decimal("101E+5"), +5),
            (Decimal("11E+6"), +6),
            (Decimal("1E+7"), +7),
        ]

        for number, expected_output in cases:
            actual_output = numbers.get_bottom_dec_place(number)
            with self.subTest(
                number=number,
                expected_output=expected_output,
                actual_output=actual_output,
            ):
                self.assertEqual(
                    expected_output,
                    actual_output,
                )
