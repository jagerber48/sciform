from __future__ import annotations

import unittest

from sciform import sciform_to_latex


class TestLatexConversion(unittest.TestCase):
    def run_latex_conversion_cases(self, cases_list: list[tuple[str, str]]):
        for input_str, expected_str in cases_list:
            converted_str = sciform_to_latex(input_str)
            with self.subTest(
                input_str=input_str,
                expected_str=expected_str,
                actual_str=converted_str,
            ):
                self.assertEqual(converted_str, expected_str)

    def test_cases(self):
        cases_list = [
            ("6.26070e-04", r"6.26070\times10^{-4}"),
            (
                "(0.000000(1.234560))e+02",
                r"\left(0.000000\left(1.234560\right)\right)\times10^{2}",
            ),
            ("000_000_004_567_899.765_432_1", r"000\_000\_004\_567\_899.765\_432\_1"),
            ("(nan)%", r"\left(\text{nan}\right)\%"),
            ("123000 ppm", r"123000\:\text{ppm}"),
            ("0b+00", r"0\times2^{0}"),
            ("16.18033E+03", r"16.18033\times10^{3}"),
            ("    1.20e+01", r"\:\:\:\:1.20\times10^{1}"),
            ("(-INF)E+00", r"\left(-\text{INF}\right)\times10^{0}"),
            (
                "(0.123456(789))e+03",
                r"\left(0.123456\left(789\right)\right)\times10^{3}",
            ),
            ("  123.46 ±     0.79", r"\:\:123.46\:\pm\:\:\:\:\:0.79"),
            ("(7.8900 ± 0.0001)×10²", r"\left(7.8900\:\pm\:0.0001\right)\times10^{2}"),
        ]

        self.run_latex_conversion_cases(cases_list)
