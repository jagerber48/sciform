import unittest

from sciform import AutoDigits, Formatter

ValUncFormatterCases = list[tuple[tuple[float, float], list[tuple[Formatter, str]]]]


class TestFormatting(unittest.TestCase):
    def run_val_unc_formatter_cases(self, cases_list: ValUncFormatterCases):
        for (val, unc), formats_list in cases_list:
            for formatter, expected_val_unc_str in formats_list:
                num_str = formatter(val, unc)
                with self.subTest(
                    val=val,
                    unc=unc,
                    expected_num_str=expected_val_unc_str,
                    actual_num_str=num_str,
                ):
                    self.assertEqual(num_str, expected_val_unc_str)

    def test_paren_uncertainty(self):
        cases_list = [
            (
                (123.456, 0.789),
                [
                    (Formatter(paren_uncertainty=True), "123.456(789)"),
                    (
                        Formatter(exp_mode="scientific", paren_uncertainty=True),
                        "(1.23456(789))e+02",
                    ),
                    (
                        Formatter(exp_mode="engineering", paren_uncertainty=True),
                        "(123.456(789))e+00",
                    ),
                    (
                        Formatter(
                            exp_mode="engineering_shifted",
                            paren_uncertainty=True,
                        ),
                        "(0.123456(789))e+03",
                    ),
                    (
                        Formatter(
                            exp_mode="scientific",
                            exp_val=+1,
                            paren_uncertainty=True,
                        ),
                        "(12.3456(789))e+01",
                    ),
                    (
                        Formatter(
                            exp_mode="scientific",
                            exp_val=-1,
                            paren_uncertainty=True,
                        ),
                        "(1234.56(7.89))e-01",
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
                        "(12.345_678(255))%",
                    ),
                ],
            ),
        ]

        self.run_val_unc_formatter_cases(cases_list)

    def test_paren_unc_separators(self):
        cases_list = [
            (
                (123.456, 0.789),
                [
                    (
                        Formatter(
                            exp_mode="scientific",
                            exp_val=-1,
                            paren_uncertainty=True,
                        ),
                        "(1234.56(7.89))e-01",
                    ),
                    (
                        Formatter(
                            exp_mode="scientific",
                            exp_val=-1,
                            paren_uncertainty_trim_separators=True,
                            paren_uncertainty=True,
                        ),
                        "(1234.56(789))e-01",
                    ),
                ],
            ),
            (
                (0.789, 123.456),
                [
                    (
                        Formatter(
                            exp_mode="scientific",
                            exp_val=-1,
                            paren_uncertainty=True,
                        ),
                        "(7.89(1234.56))e-01",
                    ),
                    # Don't remove "embedded" decimal unless val > unc.
                    (
                        Formatter(
                            exp_mode="scientific",
                            exp_val=-1,
                            paren_uncertainty_trim_separators=True,
                            paren_uncertainty=True,
                        ),
                        "(7.89(1234.56))e-01",
                    ),
                ],
            ),
            (
                (1.2, float("nan")),
                [
                    (
                        Formatter(
                            paren_uncertainty=True,
                            paren_uncertainty_trim_separators=True,
                        ),
                        "1.2(nan)",
                    ),
                    (
                        Formatter(
                            paren_uncertainty=True,
                            paren_uncertainty_trim_separators=False,
                        ),
                        "1.2(nan)",
                    ),
                ],
            ),
            (
                (float("nan"), 1.2),
                [
                    (
                        Formatter(
                            paren_uncertainty=True,
                            paren_uncertainty_trim_separators=True,
                        ),
                        "nan(1.2)",
                    ),
                    (
                        Formatter(
                            paren_uncertainty=True,
                            paren_uncertainty_trim_separators=False,
                        ),
                        "nan(1.2)",
                    ),
                ],
            ),
            (
                (float("nan"), float("nan")),
                [
                    (
                        Formatter(
                            paren_uncertainty=True,
                            paren_uncertainty_trim_separators=False,
                        ),
                        "nan(nan)",
                    ),
                    (
                        Formatter(
                            paren_uncertainty=True,
                            paren_uncertainty_trim_separators=True,
                        ),
                        "nan(nan)",
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
                    (Formatter(pdg_sig_figs=True), "10.000 ± 0.035"),
                ],
            ),
            (
                (10, 0.0354),
                [
                    (Formatter(pdg_sig_figs=True), "10.000 ± 0.035"),
                ],
            ),
            (
                (10, 0.0355),
                [
                    (Formatter(pdg_sig_figs=True), "10.00 ± 0.04"),
                ],
            ),
            (
                (10, 0.0949),
                [
                    (Formatter(pdg_sig_figs=True), "10.00 ± 0.09"),
                ],
            ),
            (
                (10, 0.0950),
                [
                    (Formatter(pdg_sig_figs=True), "10.00 ± 0.10"),
                ],
            ),
            (
                (10, 0.0951),
                [
                    (Formatter(pdg_sig_figs=True), "10.00 ± 0.10"),
                ],
            ),
            (
                (3141592.7, 1618),
                [
                    (
                        Formatter(
                            exp_mode="engineering",
                            exp_format="prefix",
                            pdg_sig_figs=True,
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
                    (Formatter(pdg_sig_figs=True), "123 ± 0"),
                ],
            ),
            (
                (-123, 0),
                [
                    (Formatter(pdg_sig_figs=True), "-123 ± 0"),
                ],
            ),
            (
                (0, 0),
                [
                    (Formatter(pdg_sig_figs=True), "0 ± 0"),
                ],
            ),
            (
                (123, float("nan")),
                [
                    (Formatter(pdg_sig_figs=True), "123 ± nan"),
                ],
            ),
            (
                (-123, float("nan")),
                [
                    (Formatter(pdg_sig_figs=True), "-123 ± nan"),
                ],
            ),
            (
                (0, float("nan")),
                [
                    (Formatter(pdg_sig_figs=True), "0 ± nan"),
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
                        Formatter(pdg_sig_figs=True, ndigits=AutoDigits),
                        "7.00 ± 0.12",
                    ),
                    (
                        Formatter(pdg_sig_figs=True, ndigits=5),
                        "7.00 ± 0.12",
                    ),
                    (
                        Formatter(pdg_sig_figs=False, ndigits=AutoDigits),
                        "7.0000 ± 0.1234",
                    ),
                    (
                        Formatter(pdg_sig_figs=False, ndigits=5),
                        "7.00000 ± 0.12340",
                    ),
                ],
            ),
        ]

        self.run_val_unc_formatter_cases(cases_list)

    def test_dec_place_warn(self):
        formatter = Formatter(round_mode="dec_place")
        self.assertWarns(Warning, formatter, 42, 24)

    def test_left_pad_matching(self):
        formatter = Formatter(left_pad_matching=True)
        result = formatter(123, 0.123)
        expected_result = "123.000 ±   0.123"
        self.assertEqual(result, expected_result)

    def test_paren_uncertainties_trim_digits(self):
        """
        Matches the example in "BIPM guide to the expression of
        uncertainty in measurements" section 7.2.2
        """
        val, unc = 100.02147, 0.00035

        with self.subTest():
            formatter = Formatter(paren_uncertainty=False)
            formatted = formatter(val, unc)
            self.assertEqual(formatted, "100.02147 ± 0.00035")

        with self.subTest():
            formatter = Formatter(
                paren_uncertainty=True,
                paren_uncertainty_trim_digits=True,
            )
            formatted = formatter(val, unc)
            self.assertEqual(formatted, "100.02147(35)")

        with self.subTest():
            formatter = Formatter(
                paren_uncertainty=True,
                paren_uncertainty_trim_digits=False,
            )
            formatted = formatter(val, unc)
            self.assertEqual(formatted, "100.02147(0.00035)")

    def test_paren_uncertainties_trimming_options(self):
        val = 123456.654321
        unc = 123.3211

        with self.subTest():
            formatter = Formatter(
                paren_uncertainty=True,
                paren_uncertainty_trim_digits=False,
                paren_uncertainty_trim_separators=False,
                upper_separator=",",
                lower_separator="_",
            )
            formatted = formatter(val, unc)
            self.assertEqual(formatted, "123,456.654_3(123.321_1)")

        with self.subTest():
            formatter = Formatter(
                paren_uncertainty=True,
                paren_uncertainty_trim_digits=True,
                paren_uncertainty_trim_separators=False,
                upper_separator=",",
                lower_separator="_",
            )
            formatted = formatter(val, unc)
            self.assertEqual(formatted, "123,456.654_3(123.321_1)")

        with self.subTest():
            formatter = Formatter(
                paren_uncertainty=True,
                paren_uncertainty_trim_digits=True,
                paren_uncertainty_trim_separators=True,
                upper_separator=",",
                lower_separator="_",
            )
            formatted = formatter(val, unc)
            self.assertEqual(formatted, "123,456.654_3(1233211)")
