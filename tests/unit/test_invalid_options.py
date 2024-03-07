import unittest
from decimal import Decimal

from sciform import Formatter
from sciform.formatting.number_formatting import format_non_finite
from sciform.formatting.output_conversion import _make_exp_str, convert_sciform_format
from sciform.options import option_types
from sciform.options.conversion import finalize_input_options
from sciform.options.input_options import InputOptions


class TestInvalidOptions(unittest.TestCase):
    def test_sig_fig_ndigits(self):
        self.assertRaises(
            ValueError,
            Formatter,
            round_mode="sig_fig",
            ndigits=0,
        )

    def test_fixed_point(self):
        self.assertRaises(
            ValueError,
            Formatter,
            exp_mode="fixed_point",
            exp_val=1,
        )

    def test_percent(self):
        self.assertRaises(
            ValueError,
            Formatter,
            exp_mode="percent",
            exp_val=1,
        )

    def test_engineering(self):
        self.assertRaises(
            ValueError,
            Formatter,
            exp_mode="engineering",
            exp_val=1,
        )

    def test_engineering_shifted(self):
        self.assertRaises(
            ValueError,
            Formatter,
            exp_mode="engineering",
            exp_val=1,
        )

    def test_binary_iec(self):
        self.assertRaises(
            ValueError,
            Formatter,
            exp_mode="binary_iec",
            exp_val=5,
        )

    def test_upper_separator_non_option(self):
        self.assertRaises(
            ValueError,
            Formatter,
            upper_separator="-",
        )

    def test_decimal_separator_non_option(self):
        self.assertRaises(
            ValueError,
            Formatter,
            decimal_separator="-",
        )

    def test_decimal_separator_underscore(self):
        self.assertRaises(
            ValueError,
            Formatter,
            decimal_separator="_",
        )

    def test_decimal_separator_space(self):
        self.assertRaises(
            ValueError,
            Formatter,
            decimal_separator=" ",
        )

    def test_decimal_separator_none(self):
        self.assertRaises(
            ValueError,
            Formatter,
            decimal_separator="",
        )

    def test_lower_separator_non_option(self):
        self.assertRaises(
            ValueError,
            Formatter,
            lower_separator="-",
        )

    def test_lower_separator_comma(self):
        self.assertRaises(
            ValueError,
            Formatter,
            lower_separator=",",
        )

    def test_lower_separator_point(self):
        self.assertRaises(
            ValueError,
            Formatter,
            lower_separator=".",
        )

    def test_upper_separator_point_default_merge(self):
        """
        This test raises a ValueError because the upper_separator is
        requested to be POINT. But the package defaults set
        decimal_separator to also be POINT. So when the Formatter
        InputOptions are rendered into FinalizedOptions, at format time,
        the result is that both upper_separator=GroupingSeparator.POINT
        and decimal_separator=GroupingSeparator.POINT This options
        combination is not allowed.
        """
        formatter = Formatter(upper_separator=".")
        self.assertRaises(ValueError, formatter, 42)

    def test_upper_decimal_separator_point(self):
        self.assertRaises(
            ValueError,
            Formatter,
            upper_separator=".",
            decimal_separator=".",
        )

    def test_upper_decimal_separator_comma(self):
        self.assertRaises(
            ValueError,
            Formatter,
            upper_separator=",",
            decimal_separator=",",
        )

    def test_format_non_finite(self):
        self.assertRaises(
            ValueError,
            format_non_finite,
            Decimal(1.0),
            finalize_input_options(InputOptions()),
        )

    def test_mode_str_to_enum_fail(self):
        self.assertRaises(
            ValueError,
            option_types.mode_str_to_enum,
            "eng",
            option_types.ExpModeEnum,
        )

    def test_convert_sciform_format_invalid_output_format(self):
        self.assertRaises(
            ValueError,
            convert_sciform_format,
            "123",
            "md",
        )

    def test_make_exp_str_invalid_output_format(self):
        self.assertRaises(
            ValueError,
            _make_exp_str,
            10,
            0,
            "rst",
        )

    def test_make_exp_str_invalid_base(self):
        self.assertRaises(
            ValueError,
            _make_exp_str,
            16,
            0,
            "ascii",
        )

    def test_invalid_translation_key(self):
        self.assertRaises(
            TypeError,
            Formatter,
            extra_si_prefixes={"3": "k"},
        )

    def test_invalid_translation_value(self):
        self.assertRaises(
            ValueError,
            Formatter,
            extra_si_prefixes={-10: "Å"},
        )
