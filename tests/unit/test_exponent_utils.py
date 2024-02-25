from __future__ import annotations

import unittest
from decimal import Decimal
from typing import Literal, Union

from sciform.format_utils import exp_translations, exponents
from sciform.options.option_types import AutoExpVal, ExpFormatEnum, ExpModeEnum

Base = Literal[10, 2]
GetTranslationDictCase = tuple[
    tuple[
        ExpFormatEnum,
        Base,
        dict[int, str],
        dict[int, str],
        dict[int, str],
    ],
    dict[int, str],
]
GetStandardExpStrCase = tuple[tuple[int, int, bool], str]
GetValUncExpCase = tuple[
    tuple[Decimal, Decimal, ExpModeEnum, Union[int, type[AutoExpVal]]],
    int,
]


class TestExponentUtils(unittest.TestCase):
    def test_get_translation_dict_si(self):
        translation_dict = exponents.get_translation_dict(
            ExpFormatEnum.PREFIX,
            10,
            extra_si_prefixes={-2: "c", -1: "d", +3: "km", -3: None},
            extra_iec_prefixes={},
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
            10,
            extra_si_prefixes={},
            extra_iec_prefixes={},
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

    def test_get_translation_dict_iec(self):
        translation_dict = exponents.get_translation_dict(
            ExpFormatEnum.PREFIX,
            2,
            extra_si_prefixes={},
            extra_iec_prefixes={10: "Kb", 20: "MiB", 30: None},
            extra_parts_per_forms={},
        )
        for key, value in exp_translations.val_to_iec_dict.items():
            self.assertIn(key, translation_dict)
            if key not in (10, 20, 30):
                self.assertEqual(value, translation_dict[key])
        self.assertEqual("Kb", translation_dict[10])
        self.assertEqual("MiB", translation_dict[20])
        self.assertEqual(None, translation_dict[30])

    def test_get_standard_exp_str(self):
        cases: list[GetStandardExpStrCase] = [
            ((10, -111, False), "e-111"),
            ((10, -15, False), "e-15"),
            ((10, -2, False), "e-02"),
            ((10, -1, False), "e-01"),
            ((10, 0, False), "e+00"),
            ((10, +1, False), "e+01"),
            ((10, +2, False), "e+02"),
            ((10, +15, False), "e+15"),
            ((10, +111, False), "e+111"),
            ((10, -111, True), "E-111"),
            ((10, -15, True), "E-15"),
            ((10, -2, True), "E-02"),
            ((10, -1, True), "E-01"),
            ((10, 0, True), "E+00"),
            ((10, +1, True), "E+01"),
            ((10, +2, True), "E+02"),
            ((10, +15, True), "E+15"),
            ((10, +111, True), "E+111"),
            ((2, -111, False), "b-111"),
            ((2, -15, False), "b-15"),
            ((2, -2, False), "b-02"),
            ((2, -1, False), "b-01"),
            ((2, 0, False), "b+00"),
            ((2, +1, False), "b+01"),
            ((2, +2, False), "b+02"),
            ((2, +15, False), "b+15"),
            ((2, +111, False), "b+111"),
            ((2, -111, True), "B-111"),
            ((2, -15, True), "B-15"),
            ((2, -2, True), "B-02"),
            ((2, -1, True), "B-01"),
            ((2, 0, True), "B+00"),
            ((2, +1, True), "B+01"),
            ((2, +2, True), "B+02"),
            ((2, +15, True), "B+15"),
            ((2, +111, True), "B+111"),
        ]

        for (base, exp_val, capitalize), expected_output in cases:
            actual_output = exponents.get_standard_exp_str(
                base=base,
                exp_val=exp_val,
                capitalize=capitalize,
            )
            with self.subTest(
                base=base,
                exp_val=exp_val,
                capitalize=capitalize,
            ):
                self.assertEqual(expected_output, actual_output)

    def test_get_superscript_exp_str(self):
        cases: list[tuple[tuple[int, int], str]] = [
            ((10, -10), "×10⁻¹⁰"),
            ((10, -1), "×10⁻¹"),
            ((10, 0), "×10⁰"),
            ((10, 1), "×10¹"),
            ((10, 2), "×10²"),
            ((10, 3), "×10³"),
            ((10, 4), "×10⁴"),
            ((10, 5), "×10⁵"),
            ((10, 6), "×10⁶"),
            ((10, 7), "×10⁷"),
            ((10, 8), "×10⁸"),
            ((10, 9), "×10⁹"),
            ((10, 10), "×10¹⁰"),
            ((2, -10), "×2⁻¹⁰"),
            ((2, -1), "×2⁻¹"),
            ((2, 0), "×2⁰"),
            ((2, 1), "×2¹"),
            ((2, 2), "×2²"),
            ((2, 3), "×2³"),
            ((2, 4), "×2⁴"),
            ((2, 5), "×2⁵"),
            ((2, 6), "×2⁶"),
            ((2, 7), "×2⁷"),
            ((2, 8), "×2⁸"),
            ((2, 9), "×2⁹"),
            ((2, 10), "×2¹⁰"),
        ]

        for (base, exp_val), expected_output in cases:
            actual_output = exponents.get_superscript_exp_str(base, exp_val)
            with self.subTest(
                base=base,
                exp_val=exp_val,
            ):
                self.assertEqual(expected_output, actual_output)

    def test_get_val_unc_exp(self):
        cases: list[GetValUncExpCase] = [
            ((Decimal("123"), Decimal("1"), ExpModeEnum.FIXEDPOINT, AutoExpVal), 0),
            ((Decimal("123"), Decimal("1"), ExpModeEnum.SCIENTIFIC, AutoExpVal), 2),
            ((Decimal("-123"), Decimal("1"), ExpModeEnum.SCIENTIFIC, AutoExpVal), 2),
            ((Decimal("1"), Decimal("123"), ExpModeEnum.SCIENTIFIC, AutoExpVal), 2),
            ((Decimal("nan"), Decimal("123"), ExpModeEnum.SCIENTIFIC, AutoExpVal), 2),
            ((Decimal("123"), Decimal("nan"), ExpModeEnum.SCIENTIFIC, AutoExpVal), 2),
            ((Decimal("nan"), Decimal("nan"), ExpModeEnum.SCIENTIFIC, AutoExpVal), 0),
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
