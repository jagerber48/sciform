from typing import Optional, Union
from sciform import global_options, modes
from sciform.user_options import UserOptions
from sciform.rendered_options import RenderedOptions


def print_global_defaults():
    """
    Print current global default formatting options as a dictionary.
    """
    print(str(global_options.GLOBAL_DEFAULT_OPTIONS))


def set_global_defaults(
            exp_mode: Optional[modes.UserExpMode] = None,
            exp_val: Optional[Union[int, type(modes.AutoExpVal)]] = None,
            round_mode: Optional[modes.UserRoundMode] = None,
            ndigits: Optional[Union[int, type(modes.AutoDigits)]] = None,
            upper_separator: Optional[modes.UserUpperSeparators] = None,
            decimal_separator: Optional[modes.UserDecimalSeparators] = None,
            lower_separator: Optional[modes.UserLowerSeparators] = None,
            sign_mode: Optional[modes.UserSignMode] = None,
            fill_mode: Optional[modes.UserFillMode] = None,
            top_dig_place: Optional[int] = None,
            exp_format: Optional[modes.UserExpFormat] = None,
            extra_si_prefixes: Optional[dict[int, str]] = None,
            extra_iec_prefixes: Optional[dict[int, str]] = None,
            extra_parts_per_forms: Optional[dict[int, str]] = None,
            capitalize: Optional[bool] = None,
            superscript_exp: Optional[bool] = None,
            latex: Optional[bool] = None,
            nan_inf_exp: Optional[bool] = None,
            bracket_unc: Optional[bool] = None,
            pdg_sig_figs: Optional[bool] = None,
            val_unc_match_widths: Optional[bool] = None,
            bracket_unc_remove_seps: Optional[bool] = None,
            unc_pm_whitespace: Optional[bool] = None,
            add_c_prefix: bool = False,
            add_small_si_prefixes: bool = False,
            add_ppth_form: bool = False,
):
    """
    Configure global default format options. Accepts the same keyword
    arguments as :class:`Formatter`.
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
        fill_mode=fill_mode,
        top_dig_place=top_dig_place,
        exp_format=exp_format,
        extra_si_prefixes=extra_si_prefixes,
        extra_iec_prefixes=extra_iec_prefixes,
        extra_parts_per_forms=extra_parts_per_forms,
        capitalize=capitalize,
        superscript_exp=superscript_exp,
        latex=latex,
        nan_inf_exp=nan_inf_exp,
        bracket_unc=bracket_unc,
        pdg_sig_figs=pdg_sig_figs,
        val_unc_match_widths=val_unc_match_widths,
        bracket_unc_remove_seps=bracket_unc_remove_seps,
        unc_pm_whitespace=unc_pm_whitespace,
        add_c_prefix=add_c_prefix,
        add_small_si_prefixes=add_small_si_prefixes,
        add_ppth_form=add_ppth_form
    )
    set_global_defaults_rendered(user_options.render())


def set_global_defaults_rendered(rendered_options: RenderedOptions):
    global_options.GLOBAL_DEFAULT_OPTIONS = rendered_options


def reset_global_defaults():
    """
    Reset global default options to :mod:`sciform` package defaults.
    """
    global_options.GLOBAL_DEFAULT_OPTIONS = global_options.PKG_DEFAULT_OPTIONS


# TODO: Need to clean up the semantics on add_c_prefix in both Formatter
#  and these global configuration options. Does it truly just add the
#  value to the dict if it's not present? Or does the whole dict get
#  overwritten? Are these helpers even needed? They're redundant with
#  set_global_defaults.
def global_add_c_prefix():
    """
    Include ``c`` as a prefix for the exponent value -2. Has no effect
    if exponent value -2 is already mapped to a prefix string. To modify
    this mapping, first use :func:`global_reset_si_prefixes` or
    use :func:`set_global_defaults`.
    """
    set_global_defaults(add_c_prefix=True)


def global_add_small_si_prefixes():
    """
    Include ``{-2: 'c', -1: 'd', +1: 'da', +2: 'h'}`` as prefix
    substitutions. Note, if any of these exponent values are mapped,
    then that mapping will NOT be overwritten. To modify existing
    mappings either first use :func:`global_reset_si_prefixes` or use
    :func:`set_global_defaults`.
    """
    set_global_defaults(add_small_si_prefixes=True)


def global_add_ppth_form():
    """
    Include ``ppth`` as a "parts-per" form for the exponent value -3.
    Has no effect if exponent value -3 is already mapped to a
    "parts-per" format string. To modify this mapping, first use
    :func:`global_reset_parts_per_forms` or use
    :func:`set_global_defaults`.
    """
    set_global_defaults(add_ppth_form=True)


def global_reset_si_prefixes():
    """
    Clear all extra SI prefix mappings.
    """
    set_global_defaults(extra_si_prefixes=dict())


def global_reset_iec_prefixes():
    """
    Clear all extra IEC prefix mappings.
    """
    set_global_defaults(extra_iec_prefixes=dict())


def global_reset_parts_per_forms():
    """
    Clear all extra "parts-per" forms.
    """
    set_global_defaults(extra_parts_per_forms=dict())


class GlobalDefaultsContext:
    """
    Temporarily update global default options. New settings are applied
    when the context is entered and original global settings are
    re-applied when the context is exited. Accepts the same keyword
    arguments as :class:`Formatter`.
    """
    def __init__(
            self,
            exp_mode: Optional[modes.UserExpMode] = None,
            exp_val: Optional[Union[int, type(modes.AutoExpVal)]] = None,
            round_mode: Optional[modes.UserRoundMode] = None,
            ndigits: Optional[Union[int, type(modes.AutoDigits)]] = None,
            upper_separator: Optional[modes.UserUpperSeparators] = None,
            decimal_separator: Optional[modes.UserDecimalSeparators] = None,
            lower_separator: Optional[modes.UserLowerSeparators] = None,
            sign_mode: Optional[modes.UserSignMode] = None,
            fill_mode: Optional[modes.UserFillMode] = None,
            top_dig_place: Optional[int] = None,
            exp_format: Optional[modes.UserExpFormat] = None,
            extra_si_prefixes: Optional[dict[int, str]] = None,
            extra_iec_prefixes: Optional[dict[int, str]] = None,
            extra_parts_per_forms: Optional[dict[int, str]] = None,
            capitalize: Optional[bool] = None,
            superscript_exp: Optional[bool] = None,
            latex: Optional[bool] = None,
            nan_inf_exp: Optional[bool] = None,
            bracket_unc: Optional[bool] = None,
            pdg_sig_figs: Optional[bool] = None,
            val_unc_match_widths: Optional[bool] = None,
            bracket_unc_remove_seps: Optional[bool] = None,
            unc_pm_whitespace: Optional[bool] = None,
            add_c_prefix: bool = False,
            add_small_si_prefixes: bool = False,
            add_ppth_form: bool = False,
    ):
        user_options = UserOptions(
            exp_mode=exp_mode,
            exp_val=exp_val,
            round_mode=round_mode,
            ndigits=ndigits,
            upper_separator=upper_separator,
            decimal_separator=decimal_separator,
            lower_separator=lower_separator,
            sign_mode=sign_mode,
            fill_mode=fill_mode,
            top_dig_place=top_dig_place,
            exp_format=exp_format,
            extra_si_prefixes=extra_si_prefixes,
            extra_iec_prefixes=extra_iec_prefixes,
            extra_parts_per_forms=extra_parts_per_forms,
            capitalize=capitalize,
            superscript_exp=superscript_exp,
            latex=latex,
            nan_inf_exp=nan_inf_exp,
            bracket_unc=bracket_unc,
            pdg_sig_figs=pdg_sig_figs,
            val_unc_match_widths=val_unc_match_widths,
            bracket_unc_remove_seps=bracket_unc_remove_seps,
            unc_pm_whitespace=unc_pm_whitespace,
            add_c_prefix=add_c_prefix,
            add_small_si_prefixes=add_small_si_prefixes,
            add_ppth_form=add_ppth_form
        )
        self.rendered_options = user_options.render()
        self.initial_global_defaults = None

    def __enter__(self):
        self.initial_global_defaults = global_options.GLOBAL_DEFAULT_OPTIONS
        set_global_defaults_rendered(self.rendered_options)

    def __exit__(self, exc_type, exc_value, exc_tb):
        set_global_defaults_rendered(self.initial_global_defaults)
