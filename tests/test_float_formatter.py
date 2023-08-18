import unittest

from sciform import (FormatOptions, Formatter, ExpMode, GroupingSeparator,
                     FillMode, RoundMode, AutoRound)


FloatFormatOptionsCases = list[tuple[float, list[tuple[FormatOptions, str]]]]


class TestFormatting(unittest.TestCase):
    def run_float_formatter_cases(self, cases_list: FloatFormatOptionsCases):
        for num, formats_list in cases_list:
            for format_options, expected_num_str in formats_list:
                formatter = Formatter(format_options)
                snum_str = formatter(num)
                with self.subTest(num=num,
                                  expected_num_str=expected_num_str,
                                  actual_num_str=snum_str):
                    self.assertEqual(snum_str, expected_num_str)

    def test_superscript_exp(self):
        cases_list = [
            (789, [
                (FormatOptions(exp_mode=ExpMode.SCIENTIFIC,
                               superscript_exp=True), '7.89×10²')
            ]),
            (1024, [
                (FormatOptions(exp_mode=ExpMode.BINARY,
                               superscript_exp=True), '1×2¹⁰')
            ])
        ]

        self.run_float_formatter_cases(cases_list)

    def test_fill_and_separators(self):
        cases_list = [
            (123456789.654321, [
                (FormatOptions(
                    upper_separator=GroupingSeparator.UNDERSCORE,
                    lower_separator=GroupingSeparator.UNDERSCORE,
                    fill_mode=FillMode.ZERO,
                    top_dig_place=14), '000_000_123_456_789.654_321'),
                (FormatOptions(
                    upper_separator=GroupingSeparator.UNDERSCORE,
                    lower_separator=GroupingSeparator.UNDERSCORE,
                    fill_mode=FillMode.SPACE,
                    top_dig_place=14), '      123_456_789.654_321'),
            ]),
            (4567899.7654321, [
                (FormatOptions(
                    upper_separator=GroupingSeparator.UNDERSCORE,
                    lower_separator=GroupingSeparator.UNDERSCORE,
                    fill_mode=FillMode.ZERO,
                    top_dig_place=14), '000_000_004_567_899.765_432_1'),
                (FormatOptions(
                    upper_separator=GroupingSeparator.UNDERSCORE,
                    lower_separator=GroupingSeparator.UNDERSCORE,
                    fill_mode=FillMode.SPACE,
                    top_dig_place=14), '        4_567_899.765_432_1'),
            ])
        ]

        self.run_float_formatter_cases(cases_list)

    def test_latex(self):
        cases_list = [
            (789, [
                (FormatOptions(exp_mode=ExpMode.SCIENTIFIC,
                               latex=True), r'7.89\times 10^{+2}'),

                # Latex mode takes precedence over superscript_exp
                (FormatOptions(exp_mode=ExpMode.SCIENTIFIC,
                               latex=True,
                               superscript_exp=True), r'7.89\times 10^{+2}')
            ]),
            (12345, [
                (FormatOptions(exp_mode=ExpMode.SCIENTIFIC,
                               exp_val=-1,
                               upper_separator=GroupingSeparator.UNDERSCORE,
                               latex=True), r'123\_450\times 10^{-1}'),
                (FormatOptions(exp_mode=ExpMode.SCIENTIFIC,
                               exp_val=3,
                               prefix_exp=True,
                               latex=True), r'12.345\text{k}')
            ])
        ]

        self.run_float_formatter_cases(cases_list)

    def test_nan(self):
        cases_list = [
            (float('nan'), [
                (FormatOptions(exp_mode=ExpMode.PERCENT), '(nan)%'),
                (FormatOptions(exp_mode=ExpMode.PERCENT,
                               latex=True), r'\left(nan\right)\%')
            ])
        ]

        self.run_float_formatter_cases(cases_list)

    def test_parts_per_exp(self):
        cases_list = [
            (123e-3, [
                (FormatOptions(exp_mode=ExpMode.SCIENTIFIC,
                               exp_val=-3,
                               parts_per_exp=True,
                               add_ppth_form=True), '123 ppth'),
                (FormatOptions(exp_mode=ExpMode.SCIENTIFIC,
                               exp_val=-6,
                               parts_per_exp=True), '123000 ppm'),
                (FormatOptions(exp_mode=ExpMode.SCIENTIFIC,
                               exp_val=-2,
                               parts_per_exp=True), '12.3e-02')
            ]),
            (123e-9, [
                (FormatOptions(exp_mode=ExpMode.ENGINEERING,
                               parts_per_exp=True), '123 ppb'),
                (FormatOptions(exp_mode=ExpMode.ENGINEERING,
                               parts_per_exp=True,
                               extra_parts_per_forms={-9: None, -12: 'ppb'}),
                 '123e-09')
            ]),
            (123e-12, [
                (FormatOptions(exp_mode=ExpMode.ENGINEERING,
                               parts_per_exp=True), '123 ppt'),
                (FormatOptions(exp_mode=ExpMode.ENGINEERING,
                               parts_per_exp=True,
                               extra_parts_per_forms={-9: None, -12: 'ppb'}),
                 '123 ppb')
            ])
        ]

        self.run_float_formatter_cases(cases_list)

    def test_no_options(self):
        sform = Formatter()
        self.assertEqual(sform(42), '42')

    def test_dec_place_auto_round(self):
        sform = Formatter(FormatOptions(round_mode=RoundMode.DEC_PLACE,
                                        ndigits=AutoRound))
        self.assertEqual(sform(123.456), '123.456')
