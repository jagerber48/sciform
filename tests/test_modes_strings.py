import unittest
from typing import get_args

from sciform import modes


class TestInvalidOptions(unittest.TestCase):
    def test_fill_mode_strings(self):
        self.assertEqual(set(get_args(modes.UserFillMode)),
                         set(modes.FillMode))

    def test_sign_mode_strings(self):
        self.assertEqual(set(get_args(modes.UserSignMode)),
                         set(modes.SignMode))

    def test_round_mode_strings(self):
        self.assertEqual(set(get_args(modes.UserRoundMode)),
                         set(modes.RoundMode))

    def test_exp_mode_strings(self):
        self.assertEqual(set(get_args(modes.UserExpMode)),
                         set(modes.ExpMode))

    def test_exp_format_strings(self):
        self.assertEqual(set(get_args(modes.UserExpFormat)),
                         set(modes.ExpFormat))

    def test_separator_strings(self):
        self.assertEqual(set(get_args(modes.UserUpperSeparators)),
                         set(modes.Separator))

    def test_upper_separator_strings(self):
        self.assertEqual(set(get_args(modes.UserUpperSeparators)),
                         set(get_args(modes.UpperSeparators)))

    def test_decimal_separator_strings(self):
        self.assertEqual(set(get_args(modes.UserDecimalSeparators)),
                         set(get_args(modes.DecimalSeparators)))

    def test_lower_separator_strings(self):
        self.assertEqual(set(get_args(modes.UserLowerSeparators)),
                         set(get_args(modes.LowerSeparators)))
