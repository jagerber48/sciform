from typing import Union
from math import floor, log10, log2
import re
from decimal import Decimal

from sciform.modes import (ExpMode, ExpFormat, RoundMode, SignMode, AutoExpVal,
                           AutoDigits)
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


def get_mantissa_exp_base(
        num: Decimal,
        exp_mode: ExpMode,
        input_exp_val: Union[int, type(AutoExpVal)] = None
) -> (Decimal, int, int):
    if (exp_mode is ExpMode.BINARY
            or exp_mode is ExpMode.BINARY_IEC):
        base = 2
    else:
        base = 10

    if not num.is_finite():
        mantissa = num
        if input_exp_val is AutoExpVal:
            exp_val = 0
        else:
            exp_val = input_exp_val
    elif num == 0:
        mantissa = Decimal(0)
        if input_exp_val is AutoExpVal:
            exp_val = 0
        else:
            exp_val = input_exp_val
    else:
        if exp_mode is ExpMode.FIXEDPOINT or exp_mode is ExpMode.PERCENT:
            if input_exp_val is not AutoExpVal and input_exp_val != 0:
                raise ValueError('Cannot set non-zero exponent in fixed point '
                                 'or percent exponent mode.')
            exp_val = 0
        elif exp_mode is ExpMode.SCIENTIFIC:
            if input_exp_val is AutoExpVal:
                exp_val = get_top_digit(num)
            else:
                exp_val = input_exp_val
        elif (exp_mode is ExpMode.ENGINEERING
              or exp_mode is ExpMode.ENGINEERING_SHIFTED):
            if input_exp_val is AutoExpVal:
                exp_val = get_top_digit(num)
                if exp_mode is ExpMode.ENGINEERING:
                    exp_val = (exp_val // 3) * 3
                else:
                    exp_val = ((exp_val + 1) // 3) * 3
            else:
                if input_exp_val % 3 != 0:
                    raise ValueError(f'Exponent must be an integer multiple '
                                     f'of 3 in engineering modes, not '
                                     f'{input_exp_val}.')
                exp_val = input_exp_val
        elif (exp_mode is ExpMode.BINARY
              or exp_mode is ExpMode.BINARY_IEC):
            if input_exp_val is AutoExpVal:
                exp_val = get_top_digit(num, binary=True)
                if exp_mode is ExpMode.BINARY_IEC:
                    exp_val = (exp_val // 10) * 10
            else:
                if exp_mode is ExpMode.BINARY_IEC and input_exp_val % 10 != 0:
                    raise ValueError(f'Exponent must be an integer multiple '
                                     f'of 10 in binary IEC mode, not '
                                     f'{input_exp_val}.')
                exp_val = input_exp_val
        else:
            raise ValueError(f'Unhandled exponent mode {exp_mode}.')

        mantissa = num * Decimal(base)**Decimal(-exp_val)
        mantissa = mantissa.normalize()
    return mantissa, exp_val, base


def get_standard_exp_str(base: int,
                         exp_val: int,
                         capitalize: bool) -> str:
    base_exp_symb_dict = {10: 'e', 2: 'b'}
    exp_symb = base_exp_symb_dict[base]
    if capitalize:
        exp_symb = exp_symb.capitalize()
    return f'{exp_symb}{exp_val:+03d}'


def get_superscript_exp_str(base: int,
                            exp_val: int) -> str:
    sup_trans = str.maketrans("+-0123456789", "⁺⁻⁰¹²³⁴⁵⁶⁷⁸⁹")
    exp_val_str = f'{exp_val}'.translate(sup_trans)
    return f'×{base}{exp_val_str}'


def get_prefix_dict(exp_format: ExpFormat,
                    base: int,
                    extra_si_prefixes: dict[int, str] = None,
                    extra_iec_prefixes: dict[int, str] = None,
                    extra_parts_per_forms: dict[int, str] = None
                    ) -> dict[int, str]:
    if exp_format is ExpFormat.PREFIX:
        if base == 10:
            prefix_dict = si_val_to_prefix_dict.copy()
            prefix_dict.update(extra_si_prefixes)
        elif base == 2:
            prefix_dict = iec_val_to_prefix_dict.copy()
            prefix_dict.update(extra_iec_prefixes)
        else:
            raise ValueError(f'Unhandled base {base}')
    elif exp_format is ExpFormat.PARTS_PER:
        prefix_dict = pp_val_to_prefix_dict.copy()
        prefix_dict.update(extra_parts_per_forms)
    else:
        raise ValueError(f'Unhandled ExpFormat, {exp_format}.')

    return prefix_dict


def get_exp_str(exp_val: int,
                exp_mode: ExpMode,
                exp_format: ExpFormat,
                capitalize: bool,
                latex: bool,
                latex_trim_whitespace: bool,
                superscript: bool,
                extra_si_prefixes: dict[int, str] = None,
                extra_iec_prefixes: dict[int, str] = None,
                extra_parts_per_forms: dict[int, str] = None) -> str:
    if exp_mode is ExpMode.FIXEDPOINT:
        return ''
    elif exp_mode is ExpMode.PERCENT:
        return '%'

    if (exp_mode is ExpMode.SCIENTIFIC
            or exp_mode is ExpMode.ENGINEERING
            or exp_mode is ExpMode.ENGINEERING_SHIFTED):
        base = 10
    elif (exp_mode is ExpMode.BINARY
          or exp_mode is ExpMode.BINARY_IEC):
        base = 2
    else:
        raise ValueError(f'Unhandled exp_mode: {exp_mode}')

    if exp_format is ExpFormat.STANDARD:
        if latex:
            return rf'\times {base}^{{{exp_val:+}}}'
        elif superscript:
            return get_superscript_exp_str(base, exp_val)
        else:
            return get_standard_exp_str(base, exp_val, capitalize)
    elif (exp_format is ExpFormat.PREFIX
            or exp_format is ExpFormat.PARTS_PER):
        prefix_dict = get_prefix_dict(exp_format,
                                      base,
                                      extra_si_prefixes,
                                      extra_iec_prefixes,
                                      extra_parts_per_forms)

        use_prefix = False
        if exp_val in prefix_dict:
            if prefix_dict[exp_val] is not None:
                use_prefix = True

        if not use_prefix:
            if superscript:
                return get_superscript_exp_str(base, exp_val)
            else:
                return get_standard_exp_str(base, exp_val, capitalize)
        else:
            exp_str = f' {prefix_dict[exp_val]}'
            exp_str = exp_str.rstrip(' ')
            if latex:
                if latex_trim_whitespace:
                    exp_str = exp_str.lstrip(' ')
                exp_str = rf'\text{{{exp_str}}}'
            return exp_str


def parse_standard_exp_str(exp_str: str) -> tuple[int, int]:
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
    if exp_symb.lower() == 'e':
        base = 10
    elif exp_symb.lower() == 'b':
        base = 2
    else:  # pragma: no cover
        assert False, 'unreachable'

    exp_val = int(f'{exp_sign}{exp_digits}')

    return base, exp_val


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


def get_pdg_round_digit(num: Decimal) -> int:
    """
    Determine what digit a number should be rounded to according to the
    particle data group 3-5-4 rounding rules.

    See
    https://pdg.lbl.gov/2010/reviews/rpp2010-rev-rpp-intro.pdf
    Section 5.2
    """
    top_digit = get_top_digit(num)

    # Bring num to be between 100 and 1000.
    num_top_three_digs = num * Decimal(10) ** (Decimal(2) - Decimal(top_digit))
    num_top_three_digs.quantize(1)
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
    else:  # pragma: no cover
        assert False, "unreachable"

    return round_digit


def get_round_digit(num: Decimal,
                    round_mode: RoundMode,
                    ndigits: Union[int, type(AutoDigits)],
                    pdg_sig_figs: bool = False) -> int:
    if round_mode is RoundMode.SIG_FIG:
        if ndigits is AutoDigits:
            if pdg_sig_figs:
                round_digit = get_pdg_round_digit(num)
            else:
                round_digit = get_bottom_digit(num)
        else:
            round_digit = get_top_digit(num) - (ndigits - 1)
    elif round_mode is RoundMode.DEC_PLACE:
        if ndigits is AutoDigits:
            round_digit = get_bottom_digit(num)
        else:
            round_digit = -ndigits
    else:
        raise ValueError(f'Unhandled round mode: {round_mode}.')
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


def latex_translate(input_str: str) -> str:
    result_str = input_str
    result_str = result_str.replace('(', r'\left(')
    result_str = result_str.replace(')', r'\right)')
    result_str = result_str.replace('%', r'\%')
    result_str = result_str.replace('_', r'\_')
    result_str = result_str.replace('nan', r'\text{nan}')
    result_str = result_str.replace('NAN', r'\text{NAN}')
    result_str = result_str.replace('inf', r'\text{inf}')
    result_str = result_str.replace('INF', r'\text{INF}')
    return result_str
