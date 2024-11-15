"""Exponent processing and string assembly utilities."""

from __future__ import annotations

from typing import TYPE_CHECKING

from sciform.format_utils.exp_translations import (
    val_to_parts_per_dict,
    val_to_si_dict,
)
from sciform.format_utils.numbers import (
    get_mantissa_exp,
)
from sciform.options.option_types import (
    ExpFormatEnum,
    ExpModeEnum,
    ExpValEnum,
)

if TYPE_CHECKING:  # pragma: no cover
    from decimal import Decimal


def get_translation_dict(
    exp_format: ExpFormatEnum,
    extra_si_prefixes: dict[int, str],
    extra_parts_per_forms: dict[int, str],
) -> dict[int, str]:
    """Resolve dictionary of prefix translations."""
    if exp_format is ExpFormatEnum.PREFIX:
        translation_dict = val_to_si_dict.copy()
        translation_dict.update(extra_si_prefixes)
    elif exp_format is ExpFormatEnum.PARTS_PER:
        translation_dict = val_to_parts_per_dict.copy()
        translation_dict.update(extra_parts_per_forms)
    else:
        msg = f"Unhandled ExpFormat, {exp_format}."
        raise ValueError(msg)

    return translation_dict


def get_standard_exp_str(exp_val: int, *, capitalize: bool = False) -> str:
    """Get standard (eg. 'e+02') exponent string."""
    base_symbol = "e"
    if capitalize:
        base_symbol = base_symbol.capitalize()
    return f"{base_symbol}{exp_val:+03d}"


superscript_translate = str.maketrans("+-0123456789", "⁺⁻⁰¹²³⁴⁵⁶⁷⁸⁹")


def get_superscript_exp_str(exp_val: int) -> str:
    """Get superscript (e.g. '×10⁺²') exponent string."""
    exp_val_str = f"{exp_val}".translate(superscript_translate)
    return f"×10{exp_val_str}"


def get_exp_str(  # noqa: PLR0913
    *,
    exp_val: int,
    exp_mode: ExpModeEnum,
    exp_format: ExpFormatEnum,
    extra_si_prefixes: dict[int, str],
    extra_parts_per_forms: dict[int, str],
    capitalize: bool,
    superscript: bool,
) -> str:
    """Get formatting exponent string."""
    if exp_mode is ExpModeEnum.FIXEDPOINT:
        return ""
    if exp_mode is ExpModeEnum.PERCENT:
        return "%"

    if exp_format is ExpFormatEnum.PREFIX or exp_format is ExpFormatEnum.PARTS_PER:
        translation_dict = get_translation_dict(
            exp_format,
            extra_si_prefixes,
            extra_parts_per_forms,
        )
        if (
            exp_val in translation_dict
            and (exp_str := translation_dict[exp_val]) is not None
        ):
            if exp_str != "":
                exp_str = f" {exp_str}"
            return exp_str

    if superscript:
        return get_superscript_exp_str(exp_val)

    return get_standard_exp_str(exp_val, capitalize=capitalize)


def get_val_unc_exp(
    val: Decimal,
    unc: Decimal,
    exp_mode: ExpModeEnum,
    input_exp: int | ExpValEnum,
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

    _, exp_val = get_mantissa_exp(
        exp_driver_val,
        exp_mode=exp_mode,
        input_exp=input_exp,
    )

    return exp_val
