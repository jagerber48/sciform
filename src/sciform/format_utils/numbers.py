"""Utilities for parsing mantissa, base, and exp."""

from __future__ import annotations

import re
from decimal import Decimal
from math import floor, log2
from typing import Literal

from sciform.formatting.parser import (
    ascii_exp_pattern,
    finite_val_pattern,
    non_finite_val_pattern,
)
from sciform.options.option_types import (
    ExpModeEnum,
    ExpValEnum,
)


def get_top_dec_place(num: Decimal) -> int:
    """Get the decimal place of a decimal's most significant digit."""
    if not num.is_finite():
        return 0
    _, digits, exp = num.normalize().as_tuple()
    return len(digits) + exp - 1


def get_top_dec_place_binary(num: Decimal) -> int:
    """Get the decimal place of a decimal's most significant digit."""
    if not num.is_finite() or num == 0:
        return 0
    return floor(log2(abs(num)))


def get_bottom_dec_place(num: Decimal) -> int:
    """Get the decimal place of a decimal's least significant digit."""
    if not num.is_finite():
        return 0
    _, _, exp = num.normalize().as_tuple()
    return exp


def get_val_unc_top_dec_place(
    val_mantissa: Decimal,
    unc_mantissa: Decimal,
    input_top_dec_place: int,
    *,
    left_pad_matching: bool,
) -> int:
    """Get top decimal place for value/uncertainty formatting."""
    if left_pad_matching:
        val_top_dec_place = get_top_dec_place(val_mantissa)
        unc_top_dec_place = get_top_dec_place(unc_mantissa)
        new_top_dec_place = max(
            input_top_dec_place,
            val_top_dec_place,
            unc_top_dec_place,
        )
    else:
        new_top_dec_place = input_top_dec_place
    new_top_dec_place = max(0, new_top_dec_place)
    return new_top_dec_place


def get_fixed_exp(
    input_exp: int | ExpValEnum,
) -> Literal[0]:
    """Get the exponent for fixed or percent format modes."""
    if input_exp is not ExpValEnum.AUTO and input_exp != 0:
        msg = "Cannot set non-zero exponent in fixed point or percent exponent mode."
        raise ValueError(msg)
    return 0


def get_scientific_exp(
    num: Decimal,
    input_exp: int | ExpValEnum,
) -> int:
    """Get the exponent for scientific formatting mode."""
    return get_top_dec_place(num) if input_exp is ExpValEnum.AUTO else input_exp


def get_engineering_exp(
    num: Decimal,
    input_exp: int | ExpValEnum,
    *,
    shifted: bool = False,
) -> int:
    """Get the exponent for engineering formatting modes."""
    if input_exp is ExpValEnum.AUTO:
        exp_val = get_top_dec_place(num)
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
    input_exp: int | ExpValEnum,
    *,
    iec: bool = False,
) -> int:
    """Get the exponent for binary formatting modes."""
    if input_exp is ExpValEnum.AUTO:
        exp_val = get_top_dec_place_binary(num)
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
    input_exp: int | ExpValEnum,
) -> tuple[Decimal, int, int]:
    """Get mantissa, exponent, and base for formatting a decimal number."""
    if exp_mode is ExpModeEnum.BINARY or exp_mode is ExpModeEnum.BINARY_IEC:
        base = 2
    else:
        base = 10

    if num == 0 or not num.is_finite():
        mantissa = Decimal(num)
        exp = 0 if input_exp is ExpValEnum.AUTO else input_exp
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


# language=pythonverboseregexp  noqa: ERA001
no_exp_pattern = rf"^(?P<mantissa>{non_finite_val_pattern})$"
# language=pythonverboseregexp  noqa: ERA001
optional_exp_pattern = rf"""
^(?P<mantissa>{finite_val_pattern})(?P<exp>{ascii_exp_pattern})?$
"""
# language=pythonverboseregexp  noqa: ERA001
always_exp_pattern = rf"""
^
\((?P<mantissa>{non_finite_val_pattern})\)
(?P<exp>{ascii_exp_pattern})
$
"""


def parse_mantissa_from_ascii_exp_str(number_str: str) -> str:
    """Break val/unc mantissa/exp strings into mantissa strings and an exp string."""
    if match := re.match(no_exp_pattern, number_str, re.VERBOSE):
        return match.group("mantissa")
    if match := re.match(optional_exp_pattern, number_str, re.VERBOSE):
        return match.group("mantissa")
    if match := re.match(always_exp_pattern, number_str, re.VERBOSE):
        return match.group("mantissa")
    msg = f'Invalid number string "{number_str}".'
    raise ValueError(msg)
