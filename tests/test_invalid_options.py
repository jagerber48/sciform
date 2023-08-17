import unittest

from sciform import FormatOptions, RoundMode, ExpMode, GroupingSeparator


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

    def test_exp_mode_exp_val(self):
        self.assertRaises(
            ValueError, FormatOptions, exp_mode=ExpMode.FIXEDPOINT,
            exp_val=1
        )
        self.assertRaises(
            ValueError, FormatOptions, exp_mode=ExpMode.PERCENT,
            exp_val=1
        )
        self.assertRaises(
            ValueError, FormatOptions, exp_mode=ExpMode.ENGINEERING,
            exp_val=1
        )
        self.assertRaises(
            ValueError, FormatOptions, exp_mode=ExpMode.ENGINEERING_SHIFTED,
            exp_val=1
        )
        self.assertRaises(
            ValueError, FormatOptions, exp_mode=ExpMode.BINARY_IEC,
            exp_val=5
        )

    def test_invalid_upper_separator(self):
        self.assertRaises(
            ValueError, FormatOptions, upper_separator='_'
        )

    def test_invalid_decimal_separator(self):
        self.assertRaises(
            ValueError, FormatOptions, decimal_separator='_'
        )
        self.assertRaises(
            ValueError, FormatOptions,
            decimal_separator=GroupingSeparator.UNDERSCORE
        )
        self.assertRaises(
            ValueError, FormatOptions,
            decimal_separator=GroupingSeparator.SPACE
        )
        self.assertRaises(
            ValueError, FormatOptions,
            decimal_separator=GroupingSeparator.NONE
        )

    def test_invalid_lower_separator(self):
        self.assertRaises(
            ValueError, FormatOptions, lower_separator='_'
        )
        self.assertRaises(
            ValueError, FormatOptions,
            lower_separator=GroupingSeparator.COMMA
        )
        self.assertRaises(
            ValueError, FormatOptions,
            lower_separator=GroupingSeparator.POINT
        )

    def test_separator_conflict(self):
        # self.assertRaises(
        #     ValueError, FormatOptions,
        #     upper_separator=GroupingSeparator.POINT
        # )
        self.assertRaises(
            ValueError, FormatOptions,
            upper_separator=GroupingSeparator.POINT,
            decimal_separator=GroupingSeparator.POINT
        )
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
