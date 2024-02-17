import unittest
from typing import get_args

from sciform.options import option_types


class TestInvalidOptions(unittest.TestCase):
    def test_left_pad_char_strings(self):
        self.assertEqual(
            set(get_args(option_types.LeftPadChar)),
            set(option_types.LeftPadCharEnum),
        )

    def test_sign_mode_strings(self):
        self.assertEqual(
            set(get_args(option_types.SignMode)),
            set(option_types.SignModeEnum),
        )

    def test_round_mode_strings(self):
        self.assertEqual(
            set(get_args(option_types.RoundMode)),
            set(option_types.RoundModeEnum),
        )

    def test_exp_mode_strings(self):
        self.assertEqual(
            set(get_args(option_types.ExpMode)),
            set(option_types.ExpModeEnum),
        )

    def test_exp_format_strings(self):
        self.assertEqual(
            set(get_args(option_types.ExpFormat)),
            set(option_types.ExpFormatEnum),
        )

    def test_separator_strings(self):
        self.assertEqual(
            set(get_args(option_types.UpperSeparators)),
            set(option_types.SeparatorEnum),
        )

    def test_upper_separator_strings(self):
        self.assertEqual(
            set(get_args(option_types.UpperSeparators)),
            set(get_args(option_types.UpperSeparatorEnums)),
        )

    def test_decimal_separator_strings(self):
        self.assertEqual(
            set(get_args(option_types.DecimalSeparators)),
            set(get_args(option_types.DecimalSeparatorEnums)),
        )

    def test_lower_separator_strings(self):
        self.assertEqual(
            set(get_args(option_types.LowerSeparators)),
            set(get_args(option_types.LowerSeparatorEnums)),
        )
