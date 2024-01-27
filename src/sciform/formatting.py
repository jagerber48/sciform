"""Main formatting functions."""

from dataclasses import replace
from decimal import Decimal
from typing import cast
from warnings import warn

from sciform.format_utils import (
    construct_val_unc_exp_str,
    construct_val_unc_str,
    format_num_by_top_bottom_dig,
    get_exp_str,
    get_mantissa_exp_base,
    get_round_digit,
    get_val_unc_exp,
    get_val_unc_mantissa_strs,
    get_val_unc_top_digit,
    round_val_unc,
)
from sciform.grouping import add_separators
from sciform.modes import (
    AutoExpVal,
    ExpFormatEnum,
    ExpModeEnum,
    RoundModeEnum,
    SignModeEnum,
)
from sciform.rendered_options import RenderedOptions


def format_non_finite(num: Decimal, options: RenderedOptions) -> str:
    """Format non-finite numbers."""
    if num.is_nan():
        num_str = "nan"
    elif num == Decimal("inf"):
        num_str = "inf"
    elif num == Decimal("-inf"):
        num_str = "-inf"
    else:
        msg = f"format_non_finite() cannot format {num}."
        raise ValueError(msg)

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
            superscript=options.superscript,
            extra_si_prefixes=options.extra_si_prefixes,
            extra_iec_prefixes=options.extra_iec_prefixes,
            extra_parts_per_forms=options.extra_parts_per_forms,
        )
    else:
        exp_str = ""

    if exp_str != "":
        result = f"({num_str}){exp_str}"
    else:
        result = f"{num_str}"

    if options.capitalize:
        result = result.upper()
    else:
        result = result.lower()

    return result


def format_num(num: Decimal, options: RenderedOptions) -> str:
    """Format a single number according to input options."""
    if not num.is_finite():
        return format_non_finite(num, options)

    if options.exp_mode is ExpModeEnum.PERCENT:
        num *= 100
        num = num.normalize()

    exp_val = options.exp_val
    round_mode = options.round_mode
    exp_mode = options.exp_mode
    ndigits = options.ndigits
    mantissa, temp_exp_val, base = get_mantissa_exp_base(num, exp_mode, exp_val)
    round_digit = get_round_digit(mantissa, round_mode, ndigits)
    mantissa_rounded = round(mantissa, -round_digit)

    """
    Repeat mantissa + exponent discovery after rounding in case rounding
    altered the required exponent.
    """
    rounded_num = mantissa_rounded * Decimal(base) ** Decimal(temp_exp_val)
    mantissa, exp_val, base = get_mantissa_exp_base(rounded_num, exp_mode, exp_val)
    round_digit = get_round_digit(mantissa, round_mode, ndigits)
    mantissa_rounded = round(mantissa, -int(round_digit))
    mantissa_rounded = cast(Decimal, mantissa_rounded)

    if mantissa_rounded == 0:
        """
        This catches an edge case involving negative ndigits when the
        resulting mantissa is zero after the second rounding. This
        result is technically correct (e.g. 0e+03 = 0e+00), but sciform
        always presents zero values with an exponent of zero.
        """
        exp_val = 0

    left_pad_char = options.left_pad_char.value
    mantissa_str = format_num_by_top_bottom_dig(
        mantissa_rounded.normalize(),
        options.left_pad_dec_place,
        round_digit,
        options.sign_mode,
        left_pad_char,
    )

    upper_separator = options.upper_separator.value
    decimal_separator = options.decimal_separator.value
    lower_separator = options.lower_separator.value
    mantissa_str = add_separators(
        mantissa_str,
        upper_separator,
        decimal_separator,
        lower_separator,
        group_size=3,
    )

    exp_str = get_exp_str(
        exp_val=exp_val,
        exp_mode=exp_mode,
        exp_format=options.exp_format,
        capitalize=options.capitalize,
        superscript=options.superscript,
        extra_si_prefixes=options.extra_si_prefixes,
        extra_iec_prefixes=options.extra_iec_prefixes,
        extra_parts_per_forms=options.extra_parts_per_forms,
    )

    result = f"{mantissa_str}{exp_str}"

    return result


def format_val_unc(val: Decimal, unc: Decimal, options: RenderedOptions) -> str:
    """Format value/uncertainty pair according to input options."""
    exp_mode = options.exp_mode

    if exp_mode is ExpModeEnum.BINARY or exp_mode is ExpModeEnum.BINARY_IEC:
        msg = (
            "Binary exponent modes are not supported for value/uncertainty formatting."
        )
        raise NotImplementedError(msg)

    if options.round_mode is RoundModeEnum.DEC_PLACE:
        msg = (
            "Precision round mode not available for value/uncertainty formatting. "
            "Rounding is always applied as significant figures for the uncertainty."
        )
        warn(msg, stacklevel=2)

    unc = abs(unc)
    if exp_mode is ExpModeEnum.PERCENT:
        val *= 100
        unc *= 100
        val = val.normalize()
        unc = unc.normalize()

        """
        In percent mode, value and uncertainty, having been multiplied
        by 100 above, will be individually formatted in fixed point mode
        """
        exp_mode = ExpModeEnum.FIXEDPOINT

    """
    We round twice in case the first rounding changes the digits place
    to which we need to round. E.g. rounding 999.999 ± 123.456 to two
    significant figures will lead to 1000.000 ± 0120.000 on the first
    pass, but we must re-round to get 1000.000 ± 0100.000.
    """
    val_rounded, unc_rounded, _ = round_val_unc(
        val,
        unc,
        options.ndigits,
        use_pdg_sig_figs=options.pdg_sig_figs,
    )
    val_rounded, unc_rounded, round_digit = round_val_unc(
        val_rounded,
        unc_rounded,
        options.ndigits,
        use_pdg_sig_figs=options.pdg_sig_figs,
    )

    exp_val = get_val_unc_exp(
        val_rounded,
        unc_rounded,
        options.exp_mode,
        options.exp_val,
    )

    val_mantissa, _, _ = get_mantissa_exp_base(
        val_rounded,
        exp_mode=exp_mode,
        input_exp=exp_val,
    )
    unc_mantissa, _, _ = get_mantissa_exp_base(
        unc_rounded,
        exp_mode=exp_mode,
        input_exp=exp_val,
    )

    new_top_digit = get_val_unc_top_digit(
        val_mantissa,
        unc_mantissa,
        options.left_pad_dec_place,
        left_pad_matching=options.left_pad_matching,
    )

    ndigits = -round_digit + exp_val

    """
    We will format the val and unc mantissas
       * using decimal place rounding mode with the ndigits calculated
         above
       * With the optionally shared left_pad_dec_place calculated above
       * With the calculated shared exponent
       * Without percent mode (percent mode for val/unc pairs is
         handled below in the scope of this function)
       * Without superscript, prefix, or parts-per translations.
         The remaining steps rely on parsing an exponent string like
         'e+03' or similar. Such translations are handled within the
         scope of this function.
    """
    val_format_options = replace(
        options,
        left_pad_dec_place=new_top_digit,
        round_mode=RoundModeEnum.DEC_PLACE,
        ndigits=ndigits,
        exp_mode=exp_mode,
        exp_val=exp_val,
        superscript=False,
        exp_format=ExpFormatEnum.STANDARD,
    )

    unc_format_options = replace(
        val_format_options,
        sign_mode=SignModeEnum.NEGATIVE,
    )

    val_mantissa_exp_str = format_num(val_rounded, val_format_options)
    unc_mantissa_exp_str = format_num(unc_rounded, unc_format_options)

    val_mantissa_str, unc_mantissa_str = get_val_unc_mantissa_strs(
        val_mantissa_exp_str,
        unc_mantissa_exp_str,
    )

    val_unc_str = construct_val_unc_str(
        val_mantissa_str,
        unc_mantissa_str,
        val_mantissa,
        unc_mantissa,
        decimal_separator=options.decimal_separator,
        paren_uncertainty=options.paren_uncertainty,
        pm_whitespace=options.pm_whitespace,
        paren_uncertainty_separators=options.paren_uncertainty_separators,
    )

    if val.is_finite() or unc.is_finite() or options.nan_inf_exp:
        val_unc_exp_str = construct_val_unc_exp_str(
            val_unc_str=val_unc_str,
            exp_val=exp_val,
            exp_mode=exp_mode,
            exp_format=options.exp_format,
            extra_si_prefixes=options.extra_si_prefixes,
            extra_iec_prefixes=options.extra_iec_prefixes,
            extra_parts_per_forms=options.extra_parts_per_forms,
            capitalize=options.capitalize,
            superscript=options.superscript,
            paren_uncertainty=options.paren_uncertainty,
        )
    else:
        val_unc_exp_str = val_unc_str

    if options.exp_mode is ExpModeEnum.PERCENT:
        val_unc_exp_str = f"({val_unc_exp_str})%"

    return val_unc_exp_str
