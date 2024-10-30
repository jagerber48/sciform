import unittest
from decimal import Decimal
from typing import List, Tuple

from sciform import Formatter
from sciform.format_utils import Number

ValUncFormatterCases = List[Tuple[Tuple[Number, Number], List[Tuple[Formatter, str]]]]


class TestValUncFormatter(unittest.TestCase):
    def run_val_unc_formatter_cases(self, cases_list: ValUncFormatterCases):
        for (val, unc), formatter_cases in cases_list:
            for formatter, expected_output in formatter_cases:
                actual_output = formatter(val, unc)
                with self.subTest(
                    value=val,
                    uncertainty=unc,
                    expected_output=expected_output,
                    actual_output=actual_output,
                ):
                    self.assertEqual(expected_output, actual_output)

    def test_paren_uncertainty(self):
        cases_list = [
            (
                (123.456, 0.789),
                [
                    (Formatter(paren_uncertainty=True), "123.456(789)"),
                    (
                        Formatter(exp_mode="scientific", paren_uncertainty=True),
                        "1.23456(789)e+02",
                    ),
                    (
                        Formatter(exp_mode="engineering", paren_uncertainty=True),
                        "123.456(789)e+00",
                    ),
                    (
                        Formatter(
                            exp_mode="engineering_shifted",
                            paren_uncertainty=True,
                        ),
                        "0.123456(789)e+03",
                    ),
                    (
                        Formatter(
                            exp_mode="scientific",
                            exp_val=+1,
                            paren_uncertainty=True,
                        ),
                        "12.3456(789)e+01",
                    ),
                    (
                        Formatter(
                            exp_mode="scientific",
                            exp_val=-1,
                            paren_uncertainty=True,
                        ),
                        "1234.56(7.89)e-01",
                    ),
                ],
            ),
        ]

        self.run_val_unc_formatter_cases(cases_list)

    def test_paren_unc_invalid_unc(self):
        cases_list = [
            (
                (123, 0),
                [
                    (Formatter(paren_uncertainty=True), "123(0)"),
                ],
            ),
            (
                (-123, 0),
                [
                    (Formatter(paren_uncertainty=True), "-123(0)"),
                ],
            ),
            (
                (123, float("nan")),
                [
                    (Formatter(paren_uncertainty=True), "123(nan)"),
                ],
            ),
            (
                (123, float("inf")),
                [
                    (Formatter(paren_uncertainty=True), "123(inf)"),
                ],
            ),
            (
                (0, 0),
                [
                    (Formatter(paren_uncertainty=True), "0(0)"),
                    (Formatter(paren_uncertainty=True, ndigits=3), "0(0)"),
                ],
            ),
            (
                (0, float("inf")),
                [
                    (Formatter(paren_uncertainty=True), "0(inf)"),
                    (Formatter(paren_uncertainty=True, ndigits=3), "0(inf)"),
                ],
            ),
        ]

        self.run_val_unc_formatter_cases(cases_list)

    def test_prefix(self):
        cases_list = [
            (
                (123.456, 0.789),
                [
                    (
                        Formatter(
                            paren_uncertainty=True,
                            exp_mode="engineering",
                            exp_format="prefix",
                        ),
                        "123.456(789)",
                    ),
                    (
                        Formatter(
                            paren_uncertainty=True,
                            exp_mode="engineering_shifted",
                            exp_format="prefix",
                        ),
                        "0.123456(789) k",
                    ),
                ],
            ),
            (
                (123456, 789),
                [
                    (
                        Formatter(
                            paren_uncertainty=True,
                            exp_mode="fixed_point",
                            exp_format="prefix",
                        ),
                        "123456(789)",
                    ),
                    (
                        Formatter(
                            paren_uncertainty=True,
                            exp_mode="engineering",
                            exp_format="prefix",
                        ),
                        "123.456(789) k",
                    ),
                    (
                        Formatter(
                            paren_uncertainty=True,
                            exp_mode="engineering_shifted",
                            exp_format="prefix",
                        ),
                        "0.123456(789) M",
                    ),
                ],
            ),
            (
                (123456e-9, 789e-9),
                [
                    (
                        Formatter(
                            paren_uncertainty=True,
                            exp_mode="engineering",
                            exp_format="parts_per",
                        ),
                        "123.456(789) ppm",
                    ),
                    (
                        Formatter(
                            paren_uncertainty=True,
                            exp_mode="engineering",
                            exp_format="prefix",
                        ),
                        "123.456(789) μ",
                    ),
                    (
                        Formatter(
                            paren_uncertainty=True,
                            exp_mode="engineering_shifted",
                            exp_format="parts_per",
                            add_ppth_form=True,
                        ),
                        "0.123456(789) ppth",
                    ),
                ],
            ),
            (
                (1.23, 0.1),
                [
                    (
                        Formatter(
                            exp_mode="scientific",
                            exp_format="parts_per",
                        ),
                        "1.2 ± 0.1",
                    ),
                ],
            ),
        ]

        self.run_val_unc_formatter_cases(cases_list)

    def test_percent(self):
        cases_list = [
            (
                (0.123_456_78, 0.000_002_55),
                [
                    (
                        Formatter(exp_mode="percent", lower_separator="_"),
                        "(12.345_678 ± 0.000_255)%",
                    ),
                    (
                        Formatter(
                            exp_mode="percent",
                            paren_uncertainty=True,
                            lower_separator="_",
                        ),
                        "12.345_678(255)%",
                    ),
                ],
            ),
        ]

        self.run_val_unc_formatter_cases(cases_list)

    def test_pm_whitespace(self):
        cases_list = [
            (
                (123.456, 0.789),
                [
                    (Formatter(pm_whitespace=True), "123.456 ± 0.789"),
                    (Formatter(pm_whitespace=False), "123.456±0.789"),
                ],
            ),
        ]

        self.run_val_unc_formatter_cases(cases_list)

    def test_superscript(self):
        cases_list = [
            (
                (789, 0.01),
                [
                    (
                        Formatter(exp_mode="scientific", superscript=True),
                        "(7.8900 ± 0.0001)×10²",
                    ),
                ],
            ),
        ]

        self.run_val_unc_formatter_cases(cases_list)

    def test_pdg(self):
        cases_list = [
            (
                (10, 0.0353),
                [
                    (Formatter(round_mode="pdg"), "10.000 ± 0.035"),
                ],
            ),
            (
                (10, 0.0354),
                [
                    (Formatter(round_mode="pdg"), "10.000 ± 0.035"),
                ],
            ),
            (
                (10, 0.03544),
                [
                    (Formatter(round_mode="pdg"), "10.000 ± 0.035"),
                ],
            ),
            (
                (10, 0.03546),
                [
                    (Formatter(round_mode="pdg"), "10.000 ± 0.035"),
                ],
            ),
            (
                (10, 0.0355),
                [
                    (Formatter(round_mode="pdg"), "10.00 ± 0.04"),
                ],
            ),
            (
                (10, 0.0949),
                [
                    (Formatter(round_mode="pdg"), "10.00 ± 0.09"),
                ],
            ),
            (
                (10, 0.09494),
                [
                    (Formatter(round_mode="pdg"), "10.00 ± 0.09"),
                ],
            ),
            (
                (10, 0.09496),
                [
                    (Formatter(round_mode="pdg"), "10.00 ± 0.09"),
                ],
            ),
            (
                (10, 0.0950),
                [
                    (Formatter(round_mode="pdg"), "10.00 ± 0.10"),
                ],
            ),
            (
                (10, 0.0951),
                [
                    (Formatter(round_mode="pdg"), "10.00 ± 0.10"),
                ],
            ),
            (
                (10, 0.09994),
                [
                    (Formatter(round_mode="pdg"), "10.00 ± 0.10"),
                ],
            ),
            (
                (10, 0.09996),
                [
                    (Formatter(round_mode="pdg"), "10.00 ± 0.10"),
                ],
            ),
            (
                (3141592.7, 1618),
                [
                    (
                        Formatter(
                            exp_mode="engineering",
                            exp_format="prefix",
                            round_mode="pdg",
                        ),
                        "(3.1416 ± 0.0016) M",
                    ),
                ],
            ),
        ]

        self.run_val_unc_formatter_cases(cases_list)

    def test_pdg_invalid_unc(self):
        cases_list = [
            (
                (123, 0),
                [
                    (Formatter(round_mode="pdg"), "120 ± 0"),
                ],
            ),
            (
                (-123, 0),
                [
                    (Formatter(round_mode="pdg"), "-120 ± 0"),
                ],
            ),
            (
                (0, 0),
                [
                    (Formatter(round_mode="pdg"), "0 ± 0"),
                ],
            ),
            (
                (123, float("nan")),
                [
                    (Formatter(round_mode="pdg"), "120 ± nan"),
                ],
            ),
            (
                (-123, float("nan")),
                [
                    (Formatter(round_mode="pdg"), "-120 ± nan"),
                ],
            ),
            (
                (0, float("nan")),
                [
                    (Formatter(round_mode="pdg"), "0 ± nan"),
                ],
            ),
        ]

        self.run_val_unc_formatter_cases(cases_list)

    def test_binary_not_implemented(self):
        formatter = Formatter(exp_mode="binary")
        self.assertRaises(NotImplementedError, formatter, 1024, 32)

    @unittest.expectedFailure
    def test_binary(self):
        """
        This test should pass when binary value/uncertainty formatting
        is implemented
        """
        formatter = Formatter(exp_mode="binary")
        self.assertEqual(formatter(1024, 32), "(1.00000 ± 0.03125)b+10")

    def test_pdg_sig_figs(self):
        cases_list = [
            (
                (7, 0.1234),
                [
                    (
                        Formatter(round_mode="pdg"),
                        "7.00 ± 0.12",
                    ),
                    (
                        Formatter(round_mode="sig_fig", ndigits=5),
                        "7.00000 ± 0.12340",
                    ),
                    (
                        Formatter(round_mode="all"),
                        "7.0000 ± 0.1234",
                    ),
                ],
            ),
        ]

        self.run_val_unc_formatter_cases(cases_list)

    def test_left_pad_matching(self):
        formatter = Formatter(left_pad_matching=True)
        result = formatter(123, 0.123)
        expected_result = "123.000 ±   0.123"
        self.assertEqual(result, expected_result)

    def test_paren_uncertainties_trim_digits(self):
        cases_list = [
            (
                (123, 0.03),
                [
                    (
                        Formatter(
                            paren_uncertainty=True,
                            paren_uncertainty_trim=True,
                        ),
                        "123.00(3)",
                    ),
                    (
                        Formatter(
                            paren_uncertainty=True,
                            paren_uncertainty_trim=False,
                        ),
                        "123.00(0.03)",
                    ),
                ],
            ),
            (
                (123.456789, 0.0012),
                [
                    (
                        Formatter(
                            paren_uncertainty=True,
                            paren_uncertainty_trim=False,
                            lower_separator="_",
                        ),
                        "123.456_8(0.001_2)",
                    ),
                    (
                        # Intermediate separators are stripped.
                        Formatter(
                            paren_uncertainty=True,
                            paren_uncertainty_trim=True,
                            lower_separator="_",
                        ),
                        "123.456_8(12)",
                    ),
                ],
            ),
            (
                (123456, 1234),
                [
                    (
                        Formatter(
                            paren_uncertainty=True,
                            paren_uncertainty_trim=False,
                            upper_separator=" ",
                        ),
                        "123 456(1 234)",
                    ),
                    (
                        # Intermediate separators are stripped.
                        Formatter(
                            paren_uncertainty=True,
                            paren_uncertainty_trim=True,
                            upper_separator=" ",
                        ),
                        "123 456(1234)",
                    ),
                ],
            ),
            (
                (123456, 1234),
                [
                    (
                        Formatter(
                            paren_uncertainty=True,
                            paren_uncertainty_trim=False,
                            upper_separator=",",
                        ),
                        "123,456(1,234)",
                    ),
                    (
                        # Intermediate separators are stripped.
                        Formatter(
                            paren_uncertainty=True,
                            paren_uncertainty_trim=True,
                            upper_separator=",",
                        ),
                        "123,456(1234)",
                    ),
                ],
            ),
            (
                (0.0012, 123.456789),
                [
                    (
                        Formatter(
                            paren_uncertainty=True,
                            paren_uncertainty_trim=False,
                            lower_separator="_",
                        ),
                        "0.001_200(123.456_789)",
                    ),
                    (
                        # No trimming for uncertainty > value
                        Formatter(
                            paren_uncertainty=True,
                            paren_uncertainty_trim=True,
                            lower_separator="_",
                        ),
                        "0.001_200(123.456_789)",
                    ),
                ],
            ),
            (
                (0.0012, 0.0012),
                [
                    (
                        Formatter(
                            paren_uncertainty=True,
                            paren_uncertainty_trim=False,
                            lower_separator="_",
                        ),
                        "0.001_2(0.001_2)",
                    ),
                    (
                        # No trimming for uncertainty == value
                        Formatter(
                            paren_uncertainty=True,
                            paren_uncertainty_trim=True,
                            lower_separator="_",
                        ),
                        "0.001_2(0.001_2)",
                    ),
                ],
            ),
        ]

        self.run_val_unc_formatter_cases(cases_list)

    def test_paren_uncertainties_trim_digits_bipm(self):
        """
        Matches the example in "BIPM guide to the expression of
        uncertainty in measurements" section 7.2.2
        """
        cases_list = [
            (
                (100.02147, 0.00035),
                [
                    (
                        Formatter(paren_uncertainty=False),
                        "100.02147 ± 0.00035",
                    ),
                    (
                        Formatter(
                            paren_uncertainty=True,
                            paren_uncertainty_trim=True,
                        ),
                        "100.02147(35)",
                    ),
                    (
                        Formatter(
                            paren_uncertainty=True,
                            paren_uncertainty_trim=False,
                        ),
                        "100.02147(0.00035)",
                    ),
                    (
                        Formatter(
                            paren_uncertainty=True,
                            paren_uncertainty_trim=False,
                            left_pad_matching=True,
                            left_pad_char="0",
                        ),
                        "100.02147(000.00035)",
                    ),
                ],
            ),
        ]

        self.run_val_unc_formatter_cases(cases_list)

    def test_decimal_normalization(self):
        formatter = Formatter(round_mode="all")
        self.assertEqual(
            formatter(Decimal("100.0"), Decimal("1.00")),
            formatter(Decimal("100"), Decimal("1.0000")),
        )
