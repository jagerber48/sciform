import unittest

from sciform import (FormatOptions, SciNum, GlobalDefaultsContext, ExpMode,
                     GroupingSeparator, RoundMode, SignMode)


class TestConfig(unittest.TestCase):
    def test_global_defaults_context(self):
        num = SciNum(123.456)
        before_str = f'{num}'
        with GlobalDefaultsContext(FormatOptions(
                sign_mode=SignMode.ALWAYS,
                exp_mode=ExpMode.SCIENTIFIC,
                round_mode=RoundMode.SIG_FIG,
                precision=2,
                decimal_separator=GroupingSeparator.COMMA)):
            during_str = f'{num}'
        after_str = f'{num}'

        expected_before_str = '123.456'
        expected_during_str = '+1,2e+02'

        self.assertEqual(before_str, expected_before_str)
        self.assertEqual(during_str, expected_during_str)
        self.assertEqual(after_str, expected_before_str)

    def test_c_prefix(self):
        num = SciNum(123.456)
        with GlobalDefaultsContext(FormatOptions(add_c_prefix=True)):
            num_str = f'{num:ex-2p}'

        expected_num_str = '12345.6 c'

        self.assertEqual(num_str, expected_num_str)

    def test_small_si_prefixes(self):
        num = SciNum(123.456)

        cases_dict = {-2: '12345.6 c',
                      -1: '1234.56 d',
                      +1: '12.3456 da',
                      +2: '1.23456 h'}

        with GlobalDefaultsContext(FormatOptions(add_small_si_prefixes=True)):
            for exp, expected_num_str in cases_dict.items():
                num_str = f'{num:ex{exp:+}p}'
                self.assertEqual(num_str, expected_num_str)


if __name__ == "__main__":
    unittest.main()
