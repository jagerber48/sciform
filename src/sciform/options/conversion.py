"""Code for converting between various types of sciform options."""

from __future__ import annotations

from dataclasses import asdict
from typing import TYPE_CHECKING

from sciform import modes
from sciform.options import global_options
from sciform.options.finalized_options import FinalizedOptions
from sciform.options.populated_options import PopulatedOptions
from sciform.options.validation import validate_options

if TYPE_CHECKING:  # pragma: no cover
    from sciform.options.input_options import InputOptions


def populate_extra_si_prefixes(
    extra_si_prefixes: dict[int, str] | None,
    *,
    add_c_prefix: bool,
    add_small_si_prefixes: bool,
) -> dict[int, str]:
    """Populate extra_si_prefixes dict."""
    if add_c_prefix:
        if extra_si_prefixes is None:
            extra_si_prefixes = {}
        if -2 not in extra_si_prefixes:
            extra_si_prefixes[-2] = "c"
    if add_small_si_prefixes:
        if extra_si_prefixes is None:
            extra_si_prefixes = {}
        if -2 not in extra_si_prefixes:
            extra_si_prefixes[-2] = "c"
        if -1 not in extra_si_prefixes:
            extra_si_prefixes[-1] = "d"
        if +1 not in extra_si_prefixes:
            extra_si_prefixes[+1] = "da"
        if +2 not in extra_si_prefixes:
            extra_si_prefixes[+2] = "h"
    return extra_si_prefixes


def populate_extra_parts_per_forms(
    extra_parts_per_forms: dict[int, str] | None,
    *,
    add_ppth_form: bool,
) -> dict[int, str]:
    """Populate extra_si_prefixes dict."""
    if add_ppth_form:
        if extra_parts_per_forms is None:
            extra_parts_per_forms = {}
        if -3 not in extra_parts_per_forms:
            extra_parts_per_forms[-3] = "ppth"
    return extra_parts_per_forms


def populate_options(input_options: InputOptions) -> PopulatedOptions:
    """Populate InputOptions into PopulatedOptions."""
    global_options_dict = asdict(global_options.GLOBAL_DEFAULT_OPTIONS)
    input_options_dict = asdict(input_options)
    kwargs = {}
    for key in list(input_options_dict.keys()):
        if key in ["add_c_prefix", "add_small_si_prefixes", "add_ppth_form"]:
            continue

        value = input_options_dict[key]
        if key == "left_pad_char" and value == 0:
            value = "0"

        if key == "extra_si_prefixes":
            value = populate_extra_si_prefixes(
                value,
                add_c_prefix=input_options.add_c_prefix,
                add_small_si_prefixes=input_options.add_small_si_prefixes,
            )
        if key == "extra_parts_per_forms" and input_options.add_ppth_form:
            value = populate_extra_parts_per_forms(
                value,
                add_ppth_form=input_options.add_ppth_form,
            )

        if value is None:
            populated_value = global_options_dict[key]
        else:
            populated_value = value

        kwargs[key] = populated_value
    populated_options = PopulatedOptions(**kwargs)
    validate_options(populated_options)
    return populated_options


key_to_enum_dict = {
    "exp_mode": modes.ExpModeEnum,
    "round_mode": modes.RoundModeEnum,
    "upper_separator": modes.SeparatorEnum,
    "decimal_separator": modes.SeparatorEnum,
    "lower_separator": modes.SeparatorEnum,
    "sign_mode": modes.SignModeEnum,
    "left_pad_char": modes.LeftPadCharEnum,
    "exp_format": modes.ExpFormatEnum,
}


def finalize_populated_options(populated_options: PopulatedOptions) -> FinalizedOptions:
    """Convert PopulatedOptions into FinalizedOptions with enum values."""
    kwargs = populated_options.as_dict()
    for key, value in kwargs.items():
        if key in key_to_enum_dict:
            enum = key_to_enum_dict[key]
            kwargs[key] = modes.mode_str_to_enum(value, enum)
    return FinalizedOptions(**kwargs)


def finalize_input_options(input_options: InputOptions) -> FinalizedOptions:
    """Convert InputOptions into FinalizedOptions."""
    populated_options = populate_options(input_options)
    finalized_options = finalize_populated_options(populated_options)
    return finalized_options
