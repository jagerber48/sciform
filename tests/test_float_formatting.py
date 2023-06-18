import unittest

from sciform import Formatter, ExpMode


class TestFormatting(unittest.TestCase):
    # TODO: Test direct call to format float (i.e. not via sfloat or Formatter)
    def do_test_case_dict(self, cases_dict: dict[float, dict[Formatter, str]]):
        for num, fmt_dict in cases_dict.items():
            for formatter, expected_num_str in fmt_dict.items():
                snum_str = formatter(num)
                with self.subTest(num=num,
                                  expected_num_str=expected_num_str,
                                  actual_num_str=snum_str):
                    self.assertEqual(snum_str, expected_num_str)

    def test_superscript_exp(self):
        cases_dict = {
            789: {
                Formatter(exp_mode=ExpMode.SCIENTIFIC,
                          superscript_exp=True): '7.89×10²'
            }
        }

        self.do_test_case_dict(cases_dict)
