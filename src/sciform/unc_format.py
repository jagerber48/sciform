import re

from sciform.modes import RoundMode, SignMode, FormatMode
from sciform.format_utils import (get_round_digit, get_top_and_bottom_digit,
                                  get_top_digit, get_mantissa_exp_base)
from sciform.formatter import format_float
from sciform.format_options import FormatOptions
from sciform.prefix import replace_prefix


def format_val_unc(val: float, unc: float, fmt: str):
    # TODO: Handle non-finite floats
    options = FormatOptions.from_format_spec_str(fmt)
    pattern = FormatOptions.pattern
    match = re.match(pattern, fmt)
    if match.group('top_dig_place'):
        match_widths = True
    else:
        match_widths = False

    unc = abs(unc)

    if options.format_mode is FormatMode.PERCENT:
        val *= 100
        unc *= 100

    unc_top_digit, unc_bottom_digit = get_top_and_bottom_digit(unc)
    round_digit = get_round_digit(unc_top_digit, unc_bottom_digit,
                                  options.precision, RoundMode.SIG_FIG)

    unc_rounded = round(unc, -round_digit)
    val_rounded = round(val, -round_digit)

    '''
    Re-round the rounded values in case the first rounding changed the most
    significant digit place.
    '''
    unc_top_digit, unc_bottom_digit = get_top_and_bottom_digit(unc_rounded)
    round_digit = get_round_digit(unc_top_digit, unc_bottom_digit,
                                  options.precision, RoundMode.SIG_FIG)

    unc_rounded = round(unc_rounded, -round_digit)
    val_rounded = round(val_rounded, -round_digit)

    val_mantissa, exp, base = get_mantissa_exp_base(
        val_rounded,
        format_mode=options.format_mode,
        exp=options.exp)

    unc_mantissa, _, _ = get_mantissa_exp_base(
        unc_rounded,
        format_mode=options.format_mode,
        exp=exp)
    unc_top_digit, unc_bottom_digit = get_top_and_bottom_digit(unc_mantissa)
    round_digit = get_round_digit(unc_top_digit, unc_bottom_digit,
                                  options.precision, options.round_mode)

    prec = -round_digit

    user_top_digit = options.top_dig_place

    if match_widths:
        val_top_digit = get_top_digit(val_mantissa)
        new_top_digit = max(user_top_digit, val_top_digit, unc_top_digit)
    else:
        new_top_digit = user_top_digit

    format_mode = options.format_mode
    if format_mode is FormatMode.PERCENT:
        format_mode = FormatMode.FIXEDPOINT

    val_format_options = FormatOptions.from_template(
        template=options,
        top_dig_place=new_top_digit,
        round_mode=RoundMode.PREC,
        precision=prec,
        format_mode=format_mode,
        exp=exp,
        use_prefix=False)

    unc_format_options = FormatOptions.from_template(
        template=val_format_options,
        sign_mode=SignMode.NEGATIVE
    )

    mantissa_exp_pattern = re.compile(
        r'^(?P<mantissa_str>.*?)(?P<exp_str>[eEbB].*?)?$')

    val_str = format_float(val_rounded, val_format_options)
    val_match = mantissa_exp_pattern.match(val_str)
    val_str = val_match.group('mantissa_str')
    exp_str = val_match.group('exp_str')

    unc_str = format_float(unc_rounded, unc_format_options)
    unc_match = mantissa_exp_pattern.match(unc_str)
    unc_str = unc_match.group('mantissa_str')
    val_unc_str = f'{val_str} +/- {unc_str}'

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

    def __format__(self, format_spec):
        return format_val_unc(self.value,
                              self.uncertainty,
                              format_spec)
