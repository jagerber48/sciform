import unittest

from sciform import (Formatter, FormatOptions, RoundMode, ExpMode,
                     GroupingSeparator)


class TestInvalidOptions(unittest.TestCase):
    def test_sig_fig_ndigits(self):
        self.assertRaises(
            ValueError, FormatOptions, round_mode=RoundMode.SIG_FIG,
            ndigits=0
        )

    def test_pdg_sig_figs_ndigits(self):
        self.assertRaises(
            ValueError, FormatOptions, pdg_sig_figs=True, ndigits=3
        )

    def test_fixed_point(self):
        self.assertRaises(
            ValueError, FormatOptions, exp_mode=ExpMode.FIXEDPOINT,
            exp_val=1
        )

    def test_percent(self):
        self.assertRaises(
            ValueError, FormatOptions, exp_mode=ExpMode.PERCENT,
            exp_val=1
        )

    def test_engineering(self):
        self.assertRaises(
            ValueError, FormatOptions, exp_mode=ExpMode.ENGINEERING,
            exp_val=1
        )

    def test_engineering_shifted(self):
        self.assertRaises(
            ValueError, FormatOptions, exp_mode=ExpMode.ENGINEERING_SHIFTED,
            exp_val=1
        )

    def test_binary_iec(self):
        self.assertRaises(
            ValueError, FormatOptions, exp_mode=ExpMode.BINARY_IEC,
            exp_val=5
        )

    def test_invalid_upper_separator(self):
        self.assertRaises(
            ValueError, FormatOptions, upper_separator='_'
        )

    def test_decimal_separator_non_option(self):
        self.assertRaises(
            ValueError, FormatOptions, decimal_separator='_'
        )

    def test_decimal_separator_underscore(self):
        self.assertRaises(
            ValueError, FormatOptions,
            decimal_separator=GroupingSeparator.UNDERSCORE
        )

    def test_decimal_separator_space(self):
        self.assertRaises(
            ValueError, FormatOptions,
            decimal_separator=GroupingSeparator.SPACE
        )

    def test_decimal_separator_none(self):
        self.assertRaises(
            ValueError, FormatOptions,
            decimal_separator=GroupingSeparator.NONE
        )

    def test_lower_separator_non_option(self):
        self.assertRaises(
            ValueError, FormatOptions, lower_separator='_'
        )

    def test_lower_separator_comma(self):
        self.assertRaises(
            ValueError, FormatOptions,
            lower_separator=GroupingSeparator.COMMA
        )

    def test_lower_separator_point(self):
        self.assertRaises(
            ValueError, FormatOptions,
            lower_separator=GroupingSeparator.POINT
        )

    @unittest.expectedFailure
    def test_upper_separator_point_default_merge(self):
        sform = Formatter(
            FormatOptions(upper_separator=GroupingSeparator.POINT))
        self.assertRaises(ValueError, sform, 42)

    def test_upper_decimal_separator_point(self):
        self.assertRaises(
            ValueError, FormatOptions,
            upper_separator=GroupingSeparator.POINT,
            decimal_separator=GroupingSeparator.POINT
        )

    def test_uppder_decimal_separator_comma(self):
        self.assertRaises(
            ValueError, FormatOptions,
            upper_separator=GroupingSeparator.COMMA,
            decimal_separator=GroupingSeparator.COMMA
        )

    def test_prefix_and_parts_per_exp(self):
        self.assertRaises(
            ValueError, FormatOptions,
            prefix_exp=True,
            parts_per_exp=True
        )


if __name__ == "__main__":
    unittest.main()
