import unittest

from sciform import (
    Formatter,
    GlobalOptionsContext,
    get_default_global_options,
    get_global_options,
)


class TestOptionsPrintOut(unittest.TestCase):
    def test_formatter_input_options(self):
        formatter = Formatter(
            exp_mode="engineering",
            add_c_prefix=True,
            ndigits=10,
            left_pad_char=0,
        )
        input_options_str = str(formatter.input_options)
        expected_str = (
            "InputOptions(\n"
            " 'exp_mode': 'engineering',\n"
            " 'ndigits': 10,\n"
            " 'left_pad_char': 0,\n"
            " 'add_c_prefix': True,\n"
            ")"
        )
        self.assertEqual(input_options_str, expected_str)

    def test_formatter_populated_options(self):
        formatter = Formatter(
            exp_mode="engineering",
            add_c_prefix=True,
            ndigits=10,
            left_pad_char=0,
        )
        input_options_str = str(formatter.populated_options)
        expected_str = (
            "PopulatedOptions(\n"
            " 'exp_mode': 'engineering',\n"
            " 'exp_val': AutoExpVal,\n"
            " 'round_mode': 'sig_fig',\n"
            " 'ndigits': 10,\n"
            " 'upper_separator': '',\n"
            " 'decimal_separator': '.',\n"
            " 'lower_separator': '',\n"
            " 'sign_mode': '-',\n"
            " 'left_pad_char': '0',\n"
            " 'left_pad_dec_place': 0,\n"
            " 'exp_format': 'standard',\n"
            " 'extra_si_prefixes': {-2: 'c'},\n"
            " 'extra_iec_prefixes': {},\n"
            " 'extra_parts_per_forms': {},\n"
            " 'capitalize': False,\n"
            " 'superscript': False,\n"
            " 'nan_inf_exp': False,\n"
            " 'paren_uncertainty': False,\n"
            " 'pdg_sig_figs': False,\n"
            " 'left_pad_matching': False,\n"
            " 'paren_uncertainty_trim': True,\n"
            " 'pm_whitespace': True,\n"
            ")"
        )
        self.assertEqual(input_options_str, expected_str)

    def test_get_default_global_options(self):
        actual_string = str(get_default_global_options())
        expected_string = (
            "PopulatedOptions(\n"
            " 'exp_mode': 'fixed_point',\n"
            " 'exp_val': AutoExpVal,\n"
            " 'round_mode': 'sig_fig',\n"
            " 'ndigits': AutoDigits,\n"
            " 'upper_separator': '',\n"
            " 'decimal_separator': '.',\n"
            " 'lower_separator': '',\n"
            " 'sign_mode': '-',\n"
            " 'left_pad_char': ' ',\n"
            " 'left_pad_dec_place': 0,\n"
            " 'exp_format': 'standard',\n"
            " 'extra_si_prefixes': {},\n"
            " 'extra_iec_prefixes': {},\n"
            " 'extra_parts_per_forms': {},\n"
            " 'capitalize': False,\n"
            " 'superscript': False,\n"
            " 'nan_inf_exp': False,\n"
            " 'paren_uncertainty': False,\n"
            " 'pdg_sig_figs': False,\n"
            " 'left_pad_matching': False,\n"
            " 'paren_uncertainty_trim': True,\n"
            " 'pm_whitespace': True,\n"
            ")"
        )
        self.assertEqual(actual_string, expected_string)

    def test_get_global_options(self):
        with GlobalOptionsContext(left_pad_dec_place=3, capitalize=True):
            actual_str = str(get_global_options())
        expected_str = (
            "PopulatedOptions(\n"
            " 'exp_mode': 'fixed_point',\n"
            " 'exp_val': AutoExpVal,\n"
            " 'round_mode': 'sig_fig',\n"
            " 'ndigits': AutoDigits,\n"
            " 'upper_separator': '',\n"
            " 'decimal_separator': '.',\n"
            " 'lower_separator': '',\n"
            " 'sign_mode': '-',\n"
            " 'left_pad_char': ' ',\n"
            " 'left_pad_dec_place': 3,\n"
            " 'exp_format': 'standard',\n"
            " 'extra_si_prefixes': {},\n"
            " 'extra_iec_prefixes': {},\n"
            " 'extra_parts_per_forms': {},\n"
            " 'capitalize': True,\n"
            " 'superscript': False,\n"
            " 'nan_inf_exp': False,\n"
            " 'paren_uncertainty': False,\n"
            " 'pdg_sig_figs': False,\n"
            " 'left_pad_matching': False,\n"
            " 'paren_uncertainty_trim': True,\n"
            " 'pm_whitespace': True,\n"
            ")"
        )
        self.assertEqual(actual_str, expected_str)
