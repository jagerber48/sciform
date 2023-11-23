from dataclasses import replace
from warnings import warn
import re
from decimal import Decimal

from sciform.modes import ExpMode, SignMode, AutoExpVal, RoundMode, ExpFormat
from sciform.rendered_options import RenderedOptions
from sciform.format_utils import (
    get_mantissa_exp_base, get_exp_str, get_top_digit, get_round_digit,
    format_num_by_top_bottom_dig, latex_translate, parse_standard_exp_str
)
from sciform.grouping import add_separators


def format_non_finite(num: Decimal, options: RenderedOptions) -> str:
    if num.is_nan():
        num_str = 'nan'
    elif num == Decimal('inf'):
        num_str = 'inf'
    elif num == Decimal('-inf'):
        num_str = '-inf'
    else:
        raise ValueError(f'format_non_finite() cannot format {num}.')

    if options.nan_inf_exp:
        exp_mode = options.exp_mode

        exp_val = options.exp_val
        if options.exp_val is AutoExpVal:
            exp_val = 0

        exp_str = get_exp_str(
            exp_val=exp_val,
            exp_mode=exp_mode,
            exp_format=options.exp_format,
            capitalize=options.capitalize,
            latex=options.latex,
            latex_trim_whitespace=True,
            superscript=options.superscript_exp,
            extra_si_prefixes=options.extra_si_prefixes,
            extra_iec_prefixes=options.extra_iec_prefixes,
            extra_parts_per_forms=options.extra_parts_per_forms
        )
    else:
        exp_str = ''

    if exp_str != '':
        result = f'({num_str}){exp_str}'
    else:
        result = f'{num_str}'

    if options.capitalize:
        result = result.upper()
    else:
        result = result.lower()

    if options.latex:
        result = latex_translate(result)

    return result


def format_num(num: Decimal, options: RenderedOptions) -> str:
    if not num.is_finite():
        return format_non_finite(num, options)

    if options.exp_mode is ExpMode.PERCENT:
        num *= 100
        num = num.normalize()

    exp_val = options.exp_val
    round_mode = options.round_mode
    exp_mode = options.exp_mode
    ndigits = options.ndigits
    mantissa, temp_exp_val, base = get_mantissa_exp_base(num, exp_mode,
                                                         exp_val)
    round_digit = get_round_digit(mantissa, round_mode, ndigits)
    mantissa_rounded = round(mantissa, -round_digit)

    '''
    Repeat mantissa + exponent discovery after rounding in case rounding
    altered the required exponent.
    '''
    rounded_num = mantissa_rounded * Decimal(base)**Decimal(temp_exp_val)
    mantissa, exp_val, base = get_mantissa_exp_base(rounded_num, exp_mode,
                                                    exp_val)
    round_digit = get_round_digit(mantissa, round_mode, ndigits)
    mantissa_rounded = round(mantissa, -int(round_digit))

    if mantissa_rounded == 0:
        '''
        This catches an edge case involving negative ndigits when the
        resulting mantissa is zero after the second rounding. This
        result is technically correct (e.g. 0e+03 = 0e+00), but sciform
        always presents zero values with an exponent of zero.
        '''
        exp_val = 0

    fill_char = options.fill_mode.value
    mantissa_str = format_num_by_top_bottom_dig(mantissa_rounded.normalize(),
                                                options.top_dig_place,
                                                round_digit,
                                                options.sign_mode,
                                                fill_char)

    upper_separator = options.upper_separator.value
    decimal_separator = options.decimal_separator.value
    lower_separator = options.lower_separator.value
    mantissa_str = add_separators(mantissa_str,
                                  upper_separator,
                                  decimal_separator,
                                  lower_separator,
                                  group_size=3)

    exp_str = get_exp_str(
        exp_val=exp_val,
        exp_mode=exp_mode,
        exp_format=options.exp_format,
        capitalize=options.capitalize,
        latex=options.latex,
        latex_trim_whitespace=False,
        superscript=options.superscript_exp,
        extra_si_prefixes=options.extra_si_prefixes,
        extra_iec_prefixes=options.extra_iec_prefixes,
        extra_parts_per_forms=options.extra_parts_per_forms
    )

    result = f'{mantissa_str}{exp_str}'

    if options.latex:
        result = latex_translate(result)

    return result


def format_val_unc(val: Decimal, unc: Decimal, options: RenderedOptions):
    if (options.exp_mode is ExpMode.BINARY
            or options.exp_mode is ExpMode.BINARY_IEC):
        raise NotImplementedError('Binary exponent modes are not supported '
                                  'for value/uncertainty formatting.')

    if options.round_mode is RoundMode.DEC_PLACE:
        warn('Precision round mode not available for value/uncertainty '
             'formatting. Rounding is always applied as significant figures '
             'for the uncertainty.')

    unc = abs(unc)
    if options.exp_mode is ExpMode.PERCENT:
        val *= 100
        unc *= 100
        val = val.normalize()
        unc = unc.normalize()

    # Find the digit place to round to
    if unc.is_finite() and unc != 0:
        round_driver = unc
        use_pdg_sig_figs = options.pdg_sig_figs
    else:
        round_driver = val
        '''
        Don't use pdg sig figs if the uncertainty doesn't drive the number of
        sig figs.
        '''
        use_pdg_sig_figs = False

    round_digit = get_round_digit(round_driver, RoundMode.SIG_FIG,
                                  options.ndigits, use_pdg_sig_figs)
    if unc.is_finite():
        unc_rounded = round(unc, -round_digit)
    else:
        unc_rounded = unc
    if val.is_finite():
        val_rounded = round(val, -round_digit)
    else:
        val_rounded = val
    if round_driver.is_finite():
        round_driver = round(round_driver, -round_digit)

    if not use_pdg_sig_figs:
        '''
        Re-round the rounded values in case the first rounding changed the most
        significant digit place. When using pdg_sig_figs this case is handled
        directly in the first call to get_round_digit.
        '''
        round_digit = get_round_digit(round_driver, RoundMode.SIG_FIG,
                                      options.ndigits, use_pdg_sig_figs)
        if unc_rounded.is_finite():
            unc_rounded = round(unc_rounded, -round_digit)
        if val_rounded.is_finite():
            val_rounded = round(val_rounded, -round_digit)

    exp_mode = options.exp_mode

    if exp_mode is ExpMode.PERCENT:
        '''
        In percent mode, value and uncertainty, having been multiplied
        by 100 above, will be individually formatted in fixed point mode
        '''
        exp_mode = ExpMode.FIXEDPOINT

    if val.is_finite() and unc.is_finite():
        if abs(val) >= unc:
            exp_driver = val_rounded
            val_exp_driver = True
        else:
            exp_driver = unc_rounded
            val_exp_driver = False
    elif val.is_finite():
        exp_driver = val_rounded
        val_exp_driver = True
    else:
        exp_driver = unc_rounded
        val_exp_driver = False

    _, exp_val, _ = get_mantissa_exp_base(
        exp_driver,
        exp_mode=options.exp_mode,
        input_exp_val=options.exp_val)
    val_mantissa, _, _ = get_mantissa_exp_base(
        val_rounded,
        exp_mode=exp_mode,
        input_exp_val=exp_val)
    unc_mantissa, _, _ = get_mantissa_exp_base(
        unc_rounded,
        exp_mode=exp_mode,
        input_exp_val=exp_val)

    ndigits = -round_digit + exp_val

    user_top_digit = options.top_dig_place
    if options.val_unc_match_widths:
        val_top_digit = get_top_digit(val_mantissa)
        unc_top_digit = get_top_digit(unc_mantissa)
        new_top_digit = max(user_top_digit, val_top_digit, unc_top_digit)
    else:
        new_top_digit = user_top_digit

    '''
    We will format the val and unc mantissas
       * using ndigits rounding mode with the ndigits calculated
         above
       * With the optionally shared top digit calculated above
       * With the calculated shared exponent
       * Without percent mode (percent mode for val/unc pairs is
         handled independently in this function)
       * Without superscript, prefix, parts-per, or latex translations.
         The remaining steps rely on parsing an exponent string like
         'e+03' or similar. Such translations are handled within the
         scope of this function.
    '''
    val_format_options = replace(
        options,
        top_dig_place=new_top_digit,
        round_mode=RoundMode.DEC_PLACE,
        ndigits=ndigits,
        exp_mode=exp_mode,
        exp_val=exp_val,
        superscript_exp=False,
        latex=False,
        exp_format=ExpFormat.STANDARD,
        pdg_sig_figs=False
    )

    unc_format_options = replace(
        val_format_options,
        sign_mode=SignMode.NEGATIVE
    )

    # Optional parentheses needed to handle (nan)e+00 case
    mantissa_exp_pattern = re.compile(
        r'^\(?(?P<mantissa_str>.*?)\)?(?P<exp_str>[eEbB].*?)?$')

    val_str = format_num(val_rounded, val_format_options)
    val_match = mantissa_exp_pattern.match(val_str)
    val_str = val_match.group('mantissa_str')

    unc_str = format_num(unc_rounded, unc_format_options)
    unc_match = mantissa_exp_pattern.match(unc_str)
    unc_str = unc_match.group('mantissa_str')

    if val_exp_driver:
        exp_str = val_match.group('exp_str')
    else:
        exp_str = unc_match.group('exp_str')

    if not options.bracket_unc:
        if options.latex:
            pm_symb = r'\pm'
        else:
            pm_symb = '±'

        if options.unc_pm_whitespace:
            pm_symb = f' {pm_symb} '

        val_unc_str = f'{val_str}{pm_symb}{unc_str}'
    else:
        if unc.is_finite() and val.is_finite():
            if unc == 0:
                unc_str = '0'
            elif unc < abs(val):
                unc_str = unc_str.lstrip('0.,_ ')
        if options.bracket_unc_remove_seps:
            unc_str = unc_str.replace(
                options.upper_separator.value, '')
            unc_str = unc_str.replace(
                options.lower_separator.value, '')
            if unc < val:
                # Only removed "embedded" decimal symbol for unc < val
                unc_str = unc_str.replace(
                    options.decimal_separator.value, '')

        val_unc_str = f'{val_str}({unc_str})'

    if exp_str is not None:
        base, exp_val = parse_standard_exp_str(exp_str)
        exp_str = get_exp_str(
            exp_val=exp_val,
            exp_mode=exp_mode,
            exp_format=options.exp_format,
            capitalize=options.capitalize,
            latex=options.latex,
            latex_trim_whitespace=True,
            superscript=options.superscript_exp,
            extra_si_prefixes=options.extra_si_prefixes,
            extra_iec_prefixes=options.extra_iec_prefixes,
            extra_parts_per_forms=options.extra_parts_per_forms
        )
        if options.bracket_unc and not re.match(r'^[eEbB][+-]\d+$', exp_str):
            val_unc_exp_str = f'{val_unc_str}{exp_str}'
        else:
            val_unc_exp_str = f'({val_unc_str}){exp_str}'
    else:
        val_unc_exp_str = val_unc_str

    if options.exp_mode is ExpMode.PERCENT:
        val_unc_exp_str = f'({val_unc_exp_str})%'

    if options.latex:
        val_unc_exp_str = latex_translate(val_unc_exp_str)

    return val_unc_exp_str
