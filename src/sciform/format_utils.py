import sys
from typing import Union
from math import floor, log10, log2, isfinite
from warnings import warn

from sciform.modes import FormatMode, RoundMode, SignMode, AutoExp, AutoPrec


def get_top_digit(num: float) -> int:
    if not isfinite(num):
        return 0
    num = abs(num)
    int_part = int(num)
    if int_part == 0:
        magnitude = 1
    else:
        magnitude = int(log10(int_part)) + 1
    max_digits = sys.float_info.dig
    if magnitude >= max_digits:
        return magnitude

    try:
        top_digit = floor(log10(num))
    except ValueError:
        top_digit = 0
    return top_digit


def get_bottom_digit(num: float) -> int:
    if not isfinite(num):
        return 0

    num = abs(num)
    max_digits = sys.float_info.dig
    int_part = int(num)
    if int_part == 0:
        magnitude = 1
    else:
        magnitude = int(log10(int_part)) + 1

    if magnitude >= max_digits:
        return 0

    frac_part = num - int_part
    multiplier = 10 ** (max_digits - magnitude)
    frac_digits = multiplier + int(multiplier * frac_part + 0.5)
    while frac_digits % 10 == 0:
        frac_digits /= 10
    precision = int(log10(frac_digits))

    bottom_digit = -precision

    return bottom_digit


def get_top_and_bottom_digit(num: float) -> tuple[int, int]:
    return get_top_digit(num), get_bottom_digit(num)


def get_mantissa_exp_base(
        num: float,
        format_mode: FormatMode,
        exp: Union[int, type(AutoExp)] = None) -> (float, int, int):
    if num == 0:
        if exp is AutoExp:
            exp = 0
        base = 10
    elif (format_mode is FormatMode.FIXEDPOINT
          or format_mode is FormatMode.PERCENT):
        if exp is not AutoExp:
            if exp != 0:
                warn('Attempt to set exponent explicity in fixed point '
                     'exponent mode. Coercing exponent to 0.')
        exp = 0
        base = 10
    elif format_mode is FormatMode.SCIENTIFIC:
        if exp is AutoExp:
            exp = floor(log10(abs(num)))
        base = 10
    elif (format_mode is FormatMode.ENGINEERING
          or format_mode is FormatMode.ENGINEERING_SHIFTED):
        if exp is not AutoExp:
            if exp % 3 != 0:
                warn(f'Attempt to set exponent explicity to a non-integer '
                     f'multiple of 3 in engineering mode. Coercing to the '
                     f'next lower multiple of 3.')
                exp = (exp // 3) * 3
            if format_mode is FormatMode.ENGINEERING_SHIFTED:
                warn(f'Engineering shifted mode is ignored when setting '
                     f'exponent explicitly.')
        else:
            exp = floor(log10(abs(num)))
            if format_mode is FormatMode.ENGINEERING:
                exp = (exp // 3) * 3
            else:
                exp = ((exp + 1) // 3) * 3
        base = 10
    elif (format_mode is FormatMode.BINARY
          or format_mode is FormatMode.BINARY_IEC):
        if exp is AutoExp:
            exp = floor(log2(abs(num)))
            if format_mode is FormatMode.BINARY_IEC:
                exp = (exp // 10) * 10
        elif format_mode is FormatMode.BINARY_IEC:
            warn(f'Binary IEC mode is ignored when setting exponent '
                 f'explicitly')
        base = 2
    else:
        raise ValueError(f'Unhandled format mode: {format_mode}')

    mantissa = num * base**-exp

    return mantissa, exp, base


def get_exp_str(exp: int, format_mode: FormatMode,
                capital_exp_char: bool) -> str:
    if (format_mode is format_mode.FIXEDPOINT
            or format_mode is format_mode.PERCENT):
        exp_str = ''
    elif (format_mode is FormatMode.SCIENTIFIC
          or format_mode is FormatMode.ENGINEERING
          or format_mode is FormatMode.ENGINEERING_SHIFTED):
        exp_char = 'E' if capital_exp_char else 'e'
        exp_str = f'{exp_char}{exp:+03d}'
    elif (format_mode is FormatMode.BINARY
          or format_mode is FormatMode.BINARY_IEC):
        exp_char = 'B' if capital_exp_char else 'b'
        exp_str = f'{exp_char}{exp:+03d}'
    else:
        raise ValueError(f'Unhandled format type {format_mode}')
    return exp_str


def get_sign_str(num: float, sign_mode: SignMode) -> str:
    if num < 0:
        sign_str = '-'
    else:
        if sign_mode is SignMode.ALWAYS:
            sign_str = '+'
        elif sign_mode is SignMode.SPACE:
            sign_str = ' '
        elif sign_mode is SignMode.NEGATIVE:
            sign_str = ''
        else:
            raise ValueError(f'Invalid sign mode {sign_mode}.')
    return sign_str


def get_round_digit(top_digit: int, bottom_digit: int,
                    prec: Union[int, type(AutoPrec)], prec_mode: RoundMode) -> int:
    # TODO: Decide on default precision/sig figs.  Minimum round-trippable or
    #  hard-coded to 6?
    if prec_mode is RoundMode.SIG_FIG:
        if prec is AutoPrec:
            prec = top_digit - bottom_digit + 1
        round_digit = top_digit - (prec - 1)
    elif prec_mode is RoundMode.PREC:
        if prec is AutoPrec:
            round_digit = bottom_digit
        else:
            round_digit = -prec
    else:
        raise TypeError(f'Unhandled precision type: {prec_mode}.')
    return round_digit


def get_fill_str(fill_char: ' ', top_digit: int, top_padded_digit: int) -> str:
    if top_padded_digit > top_digit:
        pad_len = top_padded_digit - max(top_digit, 0)
        pad_str = fill_char*pad_len
    else:
        pad_str = ''
    return pad_str


def format_float_by_top_bottom_dig(num: float,
                                   target_top_digit: int,
                                   target_bottom_digit: int,
                                   sign_mode: SignMode,
                                   fill_char: str) -> str:
    num_rounded = round(num, -target_bottom_digit)

    print_prec = max(0, -target_bottom_digit)
    abs_mantissa_str = f'{abs(num_rounded):.{print_prec}f}'

    sign_str = get_sign_str(num, sign_mode)

    num_top_digit = get_top_digit(num_rounded)
    fill_str = get_fill_str(fill_char, num_top_digit, target_top_digit)
    float_str = f'{sign_str}{fill_str}{abs_mantissa_str}'

    return float_str
