import unittest

from sciform import Formatter, ExpMode, GroupingSeparator


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

    def test_percent(self):
        cases_dict = {
            (0.123_456_78, 0.000_002_55):
                {
                    Formatter(percent=True,
                              lower_separator=GroupingSeparator.UNDERSCORE):
                        '(12.345_678 +/- 0.000_255)%',
                    Formatter(percent=True,
                              bracket_unc=True,
                              lower_separator=GroupingSeparator.UNDERSCORE):
                        '(12.345_678(255))%'
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

    def test_unicode_pm(self):
        cases_dict = {
            (123.456, 0.789):
                {
                    Formatter(unicode_pm=True): '123.456 ± 0.789'
                }
        }

        self.do_test_case_dict(cases_dict)

    def test_superscript_exp(self):
        cases_dict = {
            (789, 0.01): {
                Formatter(exp_mode=ExpMode.SCIENTIFIC,
                          superscript_exp=True): '(7.8900 +/- 0.0001)×10²'
            }
        }

        self.do_test_case_dict(cases_dict)

    def test_latex(self):
        cases_dict = {
            (12345, 0.2): {
                Formatter(exp_mode=ExpMode.SCIENTIFIC,
                          exp=-1,
                          upper_separator=GroupingSeparator.UNDERSCORE,
                          latex=True): r'\left(123\_450 \pm 2\right)\times 10^{-1}',

                # Latex mode takes precedence over unicode_pm
                Formatter(exp_mode=ExpMode.SCIENTIFIC,
                          exp=-1,
                          upper_separator=GroupingSeparator.UNDERSCORE,
                          unicode_pm=True,
                          latex=True): r'\left(123\_450 \pm 2\right)\times 10^{-1}'
            },
            (0.123_456_78, 0.000_002_55): {
                Formatter(lower_separator=GroupingSeparator.UNDERSCORE,
                          percent=True,
                          latex=True): r'\left(12.345\_678 \pm 0.000\_255\right)\%',
                Formatter(lower_separator=GroupingSeparator.UNDERSCORE,
                          percent=True,
                          bracket_unc=True,
                          latex=True): r'\left(12.345\_678\left(255\right)\right)\%'
            }
        }

        self.do_test_case_dict(cases_dict)


if __name__ == "__main__":
    unittest.main()
