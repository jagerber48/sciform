"""Utilities for parsing mantissa, base, and exp."""

from __future__ import annotations

import re
from decimal import Decimal
from math import floor, log2
from typing import Literal

from sciform.formatting.parser import any_val_pattern
from sciform.options.option_types import (
    AutoDigits,
    AutoExpVal,
    ExpModeEnum,
)


def get_top_digit(num: Decimal) -> int:
    """Get the decimal place of a decimal's most significant digit."""
    if not num.is_finite() or num == 0:
        return 0
    _, digits, exp = num.as_tuple()
    return len(digits) + exp - 1


def get_top_digit_binary(num: Decimal) -> int:
    """Get the decimal place of a decimal's most significant digit."""
    if not num.is_finite() or num == 0:
        return 0
    return floor(log2(abs(num)))


def get_bottom_digit(num: Decimal) -> int:
    """Get the decimal place of a decimal's least significant digit."""
    if not num.is_finite():
        return 0
    _, _, exp = num.as_tuple()
    return exp


def get_val_unc_top_digit(
    val_mantissa: Decimal,
    unc_mantissa: Decimal,
    input_top_digit: int | AutoDigits,
    *,
    left_pad_matching: bool,
) -> int | AutoDigits:
    """Get top digit place for value/uncertainty formatting."""
    if left_pad_matching:
        val_top_digit = get_top_digit(val_mantissa)
        unc_top_digit = get_top_digit(unc_mantissa)
        new_top_digit = max(
            input_top_digit,
            val_top_digit,
            unc_top_digit,
        )
    else:
        new_top_digit = input_top_digit
    return new_top_digit


def get_fixed_exp(
    input_exp: int | type(AutoExpVal),
) -> Literal[0]:
    """Get the exponent for fixed or percent format modes."""
    if input_exp is not AutoExpVal and input_exp != 0:
        msg = "Cannot set non-zero exponent in fixed point or percent exponent mode."
        raise ValueError(msg)
    return 0


def get_scientific_exp(
    num: Decimal,
    input_exp: int | type(AutoExpVal),
) -> int:
    """Get the exponent for scientific formatting mode."""
    return get_top_digit(num) if input_exp is AutoExpVal else input_exp


def get_engineering_exp(
    num: Decimal,
    input_exp: int | type(AutoExpVal),
    *,
    shifted: bool = False,
) -> int:
    """Get the exponent for engineering formatting modes."""
    if input_exp is AutoExpVal:
        exp_val = get_top_digit(num)
        exp_val = exp_val // 3 * 3 if not shifted else (exp_val + 1) // 3 * 3
    else:
        if input_exp % 3 != 0:
            msg = (
                f"Exponent must be an integer multiple of 3 in engineering modes, not "
                f"{input_exp}."
            )
            raise ValueError(msg)
        exp_val = input_exp
    return exp_val


def get_binary_exp(
    num: Decimal,
    input_exp: int | type(AutoExpVal),
    *,
    iec: bool = False,
) -> int:
    """Get the exponent for binary formatting modes."""
    if input_exp is AutoExpVal:
        exp_val = get_top_digit_binary(num)
        if iec:
            exp_val = (exp_val // 10) * 10
    else:
        if iec and input_exp % 10 != 0:
            msg = (
                f"Exponent must be an integer multiple of 10 in binary IEC mode, not "
                f"{input_exp}."
            )
            raise ValueError(msg)
        exp_val = input_exp
    return exp_val


def get_mantissa_exp_base(
    num: Decimal,
    exp_mode: ExpModeEnum,
    input_exp: int | type(AutoExpVal),
) -> tuple[Decimal, int, int]:
    """Get mantissa, exponent, and base for formatting a decimal number."""
    if exp_mode is ExpModeEnum.BINARY or exp_mode is ExpModeEnum.BINARY_IEC:
        base = 2
    else:
        base = 10

    if num == 0 or not num.is_finite():
        mantissa = Decimal(num)
        exp = 0 if input_exp is AutoExpVal else input_exp
    else:
        if exp_mode is ExpModeEnum.FIXEDPOINT or exp_mode is ExpModeEnum.PERCENT:
            exp = get_fixed_exp(input_exp)
        elif exp_mode is ExpModeEnum.SCIENTIFIC:
            exp = get_scientific_exp(num, input_exp)
        elif exp_mode is ExpModeEnum.ENGINEERING:
            exp = get_engineering_exp(num, input_exp)
        elif exp_mode is ExpModeEnum.ENGINEERING_SHIFTED:
            exp = get_engineering_exp(num, input_exp, shifted=True)
        elif exp_mode is ExpModeEnum.BINARY:
            exp = get_binary_exp(num, input_exp)
        elif exp_mode is ExpModeEnum.BINARY_IEC:
            exp = get_binary_exp(num, input_exp, iec=True)
        else:
            msg = f"Unhandled exponent mode {exp_mode}."
            raise ValueError(msg)
        mantissa = num * Decimal(base) ** Decimal(-exp)
    mantissa = mantissa.normalize()
    return mantissa, exp, base


# Optional parentheses needed to handle (nan)e+00 case
mantissa_exp_pattern = re.compile(
    rf"""
    ^
    \(?(?P<mantissa_str>{any_val_pattern})\)?
    (?P<exp_str>[eEbB].*?)?
    $
""",
    re.VERBOSE,
)


def parse_mantissa_from_ascii_exp_str(number_str: str) -> str:
    """Break val/unc mantissa/exp strings into mantissa strings and an exp string."""
    if match := mantissa_exp_pattern.match(number_str):
        return match.group("mantissa_str")
    msg = f'Invalid number string "{number_str}".'
    raise ValueError(msg)
