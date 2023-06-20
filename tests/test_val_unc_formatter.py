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
                },
            (0.789, 123.456):
                {
                    Formatter(exp_mode=ExpMode.SCIENTIFIC,
                              exp=-1,
                              bracket_unc=True): '(7.89(1234.56))e-01',
                    # Don't remove "embedded" decimal unless val > unc.
                    Formatter(
                        exp_mode=ExpMode.SCIENTIFIC,
                        exp=-1,
                        bracket_unc_remove_seps=True,
                        bracket_unc=True): '(7.89(1234.56))e-01',
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

    def test_pdg(self):
        """
        Note the behavior at the PDG cutoffs may be surprising due to
        finite float precision. From the python docs for ``round()``

           Note The behavior of round() for floats can be surprising:
           for example, round(2.675, 2) gives 2.67 instead of the
           expected 2.68. This is not a bug: it’s a result of the fact
           that most decimal fractions can’t be represented exactly as a
           float. See Floating Point Arithmetic: Issues and Limitations
           for more information.

        https://docs.python.org/3/library/functions.html?highlight=round#round

        For example, we would expect val=10, unc=0.0355 to be formatted
        with 2 significant figures and for 0.0355 to be rounded to
        0.036, but round(0.0355, 3) yields 0.035 instead so the result
        is '10.000 +/- 0.035'. However, val=10, unc = 0.00355 indeed
        yields '10.0000 +/- 0.0036' because round(0.00355, 4) = 0.0036.

        For that reason, these edge cases are exlcuded from the tests.
        Getting more expected behavior for these edge cases would
        require using decimal objects rather than floats.
        """
        cases_dict = {
            (10, 0.0350):
                {
                    Formatter(pdg_sig_figs=True): '10.00 +/- 0.04'
                },
            (10, 0.0356):
                {
                    Formatter(pdg_sig_figs=True): '10.000 +/- 0.036'
                },
            (10, 0.0945):
                {
                    Formatter(pdg_sig_figs=True): '10.000 +/- 0.095'
                },
            (10, 0.0996):
                {
                    Formatter(pdg_sig_figs=True): '10.00 +/- 0.10'
                }

        }

        self.do_test_case_dict(cases_dict)


if __name__ == "__main__":
    unittest.main()
