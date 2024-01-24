from __future__ import annotations

import unittest

from sciform import Formatter, sciform_to_html

ValFormatterCases = list[tuple[float, list[tuple[Formatter, str]]]]
ValUncFormatterCases = list[tuple[tuple[float, float], list[tuple[Formatter, str]]]]


class TestHTMLConversion(unittest.TestCase):
    def run_direct_conversions(self, cases_list: list[tuple[str, str]]):
        for input_str, expected_str in cases_list:
            converted_str = sciform_to_html(input_str)
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
                html_output = sciform_output.as_html()
                with self.subTest(
                    val=val,
                    expected_output=expected_output,
                    actual_output=html_output,
                ):
                    self.assertEqual(html_output, expected_output)

    def run_val_unc_formatter_conversions(self, cases_list: ValUncFormatterCases):
        for (val, unc), format_list in cases_list:
            for formatter, expected_output in format_list:
                sciform_output = formatter(val, unc)
                html_output = sciform_output.as_html()
                with self.subTest(
                    val=val,
                    expected_output=expected_output,
                    actual_output=html_output,
                ):
                    self.assertEqual(html_output, expected_output)

    def test_direct_cases(self):
        cases_list = [
            ("6.26070e-04", r"6.26070×10<sup>-4</sup>"),
            (
                "(0.000000(1.234560))e+02",
                r"(0.000000(1.234560))×10<sup>2</sup>",
            ),
            ("000_000_004_567_899.765_432_1", r"000_000_004_567_899.765_432_1"),
            ("(nan)%", r"(nan)%"),
            ("123000 ppm", r"123000 ppm"),
            ("0b+00", r"0×2<sup>0</sup>"),
            ("16.18033E+03", r"16.18033×10<sup>3</sup>"),
            ("    1.20e+01", r"    1.20×10<sup>1</sup>"),
            ("(-INF)E+00", r"(-INF)×10<sup>0</sup>"),
            (
                "(0.123456(789))e+03",
                r"(0.123456(789))×10<sup>3</sup>",
            ),
            ("  123.46 ±     0.79", r"  123.46 ±     0.79"),
            ("(7.8900 ± 0.0001)×10²", r"(7.8900 ± 0.0001)×10<sup>2</sup>"),
            ("(0.123456 ± 0.000789) k", r"(0.123456 ± 0.000789) k"),
        ]

        self.run_direct_conversions(cases_list)

    def test_val_formatter_cases(self):
        cases_list = [
            (
                789,
                [
                    (
                        Formatter(exp_mode="scientific"),
                        r"7.89×10<sup>2</sup>",
                    ),
                    (
                        Formatter(
                            exp_mode="scientific",
                            superscript=True,
                        ),
                        r"7.89×10<sup>2</sup>",
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
                        r"123_450×10<sup>-1</sup>",
                    ),
                    (
                        Formatter(
                            exp_mode="scientific",
                            exp_val=3,
                            exp_format="prefix",
                        ),
                        r"12.345 k",
                    ),
                ],
            ),
            (
                1024,
                [
                    (
                        Formatter(exp_mode="binary", exp_val=8),
                        r"4×2<sup>8</sup>",
                    ),
                ],
            ),
            (
                float("nan"),
                [
                    (Formatter(exp_mode="percent"), r"nan"),
                    (
                        Formatter(exp_mode="percent", nan_inf_exp=True),
                        r"(nan)%",
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
                        r"(123_450 ± 2)×10<sup>-1</sup>",
                    ),
                    (
                        Formatter(
                            exp_mode="scientific",
                            exp_format="prefix",
                            exp_val=3,
                        ),
                        r"(12.3450 ± 0.0002) k",
                    ),
                ],
            ),
            (
                (0.123_456_78, 0.000_002_55),
                [
                    (
                        Formatter(lower_separator="_", exp_mode="percent"),
                        r"(12.345_678 ± 0.000_255)%",
                    ),
                    (
                        Formatter(
                            lower_separator="_",
                            exp_mode="percent",
                            paren_uncertainty=True,
                        ),
                        r"(12.345_678(255))%",
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
                        r"(314.159 ± 2.718) μ",
                    ),
                ],
            ),
        ]

        self.run_val_unc_formatter_conversions(cases_list)
