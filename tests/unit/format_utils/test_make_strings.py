from __future__ import annotations

import unittest
from decimal import Decimal
from typing import Any, Tuple

from sciform.format_utils import make_strings
from sciform.options.option_types import SignModeEnum

ConstructNumStrCase = Tuple[
    Tuple[Decimal, int, int, SignModeEnum, str],
    str,
]


class TestMakeStrings(unittest.TestCase):
    def test_get_sign_str(self):
        cases: list[tuple[tuple[Decimal, SignModeEnum], str]] = [
            ((Decimal("inf"), SignModeEnum.NEGATIVE), ""),
            ((Decimal("1"), SignModeEnum.NEGATIVE), ""),
            ((Decimal("-1"), SignModeEnum.NEGATIVE), "-"),
            ((Decimal("-inf"), SignModeEnum.NEGATIVE), "-"),
            ((Decimal("0"), SignModeEnum.NEGATIVE), ""),
            ((Decimal("nan"), SignModeEnum.NEGATIVE), ""),
            ((Decimal("inf"), SignModeEnum.ALWAYS), "+"),
            ((Decimal("1"), SignModeEnum.ALWAYS), "+"),
            ((Decimal("-1"), SignModeEnum.ALWAYS), "-"),
            ((Decimal("-inf"), SignModeEnum.ALWAYS), "-"),
            ((Decimal("0"), SignModeEnum.ALWAYS), " "),
            ((Decimal("nan"), SignModeEnum.ALWAYS), " "),
            ((Decimal("inf"), SignModeEnum.SPACE), " "),
            ((Decimal("1"), SignModeEnum.SPACE), " "),
            ((Decimal("-1"), SignModeEnum.SPACE), "-"),
            ((Decimal("-inf"), SignModeEnum.SPACE), "-"),
            ((Decimal("0"), SignModeEnum.SPACE), " "),
            ((Decimal("nan"), SignModeEnum.SPACE), " "),
        ]

        for (num, sign_mode), expected_output in cases:
            kwargs = {"num": num, "sign_mode": sign_mode}
            with self.subTest(**kwargs):
                actual_output = make_strings.get_sign_str(**kwargs)
                self.assertEqual(expected_output, actual_output)

    def test_get_sign_str_invalid(self):
        self.assertRaises(
            ValueError,
            make_strings.get_sign_str,
            Decimal("1.0"),
            "+",
        )

    def test_get_pad_str(self):
        cases: list[tuple[tuple[str, int, int], str]] = [
            (("0", 3, 0), ""),
            (("0", 3, 1), ""),
            (("0", 3, 2), ""),
            (("0", 3, 3), ""),
            (("0", 3, 4), "0"),
            (("0", 3, 5), "00"),
            (("0", 3, 6), "000"),
            ((" ", 3, 0), ""),
            ((" ", 3, 1), ""),
            ((" ", 3, 2), ""),
            ((" ", 3, 3), ""),
            ((" ", 3, 4), " "),
            ((" ", 3, 5), "  "),
            ((" ", 3, 6), "   "),
        ]

        for input_options, expected_output in cases:
            left_pad_char, top_dec_place, top_padded_dec_place = input_options
            kwargs = {
                "left_pad_char": left_pad_char,
                "top_dec_place": top_dec_place,
                "top_padded_dec_place": top_padded_dec_place,
            }
            with self.subTest(**kwargs):
                actual_output = make_strings.get_pad_str(**kwargs)
                self.assertEqual(expected_output, actual_output)

    def test_get_abs_num_str_by_bottom_dec_place(self):
        cases: list[tuple[tuple[Decimal, int], str]] = [
            ((Decimal("123456.654"), 2), "123457"),
            ((Decimal("123456.654"), 1), "123457"),
            ((Decimal("123456.654"), 0), "123457"),
            ((Decimal("123456.654"), -1), "123456.7"),
            ((Decimal("123456.654"), -2), "123456.65"),
            ((Decimal("123456.654"), -3), "123456.654"),
            ((Decimal("123456.654"), -4), "123456.6540"),
            ((Decimal("123456.654"), -5), "123456.65400"),
        ]

        for (num, target_bottom_dec_place), expected_output in cases:
            kwargs = {
                "num": num,
                "target_bottom_dec_place": target_bottom_dec_place,
            }
            with self.subTest(**kwargs):
                actual_output = make_strings.get_abs_num_str_by_bottom_dec_place(
                    **kwargs,
                )
                self.assertEqual(expected_output, actual_output)

    def test_construct_num_str(self):
        cases: list[ConstructNumStrCase] = [
            (
                (Decimal("1"), 3, -3, SignModeEnum.ALWAYS, "0"),
                "+0001.000",
            ),
            (
                (Decimal("1"), 3, -3, SignModeEnum.SPACE, "0"),
                " 0001.000",
            ),
            (
                (Decimal("1"), 3, -3, SignModeEnum.SPACE, " "),
                "    1.000",
            ),
        ]

        for input_options, expected_output in cases:
            (
                num,
                target_top_dec_place,
                target_bottom_dec_place,
                sign_mode,
                left_pad_char,
            ) = input_options
            kwargs = {
                "num": num,
                "target_top_dec_place": target_top_dec_place,
                "target_bottom_dec_place": target_bottom_dec_place,
                "sign_mode": sign_mode,
                "left_pad_char": left_pad_char,
            }
            with self.subTest(**kwargs):
                actual_output = make_strings.construct_num_str(**kwargs)
                self.assertEqual(expected_output, actual_output)

    def test_construct_val_unc_str(self):
        cases: list[tuple[dict[str, Any], str]] = [
            (
                {
                    "val_mantissa_str": "123.456",
                    "unc_mantissa_str": "0.123",
                    "decimal_separator": ".",
                    "paren_uncertainty": False,
                    "pm_whitespace": True,
                    "paren_uncertainty_trim": False,
                },
                "123.456 ± 0.123",
            ),
            (
                {
                    "val_mantissa_str": "123.456",
                    "unc_mantissa_str": "0.123",
                    "decimal_separator": ".",
                    "paren_uncertainty": False,
                    "pm_whitespace": False,
                    "paren_uncertainty_trim": False,
                },
                "123.456±0.123",
            ),
            (
                {
                    "val_mantissa_str": "123,456",
                    "unc_mantissa_str": "0,123",
                    "decimal_separator": ",",
                    "paren_uncertainty": False,
                    "pm_whitespace": True,
                    "paren_uncertainty_trim": False,
                },
                "123,456 ± 0,123",
            ),
            (
                {
                    "val_mantissa_str": "123.456",
                    "unc_mantissa_str": "0.123",
                    "decimal_separator": ".",
                    "paren_uncertainty": False,
                    "pm_whitespace": True,
                    "paren_uncertainty_trim": False,
                },
                "123.456 ± 0.123",
            ),
            (
                {
                    "val_mantissa_str": "123,456",
                    "unc_mantissa_str": "0,123",
                    "decimal_separator": ",",
                    "paren_uncertainty": True,
                    "pm_whitespace": True,
                    "paren_uncertainty_trim": False,
                },
                "123,456(0,123)",
            ),
            (
                {
                    "val_mantissa_str": "123,456",
                    "unc_mantissa_str": "0,123",
                    "decimal_separator": ",",
                    "paren_uncertainty": True,
                    "pm_whitespace": True,
                    "paren_uncertainty_trim": True,
                },
                "123,456(123)",
            ),
            (
                {
                    "val_mantissa_str": "123,456,789.123_456",
                    "unc_mantissa_str": "0.123_456",
                    "decimal_separator": ",",
                    "paren_uncertainty": True,
                    "pm_whitespace": True,
                    "paren_uncertainty_trim": False,
                },
                "123,456,789.123_456(0.123_456)",
            ),
            (
                {
                    "val_mantissa_str": "123,456,789.123_456",
                    "unc_mantissa_str": "0.123_456",
                    "decimal_separator": ".",
                    "paren_uncertainty": True,
                    "pm_whitespace": True,
                    "paren_uncertainty_trim": True,
                },
                "123,456,789.123_456(123456)",
            ),
            (
                {
                    "val_mantissa_str": "0.123",
                    "unc_mantissa_str": "123,456.456",
                    "decimal_separator": ",",
                    "paren_uncertainty": True,
                    "pm_whitespace": True,
                    "paren_uncertainty_trim": True,
                },
                "0.123(123,456.456)",
            ),
        ]

        for kwargs, expected_output in cases:
            with self.subTest(**kwargs):
                actual_output = make_strings.construct_val_unc_str(**kwargs)
                self.assertEqual(expected_output, actual_output)

    def test_construct_val_unc_exp_str(self):
        cases: list[tuple[tuple[str, str, bool], str]] = [
            (("123 ± 12", "", False), "123 ± 12"),
            (("123 ± 12", "e+04", False), "(123 ± 12)e+04"),
            (("123(12)", "e+04", True), "123(12)e+04"),
        ]

        for (val_unc_str, exp_str, paren_uncertainty), expected_output in cases:
            kwargs = {
                "val_unc_str": val_unc_str,
                "exp_str": exp_str,
                "paren_uncertainty": paren_uncertainty,
            }
            with self.subTest(**kwargs):
                actual_output = make_strings.construct_val_unc_exp_str(
                    val_unc_str=val_unc_str,
                    exp_str=exp_str,
                    paren_uncertainty=paren_uncertainty,
                )
                self.assertEqual(expected_output, actual_output)
