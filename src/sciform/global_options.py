"""Global Options."""

from sciform import modes
from sciform.rendered_options import RenderedOptions

PKG_DEFAULT_OPTIONS = RenderedOptions(
    exp_mode=modes.ExpModeEnum.FIXEDPOINT,
    exp_val=modes.AutoExpVal,
    round_mode=modes.RoundModeEnum.SIG_FIG,
    ndigits=modes.AutoDigits,
    upper_separator=modes.SeparatorEnum.NONE,
    decimal_separator=modes.SeparatorEnum.POINT,
    lower_separator=modes.SeparatorEnum.NONE,
    sign_mode=modes.SignModeEnum.NEGATIVE,
    left_pad_char=modes.LeftPadCharEnum.SPACE,
    left_pad_dec_place=0,
    exp_format=modes.ExpFormatEnum.STANDARD,
    extra_si_prefixes={},
    extra_iec_prefixes={},
    extra_parts_per_forms={},
    capitalize=False,
    superscript=False,
    nan_inf_exp=False,
    paren_uncertainty=False,
    pdg_sig_figs=False,
    left_pad_matching=False,
    paren_uncertainty_separators=True,
    pm_whitespace=True,
)


GLOBAL_DEFAULT_OPTIONS = PKG_DEFAULT_OPTIONS
