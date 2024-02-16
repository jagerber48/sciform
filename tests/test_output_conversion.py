from __future__ import annotations

import unittest

from sciform import Formatter
from sciform.formatting import FormattedNumber
from sciform.options.conversion import populate_options
from sciform.options.input_options import InputOptions
from sciform.output_conversion import convert_sciform_format

ValFormatterCases = list[
    tuple[float, list[tuple[Formatter, tuple[str, str, str, str]]]]
]
ValUncFormatterCases = list[
    tuple[tuple[float, float], list[tuple[Formatter, tuple[str, str, str, str]]]]
]


class TestLatexConversion(unittest.TestCase):
    def run_direct_conversions(
        self,
        cases_list: list[tuple[str, tuple[str, str, str]]],
    ):
        for input_str, (expected_ascii, expected_html, expected_latex) in cases_list:
            ascii_str = convert_sciform_format(input_str, "ascii")
            with self.subTest(
                input_str=input_str,
                expected_str=expected_ascii,
                actual_str=ascii_str,
            ):
                self.assertEqual(ascii_str, expected_ascii)

            html_str = convert_sciform_format(input_str, "html")
            with self.subTest(
                input_str=input_str,
                expected_str=expected_html,
                actual_str=html_str,
            ):
                self.assertEqual(html_str, expected_html)

            latex_str = convert_sciform_format(input_str, "latex")
            with self.subTest(
                input_str=input_str,
                expected_str=expected_latex,
                actual_str=latex_str,
            ):
                self.assertEqual(latex_str, expected_latex)

    def run_val_formatter_conversions(self, cases_list: ValFormatterCases):
        for val, format_list in cases_list:
            for formatter, expected_outputs in format_list:
                (
                    expected_str,
                    expected_ascii,
                    expected_html,
                    expected_latex,
                ) = expected_outputs
                sciform_output = formatter(val)

                str_output = sciform_output.as_str()
                with self.subTest(
                    val=val,
                    expected_output=expected_str,
                    actual_output=str_output,
                ):
                    self.assertEqual(str_output, expected_str)

                ascii_output = sciform_output.as_ascii()
                with self.subTest(
                    val=val,
                    expected_output=expected_ascii,
                    actual_output=ascii_output,
                ):
                    self.assertEqual(ascii_output, expected_ascii)

                html_output = sciform_output.as_html()
                with self.subTest(
                    val=val,
                    expected_output=expected_html,
                    actual_output=html_output,
                ):
                    self.assertEqual(html_output, expected_html)

                latex_output = sciform_output.as_latex(strip_math_mode=True)
                with self.subTest(
                    val=val,
                    expected_output=expected_latex,
                    actual_output=latex_output,
                ):
                    self.assertEqual(latex_output, expected_latex)

    def run_val_unc_formatter_conversions(self, cases_list: ValUncFormatterCases):
        for (val, unc), format_list in cases_list:
            for formatter, expected_outputs in format_list:
                (
                    expected_str,
                    expected_ascii,
                    expected_html,
                    expected_latex,
                ) = expected_outputs
                sciform_output = formatter(val, unc)

                str_output = sciform_output.as_str()
                with self.subTest(
                    val=val,
                    unc=unc,
                    expected_output=expected_str,
                    actual_output=str_output,
                ):
                    self.assertEqual(str_output, expected_str)

                ascii_output = sciform_output.as_ascii()
                with self.subTest(
                    val=val,
                    unc=unc,
                    expected_output=expected_ascii,
                    actual_output=ascii_output,
                ):
                    self.assertEqual(ascii_output, expected_ascii)

                html_output = sciform_output.as_html()
                with self.subTest(
                    val=val,
                    unc=unc,
                    expected_output=expected_html,
                    actual_output=html_output,
                ):
                    self.assertEqual(html_output, expected_html)

                latex_output = sciform_output.as_latex(strip_math_mode=True)
                with self.subTest(
                    val=val,
                    unc=unc,
                    expected_output=expected_latex,
                    actual_output=latex_output,
                ):
                    self.assertEqual(latex_output, expected_latex)

    def test_direct_cases(self):
        cases_list = [
            (
                "6.26070e-04",
                (
                    "6.26070e-04",
                    "6.26070×10<sup>-4</sup>",
                    r"$6.26070\times10^{-4}$",
                ),
            ),
            (
                "0.000000(1.234560)e+02",
                (
                    "0.000000(1.234560)e+02",
                    "0.000000(1.234560)×10<sup>2</sup>",
                    r"$0.000000(1.234560)\times10^{2}$",
                ),
            ),
            (
                "000_000_004_567_899.765_432_1",
                (
                    "000_000_004_567_899.765_432_1",
                    "000_000_004_567_899.765_432_1",
                    r"$000\_000\_004\_567\_899.765\_432\_1$",
                ),
            ),
            (
                "(nan)%",
                (
                    "(nan)%",
                    "(nan)%",
                    r"$(\text{nan})\%$",
                ),
            ),
            (
                "123000 ppm",
                (
                    "123000 ppm",
                    "123000 ppm",
                    r"$123000\:\text{ppm}$",
                ),
            ),
            (
                "0b+00",
                (
                    "0b+00",
                    "0×2<sup>0</sup>",
                    r"$0\times2^{0}$",
                ),
            ),
            (
                "16.18033E+03",
                (
                    "16.18033E+03",
                    "16.18033×10<sup>3</sup>",
                    r"$16.18033\times10^{3}$",
                ),
            ),
            (
                "    1.20e+01",
                (
                    "    1.20e+01",
                    "    1.20×10<sup>1</sup>",
                    r"$\:\:\:\:1.20\times10^{1}$",
                ),
            ),
            (
                "(-INF)E+00",
                (
                    "(-INF)E+00",
                    "(-INF)×10<sup>0</sup>",
                    r"$(-\text{INF})\times10^{0}$",
                ),
            ),
            (
                "0.123456(789)e+03",
                (
                    "0.123456(789)e+03",
                    "0.123456(789)×10<sup>3</sup>",
                    r"$0.123456(789)\times10^{3}$",
                ),
            ),
            (
                "  123.46 ±     0.79",
                (
                    "  123.46 +/-     0.79",
                    "  123.46 ±     0.79",
                    r"$\:\:123.46\:\pm\:\:\:\:\:0.79$",
                ),
            ),
            (
                "(7.8900 ± 0.0001)×10²",
                (
                    "(7.8900 +/- 0.0001)e+02",
                    "(7.8900 ± 0.0001)×10<sup>2</sup>",
                    r"$(7.8900\:\pm\:0.0001)\times10^{2}$",
                ),
            ),
            (
                "(7.8900 ± 0.0001)×10⁻²",
                (
                    "(7.8900 +/- 0.0001)e-02",
                    "(7.8900 ± 0.0001)×10<sup>-2</sup>",
                    r"$(7.8900\:\pm\:0.0001)\times10^{-2}$",
                ),
            ),
            (
                "7.8900(0.0001)×10⁻²",
                (
                    "7.8900(0.0001)e-02",
                    "7.8900(0.0001)×10<sup>-2</sup>",
                    r"$7.8900(0.0001)\times10^{-2}$",
                ),
            ),
            (
                "(0.123456 ± 0.000789) k",
                (
                    "(0.123456 +/- 0.000789) k",
                    "(0.123456 ± 0.000789) k",
                    r"$(0.123456\:\pm\:0.000789)\:\text{k}$",
                ),
            ),
        ]

        self.run_direct_conversions(cases_list)

    def test_val_formatter_cases(self):
        cases_list = [
            (
                789,
                [
                    (
                        Formatter(exp_mode="scientific"),
                        (
                            "7.89e+02",
                            "7.89e+02",
                            "7.89×10<sup>2</sup>",
                            r"7.89\times10^{2}",
                        ),
                    ),
                    (
                        Formatter(
                            exp_mode="scientific",
                            superscript=True,
                        ),
                        (
                            "7.89×10²",
                            "7.89e+02",
                            "7.89×10<sup>2</sup>",
                            r"7.89\times10^{2}",
                        ),
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
                        (
                            "123_450e-01",
                            "123_450e-01",
                            "123_450×10<sup>-1</sup>",
                            r"123\_450\times10^{-1}",
                        ),
                    ),
                    (
                        Formatter(
                            exp_mode="scientific",
                            exp_val=3,
                            exp_format="prefix",
                        ),
                        (
                            "12.345 k",
                            "12.345 k",
                            "12.345 k",
                            r"12.345\:\text{k}",
                        ),
                    ),
                ],
            ),
            (
                1024,
                [
                    (
                        Formatter(exp_mode="binary", exp_val=8),
                        (
                            "4b+08",
                            "4b+08",
                            "4×2<sup>8</sup>",
                            r"4\times2^{8}",
                        ),
                    ),
                ],
            ),
            (
                float("nan"),
                [
                    (
                        Formatter(exp_mode="percent"),
                        (
                            "nan",
                            "nan",
                            "nan",
                            r"\text{nan}",
                        ),
                    ),
                    (
                        Formatter(exp_mode="percent", nan_inf_exp=True),
                        (
                            "(nan)%",
                            "(nan)%",
                            "(nan)%",
                            r"(\text{nan})\%",
                        ),
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
                        (
                            "(123_450 ± 2)e-01",
                            "(123_450 +/- 2)e-01",
                            "(123_450 ± 2)×10<sup>-1</sup>",
                            r"(123\_450\:\pm\:2)\times10^{-1}",
                        ),
                    ),
                    (
                        Formatter(
                            exp_mode="scientific",
                            exp_format="prefix",
                            exp_val=3,
                        ),
                        (
                            "(12.3450 ± 0.0002) k",
                            "(12.3450 +/- 0.0002) k",
                            "(12.3450 ± 0.0002) k",
                            r"(12.3450\:\pm\:0.0002)\:\text{k}",
                        ),
                    ),
                ],
            ),
            (
                (0.123_456_78, 0.000_002_55),
                [
                    (
                        Formatter(lower_separator="_", exp_mode="percent"),
                        (
                            "(12.345_678 ± 0.000_255)%",
                            "(12.345_678 +/- 0.000_255)%",
                            "(12.345_678 ± 0.000_255)%",
                            r"(12.345\_678\:\pm\:0.000\_255)\%",
                        ),
                    ),
                    (
                        Formatter(
                            lower_separator="_",
                            exp_mode="percent",
                            paren_uncertainty=True,
                        ),
                        (
                            "12.345_678(255)%",
                            "12.345_678(255)%",
                            "12.345_678(255)%",
                            r"12.345\_678(255)\%",
                        ),
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
                        (
                            "(314.159 ± 2.718) μ",
                            "(314.159 +/- 2.718) u",
                            "(314.159 ± 2.718) μ",
                            r"(314.159\:\pm\:2.718)\:\text{\textmu}",
                        ),
                    ),
                ],
            ),
        ]

        self.run_val_unc_formatter_conversions(cases_list)

    def test_special_repr_output(self):
        cases_list = [
            "6.26070e-04",
            "0.000000(1.234560)e+02",
            "000_000_004_567_899.765_432_1",
            "(nan)%",
            "123000 ppm",
            "0b+00",
            "16.18033E+03",
            "    1.20e+01",
            "(-INF)E+00",
            "(0.123456(789))e+03",
            "  123.46 ±     0.79",
            "(7.8900 ± 0.0001)×10²",
            "(7.8900 ± 0.0001)×10⁻²",
            "(0.123456 ± 0.000789) k",
        ]
        for case in cases_list:
            dummy_populated_options = populate_options(InputOptions())
            formatted_number = FormattedNumber(
                case,
                1,
                None,
                dummy_populated_options,
            )
            with self.subTest(
                name="check__repr_html_",
                input_str=case,
            ):
                self.assertEqual(
                    formatted_number._repr_html_(),  # noqa: SLF001
                    formatted_number.as_html(),
                )

            with self.subTest(
                name="check__repr_latex_",
                input_str=case,
            ):
                self.assertEqual(
                    formatted_number._repr_latex_(),  # noqa: SLF001
                    formatted_number.as_latex(strip_math_mode=False),
                )
