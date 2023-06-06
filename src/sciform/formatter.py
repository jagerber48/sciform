from typing import Union
from math import isfinite

from sciform.modes import (SignMode, FillMode, UpperGroupingSeparators,
                           DecimalGroupingSeparators, LowerGroupingSeparators,
                           FormatMode, RoundMode, AUTO)
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
    upper_separator = options.upper_separator.to_char()
    decimal_separator = options.decimal_separator.to_char()
    lower_separator = options.lower_separator.to_char()
    mantissa_str = add_separators(mantissa_str,
                                  upper_separator,
                                  decimal_separator,
                                  lower_separator,
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
            defaults: 'FormatOptions' = None,
            fill_mode: FillMode = None,
            sign_mode: SignMode = None,
            top_dig_place: int = None,
            upper_separator: UpperGroupingSeparators = None,
            decimal_separator: DecimalGroupingSeparators = None,
            lower_separator: LowerGroupingSeparators = None,
            round_mode: RoundMode = None,
            precision: Union[int, type(AUTO)] = None,
            format_mode: FormatMode = None,
            capital_exp_char: bool = None,
            exp: Union[int, type(AUTO)] = None,
            use_prefix: bool = None,
            extra_si_prefixes: dict[int, str] = None,
            extra_iec_prefixes: dict[int, str] = None,
            add_c_prefix: bool = False,
            add_small_si_prefixes: bool = False
    ):
        self.options = FormatOptions.make(
            defaults=defaults,
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
            extra_iec_prefixes=extra_iec_prefixes,
            add_c_prefix=add_c_prefix,
            add_small_si_prefixes=add_small_si_prefixes)

    def __call__(self, num: float):
        return self.format(num)

    def format(self, num: float):
        return format_float(num, self.options)

    @classmethod
    def from_format_spec_str(cls, fmt: str):
        format_options = FormatOptions.from_format_spec_str(fmt)
        return cls(defaults=format_options)
