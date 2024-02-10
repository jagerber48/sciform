import unittest
from decimal import Decimal

from sciform import Formatter, modes
from sciform.format_utils import (
    get_mantissa_exp_base,
    get_prefix_dict,
    get_round_digit,
    get_sign_str,
    get_top_digit,
    get_top_digit_binary,
)
from sciform.formatting import format_non_finite
from sciform.options.conversion import finalize_input_options
from sciform.options.input_options import InputOptions
from sciform.output_conversion import _make_exp_str, convert_sciform_format


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

    def test_get_top_digit_infinite(self):
        self.assertEqual(get_top_digit(Decimal("nan")), 0)

    def test_get_top_digit_binary_infinite(self):
        self.assertEqual(get_top_digit_binary(Decimal("nan")), 0)

    def test_get_mantissa_exp_base_fixed_point_set_exp(self):
        self.assertRaises(
            ValueError,
            get_mantissa_exp_base,
            num=Decimal(3),
            exp_mode=modes.ExpModeEnum.FIXEDPOINT,
            input_exp=1,
        )

    def test_get_mantissa_exp_base_engineering_set_exp(self):
        self.assertRaises(
            ValueError,
            get_mantissa_exp_base,
            num=Decimal(3),
            exp_mode=modes.ExpModeEnum.ENGINEERING,
            input_exp=1,
        )

    def test_get_mantissa_exp_base_binary_iec_set_exp(self):
        self.assertRaises(
            ValueError,
            get_mantissa_exp_base,
            num=Decimal(3),
            exp_mode=modes.ExpModeEnum.BINARY_IEC,
            input_exp=3,
        )

    def test_get_mantissa_exp_base_bad_exp_mode(self):
        self.assertRaises(
            ValueError,
            get_mantissa_exp_base,
            num=Decimal(3),
            exp_mode="eng",
            input_exp=3,
        )

    def test_get_sign_str_bad_sign_mode(self):
        self.assertRaises(ValueError, get_sign_str, num=Decimal(1), sign_mode="space")

    def test_get_round_digit_bad_round_mode(self):
        self.assertRaises(
            ValueError,
            get_round_digit,
            num=Decimal(123.456),
            round_mode="none",
            ndigits=0,
        )

    def test_get_prefix_dict_bad_base(self):
        self.assertRaises(
            ValueError,
            get_prefix_dict,
            exp_format=modes.ExpFormatEnum.PREFIX,
            base=3,
            extra_si_prefixes={},
            extra_iec_prefixes={},
            extra_parts_per_forms={},
        )

    def test_get_prefix_dict_bad_format(self):
        self.assertRaises(
            ValueError,
            get_prefix_dict,
            exp_format="pref",
            base=10,
            extra_si_prefixes={},
            extra_iec_prefixes={},
            extra_parts_per_forms={},
        )

    def test_mode_str_to_enum_fail(self):
        self.assertRaises(
            ValueError,
            modes.mode_str_to_enum,
            "eng",
            modes.ExpModeEnum,
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
