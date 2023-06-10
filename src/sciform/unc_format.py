import re
from math import isfinite
from warnings import warn

from sciform.modes import RoundMode, SignMode, FormatMode
from sciform.format_utils import (get_round_digit, get_top_and_bottom_digit,
                                  get_top_digit, get_mantissa_exp_base)
from sciform.formatter import format_float
from sciform.format_options import FormatOptions
from sciform.prefix import replace_prefix


def format_val_unc(val: float, unc: float, options: FormatOptions):
    """
    Convert two floats, the value and the uncertainty into a

    :param val:
    :param unc:
    :param options:
    :param match_widths:
    :return:
    """
    # TODO: Handle non-finite floats
    if options.round_mode is RoundMode.PREC:
        warn('Precision round mode not available for value/uncertainty '
             'formatting. Rounding is always applied as significant figures'
             'for the uncertainty.')

    unc = abs(unc)

    if options.format_mode is FormatMode.PERCENT:
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


    format_mode = options.format_mode

    '''
    Get a corresponding format mode which can have the exponent set
    explicitly.
    '''
    if format_mode is FormatMode.PERCENT:
        free_exp_format_mode = FormatMode.FIXEDPOINT
    elif (format_mode is FormatMode.ENGINEERING
          or format_mode is FormatMode.ENGINEERING_SHIFTED):
        free_exp_format_mode = FormatMode.SCIENTIFIC
    elif format_mode is FormatMode.BINARY_IEC:
        free_exp_format_mode = FormatMode.BINARY
    else:
        free_exp_format_mode = format_mode

    if isfinite(val) or isfinite(unc):
        if isfinite(val):
            exp_driver = val_rounded
        else:
            exp_driver = unc_rounded

        _, exp, _ = get_mantissa_exp_base(
            exp_driver,
            format_mode=options.format_mode,
            exp=options.exp)

        val_mantissa, _, _ = get_mantissa_exp_base(
            val_rounded,
            format_mode=free_exp_format_mode,
            exp=exp)

        unc_mantissa, _, _ = get_mantissa_exp_base(
            unc_rounded,
            format_mode=free_exp_format_mode,
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
        format_mode=free_exp_format_mode,
        exp=exp,
        use_prefix=False)

    unc_format_options = FormatOptions.make(
        defaults=val_format_options,
        format_mode=free_exp_format_mode,
        sign_mode=SignMode.NEGATIVE
    )

    mantissa_exp_pattern = re.compile(
        r'^(?P<mantissa_str>.*?)(?P<exp_str>[eEbB].*?)?$')

    val_str = format_float(val_rounded, val_format_options, non_inf_exp=True)
    val_match = mantissa_exp_pattern.match(val_str)
    val_str = val_match.group('mantissa_str')
    exp_str = val_match.group('exp_str')

    unc_str = format_float(unc_rounded, unc_format_options, non_inf_exp=True)
    unc_match = mantissa_exp_pattern.match(unc_str)
    unc_str = unc_match.group('mantissa_str')

    if not options.bracket_unc:
        val_unc_str = f'{val_str} +/- {unc_str}'
    else:
        unc_str = unc_str.lstrip('0.')
        val_unc_str = f'{val_str}({unc_str})'

    if exp_str is not None:
        val_unc_exp_str = f'({val_unc_str}){exp_str}'
    else:
        val_unc_exp_str = val_unc_str

    if options.use_prefix:
        val_unc_exp_str = replace_prefix(val_unc_exp_str)

    if options.format_mode is FormatMode.PERCENT:
        result_str = f'({val_unc_exp_str})%'
    else:
        result_str = val_unc_exp_str

    return result_str


class vufloat:
    """
    Here we do not inherit from float, and we do not support float operations.
    This class is purely for the convenience of formatting value/uncertainty
    pairs. Mathematical operations are not supported on vufloat objects because
    the effect of such operations on the uncertainties is non-trivial. For the
    accurate propagation of error using value/uncertainty pairs, users are
    recommended to the uncertainties package:
    https://pypi.org/project/uncertainties/
    """
    def __init__(self, val, unc, /):
        self.value = val
        self.uncertainty = unc

    def __format__(self, format_spec: str):
        options = FormatOptions.from_format_spec_str(format_spec)
        return format_val_unc(self.value,
                              self.uncertainty,
                              options)
