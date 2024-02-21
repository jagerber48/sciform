from __future__ import annotations

import unittest
from decimal import Decimal
from typing import Union

from sciform.format_utils import rounding
from sciform.options.option_types import AutoDigits, RoundModeEnum

RoundDecPlaceCase = list[
    tuple[
        tuple[Decimal, RoundModeEnum, Union[int, type[AutoDigits]]],
        int,
    ]
]


class TestRounding(unittest.TestCase):
    def test_get_pdg_round_digit(self):
        cases: list[tuple[Decimal, int]] = [
            (Decimal("10.0"), 0),
            (Decimal("20.0"), 0),
            (Decimal("30.0"), 0),
            (Decimal("35.4"), 0),
            (Decimal("35.5"), 1),
            (Decimal("40.0"), 1),
            (Decimal("50.0"), 1),
            (Decimal("60.0"), 1),
            (Decimal("70.0"), 1),
            (Decimal("80.0"), 1),
            (Decimal("90.0"), 1),
            (Decimal("94.9"), 1),
            (Decimal("95.0"), 1),
            (Decimal("99.9"), 1),
            (Decimal("100"), 1),
            (Decimal("200"), 1),
            (Decimal("300"), 1),
            (Decimal("354"), 1),
            (Decimal("355"), 2),
            (Decimal("400"), 2),
            (Decimal("500"), 2),
            (Decimal("600"), 2),
            (Decimal("700"), 2),
            (Decimal("800"), 2),
            (Decimal("900"), 2),
            (Decimal("949"), 2),
            (Decimal("950"), 2),
            (Decimal("999"), 2),
            (Decimal("1000"), 2),
            (Decimal("2000"), 2),
            (Decimal("3000"), 2),
            (Decimal("3540"), 2),
            (Decimal("3550"), 3),
            (Decimal("4000"), 3),
            (Decimal("5000"), 3),
            (Decimal("6000"), 3),
            (Decimal("7000"), 3),
            (Decimal("8000"), 3),
            (Decimal("9000"), 3),
            (Decimal("9490"), 3),
            (Decimal("9500"), 3),
            (Decimal("9990"), 3),
        ]

        for number, expected_output in cases:
            actual_output = rounding.get_pdg_round_digit(number)
            with self.subTest(
                number=number,
                expected_output=expected_output,
                actual_output=actual_output,
            ):
                self.assertEqual(expected_output, actual_output)

    def test_get_round_dec_place(self):
        cases: RoundDecPlaceCase = [
            ((Decimal("123456"), RoundModeEnum.SIG_FIG, 2), 4),
            ((Decimal("12345.6"), RoundModeEnum.SIG_FIG, 2), 3),
            ((Decimal("1234.56"), RoundModeEnum.SIG_FIG, 2), 2),
            ((Decimal("123.456"), RoundModeEnum.SIG_FIG, 2), 1),
            ((Decimal("12.3456"), RoundModeEnum.SIG_FIG, 2), 0),
            ((Decimal("1.23456"), RoundModeEnum.SIG_FIG, 2), -1),
            ((Decimal("0.123456"), RoundModeEnum.SIG_FIG, 2), -2),
            ((Decimal("0.0123456"), RoundModeEnum.SIG_FIG, 2), -3),
            ((Decimal("0.00123456"), RoundModeEnum.SIG_FIG, 2), -4),
            ((Decimal("0.000123456"), RoundModeEnum.SIG_FIG, 2), -5),
            ((Decimal("123456"), RoundModeEnum.DEC_PLACE, 2), -2),
            ((Decimal("12345.6"), RoundModeEnum.DEC_PLACE, 2), -2),
            ((Decimal("1234.56"), RoundModeEnum.DEC_PLACE, 2), -2),
            ((Decimal("123.456"), RoundModeEnum.DEC_PLACE, 2), -2),
            ((Decimal("12.3456"), RoundModeEnum.DEC_PLACE, 2), -2),
            ((Decimal("1.23456"), RoundModeEnum.DEC_PLACE, 2), -2),
            ((Decimal("0.123456"), RoundModeEnum.DEC_PLACE, 2), -2),
            ((Decimal("0.0123456"), RoundModeEnum.DEC_PLACE, 2), -2),
            ((Decimal("0.00123456"), RoundModeEnum.DEC_PLACE, 2), -2),
            ((Decimal("0.000123456"), RoundModeEnum.DEC_PLACE, 2), -2),
            ((Decimal("123456"), RoundModeEnum.DEC_PLACE, -2), 2),
            ((Decimal("12345.6"), RoundModeEnum.DEC_PLACE, -2), 2),
            ((Decimal("1234.56"), RoundModeEnum.DEC_PLACE, -2), 2),
            ((Decimal("123.456"), RoundModeEnum.DEC_PLACE, -2), 2),
            ((Decimal("12.3456"), RoundModeEnum.DEC_PLACE, -2), 2),
            ((Decimal("1.23456"), RoundModeEnum.DEC_PLACE, -2), 2),
            ((Decimal("0.123456"), RoundModeEnum.DEC_PLACE, -2), 2),
            ((Decimal("0.0123456"), RoundModeEnum.DEC_PLACE, -2), 2),
            ((Decimal("0.00123456"), RoundModeEnum.DEC_PLACE, -2), 2),
            ((Decimal("0.000123456"), RoundModeEnum.DEC_PLACE, -2), 2),
            ((Decimal("123456"), RoundModeEnum.SIG_FIG, AutoDigits), 0),
            ((Decimal("12345.6"), RoundModeEnum.SIG_FIG, AutoDigits), -1),
            ((Decimal("1234.56"), RoundModeEnum.SIG_FIG, AutoDigits), -2),
            ((Decimal("123.456"), RoundModeEnum.SIG_FIG, AutoDigits), -3),
            ((Decimal("12.3456"), RoundModeEnum.SIG_FIG, AutoDigits), -4),
            ((Decimal("1.23456"), RoundModeEnum.SIG_FIG, AutoDigits), -5),
            ((Decimal("0.123456"), RoundModeEnum.SIG_FIG, AutoDigits), -6),
            ((Decimal("0.0123456"), RoundModeEnum.SIG_FIG, AutoDigits), -7),
            ((Decimal("0.00123456"), RoundModeEnum.SIG_FIG, AutoDigits), -8),
            ((Decimal("0.000123456"), RoundModeEnum.SIG_FIG, AutoDigits), -9),
            ((Decimal("123456"), RoundModeEnum.DEC_PLACE, AutoDigits), 0),
            ((Decimal("12345.6"), RoundModeEnum.DEC_PLACE, AutoDigits), -1),
            ((Decimal("1234.56"), RoundModeEnum.DEC_PLACE, AutoDigits), -2),
            ((Decimal("123.456"), RoundModeEnum.DEC_PLACE, AutoDigits), -3),
            ((Decimal("12.3456"), RoundModeEnum.DEC_PLACE, AutoDigits), -4),
            ((Decimal("1.23456"), RoundModeEnum.DEC_PLACE, AutoDigits), -5),
            ((Decimal("0.123456"), RoundModeEnum.DEC_PLACE, AutoDigits), -6),
            ((Decimal("0.0123456"), RoundModeEnum.DEC_PLACE, AutoDigits), -7),
            ((Decimal("0.00123456"), RoundModeEnum.DEC_PLACE, AutoDigits), -8),
            ((Decimal("0.000123456"), RoundModeEnum.DEC_PLACE, AutoDigits), -9),
        ]

        for input_data, expected_output in cases:
            num, round_mode, ndigits = input_data
            pdg_sig_figs = False
            actual_output = rounding.get_round_dec_place(
                num,
                round_mode,
                ndigits,
                pdg_sig_figs=pdg_sig_figs,
            )
            with self.subTest(
                num=num,
                round_mode=round_mode,
                ndigits=ndigits,
                pdg_sig_figs=pdg_sig_figs,
                expected_output=expected_output,
                actual_output=actual_output,
            ):
                self.assertEqual(expected_output, actual_output)

    def test_get_round_dec_place_pdg(self):
        cases: RoundDecPlaceCase = [
            ((Decimal("123456"), RoundModeEnum.SIG_FIG, 2), 4),
            ((Decimal("12345.6"), RoundModeEnum.SIG_FIG, 2), 3),
            ((Decimal("1234.56"), RoundModeEnum.SIG_FIG, 2), 2),
            ((Decimal("123.456"), RoundModeEnum.SIG_FIG, 2), 1),
            ((Decimal("12.3456"), RoundModeEnum.SIG_FIG, 2), 0),
            ((Decimal("1.23456"), RoundModeEnum.SIG_FIG, 2), -1),
            ((Decimal("0.123456"), RoundModeEnum.SIG_FIG, 2), -2),
            ((Decimal("0.0123456"), RoundModeEnum.SIG_FIG, 2), -3),
            ((Decimal("0.00123456"), RoundModeEnum.SIG_FIG, 2), -4),
            ((Decimal("0.000123456"), RoundModeEnum.SIG_FIG, 2), -5),
            ((Decimal("123456"), RoundModeEnum.DEC_PLACE, 2), -2),
            ((Decimal("12345.6"), RoundModeEnum.DEC_PLACE, 2), -2),
            ((Decimal("1234.56"), RoundModeEnum.DEC_PLACE, 2), -2),
            ((Decimal("123.456"), RoundModeEnum.DEC_PLACE, 2), -2),
            ((Decimal("12.3456"), RoundModeEnum.DEC_PLACE, 2), -2),
            ((Decimal("1.23456"), RoundModeEnum.DEC_PLACE, 2), -2),
            ((Decimal("0.123456"), RoundModeEnum.DEC_PLACE, 2), -2),
            ((Decimal("0.0123456"), RoundModeEnum.DEC_PLACE, 2), -2),
            ((Decimal("0.00123456"), RoundModeEnum.DEC_PLACE, 2), -2),
            ((Decimal("0.000123456"), RoundModeEnum.DEC_PLACE, 2), -2),
            ((Decimal("123456"), RoundModeEnum.DEC_PLACE, -2), 2),
            ((Decimal("12345.6"), RoundModeEnum.DEC_PLACE, -2), 2),
            ((Decimal("1234.56"), RoundModeEnum.DEC_PLACE, -2), 2),
            ((Decimal("123.456"), RoundModeEnum.DEC_PLACE, -2), 2),
            ((Decimal("12.3456"), RoundModeEnum.DEC_PLACE, -2), 2),
            ((Decimal("1.23456"), RoundModeEnum.DEC_PLACE, -2), 2),
            ((Decimal("0.123456"), RoundModeEnum.DEC_PLACE, -2), 2),
            ((Decimal("0.0123456"), RoundModeEnum.DEC_PLACE, -2), 2),
            ((Decimal("0.00123456"), RoundModeEnum.DEC_PLACE, -2), 2),
            ((Decimal("0.000123456"), RoundModeEnum.DEC_PLACE, -2), 2),
            ((Decimal("123456"), RoundModeEnum.SIG_FIG, AutoDigits), 4),
            ((Decimal("12345.6"), RoundModeEnum.SIG_FIG, AutoDigits), 3),
            ((Decimal("1234.56"), RoundModeEnum.SIG_FIG, AutoDigits), 2),
            ((Decimal("123.456"), RoundModeEnum.SIG_FIG, AutoDigits), 1),
            ((Decimal("12.3456"), RoundModeEnum.SIG_FIG, AutoDigits), 0),
            ((Decimal("1.23456"), RoundModeEnum.SIG_FIG, AutoDigits), -1),
            ((Decimal("0.123456"), RoundModeEnum.SIG_FIG, AutoDigits), -2),
            ((Decimal("0.0123456"), RoundModeEnum.SIG_FIG, AutoDigits), -3),
            ((Decimal("0.00123456"), RoundModeEnum.SIG_FIG, AutoDigits), -4),
            ((Decimal("0.000123456"), RoundModeEnum.SIG_FIG, AutoDigits), -5),
            ((Decimal("123456"), RoundModeEnum.DEC_PLACE, AutoDigits), 0),
            ((Decimal("12345.6"), RoundModeEnum.DEC_PLACE, AutoDigits), -1),
            ((Decimal("1234.56"), RoundModeEnum.DEC_PLACE, AutoDigits), -2),
            ((Decimal("123.456"), RoundModeEnum.DEC_PLACE, AutoDigits), -3),
            ((Decimal("12.3456"), RoundModeEnum.DEC_PLACE, AutoDigits), -4),
            ((Decimal("1.23456"), RoundModeEnum.DEC_PLACE, AutoDigits), -5),
            ((Decimal("0.123456"), RoundModeEnum.DEC_PLACE, AutoDigits), -6),
            ((Decimal("0.0123456"), RoundModeEnum.DEC_PLACE, AutoDigits), -7),
            ((Decimal("0.00123456"), RoundModeEnum.DEC_PLACE, AutoDigits), -8),
            ((Decimal("0.000123456"), RoundModeEnum.DEC_PLACE, AutoDigits), -9),
        ]

        for input_data, expected_output in cases:
            num, round_mode, ndigits = input_data
            pdg_sig_figs = True
            actual_output = rounding.get_round_dec_place(
                num,
                round_mode,
                ndigits,
                pdg_sig_figs=pdg_sig_figs,
            )
            with self.subTest(
                num=num,
                round_mode=round_mode,
                ndigits=ndigits,
                pdg_sig_figs=pdg_sig_figs,
                expected_output=expected_output,
                actual_output=actual_output,
            ):
                self.assertEqual(expected_output, actual_output)

    def test_get_round_dec_place_invalid(self):
        self.assertRaises(
            ValueError,
            rounding.get_round_dec_place,
            Decimal("1"),
            "sig_fig",
            2,
        )
