from typing import Union, get_args
from dataclasses import dataclass, asdict
from pprint import pprint

from sciform.modes import (FillMode, SignMode, GroupingSeparator,
                           UpperGroupingSeparators, LowerGroupingSeparators,
                           DecimalGroupingSeparators, RoundMode, ExpMode,
                           AutoExp, AutoPrec)


@dataclass(frozen=True)
class RenderedFormatOptions:
    exp_mode: ExpMode
    exp: Union[int, type(AutoExp)]
    percent: bool
    round_mode: RoundMode
    precision: Union[int, type(AutoPrec)]
    upper_separator: UpperGroupingSeparators
    decimal_separator: DecimalGroupingSeparators
    lower_separator: LowerGroupingSeparators
    sign_mode: SignMode
    fill_mode: FillMode
    top_dig_place: int
    prefix_exp: bool
    parts_per_exp: bool
    extra_si_prefixes: dict[int, str]
    extra_iec_prefixes: dict[int, str]
    extra_parts_per_forms: dict[int, str]
    capitalize: bool
    superscript_exp: bool
    latex: bool
    nan_inf_exp: bool
    bracket_unc: bool
    pdg_sig_figs: bool
    val_unc_match_widths: bool
    bracket_unc_remove_seps: bool
    unicode_pm: bool
    unc_pm_whitespace: bool


class Free:
    """
    Sentinel class indicating that a particular option in FormatOptions
    is unpopulated. `Free` instances will be replaced with global
    defaults upon rendering of FormatOptions into RenderedFormatOptions.
    """
    pass


def is_free(obj) -> bool:
    return isinstance(obj, Free)


def is_not_free(obj) -> bool:
    return not is_free(obj)


ExpReplaceDict = dict[int, Union[str, None]]


class FormatOptions:
    def __init__(
            self,
            *,
            template: Union['FormatOptions', RenderedFormatOptions] = None,
            exp_mode: Union[ExpMode, Free] = Free(),
            exp: Union[int, type(AutoExp), Free] = Free(),
            percent: Union[bool, Free] = Free(),
            round_mode: Union[RoundMode, Free] = Free(),
            precision: Union[int, type(AutoPrec), Free] = Free(),
            upper_separator: Union[UpperGroupingSeparators, Free] = Free(),
            decimal_separator: Union[DecimalGroupingSeparators, Free] = Free(),
            lower_separator: Union[LowerGroupingSeparators, Free] = Free(),
            sign_mode: Union[SignMode, Free] = Free(),
            fill_mode: Union[FillMode, Free] = Free(),
            top_dig_place: Union[int, Free] = Free(),
            prefix_exp: Union[bool, Free] = Free(),
            parts_per_exp: Union[bool, Free] = Free(),
            extra_si_prefixes: Union[ExpReplaceDict, Free] = Free(),
            extra_iec_prefixes: Union[ExpReplaceDict, Free] = Free(),
            extra_parts_per_forms: Union[ExpReplaceDict, Free] = Free(),
            capitalize: Union[bool, Free] = Free(),
            superscript_exp: Union[bool, Free] = Free(),
            latex: Union[bool, Free] = Free(),
            nan_inf_exp: Union[bool, Free] = Free(),
            bracket_unc: Union[bool, Free] = Free(),
            pdg_sig_figs: Union[bool, Free] = Free(),
            val_unc_match_widths: Union[bool, Free] = Free(),
            bracket_unc_remove_seps: Union[bool, Free] = Free(),
            unicode_pm: Union[bool, Free] = Free(),
            unc_pm_whitespace: Union[bool, Free] = Free(),
            add_c_prefix: bool = False,
            add_small_si_prefixes: bool = False,
            add_ppth_form: bool = False
    ):
        if round_mode is RoundMode.SIG_FIG:
            if isinstance(precision, int):
                if precision < 1:
                    raise ValueError(f'Precision must be >= 1 for sig fig '
                                     f'rounding, not {precision}.')

        if not isinstance(exp, (AutoExp, Free)):
            if exp_mode is ExpMode.FIXEDPOINT:
                if exp != 0:
                    raise ValueError(f'Exponent must must be 0, not '
                                     f'exp={exp}, for fixed point exponent '
                                     f'mode.')
            elif (exp_mode is ExpMode.ENGINEERING
                  or exp_mode is ExpMode.ENGINEERING_SHIFTED):
                if exp % 3 != 0:
                    raise ValueError(f'Exponent must be a multiple of 3, not '
                                     f'exp={exp}, for engineering exponent '
                                     f'modes.')
            elif exp_mode is ExpMode.BINARY_IEC:
                if exp % 10 != 0:
                    raise ValueError(f'Exponent must be a multiple of 10, not '
                                     f'exp={exp}, for binary IEC '
                                     f'exponent mode.')

        if not is_free(upper_separator):
            if upper_separator not in get_args(UpperGroupingSeparators):
                raise ValueError(f'upper_separator must be in '
                                 f'{get_args(UpperGroupingSeparators)}, not '
                                 f'{upper_separator}.')
            if upper_separator is decimal_separator:
                raise ValueError(f'upper_separator and decimal_separator '
                                 f'({upper_separator}) cannot be equal.')

        if not is_free(decimal_separator):
            if decimal_separator not in get_args(DecimalGroupingSeparators):
                raise ValueError(f'upper_separator must be in '
                                 f'{get_args(DecimalGroupingSeparators)}, not '
                                 f'{upper_separator}.')

        if not is_free(lower_separator):
            if lower_separator not in get_args(LowerGroupingSeparators):
                raise ValueError(f'upper_separator must be in '
                                 f'{get_args(LowerGroupingSeparators)}, not '
                                 f'{upper_separator}.')

        if not is_free(prefix_exp) and not is_free(parts_per_exp):
            if prefix_exp and parts_per_exp:
                raise ValueError('Only one of prefix exponent and parts-per '
                                 'exponent modes may be selected.')

        if add_c_prefix:
            if is_free(extra_si_prefixes):
                extra_si_prefixes = dict()
            if -2 not in extra_si_prefixes:
                extra_si_prefixes[-2] = 'c'

        if add_small_si_prefixes:
            if is_free(extra_si_prefixes):
                extra_si_prefixes = dict()
            if -2 not in extra_si_prefixes:
                extra_si_prefixes[-2] = 'c'
            if -1 not in extra_si_prefixes:
                extra_si_prefixes[-1] = 'd'
            if +1 not in extra_si_prefixes:
                extra_si_prefixes[+1] = 'da'
            if +2 not in extra_si_prefixes:
                extra_si_prefixes[+2] = 'h'

        if add_ppth_form:
            if is_free(extra_parts_per_forms):
                extra_parts_per_forms = dict()
            if -3 not in extra_parts_per_forms:
                extra_parts_per_forms[-3] = 'ppth'

        if template is None:
            self.exp_mode = exp_mode
            self.exp = exp
            self.percent = percent
            self.round_mode = round_mode
            self.precision = precision
            self.upper_separator = upper_separator
            self.decimal_separator = decimal_separator
            self.lower_separator = lower_separator
            self.sign_mode = sign_mode
            self.fill_mode = fill_mode
            self.top_dig_place = top_dig_place
            self.prefix_exp = prefix_exp
            self.parts_per_exp = parts_per_exp
            self.extra_si_prefixes = extra_si_prefixes
            self.extra_iec_prefixes = extra_iec_prefixes
            self.extra_parts_per_forms = extra_parts_per_forms
            self.capitalize = capitalize
            self.superscript_exp = superscript_exp
            self.latex = latex
            self.nan_inf_exp = nan_inf_exp
            self.bracket_unc = bracket_unc
            self.pdg_sig_figs = pdg_sig_figs
            self.val_unc_match_widths = val_unc_match_widths
            self.bracket_unc_remove_seps = bracket_unc_remove_seps
            self.unicode_pm = unicode_pm
            self.unc_pm_whitespace = unc_pm_whitespace
        else:
            self.exp_mode = (template.exp_mode if is_free(exp_mode) else exp_mode)
            self.exp = template.exp if is_free(exp) else exp
            self.percent = template.percent if is_free(percent) else percent
            self.round_mode = template.round_mode if is_free(round_mode) else round_mode
            self.precision = template.precision if is_free(precision) else precision
            self.upper_separator = template.upper_separator if is_free(upper_separator) else upper_separator
            self.decimal_separator = template.decimal_separator if is_free(decimal_separator) else decimal_separator
            self.lower_separator = template.lower_separator if is_free(lower_separator) else lower_separator
            self.sign_mode = template.sign_mode if is_free(sign_mode) else sign_mode
            self.fill_mode = template.fill_mode if is_free(fill_mode) else fill_mode
            self.top_dig_place = template.top_dig_place if is_free(top_dig_place) else top_dig_place
            self.prefix_exp = template.prefix_exp if is_free(prefix_exp) else prefix_exp
            self.parts_per_exp = template.parts_per_exp if is_free(parts_per_exp) else parts_per_exp
            self.extra_si_prefixes = template.extra_si_prefixes if is_free(extra_si_prefixes) else extra_si_prefixes
            self.extra_iec_prefixes = template.extra_iec_prefixes if is_free(extra_iec_prefixes) else extra_iec_prefixes
            self.extra_parts_per_forms = template.extra_parts_per_forms if is_free(extra_parts_per_forms) else extra_parts_per_forms
            self.capitalize = template.capitalize if is_free(capitalize) else capitalize
            self.superscript_exp = template.superscript_exp if is_free(superscript_exp) else superscript_exp
            self.latex = template.latex if is_free(latex) else latex
            self.nan_inf_exp = template.nan_inf_exp if is_free(nan_inf_exp) else nan_inf_exp
            self.bracket_unc = template.bracket_unc if is_free(bracket_unc) else bracket_unc
            self.pdg_sig_figs = template.pdg_sig_figs if is_free(pdg_sig_figs) else pdg_sig_figs
            self.val_unc_match_widths = template.val_unc_match_widths if is_free(val_unc_match_widths) else val_unc_match_widths
            self.bracket_unc_remove_seps = template.bracket_unc_remove_seps if is_free(bracket_unc_remove_seps) else bracket_unc_remove_seps
            self.unicode_pm = template.unicode_pm if is_free(unicode_pm) else unicode_pm
            self.unc_pm_whitespace = template.unc_pm_whitespace if is_free(unc_pm_whitespace) else unc_pm_whitespace

    def render(self) -> RenderedFormatOptions:
        gdf = get_global_defaults()
        rendered_format_options = RenderedFormatOptions(
          exp_mode=gdf.exp_mode if is_free(self.exp_mode) else self.exp_mode,
          exp=gdf.exp if is_free(self.exp) else self.exp,
          percent=gdf.percent if is_free(self.percent) else self.percent,
          round_mode=gdf.round_mode if is_free(self.round_mode) else self.round_mode,
          precision=gdf.precision if is_free(self.precision) else self.precision,
          upper_separator=gdf.upper_separator if is_free(self.upper_separator) else self.upper_separator,
          decimal_separator=gdf.decimal_separator if is_free(self.decimal_separator) else self.decimal_separator,
          lower_separator=gdf.lower_separator if is_free(self.lower_separator) else self.lower_separator,
          sign_mode=gdf.sign_mode if is_free(self.sign_mode) else self.sign_mode,
          fill_mode=gdf.fill_mode if is_free(self.fill_mode) else self.fill_mode,
          top_dig_place=gdf.top_dig_place if is_free(self.top_dig_place) else self.top_dig_place,
          prefix_exp=gdf.prefix_exp if is_free(self.prefix_exp) else self.prefix_exp,
          parts_per_exp=gdf.parts_per_exp if is_free(self.parts_per_exp) else self.parts_per_exp,
          extra_si_prefixes=gdf.extra_si_prefixes if is_free(self.extra_si_prefixes) else self.extra_si_prefixes,
          extra_iec_prefixes=gdf.extra_iec_prefixes if is_free(self.extra_iec_prefixes) else self.extra_iec_prefixes,
          extra_parts_per_forms=gdf.extra_parts_per_forms if is_free(self.extra_parts_per_forms) else self.extra_parts_per_forms,
          capitalize=gdf.capitalize if is_free(self.capitalize) else self.capitalize,
          superscript_exp=gdf.superscript_exp if is_free(self.superscript_exp) else self.superscript_exp,
          latex=gdf.latex if is_free(self.latex) else self.latex,
          nan_inf_exp=gdf.nan_inf_exp if is_free(self.nan_inf_exp) else self.nan_inf_exp,
          bracket_unc=gdf.bracket_unc if is_free(self.bracket_unc) else self.bracket_unc,
          pdg_sig_figs=gdf.pdg_sig_figs if is_free(self.pdg_sig_figs) else self.pdg_sig_figs,
          val_unc_match_widths=gdf.val_unc_match_widths if is_free(self.val_unc_match_widths) else self.val_unc_match_widths,
          bracket_unc_remove_seps=gdf.bracket_unc_remove_seps if is_free(self.bracket_unc_remove_seps) else self.bracket_unc_remove_seps,
          unicode_pm=gdf.unicode_pm if is_free(self.unicode_pm) else self.unicode_pm,
          unc_pm_whitespace=gdf.unc_pm_whitespace if is_free(self.unc_pm_whitespace) else self.unc_pm_whitespace
        )
        return rendered_format_options


DEFAULT_PKG_OPTIONS = RenderedFormatOptions(
    exp_mode=ExpMode.FIXEDPOINT,
    exp=AutoExp,
    percent=False,
    round_mode=RoundMode.SIG_FIG,
    precision=AutoPrec,
    upper_separator=GroupingSeparator.NONE,
    decimal_separator=GroupingSeparator.POINT,
    lower_separator=GroupingSeparator.NONE,
    sign_mode=SignMode.NEGATIVE,
    fill_mode=FillMode.SPACE,
    top_dig_place=0,
    prefix_exp=False,
    parts_per_exp=False,
    extra_si_prefixes=dict(),
    extra_iec_prefixes=dict(),
    extra_parts_per_forms=dict(),
    capitalize=False,
    superscript_exp=False,
    latex=False,
    nan_inf_exp=False,
    bracket_unc=False,
    pdg_sig_figs=False,
    val_unc_match_widths=False,
    bracket_unc_remove_seps=False,
    unicode_pm=False,
    unc_pm_whitespace=True
)


GLOBAL_DEFAULT_OPTIONS = DEFAULT_PKG_OPTIONS


def get_global_defaults() -> RenderedFormatOptions:
    return GLOBAL_DEFAULT_OPTIONS


def print_global_defaults():
    """
    Print current global default formatting options as a dictionary.
    """
    pprint(asdict(get_global_defaults()), sort_dicts=False)


def set_global_defaults(format_options: FormatOptions):
    global GLOBAL_DEFAULT_OPTIONS
    GLOBAL_DEFAULT_OPTIONS = format_options.render()


def reset_global_defaults():
    """
    Reset global default options to package defaults.
    """
    global GLOBAL_DEFAULT_OPTIONS
    GLOBAL_DEFAULT_OPTIONS = DEFAULT_PKG_OPTIONS


def global_add_c_prefix():
    """
    Include ``c`` as a prefix for the exponent value -2. Has no effect
    if exponent value -2 is already mapped to a prefix string. To modify
    this mapping, first use :func:`global_reset_si_prefixes` or
    use :func:`set_global_defaults`.
    """
    set_global_defaults(FormatOptions(add_c_prefix=True))


def global_add_small_si_prefixes():
    """
    Include ``{-2: 'c', -1: 'd', +1: 'da', +2: 'h'}`` as prefix
    substitutions. Note, if any of these exponent values are mapped,
    then that mapping will NOT be overwritten. To modify existing
    mappings either first use :func:`global_reset_si_prefixes` or use
    :func:`set_global_defaults`.
    """
    set_global_defaults(FormatOptions(add_small_si_prefixes=True))


def global_add_ppth_form():
    """
    Include ``ppth`` as a "parts-per" form for the exponent value -3.
    Has no effect if exponent value -3 is already mapped to a
    "parts-per" format string. To modify this mapping, first use
    :func:`global_reset_parts_per_forms` or use
    :func:`set_global_defaults`.
    """
    set_global_defaults(FormatOptions(add_ppth_form=True))


def global_reset_si_prefixes():
    """
    Clear all extra SI prefix mappings.
    """
    set_global_defaults(FormatOptions(extra_si_prefixes=dict()))


def global_reset_iec_prefixes():
    """
    Clear all extra IEC prefix mappings.
    """
    set_global_defaults(FormatOptions(extra_iec_prefixes=dict()))


def global_reset_parts_per_forms():
    """
    Clear all extra "parts-per" forms.
    """
    set_global_defaults(FormatOptions(extra_parts_per_forms=dict()))


class GlobalDefaultsContext:
    """
    Temporarily update global default options. New settings are applied
    when the context is entered and original global settings are
    re-applied when the context is exited.
    """
    def __init__(self, format_options: FormatOptions):
        self.format_options = format_options
        self.initial_global_defaults = None

    def __enter__(self):
        global GLOBAL_DEFAULT_OPTIONS
        self.initial_global_defaults = GLOBAL_DEFAULT_OPTIONS
        GLOBAL_DEFAULT_OPTIONS = self.format_options.render()

    def __exit__(self, exc_type, exc_value, exc_tb):
        global GLOBAL_DEFAULT_OPTIONS
        GLOBAL_DEFAULT_OPTIONS = self.initial_global_defaults
