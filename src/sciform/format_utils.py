from typing import Union
from math import floor, log10, log2
from warnings import warn
import re
from copy import copy
from decimal import Decimal

from sciform.modes import ExpMode, RoundMode, SignMode, AutoExpVal, AutoRound
from sciform.prefix import (si_val_to_prefix_dict, iec_val_to_prefix_dict,
                            pp_val_to_prefix_dict)


Number = Union[Decimal, float, int, str]


def get_top_digit(num: Decimal, binary=False) -> int:
    if not num.is_finite():
        return 0
    if num == 0:
        return 0
    if not binary:
        return floor(log10(abs(num)))
    else:
        return floor(log2(abs(num)))


def get_bottom_digit(num: Decimal) -> int:
    if not num.is_finite():
        return 0
    else:
        _, _, exp = num.as_tuple()
        return exp


def get_top_and_bottom_digit(num: Decimal) -> tuple[int, int]:
    return get_top_digit(num), get_bottom_digit(num)


def get_mantissa_exp_base(
        num: Decimal,
        exp_mode: ExpMode,
        exp_val: Union[int, type(AutoExpVal)] = None
) -> (Decimal, int, int):
    if (exp_mode is ExpMode.BINARY
            or exp_mode is ExpMode.BINARY_IEC):
        base = 2
    else:
        base = 10

    if not num.is_finite():
        mantissa = num
        if exp_val is AutoExpVal:
            exp_val = 0
    elif num == 0:
        mantissa = Decimal(0)
        if exp_val is AutoExpVal:
            exp_val = 0
    else:
        if exp_mode is ExpMode.FIXEDPOINT or exp_mode is ExpMode.PERCENT:
            if exp_val is not AutoExpVal:
                if exp_val != 0:
                    warn('Attempt to set non-zero exponent explicity in fixed '
                         'point or percent exponent mode. Coercing exponent '
                         'to 0.')
            exp_val = 0
        elif exp_mode is ExpMode.SCIENTIFIC:
            if exp_val is AutoExpVal:
                exp_val = get_top_digit(num)
        elif (exp_mode is ExpMode.ENGINEERING
              or exp_mode is ExpMode.ENGINEERING_SHIFTED):
            if exp_val is AutoExpVal:
                exp_val = get_top_digit(num)
                if exp_mode is ExpMode.ENGINEERING:
                    exp_val = (exp_val // 3) * 3
                else:
                    exp_val = ((exp_val + 1) // 3) * 3
            else:
                if exp_val % 3 != 0:
                    warn('Attempt to set exponent explicity to a non-integer '
                         'multiple of 3 in engineering mode. Coercing to the '
                         'next lower multiple of 3.')
                    exp_val = (exp_val // 3) * 3
        elif (exp_mode is ExpMode.BINARY
              or exp_mode is ExpMode.BINARY_IEC):
            if exp_val is AutoExpVal:
                exp_val = get_top_digit(num, binary=True)
                if exp_mode is ExpMode.BINARY_IEC:
                    exp_val = (exp_val // 10) * 10
            else:
                if exp_mode is ExpMode.BINARY_IEC and exp_val % 10 != 0:
                    warn('Attempt to set exponent explicity to a non-integer '
                         'multiple of 10 in binary IEC mode. Coercing to the '
                         'next lower multiple of 10.')
                    exp_val = (exp_val // 10) * 10
        mantissa = num * Decimal(base)**Decimal(-exp_val)
        mantissa = mantissa.normalize()
    return mantissa, exp_val, base


def get_exp_str(exp: int, exp_mode: ExpMode,
                capitalize: bool) -> str:
    if exp_mode is exp_mode.FIXEDPOINT or exp_mode is ExpMode.PERCENT:
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


def get_sign_str(num: Decimal, sign_mode: SignMode) -> str:
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


def get_pdg_round_digit(num: Decimal):
    """
    Determine what digit a number should be rounded to according to the
    particle data group 3-5-4 rounding rules.

    See
    https://pdg.lbl.gov/2010/reviews/rpp2010-rev-rpp-intro.pdf
    Section 5.2
    """
    top_digit = get_top_digit(num)

    # Bring num to be between 100 and 1000.
    num_top_three_digs = num * 10 ** (2 - top_digit)
    num_top_three_digs = round(num_top_three_digs, 0)
    new_top_digit = get_top_digit(num_top_three_digs)
    num_top_three_digs = num_top_three_digs * 10 ** (2 - new_top_digit)
    if 100 <= num_top_three_digs <= 354:
        round_digit = top_digit - 1
    elif 355 <= num_top_three_digs <= 949:
        round_digit = top_digit
    elif 950 <= num_top_three_digs <= 999:
        '''
        Here we set the round digit equal to the top digit. But since 
        the top three digits are >= 950 this means they will be rounded
        up to 1000. So with round digit set to the top digit this will
        correspond to displaying two digits of uncertainty: "10".
        e.g. 123.45632 +/- 0.987 would be rounded as 123.5 +/- 1.0.
        '''
        round_digit = top_digit
    else:
        raise ValueError

    return round_digit


def get_round_digit(num: Decimal,
                    round_mode: RoundMode,
                    precision: Union[int, type(AutoRound)],
                    pdg_sig_figs: bool = False) -> int:
    if round_mode is RoundMode.SIG_FIG:
        if precision is AutoRound:
            if pdg_sig_figs:
                round_digit = get_pdg_round_digit(num)
            else:
                round_digit = get_bottom_digit(num)
        else:
            round_digit = get_top_digit(num) - (precision - 1)
    elif round_mode is RoundMode.DIG_PLACE:
        if precision is AutoRound:
            round_digit = get_bottom_digit(num)
        else:
            round_digit = -precision
    else:
        raise TypeError(f'Unhandled round mode: {round_mode}.')
    return round_digit


def get_fill_str(fill_char: str, top_digit: int, top_padded_digit: int) -> str:
    if top_padded_digit > top_digit:
        pad_len = top_padded_digit - max(top_digit, 0)
        pad_str = fill_char*pad_len
    else:
        pad_str = ''
    return pad_str


def format_num_by_top_bottom_dig(num: Decimal,
                                 target_top_digit: int,
                                 target_bottom_digit: int,
                                 sign_mode: SignMode,
                                 fill_char: str) -> str:
    print_prec = max(0, -target_bottom_digit)
    abs_mantissa_str = f'{abs(num):.{print_prec}f}'

    sign_str = get_sign_str(num, sign_mode)

    num_top_digit = get_top_digit(num)
    fill_str = get_fill_str(fill_char, num_top_digit, target_top_digit)
    num_str = f'{sign_str}{fill_str}{abs_mantissa_str}'

    return num_str


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

    if exp_val in val_to_prefix_dict:
        prefix = val_to_prefix_dict[exp_val]
        if prefix is not None:
            exp_str = f' {prefix}'

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
        if latex:
            exp_str = rf'\text{{{exp_str.lstrip(" ")}}}'
        return exp_str
    else:
        if latex:
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
