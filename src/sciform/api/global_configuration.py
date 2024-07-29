"""Global configuration functions and context manager."""

from __future__ import annotations

from typing import TYPE_CHECKING, Literal

from sciform.options import global_options, option_types
from sciform.options.conversion import populate_options
from sciform.options.input_options import InputOptions

if TYPE_CHECKING:  # pragma: no cover
    from types import TracebackType

    from sciform.options.populated_options import PopulatedOptions


def get_default_global_options() -> PopulatedOptions:
    """Return the package default global options."""
    return global_options.PKG_DEFAULT_OPTIONS


def get_global_options() -> PopulatedOptions:
    """Return the current global options."""
    return global_options.GLOBAL_DEFAULT_OPTIONS


def set_global_options(  # noqa: PLR0913
    *,
    exp_mode: option_types.ExpMode | None = None,
    exp_val: int | Literal["auto"] | None = None,
    round_mode: option_types.RoundMode | None = None,
    ndigits: int | Literal["all", "pdg"] | None = None,
    upper_separator: option_types.UpperSeparators | None = None,
    decimal_separator: option_types.DecimalSeparators | None = None,
    lower_separator: option_types.LowerSeparators | None = None,
    sign_mode: option_types.SignMode | None = None,
    left_pad_char: option_types.LeftPadChar | None = None,
    left_pad_dec_place: int | None = None,
    exp_format: option_types.ExpFormat | None = None,
    extra_si_prefixes: dict[int, str] | None = None,
    extra_iec_prefixes: dict[int, str] | None = None,
    extra_parts_per_forms: dict[int, str] | None = None,
    capitalize: bool | None = None,
    superscript: bool | None = None,
    nan_inf_exp: bool | None = None,
    paren_uncertainty: bool | None = None,
    left_pad_matching: bool | None = None,
    paren_uncertainty_trim: bool | None = None,
    pm_whitespace: bool | None = None,
    add_c_prefix: bool = False,
    add_small_si_prefixes: bool = False,
    add_ppth_form: bool = False,
) -> None:
    """
    Configure the global options.

    Accepts the same keyword arguments as :class:`Formatter`.
    """
    input_options = InputOptions(
        exp_mode=exp_mode,
        exp_val=exp_val,
        round_mode=round_mode,
        ndigits=ndigits,
        upper_separator=upper_separator,
        decimal_separator=decimal_separator,
        lower_separator=lower_separator,
        sign_mode=sign_mode,
        left_pad_char=left_pad_char,
        left_pad_dec_place=left_pad_dec_place,
        exp_format=exp_format,
        extra_si_prefixes=extra_si_prefixes,
        extra_iec_prefixes=extra_iec_prefixes,
        extra_parts_per_forms=extra_parts_per_forms,
        capitalize=capitalize,
        superscript=superscript,
        nan_inf_exp=nan_inf_exp,
        paren_uncertainty=paren_uncertainty,
        left_pad_matching=left_pad_matching,
        paren_uncertainty_trim=paren_uncertainty_trim,
        pm_whitespace=pm_whitespace,
        add_c_prefix=add_c_prefix,
        add_small_si_prefixes=add_small_si_prefixes,
        add_ppth_form=add_ppth_form,
    )
    set_global_options_populated(populate_options(input_options))


def set_global_options_populated(populated_options: PopulatedOptions) -> None:
    """Directly set global options to input :class:`PopulatedOptions`."""
    global_options.GLOBAL_DEFAULT_OPTIONS = populated_options


def reset_global_options() -> None:
    """Reset global options to :mod:`sciform` package defaults."""
    global_options.GLOBAL_DEFAULT_OPTIONS = global_options.PKG_DEFAULT_OPTIONS


class GlobalOptionsContext:
    """
    Temporarily update global options.

    New global options are applied when the context is entered and the
    original global settings are re-applied when the context is exited.
    Accepts the same keyword arguments as :class:`Formatter`.
    """

    def __init__(  # noqa: PLR0913
        self: GlobalOptionsContext,
        *,
        exp_mode: option_types.ExpMode | None = None,
        exp_val: int | option_types.ExpVal | None = None,
        round_mode: option_types.RoundMode | None = None,
        ndigits: int | option_types.NDigits | None = None,
        upper_separator: option_types.UpperSeparators | None = None,
        decimal_separator: option_types.DecimalSeparators | None = None,
        lower_separator: option_types.LowerSeparators | None = None,
        sign_mode: option_types.SignMode | None = None,
        left_pad_char: option_types.LeftPadChar | None = None,
        left_pad_dec_place: int | None = None,
        exp_format: option_types.ExpFormat | None = None,
        extra_si_prefixes: dict[int, str] | None = None,
        extra_iec_prefixes: dict[int, str] | None = None,
        extra_parts_per_forms: dict[int, str] | None = None,
        capitalize: bool | None = None,
        superscript: bool | None = None,
        nan_inf_exp: bool | None = None,
        paren_uncertainty: bool | None = None,
        left_pad_matching: bool | None = None,
        paren_uncertainty_trim: bool | None = None,
        pm_whitespace: bool | None = None,
        add_c_prefix: bool = False,
        add_small_si_prefixes: bool = False,
        add_ppth_form: bool = False,
    ) -> None:
        input_options = InputOptions(
            exp_mode=exp_mode,
            exp_val=exp_val,
            round_mode=round_mode,
            ndigits=ndigits,
            upper_separator=upper_separator,
            decimal_separator=decimal_separator,
            lower_separator=lower_separator,
            sign_mode=sign_mode,
            left_pad_char=left_pad_char,
            left_pad_dec_place=left_pad_dec_place,
            exp_format=exp_format,
            extra_si_prefixes=extra_si_prefixes,
            extra_iec_prefixes=extra_iec_prefixes,
            extra_parts_per_forms=extra_parts_per_forms,
            capitalize=capitalize,
            superscript=superscript,
            nan_inf_exp=nan_inf_exp,
            paren_uncertainty=paren_uncertainty,
            left_pad_matching=left_pad_matching,
            paren_uncertainty_trim=paren_uncertainty_trim,
            pm_whitespace=pm_whitespace,
            add_c_prefix=add_c_prefix,
            add_small_si_prefixes=add_small_si_prefixes,
            add_ppth_form=add_ppth_form,
        )
        self.populated_options = populate_options(input_options)
        self.initial_global_defaults = None

    def __enter__(self: GlobalOptionsContext) -> None:
        """Enter the context."""
        self.initial_global_defaults = get_global_options()
        set_global_options_populated(self.populated_options)

    def __exit__(
        self: GlobalOptionsContext,
        exc_type: type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: TracebackType | None,
    ) -> None:
        """Exit the context."""
        set_global_options_populated(self.initial_global_defaults)
