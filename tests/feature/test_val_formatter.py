import unittest
from decimal import Decimal, localcontext
from typing import List, Tuple

from sciform import Formatter
from sciform.format_utils import Number

ValFormatterCases = List[Tuple[Number, List[Tuple[Formatter, str]]]]


class TestValFormatter(unittest.TestCase):
    def run_val_formatter_cases(self, cases_list: ValFormatterCases):
        for number, formatter_cases in cases_list:
            for formatter, expected_output in formatter_cases:
                actual_output = formatter(number)
                with self.subTest(
                    number=number,
                    expected_output=expected_output,
                    actual_output=actual_output,
                ):
                    self.assertEqual(expected_output, actual_output)

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

        self.run_val_formatter_cases(cases_list)

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

        self.run_val_formatter_cases(cases_list)

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

        self.run_val_formatter_cases(cases_list)

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
        self.run_val_formatter_cases(cases_list)

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
        self.run_val_formatter_cases(cases_list)

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

        self.run_val_formatter_cases(cases_list)

    def test_no_options(self):
        formatter = Formatter()
        self.assertEqual(formatter(42), "42")

    def test_dec_place_auto_round(self):
        formatter = Formatter(round_mode="all")
        self.assertEqual(formatter(123.456), "123.456")

    def test_pdg_sig_figs(self):
        cases_list = [
            (
                6789,
                [
                    (
                        Formatter(round_mode="pdg"),
                        "7000",
                    ),
                    (
                        Formatter(round_mode="sig_fig", ndigits=5),
                        "6789.0",
                    ),
                    (
                        Formatter(round_mode="all"),
                        "6789",
                    ),
                ],
            ),
        ]

        self.run_val_formatter_cases(cases_list)

    def test_decimal_normalization(self):
        formatter = Formatter(round_mode="all")
        self.assertEqual(formatter(Decimal("1.0")), formatter(Decimal("1.00")))

    def test_long_decimal(self):
        cases_list = [
            (
                Decimal("6834682610.9043126"),
                [
                    (
                        Formatter(
                            exp_mode="engineering",
                            exp_format="prefix",
                            round_mode="all",
                            upper_separator=" ",
                            lower_separator=" ",
                        ),
                        "6.834 682 610 904 312 6 G",
                    ),
                ],
            ),
            (
                Decimal("123456789987654321.123456789987654321"),
                [
                    (
                        Formatter(
                            exp_mode="fixed_point",
                            round_mode="all",
                        ),
                        "123456789987654321.123456789987654321",
                    ),
                ],
            ),
        ]

        with localcontext() as ctx:
            # Default precision of 28 isn't sufficient for the cases above.
            ctx.prec = 50
            self.run_val_formatter_cases(cases_list)
