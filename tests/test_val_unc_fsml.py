import unittest

from sciform import GlobalDefaultsContext, SciNum

ValUncFSMLCases = list[tuple[tuple[float, float], list[tuple[str, str]]]]
NAN = float("nan")
INF = float("inf")


class TestFormatting(unittest.TestCase):
    def run_val_unc_fsml_cases(self, cases_list: ValUncFSMLCases):
        for (val, unc), formats_list in cases_list:
            for format_spec, expected_str in formats_list:
                snum = SciNum(val, unc)
                snum_str = f"{snum:{format_spec}}"
                with self.subTest(
                    val=val,
                    unc=unc,
                    format_spec=format_spec,
                    expected_str=expected_str,
                    actual_str=snum_str,
                ):
                    self.assertEqual(snum_str, expected_str)

    def test_fixed(self):
        cases_list = [
            (
                (123.456, 0.789),
                [
                    ("f", "123.456 ± 0.789"),
                    ("!1f", "123.5 ± 0.8"),
                    ("!2f", "123.46 ± 0.79"),
                    ("!3f", "123.456 ± 0.789"),
                    ("!4f", "123.4560 ± 0.7890"),
                    ("!2f()", "123.46(79)"),
                ],
            ),
            (
                (-123.456, 0.789),
                [
                    ("f", "-123.456 ± 0.789"),
                    ("!1f", "-123.5 ± 0.8"),
                    ("!2f", "-123.46 ± 0.79"),
                    ("!3f", "-123.456 ± 0.789"),
                    ("!4f", "-123.4560 ± 0.7890"),
                    ("!2f()", "-123.46(79)"),
                ],
            ),
            (
                (0.789, 123.456),
                [
                    ("f", "0.789 ± 123.456"),
                    ("!1f", "0 ± 100"),
                    ("!2f", "0 ± 120"),
                    ("!3f", "1 ± 123"),
                    ("!4f", "0.8 ± 123.5"),
                    ("!5f", "0.79 ± 123.46"),
                    ("!6f", "0.789 ± 123.456"),
                    ("!7f", "0.7890 ± 123.4560"),
                    ("!1f()", "0(100)"),
                    ("!2f()", "0(120)"),
                    ("!3f()", "1(123)"),
                    ("!4f()", "0.8(123.5)"),
                    ("!5f()", "0.79(123.46)"),
                    ("!6f()", "0.789(123.456)"),
                    ("!7f()", "0.7890(123.4560)"),
                ],
            ),
            (
                (-0.789, 123.456),
                [
                    ("f", "-0.789 ± 123.456"),
                    ("!1f", "0 ± 100"),
                    ("!2f", "0 ± 120"),
                    ("!3f", "-1 ± 123"),
                    ("!4f", "-0.8 ± 123.5"),
                    ("!5f", "-0.79 ± 123.46"),
                    ("!6f", "-0.789 ± 123.456"),
                    ("!7f", "-0.7890 ± 123.4560"),
                    ("!1f()", "0(100)"),
                    ("!2f()", "0(120)"),
                    ("!3f()", "-1(123)"),
                    ("!4f()", "-0.8(123.5)"),
                    ("!5f()", "-0.79(123.46)"),
                    ("!6f()", "-0.789(123.456)"),
                    ("!7f()", "-0.7890(123.4560)"),
                ],
            ),
        ]

        self.run_val_unc_fsml_cases(cases_list)

    def test_scientific(self):
        cases_list = [
            (
                (123.456, 0.789),
                [
                    ("e", "(1.23456 ± 0.00789)e+02"),
                    ("!1e", "(1.235 ± 0.008)e+02"),
                    ("!2e", "(1.2346 ± 0.0079)e+02"),
                    ("!3e", "(1.23456 ± 0.00789)e+02"),
                    ("!4e", "(1.234560 ± 0.007890)e+02"),
                    ("!2e()", "(1.2346(79))e+02"),
                ],
            ),
            (
                (0.789, 123.456),
                [
                    ("e", "(0.00789 ± 1.23456)e+02"),
                    ("!1e", "(0 ± 1)e+02"),
                    ("!2e", "(0.0 ± 1.2)e+02"),
                    ("!3e", "(0.01 ± 1.23)e+02"),
                    ("!4e", "(0.008 ± 1.235)e+02"),
                    ("!5e", "(0.0079 ± 1.2346)e+02"),
                    ("!6e", "(0.00789 ± 1.23456)e+02"),
                    ("!7e", "(0.007890 ± 1.234560)e+02"),
                    ("!1e()", "(0(1))e+02"),
                    ("!2e()", "(0.0(1.2))e+02"),
                    ("!3e()", "(0.01(1.23))e+02"),
                    ("!4e()", "(0.008(1.235))e+02"),
                    ("!5e()", "(0.0079(1.2346))e+02"),
                    ("!6e()", "(0.00789(1.23456))e+02"),
                    ("!7e()", "(0.007890(1.234560))e+02"),
                ],
            ),
            (
                (0, 123.456),
                [
                    ("e", "(0.00000 ± 1.23456)e+02"),
                    ("!1e", "(0 ± 1)e+02"),
                    ("!2e", "(0.0 ± 1.2)e+02"),
                    ("!3e", "(0.00 ± 1.23)e+02"),
                    ("!4e", "(0.000 ± 1.235)e+02"),
                    ("!5e", "(0.0000 ± 1.2346)e+02"),
                    ("!6e", "(0.00000 ± 1.23456)e+02"),
                    ("!7e", "(0.000000 ± 1.234560)e+02"),
                    ("!1e()", "(0(1))e+02"),
                    ("!2e()", "(0.0(1.2))e+02"),
                    ("!3e()", "(0.00(1.23))e+02"),
                    ("!4e()", "(0.000(1.235))e+02"),
                    ("!5e()", "(0.0000(1.2346))e+02"),
                    ("!6e()", "(0.00000(1.23456))e+02"),
                    ("!7e()", "(0.000000(1.234560))e+02"),
                ],
            ),
        ]

        self.run_val_unc_fsml_cases(cases_list)

    def test_engineering(self):
        cases_list = [
            (
                (1234.56, 0.789),
                [
                    ("r", "(1.234560 ± 0.000789)e+03"),
                    ("!1r", "(1.2346 ± 0.0008)e+03"),
                    ("!2r", "(1.23456 ± 0.00079)e+03"),
                    ("!3r", "(1.234560 ± 0.000789)e+03"),
                    ("!4r", "(1.2345600 ± 0.0007890)e+03"),
                    ("!2r()", "(1.23456(79))e+03"),
                ],
            ),
            (
                (0.789, 123.456),
                [
                    ("r", "(0.789 ± 123.456)e+00"),
                    ("!1r", "(0 ± 100)e+00"),
                    ("!2r", "(0 ± 120)e+00"),
                    ("!3r", "(1 ± 123)e+00"),
                    ("!4r", "(0.8 ± 123.5)e+00"),
                    ("!5r", "(0.79 ± 123.46)e+00"),
                    ("!6r", "(0.789 ± 123.456)e+00"),
                    ("!7r", "(0.7890 ± 123.4560)e+00"),
                    ("!1r()", "(0(100))e+00"),
                    ("!2r()", "(0(120))e+00"),
                    ("!3r()", "(1(123))e+00"),
                    ("!4r()", "(0.8(123.5))e+00"),
                    ("!5r()", "(0.79(123.46))e+00"),
                    ("!6r()", "(0.789(123.456))e+00"),
                    ("!7r()", "(0.7890(123.4560))e+00"),
                ],
            ),
        ]

        self.run_val_unc_fsml_cases(cases_list)

    def test_engineering_shifted(self):
        cases_list = [
            (
                (123.456, 0.789),
                [
                    ("#r", "(0.123456 ± 0.000789)e+03"),
                    ("#!1r", "(0.1235 ± 0.0008)e+03"),
                    ("#!2r", "(0.12346 ± 0.00079)e+03"),
                    ("#!3r", "(0.123456 ± 0.000789)e+03"),
                    ("#!4r", "(0.1234560 ± 0.0007890)e+03"),
                    ("#!2r()", "(0.12346(79))e+03"),
                ],
            ),
            (
                (0.789, 123.456),
                [
                    ("#r", "(0.000789 ± 0.123456)e+03"),
                    ("#!1r", "(0.0 ± 0.1)e+03"),
                    ("#!2r", "(0.00 ± 0.12)e+03"),
                    ("#!3r", "(0.001 ± 0.123)e+03"),
                    ("#!4r", "(0.0008 ± 0.1235)e+03"),
                    ("#!5r", "(0.00079 ± 0.12346)e+03"),
                    ("#!6r", "(0.000789 ± 0.123456)e+03"),
                    ("#!7r", "(0.0007890 ± 0.1234560)e+03"),
                    ("#!1r()", "(0.0(0.1))e+03"),
                    ("#!2r()", "(0.00(0.12))e+03"),
                    ("#!3r()", "(0.001(0.123))e+03"),
                    ("#!4r()", "(0.0008(0.1235))e+03"),
                    ("#!5r()", "(0.00079(0.12346))e+03"),
                    ("#!6r()", "(0.000789(0.123456))e+03"),
                    ("#!7r()", "(0.0007890(0.1234560))e+03"),
                ],
            ),
        ]

        self.run_val_unc_fsml_cases(cases_list)

    def test_percent(self):
        cases_list = [
            (
                (0.12462, 0.0001),
                [
                    ("%", "(12.46 ± 0.01)%"),
                    ("%()", "(12.46(1))%"),
                ],
            ),
        ]

        self.run_val_unc_fsml_cases(cases_list)

    def test_paren_uncertainty(self):
        cases_list = [
            (
                (123.456, 0.789),
                [
                    ("()", "123.456(789)"),
                    ("e()", "(1.23456(789))e+02"),
                    ("r()", "(123.456(789))e+00"),
                    ("#r()", "(0.123456(789))e+03"),
                    ("ex+1()", "(12.3456(789))e+01"),
                    ("ex-1()", "(1234.56(7.89))e-01"),
                ],
            ),
            (
                (-123.456, 0.789),
                [
                    ("()", "-123.456(789)"),
                    ("e()", "(-1.23456(789))e+02"),
                    ("r()", "(-123.456(789))e+00"),
                    ("#r()", "(-0.123456(789))e+03"),
                    ("ex+1()", "(-12.3456(789))e+01"),
                    ("ex-1()", "(-1234.56(7.89))e-01"),
                ],
            ),
            (
                (0.789, 123.456),
                [
                    ("()", "0.789(123.456)"),
                    ("e()", "(0.00789(1.23456))e+02"),
                    ("r()", "(0.789(123.456))e+00"),
                    ("#r()", "(0.000789(0.123456))e+03"),
                    ("ex+1()", "(0.0789(12.3456))e+01"),
                    ("ex-1()", "(7.89(1234.56))e-01"),
                ],
            ),
            (
                (-0.789, 123.456),
                [
                    ("()", "-0.789(123.456)"),
                    ("e()", "(-0.00789(1.23456))e+02"),
                    ("r()", "(-0.789(123.456))e+00"),
                    ("#r()", "(-0.000789(0.123456))e+03"),
                    ("ex+1()", "(-0.0789(12.3456))e+01"),
                    ("ex-1()", "(-7.89(1234.56))e-01"),
                ],
            ),
        ]

        self.run_val_unc_fsml_cases(cases_list)

    def test_nan_inf(self):
        cases_list = [
            (
                (12.34, NAN),
                [
                    ("", "12.34 ± nan"),
                    ("e", "(1.234 ± nan)e+01"),
                    ("()", "12.34(nan)"),
                    ("e()", "(1.234(nan))e+01"),
                ],
            ),
            (
                (12.34, INF),
                [
                    ("", "12.34 ± inf"),
                    ("e", "(1.234 ± inf)e+01"),
                    ("()", "12.34(inf)"),
                    ("e()", "(1.234(inf))e+01"),
                ],
            ),
            (
                (NAN, 12.34),
                [
                    ("", "nan ± 12.34"),
                    ("e", "(nan ± 1.234)e+01"),
                    ("()", "nan(12.34)"),
                    ("e()", "(nan(1.234))e+01"),
                ],
            ),
            (
                (INF, 12.34),
                [
                    ("", "inf ± 12.34"),
                    ("e", "(inf ± 1.234)e+01"),
                    ("()", "inf(12.34)"),
                    ("e()", "(inf(1.234))e+01"),
                ],
            ),
            (
                (NAN, NAN),
                [
                    ("", "nan ± nan"),
                    ("()", "nan(nan)"),
                    ("e", "nan ± nan"),
                    ("e()", "nan(nan)"),
                ],
            ),
        ]

        self.run_val_unc_fsml_cases(cases_list)

    def test_nan_inf_exp(self):
        cases_list = [
            (
                (NAN, NAN),
                [
                    ("", "nan ± nan"),
                    ("e", "(nan ± nan)e+00"),
                    ("()", "nan(nan)"),
                    ("e()", "(nan(nan))e+00"),
                ],
            ),
        ]
        with GlobalDefaultsContext(nan_inf_exp=True):
            self.run_val_unc_fsml_cases(cases_list)

    def test_capitalization(self):
        cases_list = [
            (
                (123.456, 0.789),
                [
                    ("e", "(1.23456 ± 0.00789)e+02"),
                    ("E", "(1.23456 ± 0.00789)E+02"),
                ],
            ),
            (
                (NAN, NAN),
                [
                    ("e", "(nan ± nan)e+00"),
                    ("E", "(NAN ± NAN)E+00"),
                ],
            ),
            (
                (INF, INF),
                [
                    ("e", "(inf ± inf)e+00"),
                    ("E", "(INF ± INF)E+00"),
                ],
            ),
        ]

        with GlobalDefaultsContext(nan_inf_exp=True):
            self.run_val_unc_fsml_cases(cases_list)

    def test_rounding(self):
        cases_list = [
            (
                (0.0999, 0.0999),
                [
                    ("!1e", "(1 ± 1)e-01"),
                ],
            ),
            (
                (0.0999, 0.999),
                [
                    ("!1e", "(0 ± 1)e+00"),
                ],
            ),
        ]
        self.run_val_unc_fsml_cases(cases_list)

    def test_left_pad(self):
        cases_list = [
            (
                (123.456, 0.789),
                [
                    ("0=0", "123.456 ± 0.789"),
                    ("0= 0", " 123.456 ± 0.789"),
                    (" 0", " 123.456 ± 0.789"),
                    ("+0", "+123.456 ± 0.789"),
                    ("0", "123.456 ± 0.789"),
                    ("0!2f", "123.46 ± 0.79"),
                    ("0=0!2f", "123.46 ± 0.79"),
                    ("0=4", "00123.456 ± 00000.789"),
                    ("0= 4", " 00123.456 ± 00000.789"),
                    (" 4", "   123.456 ±     0.789"),
                    ("+4", "+  123.456 ±     0.789"),
                    ("4", "  123.456 ±     0.789"),
                    ("4!2f", "  123.46 ±     0.79"),
                    ("0=4!2f", "00123.46 ± 00000.79"),
                ],
            ),
            (
                (0.789, 123.456),
                [
                    ("0=0", "0.789 ± 123.456"),
                    ("0= 0", " 0.789 ± 123.456"),
                    (" 0", " 0.789 ± 123.456"),
                    ("+0", "+0.789 ± 123.456"),
                    ("0", "0.789 ± 123.456"),
                    ("0!2f", "0 ± 120"),
                    ("0=0!2f", "0 ± 120"),
                    ("0=4", "00000.789 ± 00123.456"),
                    ("0= 4", " 00000.789 ± 00123.456"),
                    (" 4", "     0.789 ±   123.456"),
                    ("+4", "+    0.789 ±   123.456"),
                    ("4", "    0.789 ±   123.456"),
                    ("4!2f", "    0 ±   120"),
                    ("0=4!2f", "00000 ± 00120"),
                ],
            ),
        ]
        self.run_val_unc_fsml_cases(cases_list)

    def test_prefix(self):
        cases_list = [
            (
                (123.456, 0.789),
                [
                    ("ex+3p", "(0.123456 ± 0.000789) k"),
                    ("ex-3p", "(123456 ± 789) m"),
                ],
            ),
        ]
        self.run_val_unc_fsml_cases(cases_list)
