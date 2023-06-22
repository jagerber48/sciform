import sys
from typing import Union
from math import floor, log10, log2, isfinite
from warnings import warn
import re
from copy import copy

from sciform.modes import ExpMode, RoundMode, SignMode, AutoExp, AutoPrec
from sciform.prefix import (si_val_to_prefix_dict, iec_val_to_prefix_dict,
                            pp_val_to_prefix_dict)


def get_top_digit(num: float, binary=False) -> int:
    if not isfinite(num):
        return 0
    elif num == 0:
        return 0
    else:
        if not binary:
            return floor(log10(abs(num)))
        else:
            return floor(log2(abs(num)))


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
    frac_digits = multiplier + floor(multiplier * frac_part + 0.5)
    while frac_digits % 10 == 0:
        frac_digits /= 10
    precision = int(log10(frac_digits))

    bottom_digit = -precision

    return bottom_digit


def get_top_and_bottom_digit(num: float) -> tuple[int, int]:
    return get_top_digit(num), get_bottom_digit(num)


def get_mantissa_exp_base(
        num: float,
        exp_mode: ExpMode,
        exp: Union[int, type(AutoExp)] = None) -> (float, int, int):
    if (exp_mode is ExpMode.BINARY
            or exp_mode is ExpMode.BINARY_IEC):
        base = 2
    else:
        base = 10

    if not isfinite(num):
        mantissa = num
        if exp is AutoExp:
            exp = 0
    elif num == 0:
        mantissa = 0
        if exp is AutoExp:
            exp = 0
    else:
        if exp_mode is ExpMode.FIXEDPOINT:
            if exp is not AutoExp:
                if exp != 0:
                    warn('Attempt to set non-zero exponent explicity in fixed '
                         'point exponent mode. Coercing exponent to 0.')
            exp = 0
        elif exp_mode is ExpMode.SCIENTIFIC:
            if exp is AutoExp:
                exp = get_top_digit(num)
        elif (exp_mode is ExpMode.ENGINEERING
              or exp_mode is ExpMode.ENGINEERING_SHIFTED):
            if exp is AutoExp:
                exp = get_top_digit(num)
                if exp_mode is ExpMode.ENGINEERING:
                    exp = (exp // 3) * 3
                else:
                    exp = ((exp + 1) // 3) * 3
            else:
                if exp % 3 != 0:
                    warn(f'Attempt to set exponent explicity to a non-integer '
                         f'multiple of 3 in engineering mode. Coercing to the '
                         f'next lower multiple of 3.')
                    exp = (exp // 3) * 3
        elif (exp_mode is ExpMode.BINARY
              or exp_mode is ExpMode.BINARY_IEC):
            if exp is AutoExp:
                exp = get_top_digit(num, binary=True)
                if exp_mode is ExpMode.BINARY_IEC:
                    exp = (exp // 10) * 10
            else:
                if exp_mode is ExpMode.BINARY_IEC and exp % 10 != 0:
                    warn(f'Attempt to set exponent explicity to a non-integer '
                         f'multiple of 10 in binary IEC mode. Coercing to the '
                         f'next lower multiple of 10.')
                    exp = (exp // 10) * 10

        mantissa = num * base**-exp

    return mantissa, exp, base


def get_exp_str(exp: int, exp_mode: ExpMode,
                capitalize: bool) -> str:
    if exp_mode is exp_mode.FIXEDPOINT:
        exp_str = ''
    elif (exp_mode is ExpMode.SCIENTIFIC
          or exp_mode is ExpMode.ENGINEERING
          or exp_mode is ExpMode.ENGINEERING_SHIFTED):
        exp_char = 'E' if capitalize else 'e'
        exp_str = f'{exp_char}{exp:+03d}'
    elif (exp_mode is ExpMode.BINARY
          or exp_mode is ExpMode.BINARY_IEC):
        exp_char = 'B' if capitalize else 'b'
        exp_str = f'{exp_char}{exp:+03d}'
    else:
        raise ValueError(f'Unhandled format type {exp_mode}')
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


def get_round_digit(num: float,
                    round_mode: RoundMode,
                    precision: Union[int, type(AutoPrec)],
                    pdg_sig_figs: bool = False) -> int:
    if round_mode is RoundMode.SIG_FIG:
        top_digit = get_top_digit(num)
        if precision is AutoPrec:
            bottom_digit = get_bottom_digit(num)
            if not pdg_sig_figs:
                round_digit = bottom_digit
            else:
                num_top_three_digs = num * 10**(2-top_digit)
                num_top_three_digs = round(num_top_three_digs)
                new_top_digit = get_top_digit(num_top_three_digs)
                num_top_three_digs = num_top_three_digs * 10**(2-new_top_digit)
                if 100 <= num_top_three_digs <= 354:
                    round_digit = top_digit - 1
                elif 355 <= num_top_three_digs <= 949:
                    round_digit = top_digit
                elif 950 <= num_top_three_digs <= 999:
                    '''
                    In this case the top three digits will be rounded up to 
                    1000 so round_digit=top_digit will actually correspond to
                    two significant figures with respect to the rounded value.
                    This is in accordance with the PDG specification.
                    '''
                    round_digit = top_digit
                else:
                    raise ValueError(f'{num_top_three_digs} not right')
        else:
            round_digit = top_digit - (precision - 1)
    elif round_mode is RoundMode.PREC:
        if precision is AutoPrec:
            round_digit = get_bottom_digit(num)
        else:
            round_digit = -precision
    else:
        raise TypeError(f'Unhandled round mode: {round_mode}.')
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
    print_prec = max(0, -target_bottom_digit)
    abs_mantissa_str = f'{abs(num):.{print_prec}f}'

    sign_str = get_sign_str(num, sign_mode)

    num_top_digit = get_top_digit(num)
    fill_str = get_fill_str(fill_char, num_top_digit, target_top_digit)
    float_str = f'{sign_str}{fill_str}{abs_mantissa_str}'

    return float_str


def get_exp_symb_sign_digits(exp_str: str):
    if exp_str == '':
        return exp_str
    match = re.match(
        r'''
         ^
         (?P<exp_symb>[eEbB])
         (?P<exp_sign>[+-])
         (?P<exp_digits>\d+)
         $
         ''',
        exp_str, re.VERBOSE)
    exp_symb = match.group('exp_symb')
    exp_sign = match.group('exp_sign')
    exp_digits = match.group('exp_digits')
    return exp_symb, exp_sign, exp_digits


def convert_exp_str_to_superscript(exp_str: str):
    if exp_str == '':
        return exp_str

    exp_symb, exp_sign, exp_digits = get_exp_symb_sign_digits(exp_str)

    if exp_sign == '+':
        # Superscript + does not look good, so drop it.
        exp_sign = ''
    exp_digits = exp_digits.lstrip('0')
    if exp_digits == '':
        exp_digits = '0'

    sup_trans = str.maketrans("+-0123456789", "⁺⁻⁰¹²³⁴⁵⁶⁷⁸⁹")
    if exp_symb in ['e', 'E']:
        base = '10'
    else:
        base = '2'
    exp_val_str = f'{exp_sign}{exp_digits}'.translate(sup_trans)
    super_script_exp_str = f'×{base}{exp_val_str}'
    return super_script_exp_str


def convert_exp_str_to_latex(exp_str):
    if exp_str == '':
        return exp_str

    exp_symb, exp_sign, exp_digits = get_exp_symb_sign_digits(exp_str)

    exp_digits = exp_digits.lstrip('0')
    if exp_digits == '':
        exp_digits = '0'

    if exp_symb in ['e', 'E']:
        base = '10'
    else:
        base = '2'

    latex_exp_str = rf'\times {base}^{{{exp_sign}{exp_digits}}}'
    return latex_exp_str


def translate_exp_str(exp_str: str,
                      parts_per_exp: bool = False,
                      extra_si_prefixes: dict[int, str] = None,
                      extra_iec_prefixes: dict[int, str] = None,
                      extra_parts_per_forms: dict[int, str] = None) -> str:
    if exp_str == '':
        return exp_str

    exp_symb, exp_sign, exp_digits = get_exp_symb_sign_digits(exp_str)

    exp_val = int(f'{exp_sign}{exp_digits}')
    if exp_val == 0:
        return ''

    if exp_symb in ['e', 'E']:
        if parts_per_exp:
            val_to_prefix_dict = copy(pp_val_to_prefix_dict)
            if extra_parts_per_forms is not None:
                val_to_prefix_dict.update(extra_parts_per_forms)
        else:
            val_to_prefix_dict = copy(si_val_to_prefix_dict)
            if extra_si_prefixes is not None:
                val_to_prefix_dict.update(extra_si_prefixes)
    else:
        val_to_prefix_dict = copy(iec_val_to_prefix_dict)
        if extra_iec_prefixes is not None:
            val_to_prefix_dict.update(extra_iec_prefixes)
    try:
        # TODO: If the returned value is None, don't do the replacement.
        #  This will allow users to set certain exponent translations to
        #  None to stop particular translations. This may be useful,
        #  e.g. to stop mapping 10**-9 to ppb for locales where
        #  one billion = 10**12, not 10**9.
        prefix = val_to_prefix_dict[exp_val]
        return f' {prefix}'
    except KeyError:
        return exp_str


def convert_exp_str(exp_str: str,
                    prefix_exp: bool,
                    parts_per_exp: bool,
                    latex: bool,
                    superscript_exp: bool,
                    extra_si_prefixes: dict[int, str] = None,
                    extra_iec_prefixes: dict[int, str] = None,
                    extra_parts_per_forms: dict[int, str] = None) -> str:
    transform_applied = False
    if prefix_exp or parts_per_exp:
        transformed_exp_str = translate_exp_str(exp_str,
                                                parts_per_exp,
                                                extra_si_prefixes,
                                                extra_iec_prefixes,
                                                extra_parts_per_forms)
        if transformed_exp_str != exp_str:
            transform_applied = True
            exp_str = transformed_exp_str

    if transform_applied:
        return exp_str
    else:
        if latex:
            # TODO: \text{} if prefix_exp and transform_applied
            exp_str = convert_exp_str_to_latex(exp_str)
        elif superscript_exp:
            exp_str = convert_exp_str_to_superscript(exp_str)
    return exp_str


def latex_translate(input_str: str) -> str:
    result_str = input_str
    result_str = result_str.replace('(', r'\left(')
    result_str = result_str.replace(')', r'\right)')
    result_str = result_str.replace('%', r'\%')
    result_str = result_str.replace('_', r'\_')
    return result_str
