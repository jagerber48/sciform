import unittest
from typing import get_args

from sciform import modes


class TestInvalidOptions(unittest.TestCase):
    def test_left_pad_char_strings(self):
        self.assertEqual(set(get_args(modes.LeftPadChar)), set(modes.LeftPadCharEnum))

    def test_sign_mode_strings(self):
        self.assertEqual(set(get_args(modes.SignMode)), set(modes.SignModeEnum))

    def test_round_mode_strings(self):
        self.assertEqual(set(get_args(modes.RoundMode)), set(modes.RoundModeEnum))

    def test_exp_mode_strings(self):
        self.assertEqual(set(get_args(modes.ExpMode)), set(modes.ExpModeEnum))

    def test_exp_format_strings(self):
        self.assertEqual(set(get_args(modes.ExpFormat)), set(modes.ExpFormatEnum))

    def test_separator_strings(self):
        self.assertEqual(set(get_args(modes.UpperSeparators)), set(modes.SeparatorEnum))

    def test_upper_separator_strings(self):
        self.assertEqual(
            set(get_args(modes.UpperSeparators)),
            set(get_args(modes.UpperSeparatorEnums)),
        )

    def test_decimal_separator_strings(self):
        self.assertEqual(
            set(get_args(modes.DecimalSeparators)),
            set(get_args(modes.DecimalSeparatorEnums)),
        )

    def test_lower_separator_strings(self):
        self.assertEqual(
            set(get_args(modes.LowerSeparators)),
            set(get_args(modes.LowerSeparatorEnums)),
        )
