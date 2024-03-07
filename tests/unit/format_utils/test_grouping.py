from __future__ import annotations

import unittest

from sciform.format_utils import grouping


class TestGrouping(unittest.TestCase):
    def test_add_grouping_chars_forward(self):
        cases: list[tuple[tuple[str, str], str]] = [
            (("1", "_"), "1"),
            (("12", "_"), "12"),
            (("123", "_"), "123"),
            (("1234", "_"), "123_4"),
            (("12345", "_"), "123_45"),
            (("123456", "_"), "123_456"),
            (("1234567", "_"), "123_456_7"),
            (("12345678", "_"), "123_456_78"),
            (("1", " "), "1"),
            (("12", " "), "12"),
            (("123", " "), "123"),
            (("1234", " "), "123 4"),
            (("12345", " "), "123 45"),
            (("123456", " "), "123 456"),
            (("1234567", " "), "123 456 7"),
            (("12345678", " "), "123 456 78"),
        ]

        reverse = False
        for (num_str, group_char), expected_output in cases:
            kwargs = {
                "num_str": num_str,
                "group_char": group_char,
                "reverse": reverse,
            }
            actual_output = grouping.add_group_chars(**kwargs)
            with self.subTest(**kwargs):
                self.assertEqual(expected_output, actual_output)

    def test_add_grouping_chars_reverse(self):
        cases: list[tuple[tuple[str, str], str]] = [
            (("1", "_"), "1"),
            (("12", "_"), "12"),
            (("123", "_"), "123"),
            (("1234", "_"), "1_234"),
            (("12345", "_"), "12_345"),
            (("123456", "_"), "123_456"),
            (("1234567", "_"), "1_234_567"),
            (("12345678", "_"), "12_345_678"),
            (("1", " "), "1"),
            (("12", " "), "12"),
            (("123", " "), "123"),
            (("1234", " "), "1 234"),
            (("12345", " "), "12 345"),
            (("123456", " "), "123 456"),
            (("1234567", " "), "1 234 567"),
            (("12345678", " "), "12 345 678"),
        ]

        reverse = True
        for (num_str, group_char), expected_output in cases:
            kwargs = {
                "num_str": num_str,
                "group_char": group_char,
                "reverse": reverse,
            }
            actual_output = grouping.add_group_chars(**kwargs)
            with self.subTest(**kwargs):
                self.assertEqual(expected_output, actual_output)

    def test_add_separators(self):
        cases: list[tuple[str, str]] = [
            ("1", "1"),
            ("12", "12"),
            ("123", "123"),
            ("1234", "1u234"),
            ("12345", "12u345"),
            ("123456", "123u456"),
            ("1234567", "1u234u567"),
            ("1234567.7", "1u234u567d7"),
            ("1234567.76", "1u234u567d76"),
            ("1234567.765", "1u234u567d765"),
            ("1234567.7654", "1u234u567d765l4"),
            ("1234567.76543", "1u234u567d765l43"),
            ("1234567.765432", "1u234u567d765l432"),
            ("1234567.7654321", "1u234u567d765l432l1"),
            ("+   1234567.7654321", "+   1u234u567d765l432l1"),
            ("+0001234567.7654321", "+0u001u234u567d765l432l1"),
            ("    1234567.7654321", "    1u234u567d765l432l1"),
        ]

        separator_cases: list[tuple[str, str, str]] = [
            ("", ".", ""),
            (",", ".", ""),
            (" ", ".", ""),
            ("_", ".", ""),
            ("_", ".", "_"),
            ("_", ".", " "),
            (" ", ".", " "),
            ("", ",", ""),
            (".", ",", ""),
            (" ", ",", ""),
            ("_", ",", ""),
            ("_", ",", "_"),
            ("_", ",", " "),
            (" ", ",", " "),
        ]

        for num_str, pre_expected_ouput in cases:
            for upper_separator, decimal_separator, lower_separator in separator_cases:
                expected_output = pre_expected_ouput
                expected_output = expected_output.replace("u", upper_separator)
                expected_output = expected_output.replace("d", decimal_separator)
                expected_output = expected_output.replace("l", lower_separator)
                kwargs = {
                    "num_str": num_str,
                    "upper_separator": upper_separator,
                    "decimal_separator": decimal_separator,
                    "lower_separator": lower_separator,
                }
                actual_output = grouping.add_separators(**kwargs)
                with self.subTest(**kwargs):
                    self.assertEqual(expected_output, actual_output)
