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
            ((Decimal("inf"), SignModeEnum.ALWAYS), "+"),
            ((Decimal("1"), SignModeEnum.ALWAYS), "+"),
            ((Decimal("-1"), SignModeEnum.ALWAYS), "-"),
            ((Decimal("-inf"), SignModeEnum.ALWAYS), "-"),
            ((Decimal("0"), SignModeEnum.ALWAYS), " "),
            ((Decimal("inf"), SignModeEnum.SPACE), " "),
            ((Decimal("1"), SignModeEnum.SPACE), " "),
            ((Decimal("-1"), SignModeEnum.SPACE), "-"),
            ((Decimal("-inf"), SignModeEnum.SPACE), "-"),
            ((Decimal("0"), SignModeEnum.SPACE), " "),
        ]

        for (num, sign_mode), expected_output in cases:
            kwargs = {"num": num, "sign_mode": sign_mode}
            with self.subTest(**kwargs):
                actual_output = make_strings.get_sign_str(**kwargs)
                self.assertEqual(expected_output, actual_output)
