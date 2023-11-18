import unittest

from sciform import Formatter, AutoDigits


FloatFormatterCases = list[tuple[float, list[tuple[Formatter, str]]]]


class TestFormatting(unittest.TestCase):
    def run_float_formatter_cases(self, cases_list: FloatFormatterCases):
        for num, formats_list in cases_list:
            for formatter, expected_num_str in formats_list:
                snum_str = formatter(num)
                with self.subTest(num=num,
                                  expected_num_str=expected_num_str,
                                  actual_num_str=snum_str):
                    self.assertEqual(snum_str, expected_num_str)

    def test_superscript_exp(self):
        cases_list = [
            (789, [
                (Formatter(exp_mode='scientific',
                           superscript_exp=True), '7.89×10²')
            ]),

            # Superscript in prefix mode when there's no replacement
            (789, [
                (Formatter(exp_mode='scientific',
                           exp_format='prefix',
                           superscript_exp=True), '7.89×10²')
            ]),
            (1024, [
                (Formatter(exp_mode='binary',
                           superscript_exp=True), '1×2¹⁰')
            ])
        ]

        self.run_float_formatter_cases(cases_list)

    def test_fill_and_separators(self):
        cases_list = [
            (123456789.654321, [
                (Formatter(
                    upper_separator='_',
                    lower_separator='_',
                    fill_mode='0',
                    top_dig_place=14), '000_000_123_456_789.654_321'),
                (Formatter(
                    upper_separator='_',
                    lower_separator='_',
                    fill_mode=' ',
                    top_dig_place=14), '      123_456_789.654_321'),
            ]),
            (4567899.7654321, [
                (Formatter(
                    upper_separator='_',
                    lower_separator='_',
                    fill_mode='0',
                    top_dig_place=14), '000_000_004_567_899.765_432_1'),
                (Formatter(
                    upper_separator='_',
                    lower_separator='_',
                    fill_mode=' ',
                    top_dig_place=14), '        4_567_899.765_432_1'),
            ])
        ]

        self.run_float_formatter_cases(cases_list)

    def test_latex(self):
        cases_list = [
            (789, [
                (Formatter(exp_mode='scientific',
                           latex=True), r'7.89\times 10^{+2}'),

                # Latex mode takes precedence over superscript_exp
                (Formatter(exp_mode='scientific',
                           latex=True,
                           superscript_exp=True), r'7.89\times 10^{+2}')
            ]),
            (12345, [
                (Formatter(exp_mode='scientific',
                           exp_val=-1,
                           upper_separator='_',
                           latex=True), r'123\_450\times 10^{-1}'),
                (Formatter(exp_mode='scientific',
                           exp_val=3,
                           exp_format='prefix',
                           latex=True), r'12.345\text{ k}')
            ]),
            (1024, [
                (Formatter(exp_mode='binary',
                           exp_val=8,
                           latex=True), r'4\times 2^{+8}')
            ])
        ]

        self.run_float_formatter_cases(cases_list)

    def test_nan(self):
        cases_list = [
            (float('nan'), [
                (Formatter(exp_mode='percent'), 'nan'),
                (Formatter(exp_mode='percent',
                           nan_inf_exp=True), '(nan)%'),
                (Formatter(exp_mode='percent',
                           latex=True), r'\text{nan}'),
                (Formatter(exp_mode='percent',
                           latex=True,
                           nan_inf_exp=True), r'\left(\text{nan}\right)\%')
            ])
        ]

        self.run_float_formatter_cases(cases_list)

    def test_parts_per_exp(self):
        cases_list = [
            (123e-3, [
                (Formatter(exp_mode='scientific',
                           exp_val=-3,
                           exp_format='parts_per',
                           add_ppth_form=True), '123 ppth'),
                (Formatter(exp_mode='scientific',
                           exp_val=-6,
                           exp_format='parts_per'), '123000 ppm'),
                (Formatter(exp_mode='scientific',
                           exp_val=-2,
                           exp_format='parts_per'), '12.3e-02')
            ]),
            (123e-9, [
                (Formatter(exp_mode='engineering',
                           exp_format='parts_per'), '123 ppb'),
                (Formatter(exp_mode='engineering',
                           exp_format='parts_per',
                           extra_parts_per_forms={-9: None, -12: 'ppb'}),
                 '123e-09')
            ]),
            (123e-12, [
                (Formatter(exp_mode='engineering',
                           exp_format='parts_per'), '123 ppt'),
                (Formatter(exp_mode='engineering',
                           exp_format='parts_per',
                           extra_parts_per_forms={-9: None, -12: 'ppb'}),
                 '123 ppb')
            ])
        ]

        self.run_float_formatter_cases(cases_list)

    def test_no_options(self):
        sform = Formatter()
        self.assertEqual(sform(42), '42')

    def test_dec_place_auto_round(self):
        sform = Formatter(round_mode='dec_place',
                          ndigits=AutoDigits)
        self.assertEqual(sform(123.456), '123.456')
