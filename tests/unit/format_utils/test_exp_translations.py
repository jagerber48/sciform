from __future__ import annotations

import re
import unittest
from typing import Any

from sciform.format_utils import exp_translations

alphabetic_pattern = re.compile(r"[a-zA-Zμ]?")


class TestExpTranslations(unittest.TestCase):
    def validate_translations_dict(self, translation_dict: dict[str, Any]) -> None:
        for key, value in translation_dict.items():
            with self.subTest(key=key, value=value):
                self.assertIsInstance(key, int)
                self.assertIsNotNone(re.match(alphabetic_pattern, value))

    def test_si_prefixes(self):
        self.validate_translations_dict(exp_translations.val_to_si_dict)

    def test_iec_prefixes(self):
        self.validate_translations_dict(exp_translations.val_to_iec_dict)

    def test__prefixes(self):
        self.validate_translations_dict(exp_translations.val_to_parts_per_dict)
