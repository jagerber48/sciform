import unittest

from sciform import (
    Formatter,
    GlobalDefaultsContext,
    SciNum,
    reset_global_defaults,
    set_global_defaults,
)


class TestConfig(unittest.TestCase):
    def test_set_reset_global_defaults(self):
        num = SciNum(0.0005632)
        self.assertEqual(f"{num}", "0.0005632")
        set_global_defaults(exp_mode="engineering_shifted", capitalize=True)
        self.assertEqual(f"{num}", "0.5632E-03")
        reset_global_defaults()
        self.assertEqual(f"{num}", "0.0005632")

    def test_global_defaults_context(self):
        num = SciNum(123.456)
        self.assertEqual(f"{num}", "123.456")
        with GlobalDefaultsContext(
            sign_mode="+",
            exp_mode="scientific",
            round_mode="sig_fig",
            ndigits=2,
            decimal_separator=",",
        ):
            self.assertEqual(f"{num}", "+1,2e+02")
        self.assertEqual(f"{num}", "123.456")

    def test_c_prefix(self):
        num = SciNum(123.456)
        fmt_spec = "ex-2p"
        self.assertEqual(f"{num:{fmt_spec}}", "12345.6e-02")
        with GlobalDefaultsContext(add_c_prefix=True):
            self.assertEqual(f"{num:{fmt_spec}}", "12345.6 c")
        self.assertEqual(f"{num:{fmt_spec}}", "12345.6e-02")

    def test_small_si_prefixes(self):
        num = SciNum(123.456)

        cases_dict = {
            -2: "12345.6 c",
            -1: "1234.56 d",
            +1: "12.3456 da",
            +2: "1.23456 h",
        }

        with GlobalDefaultsContext(add_small_si_prefixes=True):
            for exp, expected_num_str in cases_dict.items():
                num_str = f"{num:ex{exp:+}p}"
                self.assertEqual(num_str, expected_num_str)

    def test_iec_prefix(self):
        num = SciNum(1024)
        fmt_spec = "bp"
        self.assertEqual(f"{num:{fmt_spec}}", "1 Ki")
        with GlobalDefaultsContext(extra_iec_prefixes={10: "KiB"}):
            self.assertEqual(f"{num:{fmt_spec}}", "1 KiB")
        self.assertEqual(f"{num:{fmt_spec}}", "1 Ki")

    def test_ppth_form(self):
        num = 0.0024
        formatter = Formatter(
            exp_mode="engineering",
            exp_format="parts_per",
        )
        self.assertEqual(formatter(num), "2.4e-03")
        with GlobalDefaultsContext(add_ppth_form=True):
            self.assertEqual(formatter(num), "2.4 ppth")
        self.assertEqual(formatter(num), "2.4e-03")
