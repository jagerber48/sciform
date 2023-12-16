"""Global Options."""

from sciform import modes
from sciform.rendered_options import RenderedOptions

PKG_DEFAULT_OPTIONS = RenderedOptions(
    exp_mode=modes.ExpMode.FIXEDPOINT,
    exp_val=modes.AutoExpVal,
    round_mode=modes.RoundMode.SIG_FIG,
    ndigits=modes.AutoDigits,
    upper_separator=modes.Separator.NONE,
    decimal_separator=modes.Separator.POINT,
    lower_separator=modes.Separator.NONE,
    sign_mode=modes.SignMode.NEGATIVE,
    fill_mode=modes.FillMode.SPACE,
    top_dig_place=0,
    exp_format=modes.ExpFormat.STANDARD,
    extra_si_prefixes={},
    extra_iec_prefixes={},
    extra_parts_per_forms={},
    capitalize=False,
    superscript=False,
    latex=False,
    nan_inf_exp=False,
    bracket_unc=False,
    pdg_sig_figs=False,
    val_unc_match_widths=False,
    bracket_unc_remove_seps=False,
    unc_pm_whitespace=True,
)


GLOBAL_DEFAULT_OPTIONS = PKG_DEFAULT_OPTIONS
