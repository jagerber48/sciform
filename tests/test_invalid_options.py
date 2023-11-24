import unittest
from decimal import Decimal

from sciform import Formatter
from sciform.formatting import format_non_finite
from sciform.grouping import add_group_chars_between_numbers, add_separators
from sciform.user_options import UserOptions
from sciform import modes
from sciform.format_utils import (
    get_top_digit, get_mantissa_exp_base, get_exp_str, get_sign_str,
    get_round_digit, get_prefix_dict, parse_standard_exp_str
)


class TestInvalidOptions(unittest.TestCase):
    def test_sig_fig_ndigits(self):
        self.assertRaises(
            ValueError, Formatter, round_mode='sig_fig',
            ndigits=0
        )

    def test_pdg_sig_figs_ndigits(self):
        self.assertRaises(
            ValueError, Formatter, pdg_sig_figs=True, ndigits=3
        )

    def test_fixed_point(self):
        self.assertRaises(
            ValueError, Formatter, exp_mode='fixed_point',
            exp_val=1
        )

    def test_percent(self):
        self.assertRaises(
            ValueError, Formatter, exp_mode='percent',
            exp_val=1
        )

    def test_engineering(self):
        self.assertRaises(
            ValueError, Formatter, exp_mode='engineering',
            exp_val=1
        )

    def test_engineering_shifted(self):
        self.assertRaises(
            ValueError, Formatter, exp_mode='engineering',
            exp_val=1
        )

    def test_binary_iec(self):
        self.assertRaises(
            ValueError, Formatter, exp_mode='binary_iec',
            exp_val=5
        )

    def test_upper_separator_non_option(self):
        self.assertRaises(
            ValueError, Formatter, upper_separator='-'
        )

    def test_decimal_separator_non_option(self):
        self.assertRaises(
            ValueError, Formatter, decimal_separator='-'
        )

    def test_decimal_separator_underscore(self):
        self.assertRaises(
            ValueError, Formatter,
            decimal_separator='_'
        )

    def test_decimal_separator_space(self):
        self.assertRaises(
            ValueError, Formatter,
            decimal_separator=' '
        )

    def test_decimal_separator_none(self):
        self.assertRaises(
            ValueError, Formatter,
            decimal_separator=''
        )

    def test_lower_separator_non_option(self):
        self.assertRaises(
            ValueError, Formatter, lower_separator='-'
        )

    def test_lower_separator_comma(self):
        self.assertRaises(
            ValueError, Formatter,
            lower_separator=','
        )

    def test_lower_separator_point(self):
        self.assertRaises(
            ValueError, Formatter,
            lower_separator='.'
        )

    def test_upper_separator_point_default_merge(self):
        """
        This test raises a ValueError because the upper_separator is
        requested to be POINT. But the package defaults set
        decimal_separator to also be POINT. So when the Formatter
        UserOptions are rendered into RenderedOptions, at format time,
        the result is that both upper_separator=GroupingSeparator.POINT
        and decimal_separator=GroupingSeparator.POINT This options
        combination is not allowed.
        """
        sform = Formatter(upper_separator='.')
        self.assertRaises(ValueError, sform, 42)

    def test_upper_decimal_separator_point(self):
        self.assertRaises(
            ValueError, Formatter,
            upper_separator='.',
            decimal_separator='.'
        )

    def test_upper_decimal_separator_comma(self):
        self.assertRaises(
            ValueError, Formatter,
            upper_separator=',',
            decimal_separator=','
        )

    def test_format_non_finite(self):
        self.assertRaises(ValueError, format_non_finite, Decimal(1.0),
                          UserOptions().render())

    def test_add_group_chars(self):
        self.assertRaises(ValueError, add_group_chars_between_numbers,
                          string='123456.654321', group_char='_',
                          direction='forwards', group_size=3)

    def test_add_separators(self):
        self.assertRaises(ValueError, add_separators,
                          num_str='123.456.789',
                          upper_separator=',',
                          decimal_separator='.',
                          lower_separator='_',
                          group_size=3)

    def test_get_top_digit_infinite(self):
        self.assertEqual(get_top_digit(Decimal('nan')), 0)

    def test_get_mantissa_exp_base_fixed_point_set_exp(self):
        self.assertRaises(ValueError, get_mantissa_exp_base,
                          num=Decimal(3),
                          exp_mode=modes.ExpMode.FIXEDPOINT,
                          input_exp_val=1)

    def test_get_mantissa_exp_base_engineering_set_exp(self):
        self.assertRaises(ValueError, get_mantissa_exp_base,
                          num=Decimal(3),
                          exp_mode=modes.ExpMode.ENGINEERING,
                          input_exp_val=1)

    def test_get_mantissa_exp_base_binary_iec_set_exp(self):
        self.assertRaises(ValueError, get_mantissa_exp_base,
                          num=Decimal(3),
                          exp_mode=modes.ExpMode.BINARY_IEC,
                          input_exp_val=3)

    def test_get_mantissa_exp_base_bad_exp_mode(self):
        self.assertRaises(ValueError, get_mantissa_exp_base,
                          num=Decimal(3),
                          exp_mode='eng',
                          input_exp_val=3)

    def test_get_exp_str_bad_exp_mode(self):
        self.assertRaises(ValueError, get_exp_str,
                          exp_val=2,
                          exp_mode='sci',
                          exp_format=modes.ExpFormat.STANDARD,
                          capitalize=False,
                          latex=False,
                          latex_trim_whitespace=False,
                          superscript=False,
                          extra_si_prefixes={},
                          extra_iec_prefixes={},
                          extra_parts_per_forms={})

    def test_get_sign_str_bad_sign_mode(self):
        self.assertRaises(ValueError, get_sign_str,
                          num=Decimal(1),
                          sign_mode='space')

    def test_get_round_digit_bad_round_mode(self):
        self.assertRaises(ValueError, get_round_digit,
                          num=Decimal(123.456),
                          round_mode='none',
                          ndigits=0)

    def test_get_prefix_dict_bad_base(self):
        self.assertRaises(ValueError, get_prefix_dict,
                          exp_format=modes.ExpFormat.PREFIX,
                          base=3,
                          extra_si_prefixes={},
                          extra_iec_prefixes={},
                          extra_parts_per_forms={})

    def test_get_prefix_dict_bad_format(self):
        self.assertRaises(ValueError, get_prefix_dict,
                          exp_format='pref',
                          base=10,
                          extra_si_prefixes={},
                          extra_iec_prefixes={},
                          extra_parts_per_forms={})

    def test_parse_standard_exp_str_binary(self):
        """
        This is the only place that this is tested while binary
        value/uncertainty is not implemented.
        """
        self.assertEqual(parse_standard_exp_str('b+10'), (2, 10))

    def test_mode_str_to_enum_fail(self):
        self.assertRaises(
            ValueError,
            modes.mode_str_to_enum,
            'eng',
            modes.ExpMode
        )
