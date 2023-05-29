from typing import Union
from math import isfinite

from sciform.types import (_FILL_TYPES, _SIGN_TYPES, _UPPER_SEP_TYPES,
                           _DECIMAL_SEP_TYPES, _LOWER_SEP_TYPES, _ROUND_TYPES,
                           _FORMAT_TYPES)
from sciform.modes import (FillMode, GroupingSeparator,
                           FormatMode, AUTO)
from sciform.format_options import FormatOptions
from sciform.format_utils import (get_mantissa_exp_base, get_exp_str,
                                  get_top_and_bottom_digit,
                                  get_round_digit,
                                  format_float_by_top_bottom_dig)
from sciform.grouping import add_separators
from sciform.prefix import replace_prefix


def format_float(num: float, options: FormatOptions) -> str:
    format_mode = options.format_mode
    round_mode = options.round_mode
    precision = options.precision
    top_padded_digit = options.top_dig_place
    sign_mode = options.sign_mode
    capital_exp_char = options.capital_exp_char
    fill_char = FillMode.to_char(options.fill_mode)
    if not isfinite(num):
        if capital_exp_char:
            return str(num).upper()
        else:
            return str(num).lower()

    if format_mode is FormatMode.PERCENT:
        num *= 100

    exp = options.exp
    mantissa, temp_exp, base = get_mantissa_exp_base(num, format_mode, exp)

    top_digit, bottom_digit = get_top_and_bottom_digit(mantissa)
    round_digit = get_round_digit(top_digit, bottom_digit,
                                  precision, round_mode)

    mantissa_rounded = round(mantissa, -round_digit)

    '''
    Repeat mantissa + exponent discovery after rounding in case rounding
    altered the required exponent.
    '''
    rounded_num = mantissa_rounded * base**temp_exp
    mantissa, exp, base = get_mantissa_exp_base(rounded_num, format_mode, exp)

    top_digit, bottom_digit = get_top_and_bottom_digit(mantissa)
    round_digit = get_round_digit(top_digit, bottom_digit,
                                  precision, round_mode)

    mantissa_rounded = round(mantissa, -round_digit)
    if mantissa_rounded == 0:
        exp = 0

    exp_str = get_exp_str(exp, format_mode, capital_exp_char)

    if mantissa_rounded == -0.0:
        mantissa_rounded = abs(mantissa_rounded)
    mantissa_str = format_float_by_top_bottom_dig(mantissa_rounded,
                                                  top_padded_digit,
                                                  round_digit, sign_mode,
                                                  fill_char)

    # TODO: Think about the interaction between separators and fill
    #  characters
    thousands_separator = GroupingSeparator.to_char(
        options.upper_separator)
    decimal_separator = GroupingSeparator.to_char(options.decimal_separator)
    thousandths_separator = GroupingSeparator.to_char(
        options.lower_separator)
    mantissa_str = add_separators(mantissa_str,
                                  thousands_separator,
                                  decimal_separator,
                                  thousandths_separator,
                                  group_size=3)

    full_str = f'{mantissa_str}{exp_str}'

    if options.use_prefix:
        full_str = replace_prefix(full_str,
                                  options.extra_si_prefixes,
                                  options.extra_iec_prefixes)

    if format_mode is FormatMode.PERCENT:
        full_str = full_str + '%'

    return full_str


class Formatter:
    def __init__(
            self,
            *,
            fill_mode: _FILL_TYPES = None,
            sign_mode: _SIGN_TYPES = None,
            top_dig_place: int = None,
            upper_separator: _UPPER_SEP_TYPES = None,
            decimal_separator: _DECIMAL_SEP_TYPES = None,
            lower_separator: _LOWER_SEP_TYPES = None,
            round_mode: _ROUND_TYPES = None,
            precision: Union[int, type(AUTO)] = None,
            format_mode: _FORMAT_TYPES = None,
            capital_exp_char: bool = None,
            exp: Union[int, type(AUTO)] = None,
            use_prefix: bool = None,
            extra_si_prefixes: dict[int, str] = None,
            include_c_prefix: bool = False,
            include_small_si_prefixes: bool = False,
            extra_iec_prefixes: dict[int, str] = None,
            defaults: FormatOptions = None):
        self.options = FormatOptions.from_user_input(
            fill_mode=fill_mode,
            sign_mode=sign_mode,
            top_dig_place=top_dig_place,
            upper_separator=upper_separator,
            decimal_separator=decimal_separator,
            lower_separator=lower_separator,
            round_mode=round_mode,
            precision=precision,
            format_mode=format_mode,
            capital_exp_char=capital_exp_char,
            exp=exp,
            use_prefix=use_prefix,
            extra_si_prefixes=extra_si_prefixes,
            include_c_prefix=include_c_prefix,
            include_small_si_prefixes=include_small_si_prefixes,
            extra_iec_prefixes=extra_iec_prefixes,
            defaults=defaults
        )

    def format(self, num: float):
        return format_float(num, self.options)

    @classmethod
    def from_format_spec_str(cls, fmt: str):
        format_options = FormatOptions.from_format_spec_str(fmt)
        return cls(defaults=format_options)
