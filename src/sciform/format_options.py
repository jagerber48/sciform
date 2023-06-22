from typing import Union, Optional, get_args
from dataclasses import dataclass, asdict
import re
from copy import copy
from pprint import pprint

from sciform.modes import (FillMode, SignMode, GroupingSeparator,
                           UpperGroupingSeparators, LowerGroupingSeparators,
                           DecimalGroupingSeparators, RoundMode, ExpMode,
                           AutoExp, AutoPrec)


@dataclass(frozen=True)
class FormatOptions:
    fill_mode: FillMode
    sign_mode: SignMode
    top_dig_place: int
    upper_separator: UpperGroupingSeparators
    decimal_separator: DecimalGroupingSeparators
    lower_separator: LowerGroupingSeparators
    round_mode: RoundMode
    precision: Union[int, type(AutoPrec)]
    exp_mode: ExpMode
    exp: Union[int, type(AutoExp)]
    capitalize: bool
    percent: bool
    superscript_exp: bool
    latex: bool
    nan_inf_exp: bool
    prefix_exp: bool
    parts_per_exp: bool
    extra_si_prefixes: dict[int, str]
    extra_iec_prefixes: dict[int, str]
    extra_parts_per_forms: dict[int, str]
    pdg_sig_figs: bool
    bracket_unc: bool
    val_unc_match_widths: bool
    bracket_unc_remove_seps: bool
    unicode_pm: bool
    unc_pm_whitespace: bool

    def __post_init__(self):
        if self.round_mode is RoundMode.SIG_FIG:
            if isinstance(self.precision, int):
                if self.precision < 1:
                    raise ValueError(f'Precision must be >= 1 for sig fig '
                                     f'rounding, not {self.precision}.')

        if self.exp is not AutoExp:
            if self.exp_mode is ExpMode.FIXEDPOINT:
                if self.exp != 0:
                    raise ValueError(f'Exponent must must be 0, not '
                                     f'exp={self.exp}, for fixed point'
                                     f'exponent mode.')
            elif (self.exp_mode is ExpMode.ENGINEERING
                  or self.exp_mode is ExpMode.ENGINEERING_SHIFTED):
                if self.exp % 3 != 0:
                    raise ValueError(f'Exponent must be a multiple of 3, not '
                                     f'exp={self.exp}, for engineering '
                                     f'exponent modes.')
            elif self.exp_mode is ExpMode.BINARY_IEC:
                if self.exp % 10 != 0:
                    raise ValueError(f'Exponent must be a multiple of 10, not '
                                     f'exp={self.exp}, for binary IEC '
                                     f'exponent mode.')

        if self.percent and self.exp_mode is not ExpMode.FIXEDPOINT:
            raise ValueError(f'percent mode can only be sued with fixed point '
                             f'exponent mode.')

        if self.upper_separator not in get_args(UpperGroupingSeparators):
            raise ValueError(f'upper_separator {self.upper_separator} not in '
                             f'{get_args(UpperGroupingSeparators)}.')

        if self.decimal_separator not in get_args(DecimalGroupingSeparators):
            raise ValueError(f'decimal_separator {self.upper_separator} not '
                             f'in {get_args(DecimalGroupingSeparators)}.')

        if self.lower_separator not in get_args(LowerGroupingSeparators):
            raise ValueError(f'lower_separator {self.lower_separator} not in '
                             f'{get_args(LowerGroupingSeparators)}.')

        if self.upper_separator is self.decimal_separator:
            raise ValueError(f'upper_separator and decimal_separator '
                             f'{self.upper_separator} cannot be equal.')

        if self.prefix_exp and self.parts_per_exp:
            raise ValueError(f'Only one of prefix exponent and parts-per '
                             f'exponent modes may be selected.')

    @classmethod
    def make(
            cls,
            *,
            defaults: 'FormatOptions' = None,
            fill_mode: FillMode = None,
            sign_mode: SignMode = None,
            top_dig_place: int = None,
            upper_separator: UpperGroupingSeparators = None,
            decimal_separator: DecimalGroupingSeparators = None,
            lower_separator: LowerGroupingSeparators = None,
            round_mode: RoundMode = None,
            precision: Union[int, type(AutoPrec)] = None,
            exp_mode: ExpMode = None,
            exp: Union[int, type(AutoExp)] = None,
            capitalize: bool = None,
            percent: bool = None,
            superscript_exp: bool = None,
            latex: bool = None,
            nan_inf_exp: bool = None,
            prefix_exp: bool = None,
            parts_per_exp: bool = None,
            extra_si_prefixes: dict[int, str] = None,
            extra_iec_prefixes: dict[int, str] = None,
            extra_parts_per_forms: dict[int, str] = None,
            add_c_prefix: bool = False,
            add_small_si_prefixes: bool = False,
            add_ppth_form: bool = False,
            pdg_sig_figs: bool = None,
            bracket_unc: bool = None,
            val_unc_match_widths: bool = None,
            bracket_unc_remove_seps: bool = None,
            unicode_pm: bool = None,
            unc_pm_whitespace: bool = None
    ):
        if defaults is None:
            defaults = DEFAULT_GLOBAL_OPTIONS

        if fill_mode is None:
            fill_mode = defaults.fill_mode
        if sign_mode is None:
            sign_mode = defaults.sign_mode
        if top_dig_place is None:
            top_dig_place = defaults.top_dig_place
        if upper_separator is None:
            upper_separator = defaults.upper_separator
        if decimal_separator is None:
            decimal_separator = defaults.decimal_separator
        if lower_separator is None:
            lower_separator = defaults.lower_separator
        if round_mode is None:
            round_mode = defaults.round_mode
        if precision is None:
            precision = defaults.precision
        if exp_mode is None:
            exp_mode = defaults.exp_mode
        if exp is None:
            exp = defaults.exp
        if capitalize is None:
            capitalize = defaults.capitalize
        if percent is None:
            percent = defaults.percent
        if superscript_exp is None:
            superscript_exp = defaults.superscript_exp
        if latex is None:
            latex = defaults.latex
        if nan_inf_exp is None:
            nan_inf_exp = defaults.nan_inf_exp
        if prefix_exp is None:
            prefix_exp = defaults.prefix_exp
        if parts_per_exp is None:
            parts_per_exp = defaults.parts_per_exp
        if extra_si_prefixes is None:
            extra_si_prefixes = copy(defaults.extra_si_prefixes)
        else:
            extra_si_prefixes = copy(extra_si_prefixes)
        if extra_iec_prefixes is None:
            extra_iec_prefixes = copy(defaults.extra_iec_prefixes)
        else:
            extra_iec_prefixes = copy(extra_iec_prefixes)
        if extra_parts_per_forms is None:
            extra_parts_per_forms = copy(defaults.extra_parts_per_forms)
        else:
            extra_parts_per_forms = copy(extra_parts_per_forms)
        if pdg_sig_figs is None:
            pdg_sig_figs = defaults.pdg_sig_figs
        if bracket_unc is None:
            bracket_unc = defaults.bracket_unc
        if val_unc_match_widths is None:
            val_unc_match_widths = defaults.val_unc_match_widths
        if bracket_unc_remove_seps is None:
            bracket_unc_remove_seps = defaults.bracket_unc_remove_seps
        if unicode_pm is None:
            unicode_pm = defaults.unicode_pm
        if unc_pm_whitespace is None:
            unc_pm_whitespace = defaults.unc_pm_whitespace

        if add_c_prefix and -2 not in extra_si_prefixes:
            extra_si_prefixes[-2] = 'c'

        if add_small_si_prefixes:
            if -2 not in extra_si_prefixes:
                extra_si_prefixes[-2] = 'c'
            if -1 not in extra_si_prefixes:
                extra_si_prefixes[-1] = 'd'
            if +1 not in extra_si_prefixes:
                extra_si_prefixes[+1] = 'da'
            if +2 not in extra_si_prefixes:
                extra_si_prefixes[+2] = 'h'

        if add_ppth_form:
            if -3 not in extra_parts_per_forms:
                extra_parts_per_forms[-3] = 'ppth'

        return cls(
            fill_mode=fill_mode,
            sign_mode=sign_mode,
            top_dig_place=top_dig_place,
            upper_separator=upper_separator,
            decimal_separator=decimal_separator,
            lower_separator=lower_separator,
            round_mode=round_mode,
            precision=precision,
            exp_mode=exp_mode,
            exp=exp,
            capitalize=capitalize,
            percent=percent,
            superscript_exp=superscript_exp,
            latex=latex,
            nan_inf_exp=nan_inf_exp,
            prefix_exp=prefix_exp,
            parts_per_exp=parts_per_exp,
            extra_si_prefixes=extra_si_prefixes,
            extra_iec_prefixes=extra_iec_prefixes,
            extra_parts_per_forms=extra_parts_per_forms,
            pdg_sig_figs=pdg_sig_figs,
            bracket_unc=bracket_unc,
            val_unc_match_widths=val_unc_match_widths,
            bracket_unc_remove_seps=bracket_unc_remove_seps,
            unicode_pm=unicode_pm,
            unc_pm_whitespace=unc_pm_whitespace
        )

# TODO: fix prefix_mode lower case but bracket_unc upper case. reconsider
#   letter for bracket_unc?
    pattern = re.compile(r'''^
                             (?:(?P<fill_mode>[ 0])=)?
                             (?P<sign_mode>[-+ ])?
                             (?P<alternate_mode>\#)?                         
                             (?P<top_dig_place>\d+)?
                             (?P<upper_separator>[n,.s_])?                     
                             (?P<decimal_separator>[.,])?            
                             (?P<lower_separator>[ns_])?                  
                             (?:(?P<round_mode>[.!])(?P<prec>[+-]?\d+))?
                             (?P<exp_mode>[fF%eErRbB])?
                             (?:x(?P<exp>[+-]?\d+))?
                             (?P<prefix_mode>p)?
                             (?P<bracket_unc>\(\))?
                             $''', re.VERBOSE)

    fill_mode_mapping = {' ': FillMode.SPACE,
                         '0': FillMode.ZERO,
                         None: None}

    sign_mode_mapping = {'-': SignMode.NEGATIVE,
                         '+': SignMode.ALWAYS,
                         ' ': SignMode.SPACE,
                         None: None}

    separator_mapping = {'n': GroupingSeparator.NONE,
                         ',': GroupingSeparator.COMMA,
                         '.': GroupingSeparator.POINT,
                         's': GroupingSeparator.SPACE,
                         '_': GroupingSeparator.UNDERSCORE,
                         None: None}

    round_mode_mapping = {'!': RoundMode.SIG_FIG,
                          '.': RoundMode.PREC,
                          None: None}

    @classmethod
    def from_format_spec_str(
            cls,
            fmt: str,
            defaults: Optional['FormatOptions'] = None) -> 'FormatOptions':

        match = cls.pattern.match(fmt)
        if match is None:
            raise ValueError(f'Invalid format specifier: \'{fmt}\'')

        fill_mode_flag = match.group('fill_mode')
        fill_mode = cls.fill_mode_mapping[fill_mode_flag]

        sign_mode_flag = match.group('sign_mode')
        sign_mode = cls.sign_mode_mapping[sign_mode_flag]

        alternate_mode = match.group('alternate_mode')
        if alternate_mode is not None:
            alternate_mode = True

        top_dig_place = match.group('top_dig_place')
        if top_dig_place is not None:
            top_dig_place = int(top_dig_place)
            val_unc_match_widths = True
        else:
            val_unc_match_widths = None

        upper_separator_flag = match.group('upper_separator')
        upper_separator = cls.separator_mapping[upper_separator_flag]

        decimal_separator_flag = match.group('decimal_separator')
        decimal_separator = cls.separator_mapping[decimal_separator_flag]

        lower_separator_flag = match.group('lower_separator')
        lower_separator = cls.separator_mapping[lower_separator_flag]

        round_mode_flag = match.group('round_mode')
        round_mode = cls.round_mode_mapping[round_mode_flag]

        precision = match.group('prec')
        if precision is not None:
            precision = int(precision)

        exp_mode = match.group('exp_mode')
        percent = False
        if exp_mode is not None:
            capitalize = exp_mode.isupper()
            if exp_mode in ['f', 'F']:
                exp_mode = ExpMode.FIXEDPOINT
            elif exp_mode == '%':
                exp_mode = ExpMode.FIXEDPOINT
                percent = True
            elif exp_mode in ['e', 'E']:
                exp_mode = ExpMode.SCIENTIFIC
            elif exp_mode in ['r', 'R']:
                if alternate_mode:
                    exp_mode = ExpMode.ENGINEERING_SHIFTED
                else:
                    exp_mode = ExpMode.ENGINEERING
            elif exp_mode in ['b', 'B']:
                if alternate_mode:
                    exp_mode = ExpMode.BINARY_IEC
                else:
                    exp_mode = ExpMode.BINARY
        else:
            capitalize = None

        exp = match.group('exp')
        if exp is not None:
            exp = int(exp)

        prefix_exp = match.group('prefix_mode')
        if prefix_exp is not None:
            prefix_exp = True

        bracket_unc = match.group('bracket_unc')
        if bracket_unc is not None:
            bracket_unc = True

        if defaults is None:
            defaults = DEFAULT_GLOBAL_OPTIONS

        return cls.make(
            defaults=defaults,
            fill_mode=fill_mode,
            sign_mode=sign_mode,
            top_dig_place=top_dig_place,
            upper_separator=upper_separator,
            decimal_separator=decimal_separator,
            lower_separator=lower_separator,
            round_mode=round_mode,
            precision=precision,
            exp_mode=exp_mode,
            exp=exp,
            capitalize=capitalize,
            percent=percent,
            prefix_exp=prefix_exp,
            bracket_unc=bracket_unc,
            val_unc_match_widths=val_unc_match_widths
        )


DEFAULT_PKG_OPTIONS = FormatOptions(
    fill_mode=FillMode.SPACE,
    sign_mode=SignMode.NEGATIVE,
    top_dig_place=0,
    upper_separator=GroupingSeparator.NONE,
    decimal_separator=GroupingSeparator.POINT,
    lower_separator=GroupingSeparator.NONE,
    round_mode=RoundMode.SIG_FIG,
    precision=AutoPrec,
    exp_mode=ExpMode.FIXEDPOINT,
    exp=AutoExp,
    capitalize=False,
    percent=False,
    superscript_exp=False,
    latex=False,
    nan_inf_exp=False,
    prefix_exp=False,
    parts_per_exp=False,
    extra_si_prefixes=dict(),
    extra_iec_prefixes=dict(),
    extra_parts_per_forms=dict(),
    pdg_sig_figs=False,
    bracket_unc=False,
    val_unc_match_widths=False,
    bracket_unc_remove_seps=False,
    unicode_pm=False,
    unc_pm_whitespace=True
)

DEFAULT_GLOBAL_OPTIONS = FormatOptions.make(
    defaults=DEFAULT_PKG_OPTIONS)


def get_global_defaults() -> FormatOptions:
    return DEFAULT_GLOBAL_OPTIONS


def print_global_defaults():
    """
    Print current global default formatting options as a dictionary.
    """
    pprint(asdict(get_global_defaults()), sort_dicts=False)


def set_global_defaults(
        *,
        defaults: 'FormatOptions' = None,
        fill_mode: FillMode = None,
        sign_mode: SignMode = None,
        top_dig_place: int = None,
        upper_separator: UpperGroupingSeparators = None,
        decimal_separator: DecimalGroupingSeparators = None,
        lower_separator: LowerGroupingSeparators = None,
        round_mode: RoundMode = None,
        precision: Union[int, type(AutoPrec)] = None,
        exp_mode: ExpMode = None,
        exp: Union[int, type(AutoExp)] = None,
        capitalize: bool = None,
        percent: bool = None,
        superscript_exp: bool = None,
        latex: bool = None,
        nan_inf_exp=None,
        prefix_exp: bool = None,
        parts_per_exp: bool = None,
        extra_si_prefixes: dict[int, str] = None,
        extra_iec_prefixes: dict[int, str] = None,
        extra_parts_per_forms: dict[int, str] = None,
        add_c_prefix: bool = False,
        add_small_si_prefixes: bool = False,
        add_ppth_form: bool = False,
        pdg_sig_figs: bool = None,
        bracket_unc=None,
        val_unc_match_widths=None,
        bracket_unc_remove_seps=None,
        unicode_pm=None,
        unc_pm_whitespace=None
):
    """
    Update global default options. Accepts the same input keyword
    arguments as :class:`Formatter` and undergoes the same input
    validation. Any unspecified parameters retain their existing
    global settings.
    """
    global DEFAULT_GLOBAL_OPTIONS
    if defaults is None:
        defaults = DEFAULT_GLOBAL_OPTIONS
    new_default_options = FormatOptions.make(
        defaults=defaults,
        fill_mode=fill_mode,
        sign_mode=sign_mode,
        top_dig_place=top_dig_place,
        upper_separator=upper_separator,
        decimal_separator=decimal_separator,
        lower_separator=lower_separator,
        round_mode=round_mode,
        precision=precision,
        exp_mode=exp_mode,
        exp=exp,
        capitalize=capitalize,
        percent=percent,
        superscript_exp=superscript_exp,
        latex=latex,
        nan_inf_exp=nan_inf_exp,
        prefix_exp=prefix_exp,
        parts_per_exp=parts_per_exp,
        extra_si_prefixes=extra_si_prefixes,
        extra_iec_prefixes=extra_iec_prefixes,
        extra_parts_per_forms=extra_parts_per_forms,
        add_c_prefix=add_c_prefix,
        add_small_si_prefixes=add_small_si_prefixes,
        add_ppth_form=add_ppth_form,
        pdg_sig_figs=pdg_sig_figs,
        bracket_unc=bracket_unc,
        val_unc_match_widths=val_unc_match_widths,
        bracket_unc_remove_seps=bracket_unc_remove_seps,
        unicode_pm=unicode_pm,
        unc_pm_whitespace=unc_pm_whitespace
    )
    DEFAULT_GLOBAL_OPTIONS = new_default_options


def reset_global_defaults():
    """
    Reset global default options to package defaults.
    """
    global DEFAULT_GLOBAL_OPTIONS
    DEFAULT_GLOBAL_OPTIONS = DEFAULT_PKG_OPTIONS


def global_add_c_prefix():
    """
    Include 'c' as a prefix for the exponent value -2. Has no effect if
    exponent value -2 is already mapped to a prefix string. To modify
    this mapping, first use :func:`global_reset_si_prefixes` or
    use :func:`set_global_defaults`.
    """
    set_global_defaults(add_c_prefix=True)


def global_add_small_si_prefixes():
    """
    Include {-2: 'c', -1: 'd', +1: 'da', +2: 'h'} exponnet value to
    prefix subsitutions. Note, if any of these exponent values are
    mapped then that mapping will NOT be overwritten. To modify existing
    mappings either first use :func:`global_reset_si_prefixes` or use
    :func:`set_global_defaults`.
    """
    set_global_defaults(add_small_si_prefixes=True)


def global_add_ppth_form():
    """
    Include 'ppth' as a "parts-per" form for the exponent value -3.
    Has no effect if exponent value -3 is already mapped to a
    "parts-per" form string. To modify this mapping, first use
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
    Temporarily update global default options. Accepts the same input
    keyword arguments as :class:`Formatter` and undergoes the same input
    validation. Any unspecified parameters retain their existing
    global settings. New settings are applied when the context is
    entered and original global settings are re-applied when the context
    is exited.
    """
    def __init__(
            self,
            *,
            defaults: 'FormatOptions' = None,
            fill_mode: FillMode = None,
            sign_mode: SignMode = None,
            top_dig_place: int = None,
            upper_separator: UpperGroupingSeparators = None,
            decimal_separator: DecimalGroupingSeparators = None,
            lower_separator: LowerGroupingSeparators = None,
            round_mode: RoundMode = None,
            precision: Union[int, type(AutoPrec)] = None,
            exp_mode: ExpMode = None,
            exp: Union[int, type(AutoExp)] = None,
            capitalize: bool = None,
            percent: bool = None,
            superscript_exp: bool = None,
            latex: bool = None,
            nan_inf_exp: bool = None,
            prefix_exp: bool = None,
            parts_per_exp: bool = None,
            extra_si_prefixes: dict[int, str] = None,
            extra_iec_prefixes: dict[int, str] = None,
            extra_parts_per_forms: dict[int, str] = None,
            add_c_prefix: bool = False,
            add_small_si_prefixes: bool = False,
            add_ppth_form: bool = False,
            pdg_sig_figs: bool = None,
            bracket_unc: bool = None,
            val_unc_match_widths: bool = None,
            bracket_unc_remove_seps: bool = None,
            unicode_pm: bool = None,
            unc_pm_whitespace: bool = None
    ):
        self.options = FormatOptions.make(
            defaults=defaults,
            fill_mode=fill_mode,
            sign_mode=sign_mode,
            top_dig_place=top_dig_place,
            upper_separator=upper_separator,
            decimal_separator=decimal_separator,
            lower_separator=lower_separator,
            round_mode=round_mode,
            precision=precision,
            exp_mode=exp_mode,
            exp=exp,
            capitalize=capitalize,
            percent=percent,
            superscript_exp=superscript_exp,
            latex=latex,
            nan_inf_exp=nan_inf_exp,
            prefix_exp=prefix_exp,
            parts_per_exp=parts_per_exp,
            extra_si_prefixes=extra_si_prefixes,
            extra_iec_prefixes=extra_iec_prefixes,
            extra_parts_per_forms=extra_parts_per_forms,
            add_c_prefix=add_c_prefix,
            add_small_si_prefixes=add_small_si_prefixes,
            add_ppth_form=add_ppth_form,
            pdg_sig_figs=pdg_sig_figs,
            bracket_unc=bracket_unc,
            val_unc_match_widths=val_unc_match_widths,
            bracket_unc_remove_seps=bracket_unc_remove_seps,
            unicode_pm=unicode_pm,
            unc_pm_whitespace=unc_pm_whitespace
        )
        self.initial_global_defaults = None

    def __enter__(self):
        self.initial_global_defaults = get_global_defaults()
        set_global_defaults(defaults=self.options)

    def __exit__(self, exc_type, exc_value, exc_tb):
        set_global_defaults(defaults=self.initial_global_defaults)
