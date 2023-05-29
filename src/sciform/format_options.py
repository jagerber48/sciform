from typing import Union, Optional
from dataclasses import dataclass
import re
from copy import copy

from sciform.types import (_FILL_TYPES, _SIGN_TYPES, _UPPER_SEP_TYPES,
                           _DECIMAL_SEP_TYPES, _LOWER_SEP_TYPES, _ROUND_TYPES,
                           _FORMAT_TYPES)
from sciform.modes import (FillMode, SignMode, GroupingSeparator,
                           RoundMode, FormatMode, AUTO)


@dataclass
class FormatOptions:
    fill_mode: FillMode
    sign_mode: SignMode
    top_dig_place: int
    upper_separator: GroupingSeparator
    decimal_separator: GroupingSeparator
    lower_separator: GroupingSeparator
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

    @classmethod
    def from_user_input(
            cls,
            *,
            fill_mode: _FILL_TYPES = None,
            sign_mode: _SIGN_TYPES = None,
            top_dig_place: int = None,
            upper_separator: _UPPER_SEP_TYPES = None,
            decimal_separator: _DECIMAL_SEP_TYPES = None,
            lower_separator: _LOWER_SEP_TYPES = None,
            round_mode: _ROUND_TYPES = None,
            precision: Union[int, type(AUTO)] = None,
            format_mode: _FORMAT_TYPES = None,
            capital_exp_char: bool = None,
            exp: Union[int, type(AUTO)] = None,
            use_prefix: bool = None,
            extra_si_prefixes: dict[int, str] = None,
            include_c_prefix: bool = False,
            include_small_si_prefixes: bool = False,
            extra_iec_prefixes: dict[int, str] = None,
            defaults: 'FormatOptions' = None):
        if defaults is None:
            defaults = DEFAULT_GLOBAL_OPTIONS

        if fill_mode is not None:
            fill_mode = FillMode.from_flag(fill_mode)
        else:
            fill_mode = defaults.fill_mode

        if sign_mode is not None:
            sign_mode = SignMode.from_flag(sign_mode)
        else:
            sign_mode = defaults.sign_mode

        if top_dig_place is None:
            top_dig_place = defaults.top_dig_place

        if upper_separator is not None:
            upper_separator = GroupingSeparator.from_flag(
                upper_separator
            )
        else:
            upper_separator = defaults.upper_separator

        if decimal_separator is not None:
            decimal_separator = GroupingSeparator.from_flag(
                decimal_separator
            )
        else:
            decimal_separator = defaults.decimal_separator

        if lower_separator is not None:
            lower_separator = GroupingSeparator.from_flag(
                lower_separator
            )
        else:
            lower_separator = defaults.lower_separator

        if round_mode is not None:
            round_mode = RoundMode.from_flag(round_mode)
        else:
            round_mode = defaults.round_mode

        if precision is None:
            precision = defaults.precision

        if format_mode is not None:
            format_mode = FormatMode.from_flag(format_mode)
        else:
            format_mode = defaults.format_mode

        if capital_exp_char is None:
            capital_exp_char = defaults.capital_exp_char

        if exp is None:
            exp = defaults.exp

        if use_prefix is None:
            use_prefix = defaults.use_prefix

        if extra_si_prefixes is None:
            if include_c_prefix:
                extra_si_prefixes = {-2: 'c'}
            if include_small_si_prefixes:
                extra_si_prefixes = {-2: 'c', -1: 'd',
                                     +1: 'da', +2: 'h'}
        if extra_si_prefixes is None:
            extra_si_prefixes = defaults.extra_si_prefixes

        if extra_iec_prefixes is None:
            extra_iec_prefixes = defaults.extra_iec_prefixes

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
            capital_exp_char=capital_exp_char,
            exp=exp,
            use_prefix=use_prefix,
            extra_si_prefixes=extra_si_prefixes,
            extra_iec_prefixes=extra_iec_prefixes
        )

    pattern = re.compile(r'''^
                             (?:(?P<fill>[ 0])=)?
                             (?P<sign>[+\- ])?
                             (?P<alternate>\#)?                         
                             (?P<top_dig_place>\d+)?
                             (?P<upper_separator>[n,.s_])?                     
                             (?P<decimal_separator>[.,])?            
                             (?P<lower_separator>[ns_])?                  
                             (?:(?P<round_mode>[.!])(?P<prec>[+-]?\d+))?
                             (?P<format_mode>[fF%eErRbB])?
                             (?:x(?P<exp>[+-]?\d+))?
                             (?P<prefix_mode>p)?
                             $''', re.VERBOSE)

    @classmethod
    def from_format_spec_str(cls, fmt: str) -> 'FormatOptions':
        # TODO: Catch more formatting errors as early as possible
        match = cls.pattern.match(fmt)
        if match is None:
            raise ValueError(f'Invalid format specifier: \'{fmt}\'')

        fill_mode = match.group('fill')
        sign_mode = match.group('sign')
        alternate_mode = match.group('alternate')
        top_dig_place = match.group('top_dig_place')
        if top_dig_place is not None:
            top_dig_place = int(top_dig_place)

        upper_separator = match.group('upper_separator')
        if upper_separator is not None:
            if upper_separator == 'n':
                upper_separator = 'none'
            elif upper_separator == ',':
                upper_separator = ','
            elif upper_separator == '.':
                upper_separator = '.'
            elif upper_separator == 's':
                upper_separator = ' '
            elif upper_separator == '_':
                upper_separator = '_'
            else:
                raise NotImplemented

        decimal_separator = match.group('decimal_separator')
        if decimal_separator is not None:
            if decimal_separator == '.':
                decimal_separator = '.'
            elif decimal_separator == ',':
                decimal_separator = ','
            else:
                raise NotImplemented

        lower_separator = match.group('lower_separator')
        if lower_separator is not None:
            if lower_separator == 'n':
                lower_separator = 'none'
            elif lower_separator == 's':
                lower_separator = ' '
            elif lower_separator == '_':
                lower_separator = '_'
            else:
                raise NotImplemented

        round_mode = match.group('round_mode')
        if round_mode is not None:
            if round_mode == '!':
                round_mode = 'sig_fig'
            elif round_mode == '.':
                round_mode = 'precision'
            else:
                raise NotImplemented

        # TODO Think about default values here, force a default precision or
        #  number of sig figs?
        precision = match.group('prec')
        if precision is not None:
            precision = int(precision)

        format_mode = match.group('format_mode')
        if format_mode is not None:
            capital_exp_char = format_mode.isupper()
            if format_mode in ['f', 'F']:
                format_mode = 'fixed_point'
            elif format_mode in ['e', 'E']:
                format_mode = 'scientific'
            elif format_mode in ['r', 'R']:
                if alternate_mode:
                    format_mode = 'engineering_shifted'
                else:
                    format_mode = 'engineering'
            elif format_mode in ['b', 'B']:
                if alternate_mode:
                    format_mode = 'binary_iec'
                else:
                    format_mode = 'binary'
        else:
            capital_exp_char = None

        exp = match.group('exp')
        if exp is not None:
            exp = int(exp)

        use_prefix = match.group('prefix_mode')

        return cls.from_user_input(
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

    @classmethod
    def from_template(
            cls,
            *,
            template: 'FormatOptions',
            fill_mode: FillMode = None,
            sign_mode: SignMode = None,
            top_dig_place: int = None,
            upper_separator: GroupingSeparator = None,
            decimal_separator: GroupingSeparator = None,
            lower_separator: GroupingSeparator = None,
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
            extra_si_prefixes=(extra_si_prefixes or
                               template.extra_si_prefixes),
            extra_iec_prefixes=(extra_iec_prefixes or
                                extra_iec_prefixes)
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
                        **kwargs):
    global DEFAULT_GLOBAL_OPTIONS
    if template is None:
        template = DEFAULT_GLOBAL_OPTIONS
    new_default_options = FormatOptions.from_user_input(defaults=template,
                                                        **kwargs)
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
        self.initial_global_defaults = copy(get_global_defaults())
        set_global_defaults(self.template, **self.kwargs)

    def __exit__(self, exc_type, exc_value, exc_tb):
        set_global_defaults(self.initial_global_defaults)
