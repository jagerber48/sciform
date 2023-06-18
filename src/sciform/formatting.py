from math import isfinite
from warnings import warn
import re

from sciform.modes import FillMode, ExpMode, SignMode, AutoExp
from sciform.format_options import FormatOptions, RoundMode
from sciform.format_utils import (get_mantissa_exp_base, get_exp_str,
                                  get_top_digit,
                                  get_top_and_bottom_digit,
                                  get_round_digit,
                                  format_float_by_top_bottom_dig,
                                  convert_exp_str_to_superscript,
                                  convert_exp_str_to_latex)
from sciform.grouping import add_separators
from sciform.prefix import replace_prefix


# TODO: Latex Printing
# TODO: ppm format


def format_float(num: float, options: FormatOptions) -> str:
    exp_mode = options.exp_mode
    round_mode = options.round_mode
    precision = options.precision
    top_padded_digit = options.top_dig_place
    sign_mode = options.sign_mode
    capitalize = options.capitalize
    fill_char = FillMode.to_char(options.fill_mode)
    if not isfinite(num):
        if options.nan_inf_exp:
            if options.exp is AutoExp:
                exp = 0
            else:
                exp = options.exp
            if exp_mode is ExpMode.FIXEDPOINT:
                exp_str = ''
            elif (exp_mode is ExpMode.SCIENTIFIC
                  or exp_mode is ExpMode.ENGINEERING
                  or exp_mode is ExpMode.ENGINEERING_SHIFTED):
                exp_str = f'e+{exp:02d}'
            else:
                exp_str = f'b+{exp:02d}'
        else:
            exp_str = ''
        if options.latex:
            exp_str = convert_exp_str_to_latex(exp_str)
        elif options.superscript_exp:
            exp_str = convert_exp_str_to_superscript(exp_str)

        if exp_str != '':
            full_str = f'({num}){exp_str}'
        else:
            full_str = f'{num}'
            if options.percent:
                full_str = f'{full_str}%'

        if capitalize:
            full_str = full_str.upper()
        else:
            full_str = full_str.lower()

        if options.latex:
            full_str = full_str.replace('(', r'\left(')
            full_str = full_str.replace(')', r'\right)')
            full_str = full_str.replace('%', r'\%)')

        return full_str

    if options.percent:
        num *= 100

    exp = options.exp
    mantissa, temp_exp, base = get_mantissa_exp_base(num, exp_mode, exp)

    top_digit, bottom_digit = get_top_and_bottom_digit(mantissa)
    round_digit = get_round_digit(top_digit, bottom_digit,
                                  precision, round_mode)

    mantissa_rounded = round(mantissa, -round_digit)

    '''
    Repeat mantissa + exponent discovery after rounding in case rounding
    altered the required exponent.
    '''
    rounded_num = mantissa_rounded * base**temp_exp
    mantissa, exp, base = get_mantissa_exp_base(rounded_num, exp_mode, exp)

    top_digit, bottom_digit = get_top_and_bottom_digit(mantissa)
    round_digit = get_round_digit(top_digit, bottom_digit,
                                  precision, round_mode)

    mantissa_rounded = round(mantissa, -round_digit)
    if mantissa_rounded == 0:
        exp = 0

    exp_str = get_exp_str(exp, exp_mode, capitalize)
    if options.latex:
        exp_str = convert_exp_str_to_latex(exp_str)
    elif options.superscript_exp:
        exp_str = convert_exp_str_to_superscript(exp_str)

    if mantissa_rounded == -0.0:
        mantissa_rounded = abs(mantissa_rounded)
    mantissa_str = format_float_by_top_bottom_dig(mantissa_rounded,
                                                  top_padded_digit,
                                                  round_digit, sign_mode,
                                                  fill_char)

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

    if options.percent:
        full_str = full_str + '%'

    if options.latex:
        full_str = full_str.replace('%', r'\%')
        full_str = full_str.replace('_', r'\_')

    return full_str


def format_val_unc(val: float, unc: float, options: FormatOptions):
    """
    Convert two floats, the value and the uncertainty into a

    :param val:
    :param unc:
    :param options:
    :return:
    """
    if options.round_mode is RoundMode.PREC:
        warn('Precision round mode not available for value/uncertainty '
             'formatting. Rounding is always applied as significant figures'
             'for the uncertainty.')

    unc = abs(unc)

    if options.percent:
        val *= 100
        unc *= 100

    # Find the digit place to round to
    if isfinite(unc) and unc != 0:
        round_driver = unc
    else:
        round_driver = val

    top_digit_1, bottom_digit_1 = get_top_and_bottom_digit(round_driver)
    round_digit = get_round_digit(top_digit_1, bottom_digit_1,
                                  options.precision, RoundMode.SIG_FIG)

    # Perform rounding
    unc_rounded = round(unc, -round_digit)
    val_rounded = round(val, -round_digit)
    round_driver = round(round_driver, -round_digit)

    '''
    Re-round the rounded values in case the first rounding changed the most
    significant digit place.
    '''
    top_digit_2, bottom_digit_2 = get_top_and_bottom_digit(round_driver)
    round_digit = get_round_digit(top_digit_2, bottom_digit_2,
                                  options.precision, RoundMode.SIG_FIG)

    unc_rounded = round(unc_rounded, -round_digit)
    val_rounded = round(val_rounded, -round_digit)

    exp_mode = options.exp_mode

    '''
    Get a corresponding exponent mode which can have the exponent set
    explicitly.
    '''
    if (exp_mode is ExpMode.ENGINEERING
            or exp_mode is ExpMode.ENGINEERING_SHIFTED):
        free_exp_mode = ExpMode.SCIENTIFIC
    elif exp_mode is ExpMode.BINARY_IEC:
        free_exp_mode = ExpMode.BINARY
    else:
        free_exp_mode = exp_mode

    if isfinite(val) or isfinite(unc):
        if isfinite(val):
            exp_driver = val_rounded
        else:
            exp_driver = unc_rounded

        _, exp, _ = get_mantissa_exp_base(
            exp_driver,
            exp_mode=options.exp_mode,
            exp=options.exp)

        val_mantissa, _, _ = get_mantissa_exp_base(
            val_rounded,
            exp_mode=free_exp_mode,
            exp=exp)

        unc_mantissa, _, _ = get_mantissa_exp_base(
            unc_rounded,
            exp_mode=free_exp_mode,
            exp=exp)

        prec = -round_digit + exp
    else:
        exp = 0
        prec = 0
        val_mantissa = val_rounded
        unc_mantissa = unc_rounded

    user_top_digit = options.top_dig_place

    if options.val_unc_match_widths:
        val_top_digit = get_top_digit(val_mantissa)
        unc_top_digit = get_top_digit(unc_mantissa)
        new_top_digit = max(user_top_digit, val_top_digit, unc_top_digit)
    else:
        new_top_digit = user_top_digit

    val_format_options = FormatOptions.make(
        defaults=options,
        top_dig_place=new_top_digit,
        round_mode=RoundMode.PREC,
        precision=prec,
        exp_mode=free_exp_mode,
        exp=exp,
        percent=False,
        superscript_exp=False,
        latex=False,
        use_prefix=False,
    )

    unc_format_options = FormatOptions.make(
        defaults=val_format_options,
        sign_mode=SignMode.NEGATIVE,
    )

    # Optional parentheses needed to handle (nan)e+00 case
    mantissa_exp_pattern = re.compile(
        r'^\(?(?P<mantissa_str>.*?)\)?(?P<exp_str>[eEbB].*?)?$')

    val_str = format_float(val_rounded, val_format_options)
    val_match = mantissa_exp_pattern.match(val_str)
    val_str = val_match.group('mantissa_str')

    unc_str = format_float(unc_rounded, unc_format_options)
    unc_match = mantissa_exp_pattern.match(unc_str)
    unc_str = unc_match.group('mantissa_str')

    if isfinite(val):
        exp_str = val_match.group('exp_str')
    else:
        exp_str = unc_match.group('exp_str')

    if not options.bracket_unc:
        if options.latex:
            pm_symb = r'\pm'
        elif options.unicode_pm:
            pm_symb = '±'
        else:
            pm_symb = '+/-'

        if options.unc_pm_whitespace:
            val_unc_str = f'{val_str} {pm_symb} {unc_str}'
        else:
            val_unc_str = f'{val_str}{pm_symb}{unc_str}'
    else:
        unc_str = unc_str.lstrip('0.,_ ')
        if options.bracket_unc_remove_seps:
            unc_str = unc_str.replace('.', '')
            unc_str = unc_str.replace(',', '')
            unc_str = unc_str.replace(' ', '')
            unc_str = unc_str.replace('_', '')
        val_unc_str = f'{val_str}({unc_str})'

    if exp_str is not None:
        if options.latex:
            exp_str = convert_exp_str_to_latex(exp_str)
        elif options.superscript_exp:
            exp_str = convert_exp_str_to_superscript(exp_str)
        val_unc_exp_str = f'({val_unc_str}){exp_str}'
    else:
        val_unc_exp_str = val_unc_str

    if options.use_prefix:
        val_unc_exp_str = replace_prefix(val_unc_exp_str)

    if options.percent:
        result_str = f'({val_unc_exp_str})%'
    else:
        result_str = val_unc_exp_str

    if options.latex:
        result_str = result_str.replace('(', r'\left(')
        result_str = result_str.replace(')', r'\right)')
        result_str = result_str.replace('%', r'\%')
        result_str = result_str.replace('_', r'\_')

    return result_str
