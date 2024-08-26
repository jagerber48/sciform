"""String assembly utilities."""

from __future__ import annotations

import decimal
from decimal import Decimal

from sciform.format_utils.numbers import (
    get_top_dec_place,
)
from sciform.options.option_types import (
    DecimalSeparatorEnums,
    SeparatorEnum,
    SignModeEnum,
)


def get_sign_str(num: Decimal, sign_mode: SignModeEnum) -> str:
    """Get the format sign string."""
    with decimal.localcontext() as ctx:
        # TODO: Consider wrapping all the formatting in this context.
        ctx.traps[decimal.InvalidOperation] = False

        if num < 0:
            # Always return "-" for negative numbers.
            sign_str = "-"
        elif num > 0:
            # Return "+", " ", or "" for positive numbers.
            if sign_mode is SignModeEnum.ALWAYS:
                sign_str = "+"
            elif sign_mode is SignModeEnum.SPACE:
                sign_str = " "
            elif sign_mode is SignModeEnum.NEGATIVE:
                sign_str = ""
            else:
                msg = f"Invalid sign mode {sign_mode}."
                raise ValueError(msg)
        elif sign_mode is SignModeEnum.ALWAYS or sign_mode is SignModeEnum.SPACE:
            """
            For anything else (typically 0, possibly nan) return " " in "+" and " "
            modes.
            """
            sign_str = " "
        else:
            # Otherwise return the empty string.
            sign_str = ""

    return sign_str


def get_pad_str(
    left_pad_char: str,
    top_dec_place: int,
    top_padded_dec_place: int,
) -> str:
    """Get the string padding from top_dec_place place to top_padded_dec_place place."""
    if top_padded_dec_place > top_dec_place:
        pad_len = top_padded_dec_place - max(top_dec_place, 0)
        pad_str = left_pad_char * pad_len
    else:
        pad_str = ""
    return pad_str


def get_abs_num_str_by_bottom_dec_place(
    num: Decimal,
    target_bottom_dec_place: int,
) -> str:
    """Format a number according to specified bottom decimal places."""
    prec = max(0, -target_bottom_dec_place)
    abs_mantissa_str = f"{abs(num):.{prec}f}"
    return abs_mantissa_str


def construct_num_str(
    num: Decimal,
    target_top_dec_place: int,
    target_bottom_dec_place: int,
    sign_mode: SignModeEnum,
    left_pad_char: str,
) -> str:
    """Format a number to a specified decimal place, with left padding and a sign symbol."""  # noqa: E501
    abs_num_str = get_abs_num_str_by_bottom_dec_place(
        num,
        target_bottom_dec_place,
    )

    sign_str = get_sign_str(num, sign_mode)

    num_top_dec_place = get_top_dec_place(num)
    pad_str = get_pad_str(left_pad_char, num_top_dec_place, target_top_dec_place)
    return f"{sign_str}{pad_str}{abs_num_str}"


def parse_mantissa_str_to_dec(
    mantissa_str: str,
    decimal_separator: DecimalSeparatorEnums,
) -> Decimal:
    """Convert a string, possibly with non-standard separators, to a decimal."""
    clean_mantissa_str = mantissa_str
    for separator in SeparatorEnum:
        if separator != decimal_separator:
            clean_mantissa_str = clean_mantissa_str.replace(
                separator,
                "",
            )
    clean_mantissa_str = clean_mantissa_str.replace(decimal_separator, ".")
    mantissa_dec = Decimal(clean_mantissa_str)
    return mantissa_dec


def construct_val_unc_str(  # noqa: PLR0913
    val_mantissa_str: str,
    unc_mantissa_str: str,
    decimal_separator: DecimalSeparatorEnums,
    *,
    paren_uncertainty: bool,
    pm_whitespace: bool,
    paren_uncertainty_trim: bool,
) -> str:
    """Construct the value/uncertainty part of the formatted string."""
    if not paren_uncertainty:
        pm_symb = "±"
        if pm_whitespace:
            pm_symb = f" {pm_symb} "
        val_unc_str = f"{val_mantissa_str}{pm_symb}{unc_mantissa_str}"
    else:
        if paren_uncertainty_trim:
            val_dec = parse_mantissa_str_to_dec(val_mantissa_str, decimal_separator)
            unc_dec = parse_mantissa_str_to_dec(unc_mantissa_str, decimal_separator)
            if unc_dec.is_finite() and val_dec.is_finite():
                if unc_dec == 0:
                    unc_mantissa_str = "0"
                elif unc_dec < abs(val_dec):
                    for separator in SeparatorEnum:
                        if separator != decimal_separator:
                            unc_mantissa_str = unc_mantissa_str.replace(
                                separator,
                                "",
                            )
                    unc_mantissa_str = unc_mantissa_str.lstrip("0" + decimal_separator)
        val_unc_str = f"{val_mantissa_str}({unc_mantissa_str})"
    return val_unc_str


def construct_val_unc_exp_str(
    *,
    val_unc_str: str,
    exp_str: str,
    paren_uncertainty: bool,
) -> str:
    """Combine the val_unc_str into the final val_unc_exp_str."""
    if exp_str == "":
        val_unc_exp_str = val_unc_str
    elif paren_uncertainty:
        # No parentheses for paren_uncertainty, e.g. 123(4)e+03
        val_unc_exp_str = f"{val_unc_str}{exp_str}"
    else:
        # Wrapping parentheses for ± uncertainty, e.g. (123 ± 4)e+03
        val_unc_exp_str = f"({val_unc_str}){exp_str}"

    return val_unc_exp_str
