import unittest
from decimal import Decimal
from math import isnan
from typing import Optional

from sciform import GlobalOptionsContext, SciNum, modes
from sciform.format_utils import Number
from sciform.parser import parse_val_unc_from_str

CasesList = list[tuple[str, tuple[Number, Optional[Number]]]]


NAN = float("nan")
INF = float("inf")

shared_cases = [
    (
        "000_000_123_456_789.654_321",
        (123456789.654321, None),
    ),
    (
        "123_456_789.654_321",
        (123456789.654321, None),
    ),
    (
        "nan",
        (NAN, None),
    ),
    (
        "inf",
        (INF, None),
    ),
    (
        "-inf",
        (-INF, None),
    ),
    (
        "NAN",
        (NAN, None),
    ),
    (
        "INF",
        (INF, None),
    ),
    (
        "-INF",
        (-INF, None),
    ),
    (
        "(nan)%",
        (NAN, None),
    ),
    (
        "(nan)e+00",
        (NAN, None),
    ),
    (
        "0.000123e+03",
        (0.123, None),
    ),
    (
        "0.123",
        (0.123, None),
    ),
    (
        "123e-09",
        (123e-9, None),
    ),
    (
        "123 ppb",
        (123e-9, None),
    ),
    (
        "7.89×10²",
        (7.89e2, None),
    ),
    (
        "1×2¹⁰",
        (1024, None),
    ),
    (
        "1b+10",
        (1024, None),
    ),
    (
        "0b+00",
        (0, None),
    ),
    (
        "1.618033e+04",
        (16180.33, None),
    ),
    (
        "-1.618033e+04",
        (-16180.33, None),
    ),
    (
        "12.3456%",
        (0.123456, None),
    ),
    (
        "3.1415 q",
        (3.1415e-30, None),
    ),
    (
        "3.1415 Q",
        (3.1415e30, None),
    ),
    (
        "1 Ki",
        (1024, None),
    ),
    (
        "1 Pi",
        (2**50, None),
    ),
    (
        "123.456.789,987_654_321",
        ("123456789.987654321", None),
    ),
    (
        "123,456,789.987 654 321",
        ("123456789.987654321", None),
    ),
    (
        "123(0)",
        (123, 00),
    ),
    (
        "123(nan)",
        (123, NAN),
    ),
    (
        "123(inf)",
        (123, INF),
    ),
    (
        "1234.56(7.89)e-01",
        (123.456, 0.789),
    ),
    (
        "nan(1.2)",
        (NAN, 1.2),
    ),
    (
        "nan(nan)",
        (NAN, NAN),
    ),
    (
        "10.000 ± 0.035",
        (10, 0.035),
    ),
    (
        "(3.1416 ± 0.0016) M",
        (3.1416e6, 0.0016e6),
    ),
    (
        "(12.345_678 ± 0.000_255)%",
        (0.12345678, 0.00000255),
    ),
    (
        "123.456(789) k",
        (123.456e3, 0.789e3),
    ),
    (
        "123.456(789) ppm",
        (123.456e-6, 0.789e-6),
    ),
    (
        "123.456(789) μ",
        (123.456e-6, 0.789e-6),
    ),
    (
        "(7.8900 ± 0.0001)×10²",
        (7.89e2, 0.0001e2),
    ),
    (
        "(7.8900±0.0001)×10²",
        (7.89e2, 0.0001e2),
    ),
    (
        "(1.23456 ± 0.00789)E+02",
        (123.456, 0.789),
    ),
    (
        "(NAN ± NAN)E+00",
        (NAN, NAN),
    ),
    (
        "(INF ± NAN)E+00",
        (INF, NAN),
    ),
    (
        "+  123.456 ±     0.789",
        (123.456, 0.789),
    ),
    (
        "-  123.456 ±     0.789",
        (-123.456, 0.789),
    ),
    (
        "00123.46 ± 00000.79",
        (123.46, 0.79),
    ),
    (
        "00123.46 +/- 00000.79",
        (123.46, 0.79),
    ),
    (
        "00000.789 ± 00123.456",
        (0.789, 123.456),
    ),
    (
        "(inf ± 1.234)e+01",
        (INF, 12.34),
    ),
    (
        "0.000000(1.234560)e+02",
        (0, 123.456),
    ),
    (
        "123,456",
        (123456, None),
    ),
    (
        "1234,567",
        (1234.567, None),
    ),
    (
        "123,45",
        (123.45, None),
    ),
    (
        "123.456",
        (123.456, None),
    ),
    (
        "1234.567",
        (1234.567, None),
    ),
    (
        "123.45",
        (123.45, None),
    ),
    (
        "1.0 +/- 23",
        (1, 23),
    ),
    (
        "1.0+/-23",
        (1, 23),
    ),
]


class TestStringParser(unittest.TestCase):
    def assertNanNoneEqual(self, first, second, msg=None):  # noqa: N802
        if first is None:
            self.assertIsNone(second, msg=msg)
        elif isnan(first):
            self.assertTrue(isnan(second), msg=msg)
        else:
            self.assertEqual(first, second, msg=msg)

    def run_direct_cases(
        self,
        cases: CasesList,
        decimal_separator: modes.DecimalSeparators = ".",
    ):
        for string, (val, unc) in cases:
            expected_val = Decimal(str(val))
            expected_unc = Decimal(str(unc)) if unc is not None else unc
            result_val, result_unc = parse_val_unc_from_str(
                string,
                decimal_separator=decimal_separator,
            )
            with self.subTest(
                input_string=string,
                expected_val=expected_val,
                expected_unc=expected_unc,
                result_val=result_val,
                result_unc=result_unc,
            ):
                self.assertNanNoneEqual(
                    result_val,
                    expected_val,
                    msg="Value not equal",
                )
                self.assertNanNoneEqual(
                    result_unc,
                    expected_unc,
                    msg="Uncertainty not equal",
                )

    def run_scinum_cases(self, cases: CasesList):
        for string, (val, unc) in cases:
            expected_scinum = SciNum(val, unc)
            result_scinum = SciNum(string)
            with self.subTest(
                input_string=string,
                expected_scinum=expected_scinum,
                result_scinum=result_scinum,
            ):
                self.assertEqual(result_scinum, expected_scinum)

    def test_string_parse_cases(self):
        self.run_direct_cases(shared_cases)

    def test_scinum_cases(self):
        self.run_scinum_cases(shared_cases)

    def test_scinum_double_input(self):
        self.assertEqual(SciNum("1 k", "1 m"), SciNum(1e3, 1e-3))

    def test_unrecognized_prefix(self):
        self.assertRaises(
            ValueError,
            parse_val_unc_from_str,
            "1 d",
        )

    def test_comma_decimal_separator(self):
        cases = [
            (
                "123,456",
                (123.456, None),
            ),
        ]
        self.run_direct_cases(cases, decimal_separator=",")

    def test_cannot_parse(self):
        self.assertRaises(
            ValueError,
            parse_val_unc_from_str,
            "nan%",
        )

    def test_paren_uncertainty_too_many_digits(self):
        self.assertRaises(
            ValueError,
            parse_val_unc_from_str,
            "123.4(56)",
        )

    def test_multiple_translations(self):
        with GlobalOptionsContext(
            extra_si_prefixes={-9: "ppb"},
            extra_parts_per_forms={-12: "ppb"},
        ):
            self.assertRaises(
                ValueError,
                parse_val_unc_from_str,
                "3 ppb",
            )

    def test_extra_translations(self):
        cases = [
            (
                "1 c",
                (1e-2, None),
            ),
            (
                "1 da",
                (1e1, None),
            ),
            (
                "3 ppth",
                (3e-3, None),
            ),
        ]
        with GlobalOptionsContext(
            add_small_si_prefixes=True,
            add_ppth_form=True,
        ):
            self.run_direct_cases(cases)

    def test_decimal_comma_separator(self):
        cases = [
            (
                "123,456",
                (123.456, None),
            ),
            (
                "123.456",
                (123456, None),
            ),
            (
                "123,456.789",
                (123456.789, None),
            ),
            (
                "123.456,789",
                (123456.789, None),
            ),
            (
                "123.456.789",
                (123456789, None),
            ),
            (
                "123,456,789",
                (123456789, None),
            ),
            (
                "123,45 +/- 123.456",
                (123.45, 123456),
            ),
            (
                "123.45 +/- 123,456",
                (123.45, 123456),
            ),
        ]
        with GlobalOptionsContext(decimal_separator=","):
            self.run_scinum_cases(cases)

    def test_decimal_point_separator(self):
        cases = [
            (
                "123,456",
                (123456, None),
            ),
            (
                "123.456",
                (123.456, None),
            ),
            (
                "123.456,789",
                (123456.789, None),
            ),
            (
                "123,456.789",
                (123456.789, None),
            ),
            (
                "123.456.789",
                (123456789, None),
            ),
            (
                "123,456,789",
                (123456789, None),
            ),
            (
                "123,45 +/- 123.456",
                (123.45, 123456),
            ),
            (
                "123.45 +/- 123,456",
                (123.45, 123456),
            ),
        ]
        with GlobalOptionsContext(decimal_separator="."):
            self.run_scinum_cases(cases)

    def test_conflicting_decimal_separator(self):
        self.assertRaises(
            ValueError,
            parse_val_unc_from_str,
            "123.45(0,3)",
        )
