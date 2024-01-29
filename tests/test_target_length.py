from __future__ import annotations

import unittest
from typing import Sequence

from sciform import Formatter, format_to_target_length, modes


class TestFormatToTargetLength(unittest.TestCase):
    def run_val_cases(
        self,
        cases: list[tuple[tuple[float, float | None], str]],
        *,
        target_length: int,
        allowed_exp_modes: Sequence[modes.ExpMode],
        base_formatter: Formatter | None,
    ):
        for (val, unc), expected_str in cases:
            with self.subTest(
                val=val,
                expected_str=expected_str,
            ):
                actual_str = format_to_target_length(
                    val,
                    unc,
                    target_length=target_length,
                    allowed_exp_modes=allowed_exp_modes,
                    base_formatter=base_formatter,
                )
                self.assertEqual(actual_str, expected_str)

    def test_cases(self):
        cases = [
            (
                (11301.3646429824, None),
                " 11301.3646",
            ),
            (
                (7.55438813238573, None),
                " 7.55438813",
            ),
            (
                (3037.18756328971, None),
                " 3037.18756",
            ),
            (
                (3058.4404411981735, None),
                " 3058.44044",
            ),
            (
                (13.8904759429872987, None),
                " 13.8904759",
            ),
            (
                (5.440263872938719, None),
                " 5.44026387",
            ),
            (
                (0.124643890130481, None),
                " 0.12464389",
            ),
            (
                (0.009963634432798437298, None),
                " 0.00996363",
            ),
            (
                (0.2441075332894732, None),
                " 0.24410753",
            ),
            (
                (0.0141610629879, None),
                " 0.01416106",
            ),
            (
                (0.0241421029837978, None),
                " 0.02414210",
            ),
            (
                (0.0002027524899875, None),
                " 0.00020275",
            ),
            (
                (0.00002027524899875, None),
                " 2.0275e-05",
            ),
        ]

        self.run_val_cases(
            cases,
            target_length=11,
            allowed_exp_modes=["fixed_point", "scientific"],
            base_formatter=Formatter(sign_mode=" "),
        )

    def test_lmfit_gformat_data(self):
        test_data_gformat = [
            (-1.25, "-1.25000000"),
            (1.25, " 1.25000000"),
            (-1234567890.1234567890, "-1.2346e+09"),
            (1234567890.1234567890, " 1.2346e+09"),
            (12345.67890e150, " 1.235e+154"),
        ]

        for val, expected_str in test_data_gformat:
            with self.subTest(
                val=val,
                expected_str=expected_str,
            ):
                result_str = format_to_target_length(
                    val,
                    target_length=11,
                    allowed_exp_modes=["fixed_point", "scientific"],
                    base_formatter=Formatter(sign_mode=" "),
                )
                self.assertEqual(result_str, expected_str)
