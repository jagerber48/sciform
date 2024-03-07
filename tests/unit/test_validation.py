import unittest

from sciform.options.input_options import InputOptions


class TestValidation(unittest.TestCase):
    def test_validate_exp_mode(self):
        self.assertRaises(
            ValueError,
            InputOptions,
            exp_mode="sci",
        )

    def test_validate_exp_val(self):
        self.assertRaises(
            TypeError,
            InputOptions,
            exp_val=1.0,
        )

    def test_validate_round_mode(self):
        self.assertRaises(
            ValueError,
            InputOptions,
            round_mode="sigfig",
        )

    def test_validate_ndigits(self):
        self.assertRaises(
            TypeError,
            InputOptions,
            ndigits=3.0,
        )

    def test_validate_upper_separator(self):
        self.assertRaises(
            ValueError,
            InputOptions,
            upper_separator="-",
        )

    def test_validate_decimal_separator(self):
        self.assertRaises(
            ValueError,
            InputOptions,
            decimal_separator="_",
        )

    def test_validate_lower_separator(self):
        self.assertRaises(
            ValueError,
            InputOptions,
            lower_separator=",",
        )

    def test_validate_upper_decimal_separator(self):
        with self.subTest(msg="double_commas"):
            self.assertRaises(
                ValueError,
                InputOptions,
                upper_separator=",",
                lower_separator=",",
            )
        with self.subTest(msg="double_periods"):
            self.assertRaises(
                ValueError,
                InputOptions,
                upper_separator=".",
                lower_separator=".",
            )

    def test_validate_sign_mode(self):
        self.assertRaises(
            ValueError,
            InputOptions,
            sign_mode="always",
        )

    def test_validate_left_pad_char(self):
        self.assertRaises(
            ValueError,
            InputOptions,
            left_pad_char="-",
        )

    def test_validate_left_pad_dec_place(self):
        with self.subTest(msg="non_int"):
            self.assertRaises(
                TypeError,
                InputOptions,
                left_pad_dec_place=1.0,
            )
        with self.subTest(msg="negative"):
            self.assertRaises(
                ValueError,
                InputOptions,
                left_pad_dec_place=-2,
            )

    def test_validate_exp_format(self):
        self.assertRaises(
            ValueError,
            InputOptions,
            exp_format="super",
        )

    def test_validate_extra_translations(self):
        translation_keys = (
            "extra_si_prefixes",
            "extra_iec_prefixes",
            "extra_parts_per_forms",
        )

        invalid_keys = (-1.0, "3")
        for translation_key in translation_keys:
            for key in invalid_keys:
                with self.subTest(
                    msg="test_non_int_key",
                    translation_key=translation_key,
                    key=key,
                ):
                    kwargs = {translation_key: {key: "test"}}
                    self.assertRaises(
                        TypeError,
                        InputOptions,
                        **kwargs,
                    )

        invalid_strs = ("3", "Å")
        for translation_key in translation_keys:
            for invalid_str in invalid_strs:
                with self.subTest(
                    msg="non_alphabetic_val",
                    translation_key=translation_key,
                    invalid_str=invalid_str,
                ):
                    kwargs = {translation_key: {3: invalid_str}}
                    self.assertRaises(
                        ValueError,
                        InputOptions,
                        **kwargs,
                    )
