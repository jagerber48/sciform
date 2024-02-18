import unittest
from decimal import Decimal

from sciform import AutoDigits, Formatter

FloatFormatterCases = list[tuple[float, list[tuple[Formatter, str]]]]


class TestFormatting(unittest.TestCase):
    def run_float_formatter_cases(self, cases_list: FloatFormatterCases):
        for num, formats_list in cases_list:
            for formatter, expected_num_str in formats_list:
                num_str = formatter(num)
                with self.subTest(
                    num=num,
                    expected_num_str=expected_num_str,
                    actual_num_str=num_str,
                ):
                    self.assertEqual(num_str, expected_num_str)

    def test_superscript(self):
        cases_list = [
            (
                789,
                [
                    (
                        Formatter(exp_mode="scientific", superscript=True),
                        "7.89×10²",
                    ),
                ],
            ),
            # Superscript in prefix mode when there's no replacement
            (
                789,
                [
                    (
                        Formatter(
                            exp_mode="scientific",
                            exp_format="prefix",
                            superscript=True,
                        ),
                        "7.89×10²",
                    ),
                ],
            ),
            (
                1024,
                [
                    (Formatter(exp_mode="binary", superscript=True), "1×2¹⁰"),
                ],
            ),
        ]

        self.run_float_formatter_cases(cases_list)

    def test_left_pad_and_separators(self):
        cases_list = [
            (
                123456789.654321,
                [
                    (
                        Formatter(
                            upper_separator="_",
                            lower_separator="_",
                            left_pad_char="0",
                            left_pad_dec_place=14,
                        ),
                        "000_000_123_456_789.654_321",
                    ),
                    (
                        Formatter(
                            upper_separator="_",
                            lower_separator="_",
                            left_pad_char=0,
                            left_pad_dec_place=14,
                        ),
                        "000_000_123_456_789.654_321",
                    ),
                    (
                        Formatter(
                            upper_separator="_",
                            lower_separator="_",
                            left_pad_char=" ",
                            left_pad_dec_place=14,
                        ),
                        "      123_456_789.654_321",
                    ),
                ],
            ),
            (
                4567899.7654321,
                [
                    (
                        Formatter(
                            upper_separator="_",
                            lower_separator="_",
                            left_pad_char="0",
                            left_pad_dec_place=14,
                        ),
                        "000_000_004_567_899.765_432_1",
                    ),
                    (
                        Formatter(
                            upper_separator="_",
                            lower_separator="_",
                            left_pad_char=0,
                            left_pad_dec_place=14,
                        ),
                        "000_000_004_567_899.765_432_1",
                    ),
                    (
                        Formatter(
                            upper_separator="_",
                            lower_separator="_",
                            left_pad_char=" ",
                            left_pad_dec_place=14,
                        ),
                        "        4_567_899.765_432_1",
                    ),
                ],
            ),
        ]

        self.run_float_formatter_cases(cases_list)

    def test_nan(self):
        cases_list = [
            (
                float("nan"),
                [
                    (Formatter(sign_mode="-"), "nan"),
                    (Formatter(sign_mode="+"), " nan"),
                    (Formatter(sign_mode=" "), " nan"),
                    (Formatter(exp_mode="percent"), "nan"),
                    (Formatter(exp_mode="percent", nan_inf_exp=True), "(nan)%"),
                ],
            ),
            (
                float("-nan"),
                [
                    (Formatter(sign_mode="-"), "nan"),
                    (Formatter(sign_mode="+"), " nan"),
                    (Formatter(sign_mode=" "), " nan"),
                    (Formatter(exp_mode="percent"), "nan"),
                    (Formatter(exp_mode="percent", nan_inf_exp=True), "(nan)%"),
                ],
            ),
        ]

        self.run_float_formatter_cases(cases_list)

    def test_inf(self):
        cases_list = [
            (
                float("inf"),
                [
                    (Formatter(sign_mode="-"), "inf"),
                    (Formatter(sign_mode="+"), "+inf"),
                    (Formatter(sign_mode=" "), " inf"),
                    (Formatter(exp_mode="percent", nan_inf_exp=False), "inf"),
                    (Formatter(exp_mode="percent", nan_inf_exp=True), "(inf)%"),
                ],
            ),
            (
                float("-inf"),
                [
                    (Formatter(sign_mode="-"), "-inf"),
                    (Formatter(sign_mode="+"), "-inf"),
                    (Formatter(sign_mode=" "), "-inf"),
                    (Formatter(exp_mode="percent", nan_inf_exp=False), "-inf"),
                    (Formatter(exp_mode="percent", nan_inf_exp=True), "(-inf)%"),
                ],
            ),
        ]
        self.run_float_formatter_cases(cases_list)

    def test_zero(self):
        cases_list = [
            (
                float("+0"),
                [
                    (Formatter(sign_mode="-"), "0"),
                    (Formatter(sign_mode="+"), " 0"),
                    (Formatter(sign_mode=" "), " 0"),
                    (Formatter(exp_mode="percent", nan_inf_exp=False), "0%"),
                ],
            ),
            (
                float("-0"),
                [
                    (Formatter(sign_mode="-"), "0"),
                    (Formatter(sign_mode="+"), " 0"),
                    (Formatter(sign_mode=" "), " 0"),
                    (Formatter(exp_mode="percent", nan_inf_exp=False), "0%"),
                ],
            ),
        ]
        self.run_float_formatter_cases(cases_list)

    def test_parts_per_exp(self):
        cases_list = [
            (
                123e-3,
                [
                    (
                        Formatter(
                            exp_mode="scientific",
                            exp_val=3,
                            exp_format="parts_per",
                        ),
                        "0.000123e+03",
                    ),
                    (
                        Formatter(
                            exp_mode="scientific",
                            exp_val=0,
                            exp_format="parts_per",
                        ),
                        "0.123",
                    ),
                    (
                        Formatter(
                            exp_mode="scientific",
                            exp_val=-3,
                            exp_format="parts_per",
                            add_ppth_form=True,
                        ),
                        "123 ppth",
                    ),
                    (
                        Formatter(
                            exp_mode="scientific",
                            exp_val=-6,
                            exp_format="parts_per",
                        ),
                        "123000 ppm",
                    ),
                    (
                        Formatter(
                            exp_mode="scientific",
                            exp_val=-2,
                            exp_format="parts_per",
                        ),
                        "12.3e-02",
                    ),
                ],
            ),
            (
                123e-9,
                [
                    (
                        Formatter(exp_mode="engineering", exp_format="parts_per"),
                        "123 ppb",
                    ),
                    (
                        Formatter(
                            exp_mode="engineering",
                            exp_format="parts_per",
                            extra_parts_per_forms={-9: None, -12: "ppb"},
                        ),
                        "123e-09",
                    ),
                ],
            ),
            (
                123e-12,
                [
                    (
                        Formatter(exp_mode="engineering", exp_format="parts_per"),
                        "123 ppt",
                    ),
                    (
                        Formatter(
                            exp_mode="engineering",
                            exp_format="parts_per",
                            extra_parts_per_forms={-9: None, -12: "ppb"},
                        ),
                        "123 ppb",
                    ),
                ],
            ),
        ]

        self.run_float_formatter_cases(cases_list)

    def test_no_options(self):
        formatter = Formatter()
        self.assertEqual(formatter(42), "42")

    def test_dec_place_auto_round(self):
        formatter = Formatter(round_mode="dec_place", ndigits=AutoDigits)
        self.assertEqual(formatter(123.456), "123.456")

    def test_pdg_sig_figs(self):
        cases_list = [
            (
                6789,
                [
                    (
                        Formatter(pdg_sig_figs=True, ndigits=AutoDigits),
                        "6789",
                    ),
                    (
                        Formatter(pdg_sig_figs=True, ndigits=5),
                        "6789.0",
                    ),
                    (
                        Formatter(pdg_sig_figs=False, ndigits=AutoDigits),
                        "6789",
                    ),
                    (
                        Formatter(pdg_sig_figs=False, ndigits=5),
                        "6789.0",
                    ),
                ],
            ),
        ]

        self.run_float_formatter_cases(cases_list)

    def test_decimal_normalization(self):
        formatter = Formatter(ndigits=AutoDigits)
        self.assertEqual(formatter(Decimal("1.0")), formatter(Decimal("1.00")))
