from typing import Union, Optional, get_args
from dataclasses import dataclass
import re
from copy import copy

from sciform.modes import (FillMode, SignMode, GroupingSeparator,
                           UpperGroupingSeparators, LowerGroupingSeparators,
                           DecimalGroupingSeparators, RoundMode, FormatMode,
                           AUTO)


@dataclass
class FormatOptions:
    fill_mode: FillMode
    sign_mode: SignMode
    top_dig_place: int
    upper_separator: UpperGroupingSeparators
    decimal_separator: DecimalGroupingSeparators
    lower_separator: LowerGroupingSeparators
    round_mode: RoundMode
    precision: Union[int, type(AUTO)]
    format_mode: FormatMode
    capital_exp_char: bool
    exp: Union[int, type(AUTO)]
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

    def add_si_prefix(self, exp: int, prefix: str):
        self.extra_si_prefixes[exp] = prefix

    def add_iec_prefix(self, exp: int, prefix: str):
        self.extra_iec_prefixes[exp] = prefix

    def add_si_prefixes(self, si_prefixes: dict[int, str]):
        self.extra_si_prefixes.update(si_prefixes)

    def add_iec_prefixes(self, iec_prefixes: dict[int, str]):
        self.extra_iec_prefixes.update(iec_prefixes)

    def include_c_prefix(self):
        self.add_si_prefix(exp=-2, prefix='c')

    def include_small_si_prefixes(self):
        self.add_si_prefixes({-2: 'c', -1: 'd', +1: 'da', +2: 'h'})

    @classmethod
    def from_template(
            cls,
            *,
            template: 'FormatOptions',
            fill_mode: FillMode = None,
            sign_mode: SignMode = None,
            top_dig_place: int = None,
            upper_separator: UpperGroupingSeparators = None,
            decimal_separator: DecimalGroupingSeparators = None,
            lower_separator: LowerGroupingSeparators = None,
            round_mode: RoundMode = None,
            precision: Union[int, type(AUTO)] = None,
            format_mode: FormatMode = None,
            capital_exp_char: bool = None,
            exp: Union[int, type(AUTO)] = None,
            use_prefix: bool = None,
            extra_si_prefixes: dict[int, str] = None,
            extra_iec_prefixes: dict[int, str] = None,
    ):
        return cls(
            fill_mode=template.fill_mode if fill_mode is None else fill_mode,
            sign_mode=sign_mode or template.sign_mode,
            top_dig_place=(template.top_dig_place if top_dig_place is None
                           else top_dig_place),
            upper_separator=(upper_separator or
                             template.upper_separator),
            decimal_separator=(decimal_separator or
                               template.decimal_separator),
            lower_separator=(lower_separator or
                             template.lower_separator),
            round_mode=round_mode or template.round_mode,
            precision=template.precision if precision is None else precision,
            format_mode=format_mode or template.format_mode,
            capital_exp_char=(capital_exp_char or
                              template.capital_exp_char),
            exp=template.exp if exp is None else exp,
            use_prefix=use_prefix or template.use_prefix,
            extra_si_prefixes=(copy(extra_si_prefixes) or
                               copy(template.extra_si_prefixes)),
            extra_iec_prefixes=(copy(extra_iec_prefixes) or
                                copy(template.extra_iec_prefixes))
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
            template: Optional['FormatOptions'] = None) -> 'FormatOptions':
        # TODO: Catch more formatting errors as early as possible
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

        # TODO Think about default values here, force a default precision or
        #  number of sig figs?
        precision = match.group('prec')
        if precision is not None:
            precision = int(precision)

        format_mode = match.group('format_mode')
        if format_mode is not None:
            capital_exp_char = format_mode.isupper()
            if format_mode in ['f', 'F']:
                format_mode = FormatMode.FIXEDPOINT
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

        if template is None:
            template = DEFAULT_GLOBAL_OPTIONS

        return cls.from_template(
            template=template,
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
    precision=AUTO,
    format_mode=FormatMode.FIXEDPOINT,
    capital_exp_char=False,
    exp=AUTO,
    use_prefix=False,
    extra_si_prefixes=dict(),
    extra_iec_prefixes=dict()
)

DEFAULT_GLOBAL_OPTIONS = FormatOptions.from_template(
    template=DEFAULT_PKG_OPTIONS)


def get_global_defaults():
    return DEFAULT_GLOBAL_OPTIONS


def set_global_defaults(template: Optional[FormatOptions] = None,
                        include_c_prefix: bool = False,
                        include_small_si_prefixes: bool = False,
                        **kwargs):
    global DEFAULT_GLOBAL_OPTIONS
    if template is None:
        template = DEFAULT_GLOBAL_OPTIONS
    new_default_options = FormatOptions.from_template(template=template,
                                                      **kwargs)
    if include_c_prefix:
        new_default_options.include_c_prefix()
    if include_small_si_prefixes:
        new_default_options.include_small_si_prefixes()

    DEFAULT_GLOBAL_OPTIONS = new_default_options


def reset_global_defaults():
    global DEFAULT_GLOBAL_OPTIONS
    DEFAULT_GLOBAL_OPTIONS = DEFAULT_PKG_OPTIONS


class GlobalDefaultsContext:
    def __init__(self,
                 template: Optional[FormatOptions] = None,
                 **kwargs):
        self.template = template
        self.kwargs = kwargs
        self.initial_global_defaults = None

    def __enter__(self):
        self.initial_global_defaults = get_global_defaults()
        set_global_defaults(self.template, **self.kwargs)

    def __exit__(self, exc_type, exc_value, exc_tb):
        set_global_defaults(self.initial_global_defaults)
