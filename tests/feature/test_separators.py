import unittest
from typing import List, Tuple

from sciform import Formatter
from sciform.format_utils import Number

FloatFormatterCases = List[Tuple[Number, List[Tuple[Formatter, str]]]]
ValUncFormatterCases = List[Tuple[Tuple[Number, Number], List[Tuple[Formatter, str]]]]


class TestSeparators(unittest.TestCase):
    def run_val_formatter_cases(self, cases_list: FloatFormatterCases):
        for number, formatter_cases in cases_list:
            for formatter, expected_output in formatter_cases:
                actual_output = formatter(number)
                with self.subTest(
                    number=number,
                    expected_output=expected_output,
                    actual_output=actual_output,
                ):
                    self.assertEqual(expected_output, actual_output)

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

        self.run_val_formatter_cases(cases_list)

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
