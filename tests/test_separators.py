import unittest

from sciform import Formatter

FloatFormatterCases = list[tuple[float, list[tuple[Formatter, str]]]]
ValUncFormatterCases = list[tuple[tuple[float, float], list[tuple[Formatter, str]]]]


class TestSeparators(unittest.TestCase):
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

    def test_val_separators(self):
        cases_list = [
            (
                123456.654321,
                [
                    (
                        Formatter(),
                        "123456.654321",
                    ),
                    (
                        Formatter(upper_separator=","),
                        "123,456.654321",
                    ),
                    (
                        Formatter(
                            upper_separator=",",
                            decimal_separator=".",
                            lower_separator=" ",
                        ),
                        "123,456.654 321",
                    ),
                    (
                        Formatter(
                            upper_separator=",",
                            decimal_separator=".",
                            lower_separator="_",
                        ),
                        "123,456.654_321",
                    ),
                    (
                        Formatter(
                            upper_separator="_",
                            decimal_separator=".",
                            lower_separator="_",
                        ),
                        "123_456.654_321",
                    ),
                    (
                        Formatter(
                            upper_separator=" ",
                            decimal_separator=".",
                            lower_separator=" ",
                        ),
                        "123 456.654 321",
                    ),
                    (
                        Formatter(
                            upper_separator="",
                            decimal_separator=".",
                            lower_separator="",
                        ),
                        "123456.654321",
                    ),
                    (
                        Formatter(
                            upper_separator=".",
                            decimal_separator=",",
                        ),
                        "123.456,654321",
                    ),
                    (
                        Formatter(
                            upper_separator=".",
                            decimal_separator=",",
                            lower_separator=" ",
                        ),
                        "123.456,654 321",
                    ),
                    (
                        Formatter(
                            upper_separator=".",
                            decimal_separator=",",
                            lower_separator="_",
                        ),
                        "123.456,654_321",
                    ),
                    (
                        Formatter(
                            upper_separator="_",
                            decimal_separator=",",
                            lower_separator="_",
                        ),
                        "123_456,654_321",
                    ),
                    (
                        Formatter(
                            upper_separator=" ",
                            decimal_separator=",",
                            lower_separator=" ",
                        ),
                        "123 456,654 321",
                    ),
                ],
            ),
            (
                12345.54321,
                [
                    (
                        Formatter(),
                        "12345.54321",
                    ),
                    (
                        Formatter(
                            upper_separator=",",
                        ),
                        "12,345.54321",
                    ),
                    (
                        Formatter(
                            upper_separator=",",
                            decimal_separator=".",
                            lower_separator=" ",
                        ),
                        "12,345.543 21",
                    ),
                    (
                        Formatter(
                            upper_separator=",",
                            decimal_separator=".",
                            lower_separator="_",
                        ),
                        "12,345.543_21",
                    ),
                    (
                        Formatter(
                            upper_separator="_",
                            decimal_separator=".",
                            lower_separator="_",
                        ),
                        "12_345.543_21",
                    ),
                    (
                        Formatter(
                            upper_separator=" ",
                            decimal_separator=".",
                            lower_separator=" ",
                        ),
                        "12 345.543 21",
                    ),
                    (
                        Formatter(
                            upper_separator="",
                            decimal_separator=".",
                            lower_separator="",
                        ),
                        "12345.54321",
                    ),
                    (
                        Formatter(
                            upper_separator=".",
                            decimal_separator=",",
                        ),
                        "12.345,54321",
                    ),
                    (
                        Formatter(
                            upper_separator=".",
                            decimal_separator=",",
                            lower_separator=" ",
                        ),
                        "12.345,543 21",
                    ),
                    (
                        Formatter(
                            upper_separator=".",
                            decimal_separator=",",
                            lower_separator="_",
                        ),
                        "12.345,543_21",
                    ),
                    (
                        Formatter(
                            upper_separator="_",
                            decimal_separator=",",
                            lower_separator="_",
                        ),
                        "12_345,543_21",
                    ),
                    (
                        Formatter(
                            upper_separator=" ",
                            decimal_separator=",",
                            lower_separator=" ",
                        ),
                        "12 345,543 21",
                    ),
                ],
            ),
            (
                1234567.7654321,
                [
                    (
                        Formatter(),
                        "1234567.7654321",
                    ),
                    (
                        Formatter(
                            upper_separator=",",
                        ),
                        "1,234,567.7654321",
                    ),
                    (
                        Formatter(
                            upper_separator=",",
                            decimal_separator=".",
                            lower_separator=" ",
                        ),
                        "1,234,567.765 432 1",
                    ),
                    (
                        Formatter(
                            upper_separator=",",
                            decimal_separator=".",
                            lower_separator="_",
                        ),
                        "1,234,567.765_432_1",
                    ),
                    (
                        Formatter(
                            upper_separator="_",
                            decimal_separator=".",
                            lower_separator="_",
                        ),
                        "1_234_567.765_432_1",
                    ),
                    (
                        Formatter(
                            upper_separator=" ",
                            decimal_separator=".",
                            lower_separator=" ",
                        ),
                        "1 234 567.765 432 1",
                    ),
                    (
                        Formatter(
                            upper_separator="",
                            decimal_separator=".",
                            lower_separator="",
                        ),
                        "1234567.7654321",
                    ),
                    (
                        Formatter(
                            upper_separator=".",
                            decimal_separator=",",
                        ),
                        "1.234.567,7654321",
                    ),
                    (
                        Formatter(
                            upper_separator=".",
                            decimal_separator=",",
                            lower_separator=" ",
                        ),
                        "1.234.567,765 432 1",
                    ),
                    (
                        Formatter(
                            upper_separator=".",
                            decimal_separator=",",
                            lower_separator="_",
                        ),
                        "1.234.567,765_432_1",
                    ),
                    (
                        Formatter(
                            upper_separator="_",
                            decimal_separator=",",
                            lower_separator="_",
                        ),
                        "1_234_567,765_432_1",
                    ),
                    (
                        Formatter(
                            upper_separator=" ",
                            decimal_separator=",",
                            lower_separator=" ",
                        ),
                        "1 234 567,765 432 1",
                    ),
                ],
            ),
        ]

        self.run_float_formatter_cases(cases_list)

    def test_val_unc_separators(self):
        cases_list = [
            (
                (123456.654321, 0.000002),
                [
                    (
                        Formatter(
                            ndigits=1,
                            upper_separator=",",
                            decimal_separator=".",
                            lower_separator="_",
                            paren_uncertainty=True,
                        ),
                        "123,456.654_321(2)",
                    ),
                ],
            ),
        ]

        self.run_val_unc_formatter_cases(cases_list)
