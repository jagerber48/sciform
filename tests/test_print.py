from io import StringIO
from contextlib import redirect_stdout

import unittest

from sciform import print_global_defaults, GlobalDefaultsContext


class TestPrint(unittest.TestCase):
    def test_print_global_defaults(self):
        with redirect_stdout(StringIO()) as sout:
            print_global_defaults()
        actual_printout = sout.getvalue()
        expected_printout = (
            "{'exp_mode': 'fixed_point',\n"
            " 'exp_val': AutoExpVal,\n"
            " 'round_mode': 'sig_fig',\n"
            " 'ndigits': AutoDigits,\n"
            " 'upper_separator': '',\n"
            " 'decimal_separator': '.',\n"
            " 'lower_separator': '',\n"
            " 'sign_mode': '-',\n"
            " 'fill_mode': ' ',\n"
            " 'top_dig_place': 0,\n"
            " 'exp_format': 'standard',\n"
            " 'extra_si_prefixes': {},\n"
            " 'extra_iec_prefixes': {},\n"
            " 'extra_parts_per_forms': {},\n"
            " 'capitalize': False,\n"
            " 'superscript_exp': False,\n"
            " 'latex': False,\n"
            " 'nan_inf_exp': False,\n"
            " 'bracket_unc': False,\n"
            " 'pdg_sig_figs': False,\n"
            " 'val_unc_match_widths': False,\n"
            " 'bracket_unc_remove_seps': False,\n"
            " 'unc_pm_whitespace': True}\n"
        )
        self.assertEqual(actual_printout, expected_printout)

    def test_unrendered_options_repr(self):
        with redirect_stdout(StringIO()) as sout:
            with GlobalDefaultsContext(top_dig_place=3, capitalize=True):
                print_global_defaults()

        actual_printout = sout.getvalue()
        expected_printout = (
            "{'exp_mode': 'fixed_point',\n"
            " 'exp_val': AutoExpVal,\n"
            " 'round_mode': 'sig_fig',\n"
            " 'ndigits': AutoDigits,\n"
            " 'upper_separator': '',\n"
            " 'decimal_separator': '.',\n"
            " 'lower_separator': '',\n"
            " 'sign_mode': '-',\n"
            " 'fill_mode': ' ',\n"
            " 'top_dig_place': 3,\n"
            " 'exp_format': 'standard',\n"
            " 'extra_si_prefixes': {},\n"
            " 'extra_iec_prefixes': {},\n"
            " 'extra_parts_per_forms': {},\n"
            " 'capitalize': True,\n"
            " 'superscript_exp': False,\n"
            " 'latex': False,\n"
            " 'nan_inf_exp': False,\n"
            " 'bracket_unc': False,\n"
            " 'pdg_sig_figs': False,\n"
            " 'val_unc_match_widths': False,\n"
            " 'bracket_unc_remove_seps': False,\n"
            " 'unc_pm_whitespace': True}\n"
        )
        self.assertEqual(actual_printout, expected_printout)
