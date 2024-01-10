"""Global configuration functions and context manager."""

from __future__ import annotations

from typing import TYPE_CHECKING

from sciform import global_options, modes
from sciform.user_options import UserOptions

if TYPE_CHECKING:  # pragma: no cover
    from types import TracebackType

    from sciform.rendered_options import RenderedOptions


def print_global_defaults() -> None:
    """Print current global default formatting options as a dictionary."""
    print(str(global_options.GLOBAL_DEFAULT_OPTIONS))  # noqa: T201


def set_global_defaults(  # noqa: PLR0913
    *,
    exp_mode: modes.UserExpMode | None = None,
    exp_val: int | type(modes.AutoExpVal) | None = None,
    round_mode: modes.UserRoundMode | None = None,
    ndigits: int | type(modes.AutoDigits) | None = None,
    upper_separator: modes.UserUpperSeparators | None = None,
    decimal_separator: modes.UserDecimalSeparators | None = None,
    lower_separator: modes.UserLowerSeparators | None = None,
    sign_mode: modes.UserSignMode | None = None,
    fill_char: modes.UserFillChar | None = None,
    left_pad_dec_place: int | None = None,
    exp_format: modes.UserExpFormat | None = None,
    extra_si_prefixes: dict[int, str] | None = None,
    extra_iec_prefixes: dict[int, str] | None = None,
    extra_parts_per_forms: dict[int, str] | None = None,
    capitalize: bool | None = None,
    superscript: bool | None = None,
    latex: bool | None = None,
    nan_inf_exp: bool | None = None,
    paren_uncertainty: bool | None = None,
    pdg_sig_figs: bool | None = None,
    left_pad_matching: bool | None = None,
    paren_uncertainty_separators: bool | None = None,
    pm_whitespace: bool | None = None,
    add_c_prefix: bool = False,
    add_small_si_prefixes: bool = False,
    add_ppth_form: bool = False,
) -> None:
    """
    Configure global default format options.

    Accepts the same keyword arguments as :class:`Formatter`.
    """
    user_options = UserOptions(
        exp_mode=exp_mode,
        exp_val=exp_val,
        round_mode=round_mode,
        ndigits=ndigits,
        upper_separator=upper_separator,
        decimal_separator=decimal_separator,
        lower_separator=lower_separator,
        sign_mode=sign_mode,
        fill_char=fill_char,
        left_pad_dec_place=left_pad_dec_place,
        exp_format=exp_format,
        extra_si_prefixes=extra_si_prefixes,
        extra_iec_prefixes=extra_iec_prefixes,
        extra_parts_per_forms=extra_parts_per_forms,
        capitalize=capitalize,
        superscript=superscript,
        latex=latex,
        nan_inf_exp=nan_inf_exp,
        paren_uncertainty=paren_uncertainty,
        pdg_sig_figs=pdg_sig_figs,
        left_pad_matching=left_pad_matching,
        paren_uncertainty_separators=paren_uncertainty_separators,
        pm_whitespace=pm_whitespace,
        add_c_prefix=add_c_prefix,
        add_small_si_prefixes=add_small_si_prefixes,
        add_ppth_form=add_ppth_form,
    )
    set_global_defaults_rendered(user_options.render())


def set_global_defaults_rendered(rendered_options: RenderedOptions) -> None:
    """Directly set global defaults to input RenderedOptions."""
    global_options.GLOBAL_DEFAULT_OPTIONS = rendered_options


def reset_global_defaults() -> None:
    """Reset global default options to :mod:`sciform` package defaults."""
    global_options.GLOBAL_DEFAULT_OPTIONS = global_options.PKG_DEFAULT_OPTIONS


class GlobalDefaultsContext:
    """
    Temporarily update global default options.

    New settings are applied when the context is entered and original
    global settings are re-applied when the context is exited. Accepts
    the same keyword arguments as :class:`Formatter`.
    """

    def __init__(  # noqa: PLR0913
        self: GlobalDefaultsContext,
        *,
        exp_mode: modes.UserExpMode | None = None,
        exp_val: int | type(modes.AutoExpVal) | None = None,
        round_mode: modes.UserRoundMode | None = None,
        ndigits: int | type(modes.AutoDigits) | None = None,
        upper_separator: modes.UserUpperSeparators | None = None,
        decimal_separator: modes.UserDecimalSeparators | None = None,
        lower_separator: modes.UserLowerSeparators | None = None,
        sign_mode: modes.UserSignMode | None = None,
        fill_char: modes.UserFillChar | None = None,
        left_pad_dec_place: int | None = None,
        exp_format: modes.UserExpFormat | None = None,
        extra_si_prefixes: dict[int, str] | None = None,
        extra_iec_prefixes: dict[int, str] | None = None,
        extra_parts_per_forms: dict[int, str] | None = None,
        capitalize: bool | None = None,
        superscript: bool | None = None,
        latex: bool | None = None,
        nan_inf_exp: bool | None = None,
        paren_uncertainty: bool | None = None,
        pdg_sig_figs: bool | None = None,
        left_pad_matching: bool | None = None,
        paren_uncertainty_separators: bool | None = None,
        pm_whitespace: bool | None = None,
        add_c_prefix: bool = False,
        add_small_si_prefixes: bool = False,
        add_ppth_form: bool = False,
    ) -> None:
        user_options = UserOptions(
            exp_mode=exp_mode,
            exp_val=exp_val,
            round_mode=round_mode,
            ndigits=ndigits,
            upper_separator=upper_separator,
            decimal_separator=decimal_separator,
            lower_separator=lower_separator,
            sign_mode=sign_mode,
            fill_char=fill_char,
            left_pad_dec_place=left_pad_dec_place,
            exp_format=exp_format,
            extra_si_prefixes=extra_si_prefixes,
            extra_iec_prefixes=extra_iec_prefixes,
            extra_parts_per_forms=extra_parts_per_forms,
            capitalize=capitalize,
            superscript=superscript,
            latex=latex,
            nan_inf_exp=nan_inf_exp,
            paren_uncertainty=paren_uncertainty,
            pdg_sig_figs=pdg_sig_figs,
            left_pad_matching=left_pad_matching,
            paren_uncertainty_separators=paren_uncertainty_separators,
            pm_whitespace=pm_whitespace,
            add_c_prefix=add_c_prefix,
            add_small_si_prefixes=add_small_si_prefixes,
            add_ppth_form=add_ppth_form,
        )
        self.rendered_options = user_options.render()
        self.initial_global_defaults = None

    def __enter__(self: GlobalDefaultsContext) -> None:
        """Enter the context."""
        self.initial_global_defaults = global_options.GLOBAL_DEFAULT_OPTIONS
        set_global_defaults_rendered(self.rendered_options)

    def __exit__(
        self: GlobalDefaultsContext,
        exc_type: type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: TracebackType | None,
    ) -> None:
        """Exit the context."""
        set_global_defaults_rendered(self.initial_global_defaults)
