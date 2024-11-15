from __future__ import annotations

import unittest
from decimal import Decimal
from typing import Any, Dict, Tuple, Union

from sciform.format_utils import exp_translations, exponents
from sciform.options.option_types import ExpFormatEnum, ExpModeEnum, ExpValEnum

GetTranslationDictCase = Tuple[
    Tuple[
        ExpFormatEnum,
        Dict[int, str],
        Dict[int, str],
        Dict[int, str],
    ],
    Dict[int, str],
]
GetStandardExpStrCase = Tuple[Tuple[int, int, bool], str]
GetValUncExpCase = Tuple[
    Tuple[Decimal, Decimal, ExpModeEnum, Union[int, ExpValEnum]],
    int,
]


class TestExponentUtils(unittest.TestCase):
    def test_get_translation_dict_si(self):
        translation_dict = exponents.get_translation_dict(
            ExpFormatEnum.PREFIX,
            extra_si_prefixes={-2: "c", -1: "d", +3: "km", -3: None},
            extra_parts_per_forms={},
        )
        for key, value in exp_translations.val_to_si_dict.items():
            self.assertIn(key, translation_dict)
            if key not in (-3, +3):
                self.assertEqual(value, translation_dict[key])
        self.assertIn(-2, translation_dict)
        self.assertEqual("c", translation_dict[-2])
        self.assertIn(-1, translation_dict)
        self.assertEqual("d", translation_dict[-1])
        self.assertEqual("km", translation_dict[3])
        self.assertEqual(None, translation_dict[-3])

    def test_get_translation_dict_parts_per(self):
        translation_dict = exponents.get_translation_dict(
            ExpFormatEnum.PARTS_PER,
            extra_si_prefixes={},
            extra_parts_per_forms={-3: "ppth", -4: "pptt", -9: None, -12: "ppb"},
        )
        for key, value in exp_translations.val_to_parts_per_dict.items():
            self.assertIn(key, translation_dict)
            if key not in (-9, -12):
                self.assertEqual(value, translation_dict[key])
        self.assertEqual("ppth", translation_dict[-3])
        self.assertIn(-4, translation_dict)
        self.assertEqual("pptt", translation_dict[-4])
        self.assertEqual(None, translation_dict[-9])
        self.assertEqual("ppb", translation_dict[-12])

    def test_get_translation_dict_invalid_format(self):
        self.assertRaises(
            ValueError,
            exponents.get_translation_dict,
            "prefix",
            {},
            {},
        )

    def test_get_standard_exp_str(self):
        cases: list[GetStandardExpStrCase] = [
            ((-111, False), "e-111"),
            ((-15, False), "e-15"),
            ((-2, False), "e-02"),
            ((-1, False), "e-01"),
            ((0, False), "e+00"),
            ((+1, False), "e+01"),
            ((+2, False), "e+02"),
            ((+15, False), "e+15"),
            ((+111, False), "e+111"),
            ((-111, True), "E-111"),
            ((-15, True), "E-15"),
            ((-2, True), "E-02"),
            ((-1, True), "E-01"),
            ((0, True), "E+00"),
            ((+1, True), "E+01"),
            ((+2, True), "E+02"),
            ((+15, True), "E+15"),
            ((+111, True), "E+111"),
        ]

        for (exp_val, capitalize), expected_output in cases:
            actual_output = exponents.get_standard_exp_str(
                exp_val=exp_val,
                capitalize=capitalize,
            )
            with self.subTest(
                exp_val=exp_val,
                capitalize=capitalize,
            ):
                self.assertEqual(expected_output, actual_output)

    def test_get_superscript_exp_str(self):
        cases: list[tuple[tuple[int, int], str]] = [
            (-10, "×10⁻¹⁰"),
            (-1, "×10⁻¹"),
            (0, "×10⁰"),
            (1, "×10¹"),
            (2, "×10²"),
            (3, "×10³"),
            (4, "×10⁴"),
            (5, "×10⁵"),
            (6, "×10⁶"),
            (7, "×10⁷"),
            (8, "×10⁸"),
            (9, "×10⁹"),
            (10, "×10¹⁰"),
        ]

        for exp_val, expected_output in cases:
            actual_output = exponents.get_superscript_exp_str(exp_val)
            with self.subTest(
                exp_val=exp_val,
            ):
                self.assertEqual(expected_output, actual_output)

    def test_get_val_unc_exp(self):
        cases: list[GetValUncExpCase] = [
            (
                (Decimal("123"), Decimal("1"), ExpModeEnum.FIXEDPOINT, ExpValEnum.AUTO),
                0,
            ),
            (
                (Decimal("123"), Decimal("1"), ExpModeEnum.SCIENTIFIC, ExpValEnum.AUTO),
                2,
            ),
            (
                (
                    Decimal("-123"),
                    Decimal("1"),
                    ExpModeEnum.SCIENTIFIC,
                    ExpValEnum.AUTO,
                ),
                2,
            ),
            (
                (Decimal("1"), Decimal("123"), ExpModeEnum.SCIENTIFIC, ExpValEnum.AUTO),
                2,
            ),
            (
                (
                    Decimal("nan"),
                    Decimal("123"),
                    ExpModeEnum.SCIENTIFIC,
                    ExpValEnum.AUTO,
                ),
                2,
            ),
            (
                (
                    Decimal("123"),
                    Decimal("nan"),
                    ExpModeEnum.SCIENTIFIC,
                    ExpValEnum.AUTO,
                ),
                2,
            ),
            (
                (
                    Decimal("nan"),
                    Decimal("nan"),
                    ExpModeEnum.SCIENTIFIC,
                    ExpValEnum.AUTO,
                ),
                0,
            ),
        ]

        for (val, unc, exp_mode, input_exp), expected_output in cases:
            actual_output = exponents.get_val_unc_exp(
                val=val,
                unc=unc,
                exp_mode=exp_mode,
                input_exp=input_exp,
            )
            with self.subTest(
                val=val,
                unc=unc,
                exp_mode=exp_mode,
                input_exp=input_exp,
            ):
                self.assertEqual(expected_output, actual_output)

    def test_get_exp_str(self):
        cases: list[tuple[dict[str, Any], str]] = [
            (
                {
                    "exp_val": 0,
                    "exp_mode": ExpModeEnum.FIXEDPOINT,
                    "exp_format": ExpFormatEnum.STANDARD,
                    "extra_si_prefixes": {},
                    "extra_parts_per_forms": {},
                    "capitalize": False,
                    "superscript": False,
                },
                "",
            ),
            (
                {
                    "exp_val": 0,
                    "exp_mode": ExpModeEnum.PERCENT,
                    "exp_format": ExpFormatEnum.STANDARD,
                    "extra_si_prefixes": {},
                    "extra_parts_per_forms": {},
                    "capitalize": False,
                    "superscript": False,
                },
                "%",
            ),
            (
                {
                    "exp_val": -2,
                    "exp_mode": ExpModeEnum.ENGINEERING_SHIFTED,
                    "exp_format": ExpFormatEnum.PREFIX,
                    "extra_si_prefixes": {-2: "c"},
                    "extra_parts_per_forms": {},
                    "capitalize": False,
                    "superscript": False,
                },
                " c",
            ),
            (
                {
                    "exp_val": -3,
                    "exp_mode": ExpModeEnum.ENGINEERING_SHIFTED,
                    "exp_format": ExpFormatEnum.PREFIX,
                    "extra_si_prefixes": {-3: None},
                    "extra_parts_per_forms": {},
                    "capitalize": False,
                    "superscript": False,
                },
                "e-03",
            ),
            (
                {
                    "exp_val": 0,
                    "exp_mode": ExpModeEnum.ENGINEERING_SHIFTED,
                    "exp_format": ExpFormatEnum.PARTS_PER,
                    "extra_si_prefixes": {},
                    "extra_parts_per_forms": {},
                    "capitalize": False,
                    "superscript": False,
                },
                "",
            ),
            (
                {
                    "exp_val": -3,
                    "exp_mode": ExpModeEnum.ENGINEERING_SHIFTED,
                    "exp_format": ExpFormatEnum.STANDARD,
                    "extra_si_prefixes": {-3: None},
                    "extra_parts_per_forms": {},
                    "capitalize": False,
                    "superscript": True,
                },
                "×10⁻³",
            ),
        ]

        for kwargs, expected_output in cases:
            actual_output = exponents.get_exp_str(**kwargs)
            with self.subTest(**kwargs):
                self.assertEqual(expected_output, actual_output)
