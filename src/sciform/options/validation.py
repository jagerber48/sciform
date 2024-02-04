"""Options validation."""

from __future__ import annotations

from typing import TYPE_CHECKING, get_args

from sciform import modes

if TYPE_CHECKING:  # pragma: no cover
    from sciform.options.finalized_options import FinalizedOptions
    from sciform.options.input_options import InputOptions
    from sciform.options.populated_options import PopulatedOptions


def validate_options(
    options: InputOptions | PopulatedOptions | FinalizedOptions,
) -> None:
    """Validate user inputs."""
    validate_sig_fig_round_mode(options)
    validate_exp_val(options)
    validate_separator_options(options)


def validate_sig_fig_round_mode(
    options: InputOptions | PopulatedOptions | FinalizedOptions,
) -> None:
    r"""Validate ndigits if round_mode == "sig_fig"."""
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
    if options.exp_val is not modes.AutoExpVal and options.exp_val is not None:
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
        if options.upper_separator not in get_args(modes.UpperSeparators):
            msg = (
                f"upper_separator must be in "
                f"{get_args(modes.UpperSeparators)}, not "
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
        options.decimal_separator not in get_args(modes.DecimalSeparators)
    ):
        msg = (
            f"decimal_separator must be in "
            f"{get_args(modes.DecimalSeparators)}, not "
            f"{options.decimal_separator}."
        )
        raise ValueError(msg)

    if options.lower_separator is not None and (
        options.lower_separator not in get_args(modes.LowerSeparators)
    ):
        msg = (
            f"lower_separator must be in {get_args(modes.LowerSeparators)}, "
            f"not {options.lower_separator}."
        )
        raise ValueError(msg)
