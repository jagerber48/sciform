from __future__ import annotations

import unittest
from decimal import Decimal

from sciform import AutoExpVal
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
        cases: list[tuple[Decimal, int]] = [
            # Unnormalized:
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
            # Normalized:
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

    def test_get_val_unc_top_dec_place(self):
        cases: list[tuple[tuple[Decimal, Decimal, int], int]] = [
            ((Decimal("123"), Decimal("0.456"), 0), 0),
            ((Decimal("123"), Decimal("0.456"), 1), 1),
            ((Decimal("123"), Decimal("0.456"), 2), 2),
            ((Decimal("123"), Decimal("0.456"), 3), 3),
            ((Decimal("123"), Decimal("0.456"), 4), 4),
            ((Decimal("123"), Decimal("0.456"), 5), 5),
            ((Decimal("123"), Decimal("0.456"), 6), 6),
            ((Decimal("0.456"), Decimal("123"), 0), 0),
            ((Decimal("0.456"), Decimal("123"), 1), 1),
            ((Decimal("0.456"), Decimal("123"), 2), 2),
            ((Decimal("0.456"), Decimal("123"), 3), 3),
            ((Decimal("0.456"), Decimal("123"), 4), 4),
            ((Decimal("0.456"), Decimal("123"), 5), 5),
            ((Decimal("0.456"), Decimal("123"), 6), 6),
            ((Decimal("0.000123"), Decimal("0.000000456"), -1), 0),
            ((Decimal("0.000000456"), Decimal("0.000123"), -1), 0),
        ]

        left_pad_matching = False
        for (val, unc, input_top_dec_place), expected_output in cases:
            actual_output = numbers.get_val_unc_top_dec_place(
                val_mantissa=val,
                unc_mantissa=unc,
                input_top_dec_place=input_top_dec_place,
                left_pad_matching=left_pad_matching,
            )
            with self.subTest(
                val_mantissa=val,
                unc_mantissa=unc,
                input_top_dec_place=input_top_dec_place,
                left_pad_matching=left_pad_matching,
                expected_output=expected_output,
                actual_output=actual_output,
            ):
                self.assertEqual(expected_output, actual_output)

    def test_get_val_unc_top_dec_place_left_pad_match(self):
        cases: list[tuple[tuple[Decimal, Decimal, int], int]] = [
            ((Decimal("123"), Decimal("0.456"), 0), 2),
            ((Decimal("123"), Decimal("0.456"), 1), 2),
            ((Decimal("123"), Decimal("0.456"), 2), 2),
            ((Decimal("123"), Decimal("0.456"), 3), 3),
            ((Decimal("123"), Decimal("0.456"), 4), 4),
            ((Decimal("123"), Decimal("0.456"), 5), 5),
            ((Decimal("123"), Decimal("0.456"), 6), 6),
            ((Decimal("0.456"), Decimal("123"), 0), 2),
            ((Decimal("0.456"), Decimal("123"), 1), 2),
            ((Decimal("0.456"), Decimal("123"), 2), 2),
            ((Decimal("0.456"), Decimal("123"), 3), 3),
            ((Decimal("0.456"), Decimal("123"), 4), 4),
            ((Decimal("0.456"), Decimal("123"), 5), 5),
            ((Decimal("0.456"), Decimal("123"), 6), 6),
            ((Decimal("0.000123"), Decimal("0.000000456"), -1), 0),
            ((Decimal("0.000000456"), Decimal("0.000123"), -1), 0),
        ]

        left_pad_matching = True
        for (val, unc, input_top_dec_place), expected_output in cases:
            actual_output = numbers.get_val_unc_top_dec_place(
                val_mantissa=val,
                unc_mantissa=unc,
                input_top_dec_place=input_top_dec_place,
                left_pad_matching=left_pad_matching,
            )
            with self.subTest(
                val_mantissa=val,
                unc_mantissa=unc,
                input_top_dec_place=input_top_dec_place,
                left_pad_matching=left_pad_matching,
                expected_output=expected_output,
                actual_output=actual_output,
            ):
                self.assertEqual(expected_output, actual_output)

    def test_get_fixed_exp(self):
        self.assertEqual(0, numbers.get_fixed_exp(0))
        self.assertEqual(0, numbers.get_fixed_exp(AutoExpVal))
        self.assertRaises(
            ValueError,
            numbers.get_fixed_exp,
            3
        )

    def test_get_scientific_exp(self):
        cases: list[tuple[tuple[Decimal, int | type(AutoExpVal)], int]] = [
            ((Decimal("1000000"), AutoExpVal), 6),
            ((Decimal("100000"), AutoExpVal), 5),
            ((Decimal("10000"), AutoExpVal), 4),
            ((Decimal("1000"), AutoExpVal), 3),
            ((Decimal("100"), AutoExpVal), 2),
            ((Decimal("10"), AutoExpVal), 1),
            ((Decimal("1"), AutoExpVal), 0),
            ((Decimal("0.1"), AutoExpVal), -1),
            ((Decimal("0.01"), AutoExpVal), -2),
            ((Decimal("0.001"), AutoExpVal), -3),
            ((Decimal("0.0001"), AutoExpVal), -4),
            ((Decimal("0.00001"), AutoExpVal), -5),
            ((Decimal("0.000001"), AutoExpVal), -6),
            ((Decimal("1000000"), 3), 3),
            ((Decimal("100000"), 3), 3),
            ((Decimal("10000"), 3), 3),
            ((Decimal("1000"), 3), 3),
            ((Decimal("100"), 3), 3),
            ((Decimal("10"), 3), 3),
            ((Decimal("1"), 3), 3),
            ((Decimal("0.1"), 3), 3),
            ((Decimal("0.01"), 3), 3),
            ((Decimal("0.001"), 3), 3),
            ((Decimal("0.0001"), 3), 3),
            ((Decimal("0.00001"), 3), 3),
            ((Decimal("0.000001"), 3), 3),
        ]

        for (number, input_exp), expected_output in cases:
            actual_output = numbers.get_scientific_exp(
                number,
                input_exp,
            )
            with self.subTest(
                number=number,
                input_exp=input_exp,
                expected_output=expected_output,
                actual_output=actual_output,
            ):
                self.assertEqual(expected_output, actual_output)
