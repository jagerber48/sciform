from typing import Union, Optional, get_args
from dataclasses import dataclass, asdict
import re
from copy import copy
from pprint import pprint

from sciform.modes import (FillMode, SignMode, GroupingSeparator,
                           UpperGroupingSeparators, LowerGroupingSeparators,
                           DecimalGroupingSeparators, RoundMode, FormatMode,
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
    format_mode: FormatMode  # TODO: rename to exp_mode
    capitalize: bool
    exp: Union[int, type(AutoExp)]
    nan_inf_exp: bool
    use_prefix: bool
    extra_si_prefixes: dict[int, str]
    extra_iec_prefixes: dict[int, str]
    bracket_unc: bool
    val_unc_match_widths: bool
    bracket_unc_remove_seps: bool
    unc_pm_whitespace: bool

    def __post_init__(self):
        if self.round_mode is RoundMode.SIG_FIG:
            if isinstance(self.precision, int):
                if self.precision < 1:
                    raise ValueError(f'Precision must be >= 1 for sig fig '
                                     f'rounding, not {self.precision}.')

        if self.exp is not AutoExp:
            # TODO: Needs testing
            if (self.format_mode is FormatMode.FIXEDPOINT
                    or self.format_mode is FormatMode.PERCENT):
                if self.exp != 0:
                    raise ValueError(f'Exponent must must be 0, not '
                                     f'exp={self.exp}, for fixed point and '
                                     f'percent format modes.')
            elif (self.format_mode is FormatMode.ENGINEERING
                    or self.format_mode is FormatMode.ENGINEERING_SHIFTED):
                if self.exp % 3 != 0:
                    raise ValueError(f'Exponent must be a multiple of 3, not '
                                     f'exp={self.exp}, for engineering format '
                                     f'modes.')
            elif self.format_mode is FormatMode.BINARY_IEC:
                if self.exp % 10 != 0:
                    raise ValueError(f'Exponent must be a multiple of 10, not '
                                     f'exp={self.exp}, for binary IEC format'
                                     f'mode.')

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
            format_mode: FormatMode = None,
            capitalize: bool = None,
            exp: Union[int, type(AutoExp)] = None,
            nan_inf_exp: bool = None,
            use_prefix: bool = None,
            extra_si_prefixes: dict[int, str] = None,
            extra_iec_prefixes: dict[int, str] = None,
            add_c_prefix: bool = False,
            add_small_si_prefixes: bool = False,
            bracket_unc: bool = None,
            val_unc_match_widths: bool = None,
            bracket_unc_remove_seps: bool = None,
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
        if format_mode is None:
            format_mode = defaults.format_mode
        if capitalize is None:
            capitalize = defaults.capitalize
        if exp is None:
            exp = defaults.exp
        if use_prefix is None:
            use_prefix = defaults.use_prefix
        if extra_si_prefixes is None:
            extra_si_prefixes = copy(defaults.extra_si_prefixes)
        else:
            extra_si_prefixes = copy(extra_si_prefixes)
        if extra_iec_prefixes is None:
            extra_iec_prefixes = copy(defaults.extra_iec_prefixes)
        else:
            extra_iec_prefixes = copy(extra_iec_prefixes)
        if bracket_unc is None:
            bracket_unc = defaults.bracket_unc
        if val_unc_match_widths is None:
            val_unc_match_widths = defaults.val_unc_match_widths
        if bracket_unc_remove_seps is None:
            bracket_unc_remove_seps = defaults.bracket_unc_remove_seps
        if unc_pm_whitespace is None:
            unc_pm_whitespace = defaults.unc_pm_whitespace
        if nan_inf_exp is None:
            nan_inf_exp = defaults.nan_inf_exp

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

        return cls(
            fill_mode=fill_mode,
            sign_mode=sign_mode,
            top_dig_place=top_dig_place,
            upper_separator=upper_separator,
            decimal_separator=decimal_separator,
            lower_separator=lower_separator,
            round_mode=round_mode,
            precision=precision,
            format_mode=format_mode,
            capitalize=capitalize,
            exp=exp,
            nan_inf_exp=nan_inf_exp,
            use_prefix=use_prefix,
            extra_si_prefixes=extra_si_prefixes,
            extra_iec_prefixes=extra_iec_prefixes,
            bracket_unc=bracket_unc,
            val_unc_match_widths=val_unc_match_widths,
            bracket_unc_remove_seps=bracket_unc_remove_seps,
            unc_pm_whitespace=unc_pm_whitespace
        )

    pattern = re.compile(r'''^
                             (?:(?P<fill_mode>[ 0])=)?
                             (?P<sign_mode>[-+ ])?
                             (?P<alternate_mode>\#)?                         
                             (?P<top_dig_place>\d+)?
                             (?P<upper_separator>[n,.s_])?                     
                             (?P<decimal_separator>[.,])?            
                             (?P<lower_separator>[ns_])?                  
                             (?:(?P<round_mode>[.!])(?P<prec>[+-]?\d+))?
                             (?P<format_mode>[fF%eErRbB])?
                             (?:x(?P<exp>[+-]?\d+))?
                             (?P<prefix_mode>p)?
                             (?P<bracket_unc>S)?
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

        format_mode = match.group('format_mode')
        if format_mode is not None:
            capitalize = format_mode.isupper()
            if format_mode in ['f', 'F']:
                format_mode = FormatMode.FIXEDPOINT
            elif format_mode == '%':
                format_mode = FormatMode.PERCENT
            elif format_mode in ['e', 'E']:
                format_mode = FormatMode.SCIENTIFIC
            elif format_mode in ['r', 'R']:
                if alternate_mode:
                    format_mode = FormatMode.ENGINEERING_SHIFTED
                else:
                    format_mode = FormatMode.ENGINEERING
            elif format_mode in ['b', 'B']:
                if alternate_mode:
                    format_mode = FormatMode.BINARY_IEC
                else:
                    format_mode = FormatMode.BINARY
        else:
            capitalize = None

        exp = match.group('exp')
        if exp is not None:
            exp = int(exp)

        use_prefix = match.group('prefix_mode')
        if use_prefix is not None:
            use_prefix = True

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
            format_mode=format_mode,
            capitalize=capitalize,
            exp=exp,
            use_prefix=use_prefix,
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
    format_mode=FormatMode.FIXEDPOINT,
    capitalize=False,
    exp=AutoExp,
    nan_inf_exp=False,
    use_prefix=False,
    extra_si_prefixes=dict(),
    extra_iec_prefixes=dict(),
    bracket_unc=False,
    val_unc_match_widths=False,
    bracket_unc_remove_seps=False,
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
        format_mode: FormatMode = None,
        capitalize: bool = None,
        exp: Union[int, type(AutoExp)] = None,
        nan_inf_exp=None,
        use_prefix: bool = None,
        extra_si_prefixes: dict[int, str] = None,
        extra_iec_prefixes: dict[int, str] = None,
        add_c_prefix: bool = False,
        add_small_si_prefixes: bool = False,
        bracket_unc=None,
        val_unc_match_widths=None,
        bracket_unc_remove_seps=None,
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
        format_mode=format_mode,
        capitalize=capitalize,
        exp=exp,
        nan_inf_exp=nan_inf_exp,
        use_prefix=use_prefix,
        extra_si_prefixes=extra_si_prefixes,
        extra_iec_prefixes=extra_iec_prefixes,
        add_c_prefix=add_c_prefix,
        add_small_si_prefixes=add_small_si_prefixes,
        bracket_unc=bracket_unc,
        val_unc_match_widths=val_unc_match_widths,
        bracket_unc_remove_seps=bracket_unc_remove_seps,
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
    This mapping first use :func:`global_reset_si_prefixes` or
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
            format_mode: FormatMode = None,
            capitalize: bool = None,
            exp: Union[int, type(AutoExp)] = None,
            nan_inf_exp: bool = None,
            use_prefix: bool = None,
            extra_si_prefixes: dict[int, str] = None,
            extra_iec_prefixes: dict[int, str] = None,
            add_c_prefix: bool = False,
            add_small_si_prefixes: bool = False,
            bracket_unc: bool = None,
            val_unc_match_widths: bool = None,
            bracket_unc_remove_seps: bool = None,
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
            format_mode=format_mode,
            capitalize=capitalize,
            exp=exp,
            nan_inf_exp=nan_inf_exp,
            use_prefix=use_prefix,
            extra_si_prefixes=extra_si_prefixes,
            extra_iec_prefixes=extra_iec_prefixes,
            add_c_prefix=add_c_prefix,
            add_small_si_prefixes=add_small_si_prefixes,
            bracket_unc=bracket_unc,
            val_unc_match_widths=val_unc_match_widths,
            bracket_unc_remove_seps=bracket_unc_remove_seps,
            unc_pm_whitespace=unc_pm_whitespace
        )
        self.initial_global_defaults = None

    def __enter__(self):
        self.initial_global_defaults = get_global_defaults()
        set_global_defaults(defaults=self.options)

    def __exit__(self, exc_type, exc_value, exc_tb):
        set_global_defaults(defaults=self.initial_global_defaults)
