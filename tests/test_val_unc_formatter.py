import unittest

from sciform import Formatter, ExpMode


class TestFormatting(unittest.TestCase):
    def do_test_case_dict(self, cases_dict: dict[tuple[float, float],
                                                 dict[Formatter, str]]):
        for (val, unc), fmt_dict in cases_dict.items():
            for formatter, expected_num_str in fmt_dict.items():
                snum_str = formatter(val, unc)
                with self.subTest(val=val, unc=unc,
                                  expected_num_str=expected_num_str,
                                  actual_num_str=snum_str):
                    self.assertEqual(snum_str, expected_num_str)

    def test_bracket_unc(self):
        cases_dict = {
            (123.456, 0.789):
                {
                    Formatter(bracket_unc=True): '123.456(789)',
                    Formatter(exp_mode=ExpMode.SCIENTIFIC,
                              bracket_unc=True): '(1.23456(789))e+02',
                    Formatter(exp_mode=ExpMode.ENGINEERING,
                              bracket_unc=True): '(123.456(789))e+00',
                    Formatter(exp_mode=ExpMode.ENGINEERING_SHIFTED,
                              bracket_unc=True): '(0.123456(789))e+03',
                    Formatter(exp_mode=ExpMode.SCIENTIFIC,
                              exp=+1,
                              bracket_unc=True): '(12.3456(789))e+01',
                    Formatter(exp_mode=ExpMode.SCIENTIFIC,
                              exp=-1,
                              bracket_unc=True): '(1234.56(7.89))e-01',
                }
        }

        self.do_test_case_dict(cases_dict)

    def test_bracket_unc_remove_dec_symb(self):
        cases_dict = {
            (123.456, 0.789):
                {
                    Formatter(exp_mode=ExpMode.SCIENTIFIC,
                              exp=-1,
                              bracket_unc=True): '(1234.56(7.89))e-01',
                    Formatter(
                        exp_mode=ExpMode.SCIENTIFIC,
                        exp=-1,
                        bracket_unc_remove_seps=True,
                        bracket_unc=True): '(1234.56(789))e-01',
                }
        }

        self.do_test_case_dict(cases_dict)

    def test_unc_pm_whitespace(self):
        cases_dict = {
            (123.456, 0.789):
                {
                    Formatter(unc_pm_whitespace=True): '123.456 +/- 0.789',
                    Formatter(unc_pm_whitespace=False): '123.456+/-0.789'
                }
        }

        self.do_test_case_dict(cases_dict)
