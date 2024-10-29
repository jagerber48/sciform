"""Global Options."""

from sciform.options.populated_options import PopulatedOptions

PKG_DEFAULT_OPTIONS = PopulatedOptions(
    exp_mode="fixed_point",
    exp_val="auto",
    round_mode="all",
    ndigits=2,
    upper_separator="",
    decimal_separator=".",
    lower_separator="",
    sign_mode="-",
    left_pad_char=" ",
    left_pad_dec_place=0,
    exp_format="standard",
    extra_si_prefixes={},
    extra_iec_prefixes={},
    extra_parts_per_forms={},
    capitalize=False,
    superscript=False,
    nan_inf_exp=False,
    paren_uncertainty=False,
    left_pad_matching=False,
    paren_uncertainty_trim=True,
    pm_whitespace=True,
)


GLOBAL_DEFAULT_OPTIONS = PKG_DEFAULT_OPTIONS
