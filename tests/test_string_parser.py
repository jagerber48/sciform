import unittest
from typing import Optional

from sciform import SciNum
from sciform.format_utils import Number

CasesList = list[tuple[str, tuple[Number, Optional[Number]]]]


NAN = float("nan")
INF = float("inf")


class TestStringParser(unittest.TestCase):
    def run_cases(self, cases: CasesList):
        for string, (val, unc) in cases:
            print(string)
            expected_sci_num = SciNum(val, unc)
            result_sci_num = SciNum(string)
            with self.subTest(
                input_string=string,
                expected_sci_num=expected_sci_num,
                actual_sci_num=result_sci_num,
            ):
                self.assertEqual(result_sci_num, expected_sci_num)

    def test_string_parse_cases(self):
        cases = [
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
                (3.1415e+30, None),
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
                "1234,567",
                (1234.567, None),
            ),
            (
                "123,45",
                (123.45, None),
            ),
        ]

        self.run_cases(cases)
