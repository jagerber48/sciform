from __future__ import annotations

import unittest
from decimal import Decimal

from sciform.format_utils import make_strings
from sciform.options.option_types import SignModeEnum


class TestMakeStrings(unittest.TestCase):
    def test_get_sign_str(self):
        cases: list[tuple[tuple[Decimal, SignModeEnum], str]] = [
            ((Decimal("inf"), SignModeEnum.NEGATIVE), ""),
            ((Decimal("1"), SignModeEnum.NEGATIVE), ""),
            ((Decimal("-1"), SignModeEnum.NEGATIVE), "-"),
            ((Decimal("-inf"), SignModeEnum.NEGATIVE), "-"),
            ((Decimal("0"), SignModeEnum.NEGATIVE), ""),
            ((Decimal("nan"), SignModeEnum.NEGATIVE), ""),
            ((Decimal("inf"), SignModeEnum.ALWAYS), "+"),
            ((Decimal("1"), SignModeEnum.ALWAYS), "+"),
            ((Decimal("-1"), SignModeEnum.ALWAYS), "-"),
            ((Decimal("-inf"), SignModeEnum.ALWAYS), "-"),
            ((Decimal("0"), SignModeEnum.ALWAYS), " "),
            ((Decimal("nan"), SignModeEnum.ALWAYS), " "),
            ((Decimal("inf"), SignModeEnum.SPACE), " "),
            ((Decimal("1"), SignModeEnum.SPACE), " "),
            ((Decimal("-1"), SignModeEnum.SPACE), "-"),
            ((Decimal("-inf"), SignModeEnum.SPACE), "-"),
            ((Decimal("0"), SignModeEnum.SPACE), " "),
            ((Decimal("nan"), SignModeEnum.SPACE), " "),
        ]

        for (num, sign_mode), expected_output in cases:
            kwargs = {"num": num, "sign_mode": sign_mode}
            with self.subTest(**kwargs):
                actual_output = make_strings.get_sign_str(**kwargs)
                self.assertEqual(expected_output, actual_output)

    def test_get_pad_str(self):
        cases: list[tuple[tuple[str, int, int], str]] = [
            (("0", 3, 0), ""),
            (("0", 3, 1), ""),
            (("0", 3, 2), ""),
            (("0", 3, 3), ""),
            (("0", 3, 4), "0"),
            (("0", 3, 5), "00"),
            (("0", 3, 6), "000"),
            ((" ", 3, 0), ""),
            ((" ", 3, 1), ""),
            ((" ", 3, 2), ""),
            ((" ", 3, 3), ""),
            ((" ", 3, 4), " "),
            ((" ", 3, 5), "  "),
            ((" ", 3, 6), "   "),
        ]

        for input_options, expected_output in cases:
            left_pad_char, top_dec_place, top_padded_dec_place = input_options
            kwargs = {
                "left_pad_char": left_pad_char,
                "top_dec_place": top_dec_place,
                "top_padded_dec_place": top_padded_dec_place,
            }
            with self.subTest(**kwargs):
                actual_output = make_strings.get_pad_str(**kwargs)
                self.assertEqual(expected_output, actual_output)
