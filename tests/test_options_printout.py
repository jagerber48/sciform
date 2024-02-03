import unittest

from sciform import GlobalOptionsContext, get_global_options


class TestOptionsPrintOut(unittest.TestCase):
    def test_get_global_options(self):
        actual_string = str(get_global_options())
        expected_string = (
            "{'exp_mode': 'fixed_point',\n"
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
            " 'paren_uncertainty_separators': True,\n"
            " 'pm_whitespace': True}"
        )
        self.assertEqual(actual_string, expected_string)

    def test_modified_get_global_options(self):
        with GlobalOptionsContext(left_pad_dec_place=3, capitalize=True):
            actual_str = str(get_global_options())
        expected_str = (
            "{'exp_mode': 'fixed_point',\n"
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
            " 'paren_uncertainty_separators': True,\n"
            " 'pm_whitespace': True}"
        )
        self.assertEqual(actual_str, expected_str)
