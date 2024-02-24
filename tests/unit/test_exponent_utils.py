import unittest
from typing import Literal

from sciform.format_utils import exp_translations, exponents
from sciform.options.option_types import ExpFormatEnum

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
