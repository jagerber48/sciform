"""Exponent processing and string assembly utilities."""
from __future__ import annotations

from typing import TYPE_CHECKING, Literal, cast

from sciform.format_utils.number_utils import (
    get_mantissa_exp_base,
)
from sciform.options.option_types import (
    ExpFormatEnum,
    ExpModeEnum,
)
from sciform.prefix import (
    iec_val_to_prefix_dict,
    pp_val_to_prefix_dict,
    si_val_to_prefix_dict,
)

if TYPE_CHECKING:
    from decimal import Decimal


def get_prefix_dict(
    exp_format: ExpFormatEnum,
    base: Literal[10, 2],
    extra_si_prefixes: dict[int, str],
    extra_iec_prefixes: dict[int, str],
    extra_parts_per_forms: dict[int, str],
) -> dict[int, str]:
    """Resolve dictionary of prefix translations."""
    if exp_format is ExpFormatEnum.PREFIX:
        if base == 10:
            prefix_dict = si_val_to_prefix_dict.copy()
            prefix_dict.update(extra_si_prefixes)
        elif base == 2:
            prefix_dict = iec_val_to_prefix_dict.copy()
            prefix_dict.update(extra_iec_prefixes)
        else:
            msg = f"Unhandled base {base}"
            raise ValueError(msg)
    elif exp_format is ExpFormatEnum.PARTS_PER:
        prefix_dict = pp_val_to_prefix_dict.copy()
        prefix_dict.update(extra_parts_per_forms)
    else:
        msg = f"Unhandled ExpFormat, {exp_format}."
        raise ValueError(msg)

    return prefix_dict


def get_standard_exp_str(base: int, exp_val: int, *, capitalize: bool = False) -> str:
    """Get standard (eg. 'e+02') exponent string."""
    base_exp_symbol_dict = {10: "e", 2: "b"}
    exp_symbol = base_exp_symbol_dict[base]
    if capitalize:
        exp_symbol = exp_symbol.capitalize()
    return f"{exp_symbol}{exp_val:+03d}"


def get_superscript_exp_str(base: int, exp_val: int) -> str:
    """Get superscript (e.g. '×10⁺²') exponent string."""
    sup_trans = str.maketrans("+-0123456789", "⁺⁻⁰¹²³⁴⁵⁶⁷⁸⁹")
    exp_val_str = f"{exp_val}".translate(sup_trans)
    return f"×{base}{exp_val_str}"


def get_exp_str(  # noqa: PLR0913
    *,
    exp_val: int,
    exp_mode: ExpModeEnum,
    exp_format: ExpFormatEnum,
    extra_si_prefixes: dict[int, str],
    extra_iec_prefixes: dict[int, str],
    extra_parts_per_forms: dict[int, str],
    capitalize: bool,
    superscript: bool,
) -> str:
    """Get formatting exponent string."""
    if exp_mode is ExpModeEnum.FIXEDPOINT:
        return ""
    if exp_mode is ExpModeEnum.PERCENT:
        return "%"

    if exp_mode is ExpModeEnum.BINARY or exp_mode is ExpModeEnum.BINARY_IEC:
        base = 2
    else:
        base = 10
    base = cast(Literal[10, 2], base)

    if exp_format is ExpFormatEnum.PREFIX or exp_format is ExpFormatEnum.PARTS_PER:
        text_exp_dict = get_prefix_dict(
            exp_format,
            base,
            extra_si_prefixes,
            extra_iec_prefixes,
            extra_parts_per_forms,
        )
        if exp_val in text_exp_dict and text_exp_dict[exp_val] is not None:
            exp_str = f" {text_exp_dict[exp_val]}"
            exp_str = exp_str.rstrip(" ")
            return exp_str

    if superscript:
        return get_superscript_exp_str(base, exp_val)

    return get_standard_exp_str(base, exp_val, capitalize=capitalize)


def get_val_unc_exp(
    val: Decimal,
    unc: Decimal,
    exp_mode: ExpModeEnum,
    input_exp: int,
) -> int:
    """Get exponent for value/uncertainty formatting."""
    if val.is_finite() and unc.is_finite():
        if abs(val) >= unc:
            exp_driver_val = val
        else:
            exp_driver_val = unc
    elif val.is_finite():
        exp_driver_val = val
    else:
        exp_driver_val = unc

    _, exp_val, _ = get_mantissa_exp_base(
        exp_driver_val,
        exp_mode=exp_mode,
        input_exp=input_exp,
    )

    return exp_val
