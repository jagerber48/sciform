"""Options validation."""

from __future__ import annotations

import re
from typing import TYPE_CHECKING, get_args

from sciform.options import option_types

if TYPE_CHECKING:  # pragma: no cover
    from sciform.options.finalized_options import FinalizedOptions
    from sciform.options.input_options import InputOptions
    from sciform.options.populated_options import PopulatedOptions


def validate_options(
    options: InputOptions | PopulatedOptions | FinalizedOptions,
) -> None:
    """Validate user inputs."""
    validate_rounding(options)
    validate_exp_val(options)
    validate_separator_options(options)
    validate_extra_translations(options)
    validate_left_pad_options(options)


def validate_rounding(
    options: InputOptions | PopulatedOptions | FinalizedOptions,
) -> None:
    r"""Validate ndigits if round_mode == "sig_fig"."""
    valid_ndigit_types = (
        int,
        type(option_types.AutoDigits),
        type(None),
    )
    if not isinstance(options.ndigits, valid_ndigit_types):
        msg = f'ndigits must be an "int" or "AutoDigits", not {options.ndigits}.'
        raise TypeError(msg)

    if (
        options.round_mode == "sig_fig"
        and isinstance(options.ndigits, int)
        and options.ndigits < 1
    ):
        msg = f"ndigits must be >= 1 for sig fig rounding, not {options.ndigits}."
        raise ValueError(msg)


def validate_exp_val(
    options: InputOptions | PopulatedOptions | FinalizedOptions,
) -> None:
    """Validate exp_val."""
    if options.exp_val is not option_types.AutoExpVal and options.exp_val is not None:
        if options.exp_mode in ["fixed_point", "percent"] and options.exp_val != 0:
            msg = (
                f"Exponent must must be 0, not exp_val={options.exp_val}, for "
                f"fixed point and percent exponent modes."
            )
            raise ValueError(msg)
        if (
            options.exp_mode in ["engineering", "engineering_shifted"]
            and options.exp_val % 3 != 0
        ):
            msg = (
                f"Exponent must be a multiple of 3, not exp_val={options.exp_val}, "
                f"for engineering exponent modes."
            )
            raise ValueError(msg)
        if options.exp_mode == "binary_iec" and options.exp_val % 10 != 0:
            msg = (
                f"Exponent must be a multiple of 10, not "
                f"exp_val={options.exp_val}, for binary IEC exponent mode."
            )
            raise ValueError(msg)


def validate_separator_options(
    options: InputOptions | PopulatedOptions | FinalizedOptions,
) -> None:
    """Validate separator user input."""
    if options.upper_separator is not None:
        if options.upper_separator not in get_args(option_types.UpperSeparators):
            msg = (
                f"upper_separator must be in "
                f"{get_args(option_types.UpperSeparators)}, not "
                f"{options.upper_separator}."
            )
            raise ValueError(msg)
        if options.upper_separator == options.decimal_separator:
            msg = (
                f"upper_separator and decimal_separator "
                f"({options.upper_separator}) cannot be equal."
            )
            raise ValueError(msg)

    if options.decimal_separator is not None and (
        options.decimal_separator not in get_args(option_types.DecimalSeparators)
    ):
        msg = (
            f"decimal_separator must be in "
            f"{get_args(option_types.DecimalSeparators)}, not "
            f"{options.decimal_separator}."
        )
        raise ValueError(msg)

    if options.lower_separator is not None and (
        options.lower_separator not in get_args(option_types.LowerSeparators)
    ):
        msg = (
            f"lower_separator must be in {get_args(option_types.LowerSeparators)}, "
            f"not {options.lower_separator}."
        )
        raise ValueError(msg)


def validate_extra_translations(
    options: InputOptions | PopulatedOptions | FinalizedOptions,
) -> None:
    """Validate translation dictionary have int keys and alphabetic values."""
    translations_dicts = [
        options.extra_si_prefixes,
        options.extra_iec_prefixes,
        options.extra_parts_per_forms,
    ]

    for translation_dict in translations_dicts:
        if translation_dict is not None:
            for key, value in translation_dict.items():
                if not isinstance(key, int):
                    msg = f'Translation dictionary keys must be integers, not "{key}".'
                    raise TypeError(msg)
                if value is not None and not re.match(r"[a-zA-Z]+", value):
                    msg = (
                        f"Translation dictionary values may only contain lower or "
                        f"uppercase ASCII characters from the English alphabet, not "
                        f'"{value}".'
                    )
                    raise ValueError(msg)


def validate_left_pad_options(
    options: InputOptions | PopulatedOptions | FinalizedOptions,
) -> None:
    """Validate left padding options."""
    dec_place_msg = (
        f"left_pad_dec_place must an an int >= 0, not {options.left_pad_dec_place}."
    )
    if options.left_pad_dec_place is not None:
        if not isinstance(options.left_pad_dec_place, int):
            raise TypeError(dec_place_msg)
        if options.left_pad_dec_place < 0:
            raise ValueError(dec_place_msg)
    if options.left_pad_char is not None and options.left_pad_char not in [0, "0", " "]:
        msg = f'left_pad_char must be in [" ", "0", 0], not {options.left_pad_char}.'
        raise ValueError(msg)
