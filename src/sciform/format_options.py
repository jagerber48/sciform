from typing import Union, Optional, get_args
from dataclasses import dataclass, asdict
import re
from copy import copy
from pprint import pprint

from sciform.modes import (FillMode, SignMode, GroupingSeparator,
                           UpperGroupingSeparators, LowerGroupingSeparators,
                           DecimalGroupingSeparators, RoundMode, FormatMode,
                           AutoExp, AutoPrec)


# noinspection PyUnresolvedReferences
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
    format_mode: FormatMode
    capital_exp_char: bool
    exp: Union[int, type(AutoExp)]
    use_prefix: bool
    extra_si_prefixes: dict[int, str]
    extra_iec_prefixes: dict[int, str]

    def __post_init__(self):
        if self.round_mode is RoundMode.SIG_FIG:
            if isinstance(self.precision, int):
                if self.precision < 1:
                    raise ValueError(f'Precision must be >= 1 for sig fig '
                                     f'rounding, not {self.precision}.')

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
            capital_exp_char: bool = None,
            exp: Union[int, type(AutoExp)] = None,
            use_prefix: bool = None,
            extra_si_prefixes: dict[int, str] = None,
            extra_iec_prefixes: dict[int, str] = None,
            add_c_prefix: bool = False,
            add_small_si_prefixes: bool = False
    ):
        if defaults is None:
            defaults = DEFAULT_GLOBAL_OPTIONS

        extra_si_prefixes = (copy(extra_si_prefixes)
                             or copy(defaults.extra_si_prefixes))
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
            fill_mode=defaults.fill_mode if fill_mode is None else fill_mode,
            sign_mode=sign_mode or defaults.sign_mode,
            top_dig_place=(defaults.top_dig_place if top_dig_place is None
                           else top_dig_place),
            upper_separator=(upper_separator or
                             defaults.upper_separator),
            decimal_separator=(decimal_separator or
                               defaults.decimal_separator),
            lower_separator=(lower_separator or
                             defaults.lower_separator),
            round_mode=round_mode or defaults.round_mode,
            precision=defaults.precision if precision is None else precision,
            format_mode=format_mode or defaults.format_mode,
            capital_exp_char=(capital_exp_char or
                              defaults.capital_exp_char),
            exp=defaults.exp if exp is None else exp,
            use_prefix=use_prefix or defaults.use_prefix,
            extra_si_prefixes=extra_si_prefixes,
            extra_iec_prefixes=(copy(extra_iec_prefixes)
                                or copy(defaults.extra_iec_prefixes))
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
            capital_exp_char = format_mode.isupper()
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
            capital_exp_char = None

        exp = match.group('exp')
        if exp is not None:
            exp = int(exp)

        use_prefix = match.group('prefix_mode')
        if use_prefix is not None:
            use_prefix = True

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
            capital_exp_char=capital_exp_char,
            exp=exp,
            use_prefix=use_prefix
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
    capital_exp_char=False,
    exp=AutoExp,
    use_prefix=False,
    extra_si_prefixes=dict(),
    extra_iec_prefixes=dict()
)

DEFAULT_GLOBAL_OPTIONS = FormatOptions.make(
    defaults=DEFAULT_PKG_OPTIONS)


def get_global_defaults() -> FormatOptions:
    return DEFAULT_GLOBAL_OPTIONS


def print_global_defaults():
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
            capital_exp_char: bool = None,
            exp: Union[int, type(AutoExp)] = None,
            use_prefix: bool = None,
            extra_si_prefixes: dict[int, str] = None,
            extra_iec_prefixes: dict[int, str] = None,
            add_c_prefix: bool = False,
            add_small_si_prefixes: bool = False
):
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
        capital_exp_char=capital_exp_char,
        exp=exp,
        use_prefix=use_prefix,
        extra_si_prefixes=extra_si_prefixes,
        extra_iec_prefixes=extra_iec_prefixes,
        add_c_prefix=add_c_prefix,
        add_small_si_prefixes=add_small_si_prefixes)
    DEFAULT_GLOBAL_OPTIONS = new_default_options


def reset_global_defaults():
    global DEFAULT_GLOBAL_OPTIONS
    DEFAULT_GLOBAL_OPTIONS = DEFAULT_PKG_OPTIONS


def global_add_c_prefix():
    set_global_defaults(add_c_prefix=True)


def global_add_small_si_prefixes():
    set_global_defaults(add_small_si_prefixes=True)


def global_reset_si_prefixes():
    set_global_defaults(extra_si_prefixes=dict())


def global_reset_iec_prefixes():
    set_global_defaults(extra_iec_prefixes=dict())


class GlobalDefaultsContext:
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
            capital_exp_char: bool = None,
            exp: Union[int, type(AutoExp)] = None,
            use_prefix: bool = None,
            extra_si_prefixes: dict[int, str] = None,
            extra_iec_prefixes: dict[int, str] = None,
            add_c_prefix: bool = False,
            add_small_si_prefixes: bool = False
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
            capital_exp_char=capital_exp_char,
            exp=exp,
            use_prefix=use_prefix,
            extra_si_prefixes=extra_si_prefixes,
            extra_iec_prefixes=extra_iec_prefixes,
            add_c_prefix=add_c_prefix,
            add_small_si_prefixes=add_small_si_prefixes)
        self.initial_global_defaults = None

    def __enter__(self):
        self.initial_global_defaults = get_global_defaults()
        set_global_defaults(defaults=self.options)

    def __exit__(self, exc_type, exc_value, exc_tb):
        set_global_defaults(defaults=self.initial_global_defaults)
