from io import StringIO
from contextlib import redirect_stdout

import unittest

from sciform import print_global_defaults, FormatOptions


class TestPrint(unittest.TestCase):
    def test_print_global_defaults(self):
        with redirect_stdout(StringIO()) as sout:
            print_global_defaults()
        actual_printout = sout.getvalue()
        expected_printout = (
            "{'exp_mode': <ExpMode.FIXEDPOINT: 'fixed_point'>,\n"
            " 'exp_val': <class 'sciform.modes.AutoExpVal'>,\n"
            " 'round_mode': <RoundMode.SIG_FIG: 'sig_fig'>,\n"
            " 'ndigits': <class 'sciform.modes.AutoDigits'>,\n"
            " 'upper_separator': <GroupingSeparator.NONE: 'no_grouping'>,\n"
            " 'decimal_separator': <GroupingSeparator.POINT: 'point'>,\n"
            " 'lower_separator': <GroupingSeparator.NONE: 'no_grouping'>,\n"
            " 'sign_mode': <SignMode.NEGATIVE: 'negative'>,\n"
            " 'fill_mode': <FillMode.SPACE: 'space'>,\n"
            " 'top_dig_place': 0,\n"
            " 'exp_format': <ExpFormat.STANDARD: 'standard'>,\n"
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
            " 'unicode_pm': False,\n"
            " 'unc_pm_whitespace': True}\n"
            ""
        )
        self.assertEqual(actual_printout, expected_printout)

    def test_unrendered_options_repr(self):
        with redirect_stdout(StringIO()) as sout:
            print(FormatOptions())
        actual_printout = sout.getvalue()
        expected_printout = (
            "{'exp_mode': <ExpMode.FIXEDPOINT: 'fixed_point'>,\n"
            " 'exp_val': <class 'sciform.modes.AutoExpVal'>,\n"
            " 'round_mode': <RoundMode.SIG_FIG: 'sig_fig'>,\n"
            " 'ndigits': <class 'sciform.modes.AutoDigits'>,\n"
            " 'upper_separator': <GroupingSeparator.NONE: 'no_grouping'>,\n"
            " 'decimal_separator': <GroupingSeparator.POINT: 'point'>,\n"
            " 'lower_separator': <GroupingSeparator.NONE: 'no_grouping'>,\n"
            " 'sign_mode': <SignMode.NEGATIVE: 'negative'>,\n"
            " 'fill_mode': <FillMode.SPACE: 'space'>,\n"
            " 'top_dig_place': 0,\n"
            " 'exp_format': <ExpFormat.STANDARD: 'standard'>,\n"
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
            " 'unicode_pm': False,\n"
            " 'unc_pm_whitespace': True}\n"
            ""
        )
        self.assertEqual(actual_printout, expected_printout)
