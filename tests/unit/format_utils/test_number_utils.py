from __future__ import annotations

from decimal import Decimal
from math import isnan
from typing import List, Tuple, Union

from sciform.format_utils import numbers
from sciform.options.option_types import ExpModeEnum, ExpValEnum

from tests import NanTestCase

MantissaExpBaseCase = List[
    Tuple[
        Tuple[Decimal, ExpModeEnum, Union[int, ExpValEnum]],
        Tuple[Decimal, int, int],
    ]
]


class TestNumberUtils(NanTestCase):
    def assertNanEqual(self, first, second, msg=None):  # noqa: N802
        if isnan(first):
            self.assertTrue(isnan(second), msg=msg)
        else:
            self.assertEqual(first, second, msg=msg)

    def test_get_top_dec_place(self):
        cases = [
            (Decimal("1e-20"), -20),
            (Decimal("1e-06"), -6),
            (Decimal("1e-05"), -5),
            (Decimal("1e-04"), -4),
            (Decimal("1e-03"), -3),
            (Decimal("1e-02"), -2),
            (Decimal("1e-01"), -1),
            (Decimal("1e00"), 0),
            (Decimal("1e+01"), 1),
            (Decimal("1e+02"), 2),
            (Decimal("1e+03"), 3),
            (Decimal("1e+04"), 4),
            (Decimal("1e+05"), 5),
            (Decimal("1e+06"), 6),
            (Decimal("1e+20"), 20),
            (Decimal("nan"), 0),
            (Decimal("-inf"), 0),
            (Decimal("0"), 0),
        ]

        for base_number, expected_output in cases:
            for factor in [Decimal(1), Decimal(5)]:
                test_number = factor * base_number
                actual_output = numbers.get_top_dec_place(test_number)
                with self.subTest(
                    base_number=base_number,
                    test_number=test_number,
                    expected_output=expected_output,
                    actual_output=actual_output,
                ):
                    self.assertEqual(
                        expected_output,
                        actual_output,
                    )

    def test_get_top_dec_place_binary(self):
        cases = [
            (Decimal("32"), 5),
            (Decimal("64"), 6),
            (Decimal("nan"), 0),
            (Decimal("-inf"), 0),
            (Decimal("0"), 0),
        ]

        for base_number, expected_output in cases:
            for factor in [Decimal(1), Decimal(1.5)]:
                test_number = factor * base_number
                actual_output = numbers.get_top_dec_place_binary(test_number)
                with self.subTest(
                    base_number=base_number,
                    test_number=test_number,
                    expected_output=expected_output,
                    actual_output=actual_output,
                ):
                    self.assertEqual(
                        expected_output,
                        actual_output,
                    )

    def test_get_bottom_dec_place(self):
        cases: list[tuple[Decimal, int]] = [
            # Unnormalized:
            (Decimal("10000000.0000001"), -7),
            (Decimal("10000000.0000010"), -6),
            (Decimal("10000000.0000100"), -5),
            (Decimal("10000000.0001000"), -4),
            (Decimal("10000000.0010000"), -3),
            (Decimal("10000000.0100000"), -2),
            (Decimal("10000000.1000000"), -1),
            (Decimal("10000001.0000000"), 0),
            (Decimal("10000010.0000000"), +1),
            (Decimal("10000100.0000000"), +2),
            (Decimal("10001000.0000000"), +3),
            (Decimal("10010000.0000000"), +4),
            (Decimal("10100000.0000000"), +5),
            (Decimal("11000000.0000000"), +6),
            (Decimal("10000000.0000000"), +7),
            # Normalized:
            (Decimal("1.000001"), -6),
            (Decimal("1.00001"), -5),
            (Decimal("1.0001"), -4),
            (Decimal("1.001"), -3),
            (Decimal("1.01"), -2),
            (Decimal("1.1"), -1),
            (Decimal("1"), 0),
            (Decimal("1000001E+1"), +1),
            (Decimal("100001E+2"), +2),
            (Decimal("10001E+3"), +3),
            (Decimal("1001E+4"), +4),
            (Decimal("101E+5"), +5),
            (Decimal("11E+6"), +6),
            (Decimal("1E+7"), +7),
            (Decimal("nan"), 0),
            (Decimal("inf"), 0),
            (Decimal("-inf"), 0),
        ]

        for base_number, expected_output in cases:
            for factor in [Decimal(1), Decimal(5)]:
                test_number = factor * base_number
            actual_output = numbers.get_bottom_dec_place(test_number)
            with self.subTest(
                base_number=base_number,
                test_number=test_number,
                expected_output=expected_output,
                actual_output=actual_output,
            ):
                self.assertEqual(
                    expected_output,
                    actual_output,
                )

    def test_get_val_unc_top_dec_place(self):
        cases: list[tuple[tuple[Decimal, Decimal, int], int]] = [
            ((Decimal("123"), Decimal("0.456"), 0), 0),
            ((Decimal("123"), Decimal("0.456"), 1), 1),
            ((Decimal("123"), Decimal("0.456"), 2), 2),
            ((Decimal("123"), Decimal("0.456"), 3), 3),
            ((Decimal("123"), Decimal("0.456"), 4), 4),
            ((Decimal("123"), Decimal("0.456"), 5), 5),
            ((Decimal("123"), Decimal("0.456"), 6), 6),
            ((Decimal("0.456"), Decimal("123"), 0), 0),
            ((Decimal("0.456"), Decimal("123"), 1), 1),
            ((Decimal("0.456"), Decimal("123"), 2), 2),
            ((Decimal("0.456"), Decimal("123"), 3), 3),
            ((Decimal("0.456"), Decimal("123"), 4), 4),
            ((Decimal("0.456"), Decimal("123"), 5), 5),
            ((Decimal("0.456"), Decimal("123"), 6), 6),
            ((Decimal("0.000123"), Decimal("0.000000456"), -1), 0),
            ((Decimal("0.000000456"), Decimal("0.000123"), -1), 0),
        ]

        left_pad_matching = False
        for (val, unc, input_top_dec_place), expected_output in cases:
            actual_output = numbers.get_val_unc_top_dec_place(
                val_mantissa=val,
                unc_mantissa=unc,
                input_top_dec_place=input_top_dec_place,
                left_pad_matching=left_pad_matching,
            )
            with self.subTest(
                val_mantissa=val,
                unc_mantissa=unc,
                input_top_dec_place=input_top_dec_place,
                left_pad_matching=left_pad_matching,
                expected_output=expected_output,
                actual_output=actual_output,
            ):
                self.assertEqual(expected_output, actual_output)

    def test_get_val_unc_top_dec_place_left_pad_match(self):
        cases: list[tuple[tuple[Decimal, Decimal, int], int]] = [
            ((Decimal("123"), Decimal("0.456"), 0), 2),
            ((Decimal("123"), Decimal("0.456"), 1), 2),
            ((Decimal("123"), Decimal("0.456"), 2), 2),
            ((Decimal("123"), Decimal("0.456"), 3), 3),
            ((Decimal("123"), Decimal("0.456"), 4), 4),
            ((Decimal("123"), Decimal("0.456"), 5), 5),
            ((Decimal("123"), Decimal("0.456"), 6), 6),
            ((Decimal("0.456"), Decimal("123"), 0), 2),
            ((Decimal("0.456"), Decimal("123"), 1), 2),
            ((Decimal("0.456"), Decimal("123"), 2), 2),
            ((Decimal("0.456"), Decimal("123"), 3), 3),
            ((Decimal("0.456"), Decimal("123"), 4), 4),
            ((Decimal("0.456"), Decimal("123"), 5), 5),
            ((Decimal("0.456"), Decimal("123"), 6), 6),
            ((Decimal("0.000123"), Decimal("0.000000456"), -1), 0),
            ((Decimal("0.000000456"), Decimal("0.000123"), -1), 0),
        ]

        left_pad_matching = True
        for (val, unc, input_top_dec_place), expected_output in cases:
            actual_output = numbers.get_val_unc_top_dec_place(
                val_mantissa=val,
                unc_mantissa=unc,
                input_top_dec_place=input_top_dec_place,
                left_pad_matching=left_pad_matching,
            )
            with self.subTest(
                val_mantissa=val,
                unc_mantissa=unc,
                input_top_dec_place=input_top_dec_place,
                left_pad_matching=left_pad_matching,
                expected_output=expected_output,
                actual_output=actual_output,
            ):
                self.assertEqual(expected_output, actual_output)

    def test_get_fixed_exp(self):
        self.assertEqual(0, numbers.get_fixed_exp(0))
        self.assertEqual(0, numbers.get_fixed_exp(ExpValEnum.AUTO))
        self.assertRaises(
            ValueError,
            numbers.get_fixed_exp,
            3,
        )

    def test_get_scientific_exp(self):
        cases: list[tuple[tuple[Decimal, int | ExpValEnum], int]] = [
            ((Decimal("1000000"), ExpValEnum.AUTO), 6),
            ((Decimal("100000"), ExpValEnum.AUTO), 5),
            ((Decimal("10000"), ExpValEnum.AUTO), 4),
            ((Decimal("1000"), ExpValEnum.AUTO), 3),
            ((Decimal("100"), ExpValEnum.AUTO), 2),
            ((Decimal("10"), ExpValEnum.AUTO), 1),
            ((Decimal("1"), ExpValEnum.AUTO), 0),
            ((Decimal("0.1"), ExpValEnum.AUTO), -1),
            ((Decimal("0.01"), ExpValEnum.AUTO), -2),
            ((Decimal("0.001"), ExpValEnum.AUTO), -3),
            ((Decimal("0.0001"), ExpValEnum.AUTO), -4),
            ((Decimal("0.00001"), ExpValEnum.AUTO), -5),
            ((Decimal("0.000001"), ExpValEnum.AUTO), -6),
            ((Decimal("1000000"), 3), 3),
            ((Decimal("100000"), 3), 3),
            ((Decimal("10000"), 3), 3),
            ((Decimal("1000"), 3), 3),
            ((Decimal("100"), 3), 3),
            ((Decimal("10"), 3), 3),
            ((Decimal("1"), 3), 3),
            ((Decimal("0.1"), 3), 3),
            ((Decimal("0.01"), 3), 3),
            ((Decimal("0.001"), 3), 3),
            ((Decimal("0.0001"), 3), 3),
            ((Decimal("0.00001"), 3), 3),
            ((Decimal("0.000001"), 3), 3),
        ]

        for (base_number, input_exp), expected_output in cases:
            for factor in [Decimal(1), Decimal(5)]:
                test_number = factor * base_number
                actual_output = numbers.get_scientific_exp(
                    test_number,
                    input_exp,
                )
                with self.subTest(
                    base_number=base_number,
                    test_number=test_number,
                    input_exp=input_exp,
                    expected_output=expected_output,
                    actual_output=actual_output,
                ):
                    self.assertEqual(expected_output, actual_output)

    def test_get_engineering_exp(self):
        cases: list[tuple[tuple[Decimal, int | ExpValEnum], int]] = [
            ((Decimal("1000000"), ExpValEnum.AUTO), 6),
            ((Decimal("100000"), ExpValEnum.AUTO), 3),
            ((Decimal("10000"), ExpValEnum.AUTO), 3),
            ((Decimal("1000"), ExpValEnum.AUTO), 3),
            ((Decimal("100"), ExpValEnum.AUTO), 0),
            ((Decimal("10"), ExpValEnum.AUTO), 0),
            ((Decimal("1"), ExpValEnum.AUTO), 0),
            ((Decimal("0.1"), ExpValEnum.AUTO), -3),
            ((Decimal("0.01"), ExpValEnum.AUTO), -3),
            ((Decimal("0.001"), ExpValEnum.AUTO), -3),
            ((Decimal("0.0001"), ExpValEnum.AUTO), -6),
            ((Decimal("0.00001"), ExpValEnum.AUTO), -6),
            ((Decimal("0.000001"), ExpValEnum.AUTO), -6),
            ((Decimal("1000000"), 3), 3),
            ((Decimal("100000"), 3), 3),
            ((Decimal("10000"), 3), 3),
            ((Decimal("1000"), 3), 3),
            ((Decimal("100"), 3), 3),
            ((Decimal("10"), 3), 3),
            ((Decimal("1"), 3), 3),
            ((Decimal("0.1"), 3), 3),
            ((Decimal("0.01"), 3), 3),
            ((Decimal("0.001"), 3), 3),
            ((Decimal("0.0001"), 3), 3),
            ((Decimal("0.00001"), 3), 3),
            ((Decimal("0.000001"), 3), 3),
        ]

        shifted = False
        for (base_number, input_exp), expected_output in cases:
            for factor in [Decimal(1), Decimal(5)]:
                test_number = factor * base_number
                actual_output = numbers.get_engineering_exp(
                    base_number,
                    input_exp,
                    shifted=shifted,
                )
                with self.subTest(
                    base_number=base_number,
                    test_number=test_number,
                    input_exp=input_exp,
                    shifted=shifted,
                    expected_output=expected_output,
                    actual_output=actual_output,
                ):
                    self.assertEqual(expected_output, actual_output)

    def test_get_engineering_shifted_exp(self):
        cases: list[tuple[tuple[Decimal, int | ExpValEnum], int]] = [
            ((Decimal("1000000"), ExpValEnum.AUTO), 6),
            ((Decimal("100000"), ExpValEnum.AUTO), 6),
            ((Decimal("10000"), ExpValEnum.AUTO), 3),
            ((Decimal("1000"), ExpValEnum.AUTO), 3),
            ((Decimal("100"), ExpValEnum.AUTO), 3),
            ((Decimal("10"), ExpValEnum.AUTO), 0),
            ((Decimal("1"), ExpValEnum.AUTO), 0),
            ((Decimal("0.1"), ExpValEnum.AUTO), 0),
            ((Decimal("0.01"), ExpValEnum.AUTO), -3),
            ((Decimal("0.001"), ExpValEnum.AUTO), -3),
            ((Decimal("0.0001"), ExpValEnum.AUTO), -3),
            ((Decimal("0.00001"), ExpValEnum.AUTO), -6),
            ((Decimal("0.000001"), ExpValEnum.AUTO), -6),
            ((Decimal("1000000"), 3), 3),
            ((Decimal("100000"), 3), 3),
            ((Decimal("10000"), 3), 3),
            ((Decimal("1000"), 3), 3),
            ((Decimal("100"), 3), 3),
            ((Decimal("10"), 3), 3),
            ((Decimal("1"), 3), 3),
            ((Decimal("0.1"), 3), 3),
            ((Decimal("0.01"), 3), 3),
            ((Decimal("0.001"), 3), 3),
            ((Decimal("0.0001"), 3), 3),
            ((Decimal("0.00001"), 3), 3),
            ((Decimal("0.000001"), 3), 3),
        ]

        shifted = True
        for (base_number, input_exp), expected_output in cases:
            for factor in [Decimal(1), Decimal(5)]:
                test_number = factor * base_number
                actual_output = numbers.get_engineering_exp(
                    base_number,
                    input_exp,
                    shifted=shifted,
                )
                with self.subTest(
                    base_number=base_number,
                    test_number=test_number,
                    input_exp=input_exp,
                    shifted=shifted,
                    expected_output=expected_output,
                    actual_output=actual_output,
                ):
                    self.assertEqual(expected_output, actual_output)

    def test_get_engineering_exp_bad_input_exp(self):
        self.assertRaises(
            ValueError,
            numbers.get_engineering_exp,
            Decimal("1.0"),
            2,
        )

    def test_get_binary_exp(self):
        cases: list[tuple[tuple[Decimal, int | ExpValEnum], int]] = [
            ((Decimal("0.0625"), ExpValEnum.AUTO), -4),
            ((Decimal("0.125"), ExpValEnum.AUTO), -3),
            ((Decimal("0.25"), ExpValEnum.AUTO), -2),
            ((Decimal("0.5"), ExpValEnum.AUTO), -1),
            ((Decimal("1"), ExpValEnum.AUTO), 0),
            ((Decimal("2"), ExpValEnum.AUTO), 1),
            ((Decimal("4"), ExpValEnum.AUTO), 2),
            ((Decimal("8"), ExpValEnum.AUTO), 3),
            ((Decimal("16"), ExpValEnum.AUTO), 4),
            ((Decimal("32"), ExpValEnum.AUTO), 5),
            ((Decimal("64"), ExpValEnum.AUTO), 6),
            ((Decimal("0.0625"), 3), 3),
            ((Decimal("0.125"), 3), 3),
            ((Decimal("0.25"), 3), 3),
            ((Decimal("0.5"), 3), 3),
            ((Decimal("1"), 3), 3),
            ((Decimal("2"), 3), 3),
            ((Decimal("4"), 3), 3),
            ((Decimal("8"), 3), 3),
            ((Decimal("16"), 3), 3),
            ((Decimal("32"), 3), 3),
            ((Decimal("64"), 3), 3),
        ]

        iec: bool = False
        for (base_number, input_exp), expected_output in cases:
            for factor in [Decimal(1), Decimal(1.5)]:
                test_number = factor * base_number
                actual_output = numbers.get_binary_exp(
                    test_number,
                    input_exp,
                    iec=iec,
                )
                with self.subTest(
                    base_number=base_number,
                    test_number=test_number,
                    input_exp=input_exp,
                    iec=iec,
                    expected_output=expected_output,
                    actual_output=actual_output,
                ):
                    self.assertEqual(expected_output, actual_output)

    def test_get_binary_iec_exp(self):
        cases: list[tuple[tuple[Decimal, int | ExpValEnum], int]] = [
            ((Decimal("0.0625"), ExpValEnum.AUTO), -10),
            ((Decimal("0.125"), ExpValEnum.AUTO), -10),
            ((Decimal("0.25"), ExpValEnum.AUTO), -10),
            ((Decimal("0.5"), ExpValEnum.AUTO), -10),
            ((Decimal("1"), ExpValEnum.AUTO), 0),
            ((Decimal("2"), ExpValEnum.AUTO), 0),
            ((Decimal("4"), ExpValEnum.AUTO), 0),
            ((Decimal("8"), ExpValEnum.AUTO), 0),
            ((Decimal("16"), ExpValEnum.AUTO), 0),
            ((Decimal("32"), ExpValEnum.AUTO), 0),
            ((Decimal("64"), ExpValEnum.AUTO), 0),
            ((Decimal("1024"), ExpValEnum.AUTO), 10),
            ((Decimal(2**20), ExpValEnum.AUTO), 20),
            ((Decimal(2**30), ExpValEnum.AUTO), 30),
            ((Decimal("0.0625"), 10), 10),
            ((Decimal("0.125"), 10), 10),
            ((Decimal("0.25"), 10), 10),
            ((Decimal("0.5"), 10), 10),
            ((Decimal("1"), 10), 10),
            ((Decimal("2"), 10), 10),
            ((Decimal("4"), 10), 10),
            ((Decimal("8"), 10), 10),
            ((Decimal("16"), 10), 10),
            ((Decimal("32"), 10), 10),
            ((Decimal("64"), 10), 10),
        ]

        iec: bool = True
        for (base_number, input_exp), expected_output in cases:
            for factor in [Decimal(1), Decimal(1.5)]:
                test_number = factor * base_number
                actual_output = numbers.get_binary_exp(
                    test_number,
                    input_exp,
                    iec=iec,
                )
                with self.subTest(
                    base_number=base_number,
                    test_number=test_number,
                    input_exp=input_exp,
                    iec=iec,
                    expected_output=expected_output,
                    actual_output=actual_output,
                ):
                    self.assertEqual(expected_output, actual_output)

    def test_get_binary_iec_bad_input_exp(self):
        self.assertRaises(
            ValueError,
            numbers.get_binary_exp,
            Decimal("1.5"),
            5,
            iec=True,
        )

    def test_get_mantissa_exp_base(self):
        cases: MantissaExpBaseCase = [
            (
                (Decimal("123456"), ExpModeEnum.FIXEDPOINT, ExpValEnum.AUTO),
                (Decimal("123456"), 0, 10),
            ),
            (
                (Decimal("1234.56"), ExpModeEnum.FIXEDPOINT, ExpValEnum.AUTO),
                (Decimal("1234.56"), 0, 10),
            ),
            (
                (Decimal("12.3456"), ExpModeEnum.FIXEDPOINT, ExpValEnum.AUTO),
                (Decimal("12.3456"), 0, 10),
            ),
            (
                (Decimal("0.123456"), ExpModeEnum.FIXEDPOINT, ExpValEnum.AUTO),
                (Decimal("0.123456"), 0, 10),
            ),
            (
                (Decimal("0.00123456"), ExpModeEnum.FIXEDPOINT, ExpValEnum.AUTO),
                (Decimal("0.00123456"), 0, 10),
            ),
            (
                (Decimal("0.0000123456"), ExpModeEnum.FIXEDPOINT, ExpValEnum.AUTO),
                (Decimal("0.0000123456"), 0, 10),
            ),
            (
                (Decimal("123456"), ExpModeEnum.PERCENT, ExpValEnum.AUTO),
                (Decimal("123456"), 0, 10),
            ),
            (
                (Decimal("1234.56"), ExpModeEnum.PERCENT, ExpValEnum.AUTO),
                (Decimal("1234.56"), 0, 10),
            ),
            (
                (Decimal("12.3456"), ExpModeEnum.PERCENT, ExpValEnum.AUTO),
                (Decimal("12.3456"), 0, 10),
            ),
            (
                (Decimal("0.123456"), ExpModeEnum.PERCENT, ExpValEnum.AUTO),
                (Decimal("0.123456"), 0, 10),
            ),
            (
                (Decimal("0.00123456"), ExpModeEnum.PERCENT, ExpValEnum.AUTO),
                (Decimal("0.00123456"), 0, 10),
            ),
            (
                (Decimal("0.0000123456"), ExpModeEnum.PERCENT, ExpValEnum.AUTO),
                (Decimal("0.0000123456"), 0, 10),
            ),
            (
                (Decimal("123456"), ExpModeEnum.SCIENTIFIC, ExpValEnum.AUTO),
                (Decimal("1.23456"), 5, 10),
            ),
            (
                (Decimal("1234.56"), ExpModeEnum.SCIENTIFIC, ExpValEnum.AUTO),
                (Decimal("1.23456"), 3, 10),
            ),
            (
                (Decimal("12.3456"), ExpModeEnum.SCIENTIFIC, ExpValEnum.AUTO),
                (Decimal("1.23456"), 1, 10),
            ),
            (
                (Decimal("0.123456"), ExpModeEnum.SCIENTIFIC, ExpValEnum.AUTO),
                (Decimal("1.23456"), -1, 10),
            ),
            (
                (Decimal("0.00123456"), ExpModeEnum.SCIENTIFIC, ExpValEnum.AUTO),
                (Decimal("1.23456"), -3, 10),
            ),
            (
                (Decimal("0.0000123456"), ExpModeEnum.SCIENTIFIC, ExpValEnum.AUTO),
                (Decimal("1.23456"), -5, 10),
            ),
            (
                (Decimal("123456"), ExpModeEnum.ENGINEERING, ExpValEnum.AUTO),
                (Decimal("123.456"), 3, 10),
            ),
            (
                (Decimal("1234.56"), ExpModeEnum.ENGINEERING, ExpValEnum.AUTO),
                (Decimal("1.23456"), 3, 10),
            ),
            (
                (Decimal("12.3456"), ExpModeEnum.ENGINEERING, ExpValEnum.AUTO),
                (Decimal("12.3456"), 0, 10),
            ),
            (
                (Decimal("0.123456"), ExpModeEnum.ENGINEERING, ExpValEnum.AUTO),
                (Decimal("123.456"), -3, 10),
            ),
            (
                (Decimal("0.00123456"), ExpModeEnum.ENGINEERING, ExpValEnum.AUTO),
                (Decimal("1.23456"), -3, 10),
            ),
            (
                (Decimal("0.0000123456"), ExpModeEnum.ENGINEERING, ExpValEnum.AUTO),
                (Decimal("12.3456"), -6, 10),
            ),
            (
                (Decimal("123456"), ExpModeEnum.ENGINEERING_SHIFTED, ExpValEnum.AUTO),
                (Decimal("0.123456"), 6, 10),
            ),
            (
                (Decimal("1234.56"), ExpModeEnum.ENGINEERING_SHIFTED, ExpValEnum.AUTO),
                (Decimal("1.23456"), 3, 10),
            ),
            (
                (Decimal("12.3456"), ExpModeEnum.ENGINEERING_SHIFTED, ExpValEnum.AUTO),
                (Decimal("12.3456"), 0, 10),
            ),
            (
                (Decimal("0.123456"), ExpModeEnum.ENGINEERING_SHIFTED, ExpValEnum.AUTO),
                (Decimal("0.123456"), 0, 10),
            ),
            (
                (
                    Decimal("0.00123456"),
                    ExpModeEnum.ENGINEERING_SHIFTED,
                    ExpValEnum.AUTO,
                ),
                (Decimal("1.23456"), -3, 10),
            ),
            (
                (
                    Decimal("0.0000123456"),
                    ExpModeEnum.ENGINEERING_SHIFTED,
                    ExpValEnum.AUTO,
                ),
                (Decimal("12.3456"), -6, 10),
            ),
            (
                (Decimal(1 * 2**-10), ExpModeEnum.BINARY, ExpValEnum.AUTO),
                (Decimal("1.0"), -10, 2),
            ),
            (
                (Decimal(1.5 * 2**-10), ExpModeEnum.BINARY, ExpValEnum.AUTO),
                (Decimal("1.5"), -10, 2),
            ),
            (
                (Decimal(1 * 2**-5), ExpModeEnum.BINARY, ExpValEnum.AUTO),
                (Decimal("1.0"), -5, 2),
            ),
            (
                (Decimal(1.5 * 2**-5), ExpModeEnum.BINARY, ExpValEnum.AUTO),
                (Decimal("1.5"), -5, 2),
            ),
            (
                (Decimal(1 * 2**0), ExpModeEnum.BINARY, ExpValEnum.AUTO),
                (Decimal("1.0"), 0, 2),
            ),
            (
                (Decimal(1.5 * 2**0), ExpModeEnum.BINARY, ExpValEnum.AUTO),
                (Decimal("1.5"), 0, 2),
            ),
            (
                (Decimal(1 * 2**5), ExpModeEnum.BINARY, ExpValEnum.AUTO),
                (Decimal("1.0"), 5, 2),
            ),
            (
                (Decimal(1.5 * 2**5), ExpModeEnum.BINARY, ExpValEnum.AUTO),
                (Decimal("1.5"), 5, 2),
            ),
            (
                (Decimal(1 * 2**10), ExpModeEnum.BINARY, ExpValEnum.AUTO),
                (Decimal("1.0"), 10, 2),
            ),
            (
                (Decimal(1.5 * 2**10), ExpModeEnum.BINARY, ExpValEnum.AUTO),
                (Decimal("1.5"), 10, 2),
            ),
            (
                (Decimal(1 * 2**-10), ExpModeEnum.BINARY_IEC, ExpValEnum.AUTO),
                (Decimal("1.0"), -10, 2),
            ),
            (
                (Decimal(1.5 * 2**-10), ExpModeEnum.BINARY_IEC, ExpValEnum.AUTO),
                (Decimal("1.5"), -10, 2),
            ),
            (
                (Decimal(1 * 2**-5), ExpModeEnum.BINARY_IEC, ExpValEnum.AUTO),
                (Decimal("32"), -10, 2),
            ),
            (
                (Decimal(1.5 * 2**-5), ExpModeEnum.BINARY_IEC, ExpValEnum.AUTO),
                (Decimal("48"), -10, 2),
            ),
            (
                (Decimal(1 * 2**0), ExpModeEnum.BINARY_IEC, ExpValEnum.AUTO),
                (Decimal("1.0"), 0, 2),
            ),
            (
                (Decimal(1.5 * 2**0), ExpModeEnum.BINARY_IEC, ExpValEnum.AUTO),
                (Decimal("1.5"), 0, 2),
            ),
            (
                (Decimal(1 * 2**5), ExpModeEnum.BINARY_IEC, ExpValEnum.AUTO),
                (Decimal("32"), 0, 2),
            ),
            (
                (Decimal(1.5 * 2**5), ExpModeEnum.BINARY_IEC, ExpValEnum.AUTO),
                (Decimal("48"), 0, 2),
            ),
            (
                (Decimal(1 * 2**10), ExpModeEnum.BINARY_IEC, ExpValEnum.AUTO),
                (Decimal("1.0"), 10, 2),
            ),
            (
                (Decimal(1.5 * 2**10), ExpModeEnum.BINARY_IEC, ExpValEnum.AUTO),
                (Decimal("1.5"), 10, 2),
            ),
            (
                (Decimal("nan"), ExpModeEnum.FIXEDPOINT, ExpValEnum.AUTO),
                (Decimal("nan"), 0, 10),
            ),
            (
                (Decimal("inf"), ExpModeEnum.SCIENTIFIC, ExpValEnum.AUTO),
                (Decimal("inf"), 0, 10),
            ),
            (
                (Decimal("-inf"), ExpModeEnum.SCIENTIFIC, 5),
                (Decimal("-inf"), 5, 10),
            ),
        ]

        for input_data, output_data in cases:
            num, exp_mode, input_exp = input_data
            expected_mantissa, expected_exp, expected_base = output_data
            actual_mantissa, actual_exp, actual_base = numbers.get_mantissa_exp_base(
                num,
                exp_mode,
                input_exp,
            )
            with self.subTest(
                num=num,
                exp_mode=exp_mode,
                input_exp=input_exp,
                expected_mantissa=expected_mantissa,
                actual_mantissa=actual_mantissa,
                expected_exp=expected_exp,
                actual_exp=actual_exp,
                expected_base=expected_base,
                actual_base=actual_base,
            ):
                self.assertNanEqual(expected_mantissa, actual_mantissa)
                self.assertEqual(expected_exp, actual_exp)
                self.assertEqual(expected_base, actual_base)

    def test_get_mantissa_exp_base_input_exp(self):
        cases: MantissaExpBaseCase = [
            (
                (Decimal("123456"), ExpModeEnum.FIXEDPOINT, 0),
                (Decimal("123456"), 0, 10),
            ),
            (
                (Decimal("1234.56"), ExpModeEnum.FIXEDPOINT, 0),
                (Decimal("1234.56"), 0, 10),
            ),
            (
                (Decimal("12.3456"), ExpModeEnum.FIXEDPOINT, 0),
                (Decimal("12.3456"), 0, 10),
            ),
            (
                (Decimal("0.123456"), ExpModeEnum.FIXEDPOINT, 0),
                (Decimal("0.123456"), 0, 10),
            ),
            (
                (Decimal("0.00123456"), ExpModeEnum.FIXEDPOINT, 0),
                (Decimal("0.00123456"), 0, 10),
            ),
            (
                (Decimal("0.0000123456"), ExpModeEnum.FIXEDPOINT, 0),
                (Decimal("0.0000123456"), 0, 10),
            ),
            (
                (Decimal("123456"), ExpModeEnum.PERCENT, 0),
                (Decimal("123456"), 0, 10),
            ),
            (
                (Decimal("1234.56"), ExpModeEnum.PERCENT, 0),
                (Decimal("1234.56"), 0, 10),
            ),
            (
                (Decimal("12.3456"), ExpModeEnum.PERCENT, 0),
                (Decimal("12.3456"), 0, 10),
            ),
            (
                (Decimal("0.123456"), ExpModeEnum.PERCENT, 0),
                (Decimal("0.123456"), 0, 10),
            ),
            (
                (Decimal("0.00123456"), ExpModeEnum.PERCENT, 0),
                (Decimal("0.00123456"), 0, 10),
            ),
            (
                (Decimal("0.0000123456"), ExpModeEnum.PERCENT, 0),
                (Decimal("0.0000123456"), 0, 10),
            ),
            (
                (Decimal("123456"), ExpModeEnum.SCIENTIFIC, 2),
                (Decimal("1234.56"), 2, 10),
            ),
            (
                (Decimal("1234.56"), ExpModeEnum.SCIENTIFIC, 2),
                (Decimal("12.3456"), 2, 10),
            ),
            (
                (Decimal("12.3456"), ExpModeEnum.SCIENTIFIC, 2),
                (Decimal("0.123456"), 2, 10),
            ),
            (
                (Decimal("0.123456"), ExpModeEnum.SCIENTIFIC, 2),
                (Decimal("0.00123456"), 2, 10),
            ),
            (
                (Decimal("0.00123456"), ExpModeEnum.SCIENTIFIC, 2),
                (Decimal("0.0000123456"), 2, 10),
            ),
            (
                (Decimal("0.0000123456"), ExpModeEnum.SCIENTIFIC, 2),
                (Decimal("0.000000123456"), 2, 10),
            ),
            (
                (Decimal("123456"), ExpModeEnum.ENGINEERING, 3),
                (Decimal("123.456"), 3, 10),
            ),
            (
                (Decimal("1234.56"), ExpModeEnum.ENGINEERING, 3),
                (Decimal("1.23456"), 3, 10),
            ),
            (
                (Decimal("12.3456"), ExpModeEnum.ENGINEERING, 3),
                (Decimal("0.0123456"), 3, 10),
            ),
            (
                (Decimal("0.123456"), ExpModeEnum.ENGINEERING, 3),
                (Decimal("0.000123456"), 3, 10),
            ),
            (
                (Decimal("0.00123456"), ExpModeEnum.ENGINEERING, 3),
                (Decimal("0.00000123456"), 3, 10),
            ),
            (
                (Decimal("0.0000123456"), ExpModeEnum.ENGINEERING, 3),
                (Decimal("0.0000000123456"), 3, 10),
            ),
            (
                (Decimal("123456"), ExpModeEnum.ENGINEERING_SHIFTED, 3),
                (Decimal("123.456"), 3, 10),
            ),
            (
                (Decimal("1234.56"), ExpModeEnum.ENGINEERING_SHIFTED, 3),
                (Decimal("1.23456"), 3, 10),
            ),
            (
                (Decimal("12.3456"), ExpModeEnum.ENGINEERING_SHIFTED, 3),
                (Decimal("0.0123456"), 3, 10),
            ),
            (
                (Decimal("0.123456"), ExpModeEnum.ENGINEERING_SHIFTED, 3),
                (Decimal("0.000123456"), 3, 10),
            ),
            (
                (Decimal("0.00123456"), ExpModeEnum.ENGINEERING_SHIFTED, 3),
                (Decimal("0.00000123456"), 3, 10),
            ),
            (
                (Decimal("0.0000123456"), ExpModeEnum.ENGINEERING_SHIFTED, 3),
                (Decimal("0.0000000123456"), 3, 10),
            ),
            (
                (Decimal(1 * 2**-10), ExpModeEnum.BINARY, 5),
                (Decimal("3.0517578125e-05"), 5, 2),
            ),
            (
                (Decimal(1.5 * 2**-10), ExpModeEnum.BINARY, 5),
                (Decimal("4.57763671875e-05"), 5, 2),
            ),
            (
                (Decimal(1 * 2**-5), ExpModeEnum.BINARY, 5),
                (Decimal("0.0009765625"), 5, 2),
            ),
            (
                (Decimal(1.5 * 2**-5), ExpModeEnum.BINARY, 5),
                (Decimal("0.00146484375"), 5, 2),
            ),
            (
                (Decimal(1 * 2**0), ExpModeEnum.BINARY, 5),
                (Decimal("0.03125"), 5, 2),
            ),
            (
                (Decimal(1.5 * 2**0), ExpModeEnum.BINARY, 5),
                (Decimal("0.046875"), 5, 2),
            ),
            (
                (Decimal(1 * 2**5), ExpModeEnum.BINARY, 5),
                (Decimal("1.0"), 5, 2),
            ),
            (
                (Decimal(1.5 * 2**5), ExpModeEnum.BINARY, 5),
                (Decimal("1.5"), 5, 2),
            ),
            (
                (Decimal(1 * 2**10), ExpModeEnum.BINARY, 5),
                (Decimal("32"), 5, 2),
            ),
            (
                (Decimal(1.5 * 2**10), ExpModeEnum.BINARY, 5),
                (Decimal("48"), 5, 2),
            ),
            (
                (Decimal(1 * 2**-10), ExpModeEnum.BINARY_IEC, 10),
                (Decimal(1 * 2**-20), 10, 2),
            ),
            (
                (Decimal(1.5 * 2**-10), ExpModeEnum.BINARY_IEC, 10),
                (Decimal(1.5 * 2**-20), 10, 2),
            ),
            (
                (Decimal(1 * 2**-5), ExpModeEnum.BINARY_IEC, 10),
                (Decimal(1 * 2**-15), 10, 2),
            ),
            (
                (Decimal(1.5 * 2**-5), ExpModeEnum.BINARY_IEC, 10),
                (Decimal(1.5 * 2**-15), 10, 2),
            ),
            (
                (Decimal(1 * 2**0), ExpModeEnum.BINARY_IEC, 10),
                (Decimal(1 * 2**-10), 10, 2),
            ),
            (
                (Decimal(1.5 * 2**0), ExpModeEnum.BINARY_IEC, 10),
                (Decimal(1.5 * 2**-10), 10, 2),
            ),
            (
                (Decimal(1 * 2**5), ExpModeEnum.BINARY_IEC, 10),
                (Decimal(1 * 2**-5), 10, 2),
            ),
            (
                (Decimal(1.5 * 2**5), ExpModeEnum.BINARY_IEC, 10),
                (Decimal(1.5 * 2**-5), 10, 2),
            ),
            (
                (Decimal(1 * 2**10), ExpModeEnum.BINARY_IEC, 10),
                (Decimal("1.0"), 10, 2),
            ),
            (
                (Decimal(1.5 * 2**10), ExpModeEnum.BINARY_IEC, 10),
                (Decimal("1.5"), 10, 2),
            ),
        ]

        for input_data, output_data in cases:
            num, exp_mode, input_exp = input_data
            expected_mantissa, expected_exp, expected_base = output_data
            actual_mantissa, actual_exp, actual_base = numbers.get_mantissa_exp_base(
                num,
                exp_mode,
                input_exp,
            )
            with self.subTest(
                num=num,
                exp_mode=exp_mode,
                input_exp=input_exp,
                expected_mantissa=expected_mantissa,
                actual_mantissa=actual_mantissa,
                expected_exp=expected_exp,
                actual_exp=actual_exp,
                expected_base=expected_base,
                actual_base=actual_base,
            ):
                self.assertEqual(expected_mantissa, actual_mantissa)
                self.assertEqual(expected_exp, actual_exp)
                self.assertEqual(expected_base, actual_base)

    def test_get_mantissa_exp_base_invalid_exp_mode(self):
        self.assertRaises(
            ValueError,
            numbers.get_mantissa_exp_base,
            Decimal("3"),
            exp_mode="fixed_point",
            input_exp=3,
        )

    def test_parse_mantissa_from_ascii_exp_str(self):
        cases = [
            ("123.456e+03", "123.456"),
            ("123456e+03", "123456"),
            ("123_456e+03", "123_456"),
            ("123_456.789 876e+03", "123_456.789 876"),
            ("123.456", "123.456"),
            ("123456", "123456"),
            ("123_456", "123_456"),
            ("123_456.789 876", "123_456.789 876"),
            ("1E+03", "1"),
            ("(nan)b-4", "nan"),
            ("(nan)B-4", "nan"),
            ("inf", "inf"),
            ("-inf", "-inf"),
        ]
        for input_string, expected_output in cases:
            actual_output = numbers.parse_mantissa_from_ascii_exp_str(input_string)
            with self.subTest(
                input_string=input_string,
                expected_output=expected_output,
                actual_output=actual_output,
            ):
                self.assertEqual(expected_output, actual_output)

    def test_parse_mantissa_from_ascii_exp_str_invalid(self):
        cases = [
            "1.2c+03",
            "(nan)",
            "(1.2 ± 0.3)e+04",
        ]

        for input_str in cases:
            with self.subTest(input_str=input_str):
                self.assertRaises(
                    ValueError,
                    numbers.parse_mantissa_from_ascii_exp_str,
                    input_str,
                )

    def test_get_mantissa_exp_base_invalid_input(self):
        with self.subTest(msg="fixed_point_set_exp"):
            self.assertRaises(
                ValueError,
                numbers.get_mantissa_exp_base,
                num=Decimal(3),
                exp_mode=ExpModeEnum.FIXEDPOINT,
                input_exp=1,
            )

        with self.subTest(msg="engineering_set_exp"):
            self.assertRaises(
                ValueError,
                numbers.get_mantissa_exp_base,
                num=Decimal(3),
                exp_mode=ExpModeEnum.ENGINEERING,
                input_exp=1,
            )

        with self.subTest(msg="binary_iec_set_exp"):
            self.assertRaises(
                ValueError,
                numbers.get_mantissa_exp_base,
                num=Decimal(3),
                exp_mode=ExpModeEnum.BINARY_IEC,
                input_exp=3,
            )

        with self.subTest(msg="bad_exp_mode"):
            self.assertRaises(
                ValueError,
                numbers.get_mantissa_exp_base,
                num=Decimal(3),
                exp_mode="eng",
                input_exp=3,
            )
