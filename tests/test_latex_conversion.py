from __future__ import annotations

import unittest

from sciform import Formatter
from sciform.output_conversion import convert_sciform_format

ValFormatterCases = list[tuple[float, list[tuple[Formatter, str]]]]
ValUncFormatterCases = list[tuple[tuple[float, float], list[tuple[Formatter, str]]]]


class TestLatexConversion(unittest.TestCase):
    def run_direct_conversions(self, cases_list: list[tuple[str, str]]):
        for input_str, expected_str in cases_list:
            converted_str = convert_sciform_format(input_str, "latex")
            with self.subTest(
                input_str=input_str,
                expected_str=expected_str,
                actual_str=converted_str,
            ):
                self.assertEqual(converted_str, expected_str)

    def run_val_formatter_conversions(self, cases_list: ValFormatterCases):
        for val, format_list in cases_list:
            for formatter, expected_output in format_list:
                sciform_output = formatter(val)
                latex_output = sciform_output.as_latex(strip_env_symbs=True)
                with self.subTest(
                    val=val,
                    expected_output=expected_output,
                    actual_output=latex_output,
                ):
                    self.assertEqual(latex_output, expected_output)

    def run_val_unc_formatter_conversions(self, cases_list: ValUncFormatterCases):
        for (val, unc), format_list in cases_list:
            for formatter, expected_output in format_list:
                sciform_output = formatter(val, unc)
                latex_output = sciform_output.as_latex(strip_env_symbs=True)
                with self.subTest(
                    val=val,
                    expected_output=expected_output,
                    actual_output=latex_output,
                ):
                    self.assertEqual(latex_output, expected_output)

    def test_direct_cases(self):
        cases_list = [
            ("6.26070e-04", r"$6.26070\times10^{-4}$"),
            (
                "(0.000000(1.234560))e+02",
                r"$(0.000000(1.234560))\times10^{2}$",
            ),
            ("000_000_004_567_899.765_432_1", r"$000\_000\_004\_567\_899.765\_432\_1$"),
            ("(nan)%", r"$(\text{nan})\%$"),
            ("123000 ppm", r"$123000\:\text{ppm}$"),
            ("0b+00", r"$0\times2^{0}$"),
            ("16.18033E+03", r"$16.18033\times10^{3}$"),
            ("    1.20e+01", r"$\:\:\:\:1.20\times10^{1}$"),
            ("(-INF)E+00", r"$(-\text{INF})\times10^{0}$"),
            (
                "(0.123456(789))e+03",
                r"$(0.123456(789))\times10^{3}$",
            ),
            ("  123.46 ±     0.79", r"$\:\:123.46\:\pm\:\:\:\:\:0.79$"),
            ("(7.8900 ± 0.0001)×10²", r"$(7.8900\:\pm\:0.0001)\times10^{2}$"),
            ("(0.123456 ± 0.000789) k", r"$(0.123456\:\pm\:0.000789)\:\text{k}$"),
        ]

        self.run_direct_conversions(cases_list)

    def test_val_formatter_cases(self):
        cases_list = [
            (
                789,
                [
                    (
                        Formatter(exp_mode="scientific"),
                        r"7.89\times10^{2}",
                    ),
                    (
                        Formatter(
                            exp_mode="scientific",
                            superscript=True,
                        ),
                        r"7.89\times10^{2}",
                    ),
                ],
            ),
            (
                12345,
                [
                    (
                        Formatter(
                            exp_mode="scientific",
                            exp_val=-1,
                            upper_separator="_",
                        ),
                        r"123\_450\times10^{-1}",
                    ),
                    (
                        Formatter(
                            exp_mode="scientific",
                            exp_val=3,
                            exp_format="prefix",
                        ),
                        r"12.345\:\text{k}",
                    ),
                ],
            ),
            (
                1024,
                [
                    (
                        Formatter(exp_mode="binary", exp_val=8),
                        r"4\times2^{8}",
                    ),
                ],
            ),
            (
                float("nan"),
                [
                    (Formatter(exp_mode="percent"), r"\text{nan}"),
                    (
                        Formatter(exp_mode="percent", nan_inf_exp=True),
                        r"(\text{nan})\%",
                    ),
                ],
            ),
        ]

        self.run_val_formatter_conversions(cases_list)

    def test_val_unc_formatter_cases(self):
        cases_list = [
            (
                (12345, 0.2),
                [
                    (
                        Formatter(
                            exp_mode="scientific",
                            exp_val=-1,
                            upper_separator="_",
                        ),
                        r"(123\_450\:\pm\:2)\times10^{-1}",
                    ),
                    (
                        Formatter(
                            exp_mode="scientific",
                            exp_format="prefix",
                            exp_val=3,
                        ),
                        r"(12.3450\:\pm\:0.0002)\:\text{k}",
                    ),
                ],
            ),
            (
                (0.123_456_78, 0.000_002_55),
                [
                    (
                        Formatter(lower_separator="_", exp_mode="percent"),
                        r"(12.345\_678\:\pm\:0.000\_255)\%",
                    ),
                    (
                        Formatter(
                            lower_separator="_",
                            exp_mode="percent",
                            paren_uncertainty=True,
                        ),
                        r"(12.345\_678(255))\%",
                    ),
                ],
            ),
            (
                (314.159e-6, 2.71828e-6),
                [
                    (
                        Formatter(
                            exp_mode="engineering",
                            exp_format="prefix",
                            ndigits=4,
                        ),
                        r"(314.159\:\pm\:2.718)\:\text{\textmu}",
                    ),
                ],
            ),
        ]

        self.run_val_unc_formatter_conversions(cases_list)
