import unittest

from sciform import vufloat, GlobalDefaultsContext


NAN = float('nan')
INF = float('inf')


class TestFormatting(unittest.TestCase):
    def do_unc_val_test_case_dict(
            self,
            cases_dict: dict[tuple[float, float], dict[str, str]]):
        for (val, unc), fmt_dict in cases_dict.items():
            for format_spec, expected_str in fmt_dict.items():
                vunum = vufloat(val, unc)
                vunum_str = f'{vunum:{format_spec}}'
                with self.subTest(val=val, unc=unc, format_spec=format_spec,
                                  expected_str=expected_str,
                                  actual_str=vunum_str):
                    self.assertEqual(vunum_str, expected_str)

    def test_fixed(self):
        cases_dict = {
            (123.456, 0.789):
                {
                    'f': '123.456 +/- 0.789',
                    '!1f': '123.5 +/- 0.8',
                    '!2f': '123.46 +/- 0.79',
                    '!3f': '123.456 +/- 0.789',
                    '!4f': '123.4560 +/- 0.7890',
                    '!2fS': '123.46(79)',
                },
            (0.789, 123.456):
                {
                    'f': '0.789 +/- 123.456',
                    '!1f': '0 +/- 100',
                    '!2f': '0 +/- 120',
                    '!3f': '1 +/- 123',
                    '!4f': '0.8 +/- 123.5',
                    '!5f': '0.79 +/- 123.46',
                    '!6f': '0.789 +/- 123.456',
                    '!7f': '0.7890 +/- 123.4560',
                    '!1fS': '0(100)',
                    '!2fS': '0(120)',
                    '!3fS': '1(123)',
                    '!4fS': '0.8(123.5)',
                    '!5fS': '0.79(123.46)',
                    '!6fS': '0.789(123.456)',
                    '!7fS': '0.7890(123.4560)',
                }
        }

        self.do_unc_val_test_case_dict(cases_dict)

    def test_scientific(self):
        cases_dict = {
            (123.456, 0.789):
                {
                    'e': '(1.23456 +/- 0.00789)e+02',
                    '!1e': '(1.235 +/- 0.008)e+02',
                    '!2e': '(1.2346 +/- 0.0079)e+02',
                    '!3e': '(1.23456 +/- 0.00789)e+02',
                    '!4e': '(1.234560 +/- 0.007890)e+02',
                    '!2eS': '(1.2346(79))e+02',
                },
            (0.789, 123.456):
                {
                    'e': '(7.89 +/- 1234.56)e-01',
                    '!1e': '(0 +/- 100)e+00',
                    '!2e': '(0 +/- 120)e+00',
                    '!3e': '(1 +/- 123)e+00',
                    '!4e': '(8 +/- 1235)e-01',
                    '!5e': '(7.9 +/- 1234.6)e-01',
                    '!6e': '(7.89 +/- 1234.56)e-01',
                    '!7e': '(7.890 +/- 1234.560)e-01',
                    '!1eS': '(0(100))e+00',
                    '!2eS': '(0(120))e+00',
                    '!3eS': '(1(123))e+00',
                    '!4eS': '(8(1235))e-01',
                    '!5eS': '(7.9(1234.6))e-01',
                    '!6eS': '(7.89(1234.56))e-01',
                    '!7eS': '(7.890(1234.560))e-01',
                }
        }

        self.do_unc_val_test_case_dict(cases_dict)

    def test_engineering(self):
        cases_dict = {
            (1234.56, 0.789):
                {
                    'r': '(1.234560 +/- 0.000789)e+03',
                    '!1r': '(1.2346 +/- 0.0008)e+03',
                    '!2r': '(1.23456 +/- 0.00079)e+03',
                    '!3r': '(1.234560 +/- 0.000789)e+03',
                    '!4r': '(1.2345600 +/- 0.0007890)e+03',
                    '!2rS': '(1.23456(79))e+03',
                },
            (0.789, 123.456):
                {
                    'r': '(789 +/- 123456)e-03',
                    '!1r': '(0 +/- 100)e+00',
                    '!2r': '(0 +/- 120)e+00',
                    '!3r': '(1 +/- 123)e+00',
                    '!4r': '(800 +/- 123500)e-03',
                    '!5r': '(790 +/- 123460)e-03',
                    '!6r': '(789 +/- 123456)e-03',
                    '!7r': '(789.0 +/- 123456.0)e-03',
                    '!1rS': '(0(100))e+00',
                    '!2rS': '(0(120))e+00',
                    '!3rS': '(1(123))e+00',
                    '!4rS': '(800(123500))e-03',
                    '!5rS': '(790(123460))e-03',
                    '!6rS': '(789(123456))e-03',
                    '!7rS': '(789.0(123456.0))e-03',
                }
        }

        self.do_unc_val_test_case_dict(cases_dict)

    def test_engineering_shifted(self):
        cases_dict = {
            (123.456, 0.789):
                {
                    '#r': '(0.123456 +/- 0.000789)e+03',
                    '#!1r': '(0.1235 +/- 0.0008)e+03',
                    '#!2r': '(0.12346 +/- 0.00079)e+03',
                    '#!3r': '(0.123456 +/- 0.000789)e+03',
                    '#!4r': '(0.1234560 +/- 0.0007890)e+03',
                    '#!2rS': '(0.12346(79))e+03',
                },
            (0.789, 123.456):
                {
                    '#r': '(0.789 +/- 123.456)e+00',
                    '#!1r': '(0 +/- 100)e+00',
                    '#!2r': '(0 +/- 120)e+00',
                    '#!3r': '(1 +/- 123)e+00',
                    '#!4r': '(0.8 +/- 123.5)e+00',
                    '#!5r': '(0.79 +/- 123.46)e+00',
                    '#!6r': '(0.789 +/- 123.456)e+00',
                    '#!7r': '(0.7890 +/- 123.4560)e+00',
                    '#!1rS': '(0(100))e+00',
                    '#!2rS': '(0(120))e+00',
                    '#!3rS': '(1(123))e+00',
                    '#!4rS': '(0.8(123.5))e+00',
                    '#!5rS': '(0.79(123.46))e+00',
                    '#!6rS': '(0.789(123.456))e+00',
                    '#!7rS': '(0.7890(123.4560))e+00',
                }
        }

        self.do_unc_val_test_case_dict(cases_dict)

    def test_match_width(self):
        cases_dict = {
            (123.456, 0.789):
                {
                    '0!2f': '123.46 +/-   0.79',
                    '0=0!2f': '123.46 +/- 000.79'
                },
            (0.789, 123.456):
                {
                    '0!2f': '  0 +/- 120',
                    '0=0!2f': '000 +/- 120'
                }
        }

        self.do_unc_val_test_case_dict(cases_dict)

    def test_nan_inf(self):
        cases_dict = {
            (12.34, NAN): {
                '': '12.34 +/- nan',
                'e': '(1.234 +/- nan)e+01',
                'S': '12.34(nan)',
                'eS': '(1.234(nan))e+01'
            },
            (12.34, INF): {
                '': '12.34 +/- inf',
                'e': '(1.234 +/- inf)e+01',
                'S': '12.34(inf)',
                'eS': '(1.234(inf))e+01'
            },
            (NAN, 12.34): {
                '': 'nan +/- 12.34',
                'e': '(nan +/- 1.234)e+01',
                'S': 'nan(12.34)',
                'eS': '(nan(1.234))e+01',
            },
            (INF, 12.34): {
                '': 'inf +/- 12.34',
                'e': '(inf +/- 1.234)e+01',
                'S': 'inf(12.34)',
                'eS': '(inf(1.234))e+01'
            },
            (NAN, NAN): {
                '': 'nan +/- nan',
                'S': 'nan(nan)',
                'e': 'nan +/- nan',
                'eS': 'nan(nan)'
            }
        }

        self.do_unc_val_test_case_dict(cases_dict)

    def test_nan_exp(self):
        cases_dict = {
            (NAN, NAN): {
                '': 'nan +/- nan',
                'e': '(nan +/- nan)e+00',
                'S': 'nan(nan)',
                'eS': '(nan(nan))e+00'
            }
        }
        with GlobalDefaultsContext(val_unc_nan_include_exp=True):
            self.do_unc_val_test_case_dict(cases_dict)

    def test_capitalization(self):
        cases_dict = {
            (123.456, 0.789):
                {
                    'e': '(1.23456 +/- 0.00789)e+02',
                    'E': '(1.23456 +/- 0.00789)E+02'
                },
            (NAN, NAN): {
                'e': '(nan +/- nan)e+00',
                'E': '(NAN +/- NAN)E+00',
            },
            (INF, INF): {
                'e': '(inf +/- inf)e+00',
                'E': '(INF +/- INF)E+00',
            }
        }

        with GlobalDefaultsContext(val_unc_nan_include_exp=True):
            self.do_unc_val_test_case_dict(cases_dict)

    def test_rounding(self):
        cases_dict = {
            (0.0999, 0.0999): {
                '!1e': '(1 +/- 1)e-01'
            },
            (0.0999, 0.999): {
                '!1e': '(0 +/- 1)e+00'
            }
        }
        self.do_unc_val_test_case_dict(cases_dict)

    def test_match_widths(self):
        cases_dict = {
            (123.456, 0.789): {
                '0=0': '123.456 +/- 000.789',
                '0= 0': ' 123.456 +/- 000.789',
                ' 0': ' 123.456 +/-   0.789',
                '+0': '+123.456 +/-   0.789',
                '0': '123.456 +/-   0.789'
            },
            (0.789, 123.456): {
                '0=0': '000.789 +/- 123.456',
                '0= 0': ' 000.789 +/- 123.456',
                ' 0': '   0.789 +/- 123.456',
                '+0': '+  0.789 +/- 123.456',
                '0': '  0.789 +/- 123.456'
            }
        }
        self.do_unc_val_test_case_dict(cases_dict)


if __name__ == '__main__':
    unittest.main(verbosity=2)
