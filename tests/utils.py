from unittest import TestCase
from sciform import Formatter

FloatFormatterCases = list[tuple[float, list[tuple[Formatter, str]]]]


def run_float_formatter_cases(test_case: TestCase,
                              cases_list: FloatFormatterCases):
    for num, num_formats in cases_list:
        for formatter, expected_num_str in num_formats:
            snum_str = formatter(num)
            with test_case.subTest(num=num,
                                   expected_num_str=expected_num_str,
                                   actual_num_str=snum_str):
                test_case.assertEqual(snum_str, expected_num_str)
