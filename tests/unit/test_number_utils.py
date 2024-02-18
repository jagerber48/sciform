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
