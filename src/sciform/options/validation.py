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
    options: InputOptions | PopulatedOptions,
    *,
    none_allowed: bool,
) -> None:
    """Validate user inputs."""
    validate_rounding(options, none_allowed=none_allowed)
    validate_exp_options(options, none_allowed=none_allowed)
    validate_sign_mode(options, none_allowed=none_allowed)
    validate_separator_options(options, none_allowed=none_allowed)
    validate_extra_translations(options, none_allowed=none_allowed)
    validate_left_pad_options(options, none_allowed=none_allowed)


allowed_round_modes = get_args(option_types.RoundMode)


def validate_rounding(
    options: InputOptions | PopulatedOptions,
    *,
    none_allowed: bool,
) -> None:
    r"""Validate ndigits if round_mode == "sig_fig"."""
    if none_allowed and options.ndigits is None:
        pass
    elif not isinstance(options.ndigits, int):
        msg = f"ndigits must be an int, not {options.ndigits}."
        raise TypeError(msg)

    if none_allowed and options.round_mode is None:
        pass
    else:
        if options.round_mode not in allowed_round_modes:
            msg = (
                f"round_mode must be in {allowed_round_modes}, not "
                f"{options.round_mode}."
            )
            raise ValueError(msg)
        if options.round_mode == "sig_fig" and options.ndigits < 1:
            msg = f"ndigits must be >= 1 for sig fig rounding, not {options.ndigits}."
            raise ValueError(msg)


allowed_exp_modes = get_args(option_types.ExpMode)
allowed_exp_formats = get_args(option_types.ExpFormat)


def validate_exp_val(
    options: InputOptions | PopulatedOptions | FinalizedOptions,
    *,
    none_allowed: bool,
) -> None:
    """Validate exponent value."""
    if none_allowed and options.exp_val is None:
        pass
    else:
        if not isinstance(options.exp_val, int) and options.exp_val != "auto":
            msg = f"exp_val must be an int, 'auto', or None, not {options.exp_val}."
            raise TypeError(msg)

        if options.exp_val != "auto":
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


def validate_exp_options(
    options: InputOptions | PopulatedOptions | FinalizedOptions,
    *,
    none_allowed: bool,
) -> None:
    """Validate exponent options."""
    if none_allowed and options.exp_mode is None:
        pass
    elif options.exp_mode not in allowed_exp_modes:
        msg = f"exp_mode must be in {allowed_exp_modes}, not {options.exp_mode}."
        raise ValueError(msg)

    validate_exp_val(options, none_allowed=none_allowed)

    if none_allowed and options.exp_format is None:
        pass
    elif options.exp_format not in allowed_exp_formats:
        msg = (
            f"{options.exp_format} must be in {allowed_exp_formats}, not "
            f"{options.exp_format}."
        )
        raise ValueError(msg)


allowed_sign_modes = get_args(option_types.SignMode)


def validate_sign_mode(
    options: InputOptions | PopulatedOptions | FinalizedOptions,
    *,
    none_allowed: bool,
) -> None:
    r"""Validate ndigits if round_mode == "sig_fig"."""
    if none_allowed and options.sign_mode is None:
        pass
    elif options.sign_mode not in allowed_sign_modes:
        msg = f"sign_mode must be in {allowed_sign_modes}, not {options.sign_mode}."
        raise ValueError(msg)


def validate_separator_options(
    options: InputOptions | PopulatedOptions | FinalizedOptions,
    *,
    none_allowed: bool,
) -> None:
    """Validate separator user input."""
    if none_allowed and options.upper_separator is None:
        pass
    else:
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

    if none_allowed and options.decimal_separator is None:
        pass
    elif options.decimal_separator not in get_args(option_types.DecimalSeparators):
        msg = (
            f"decimal_separator must be in "
            f"{get_args(option_types.DecimalSeparators)}, not "
            f"{options.decimal_separator}."
        )
        raise ValueError(msg)

    if none_allowed and options.lower_separator is None:
        pass
    elif options.lower_separator not in get_args(option_types.LowerSeparators):
        msg = (
            f"lower_separator must be in {get_args(option_types.LowerSeparators)}, "
            f"not {options.lower_separator}."
        )
        raise ValueError(msg)


def validate_extra_translations(
    options: InputOptions | PopulatedOptions | FinalizedOptions,
    *,
    none_allowed: bool,
) -> None:
    """Validate translation dictionary have int keys and alphabetic values."""
    translations_dicts = [
        options.extra_si_prefixes,
        options.extra_iec_prefixes,
        options.extra_parts_per_forms,
    ]

    for translation_dict in translations_dicts:
        if none_allowed and translation_dict is None:
            pass
        else:
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
    *,
    none_allowed: bool,
) -> None:
    """Validate left padding options."""
    if none_allowed and options.left_pad_dec_place is None:
        pass
    else:
        dec_place_msg = (
            f"left_pad_dec_place must an an int >= 0, not {options.left_pad_dec_place}."
        )
        if not isinstance(options.left_pad_dec_place, int):
            raise TypeError(dec_place_msg)
        if options.left_pad_dec_place < 0:
            raise ValueError(dec_place_msg)

    if none_allowed and options.left_pad_char is None:
        pass
    elif options.left_pad_char not in [0, "0", " "]:
        msg = f'left_pad_char must be in [" ", "0", 0], not {options.left_pad_char}.'
        raise ValueError(msg)
