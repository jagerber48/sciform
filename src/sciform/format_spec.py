from dataclasses import dataclass, field
from typing import Optional, Union
import re
from warnings import warn

from sciform.modes import (FillMode, FormatMode, PrecMode, SignMode,
                           GroupingSeparator, DecimalSeparator)


@dataclass
class FormatSpecDefaultOptions:
    FILL_MODE: FillMode = FillMode.SPACE
    SIGN_MODE: SignMode = SignMode.NEGATIVE
    ALTERNATE_MODE: bool = False
    TOP_DIG_PLACE: int = 0
    THOUSANDS_SEPARATOR: GroupingSeparator = GroupingSeparator.NO_GROUPING
    DECIMAL_SEPARATOR: DecimalSeparator = DecimalSeparator.POINT
    THOUSANDTHS_SEPARATOR: GroupingSeparator = GroupingSeparator.NO_GROUPING
    PREC_MODE: PrecMode = PrecMode.SIG_FIG
    PREC: Optional[int] = None
    FORMAT_MODE: FormatMode = FormatMode.FIXEDPOINT
    CAPITAL_EXP_CHAR: bool = False
    PERCENT_MODE: bool = False
    EXP: Optional[int] = None
    PREFIX_MODE: bool = False
    EXTRA_SI_PREFIXES: dict[int, str] = field(default_factory=dict)
    INCLUDE_C: bool = False
    INCLUDE_SMALL_SI_PREFIXES: bool = False
    EXTRA_IEC_PREFIXES: dict[int, str] = field(default_factory=dict)

    def update(self, *,
               fill_mode: Union[str, FillMode] = None,
               sign_mode: Union[str, SignMode] = None,
               alternate_mode: bool = None,
               top_dig_place: int = None,
               thousands_separator: Union[str, GroupingSeparator] = None,
               decimal_separator: Union[str, DecimalSeparator] = None,
               thousandths_separator: Union[str, GroupingSeparator] = None,
               prec_mode: Union[str, PrecMode] = None,
               prec: int = None,
               format_mode: Union[str, FormatMode] = None,
               capital_exp_char: bool = None,
               percent_mode: bool = None,
               exp: int = None,
               prefix_mode: bool = None,
               extra_si_prefixes: Optional[dict[int, str]] = None,
               include_c: bool = None,
               include_small_si_prefixes: bool = None,
               extra_iec_prefixes: Optional[dict[int, str]] = None):
        if fill_mode is not None:
            if isinstance(fill_mode, str):
                fill_mode = FillMode.from_flag(fill_mode)
            self.FILL_MODE = fill_mode

        if sign_mode is not None:
            if isinstance(sign_mode, str):
                sign_mode = SignMode.from_flag(sign_mode)
            self.SIGN_MODE = sign_mode

        if alternate_mode is not None:
            self.ALTERNATE_MODE = alternate_mode

        if top_dig_place is not None:
            self.TOP_DIG_PLACE = top_dig_place

        if thousands_separator is not None:
            if isinstance(thousands_separator, str):
                thousands_separator = GroupingSeparator.from_flag(
                    thousands_separator)
            self.THOUSANDTHS_SEPARATOR = thousands_separator

        if decimal_separator is not None:
            if isinstance(decimal_separator, str):
                decimal_separator = DecimalSeparator.from_flag(
                    decimal_separator)
            self.DECIMAL_SEPARATOR = decimal_separator

        if thousandths_separator is not None:
            if isinstance(thousandths_separator, str):
                thousandths_separator = GroupingSeparator.from_flag(
                    thousandths_separator)
            self.THOUSANDTHS_SEPARATOR = thousandths_separator

        if prec_mode is not None:
            if isinstance(prec_mode, str):
                prec_mode = PrecMode.from_flag(prec_mode)
            self.PREC_MODE = prec_mode

        if prec is not None:
            self.PREC = prec

        if self.PREC_MODE is PrecMode.SIG_FIG:
            # Validate prec >= 1 for SIG_FIG mode
            if isinstance(self.PREC, int):
                if self.PREC < 1:
                    raise ValueError(
                        f'Precision must be >= 1 for sig fig format '
                        f'mode, not {self.PREC}.')

        if format_mode is not None:
            if isinstance(format_mode, str):
                '''
                Validate consistency between format mode flag and 
                capital_exp_char and percent_mode options
                '''
                derived_capital_exp_char = format_mode.isupper()
                if capital_exp_char is None:
                    capital_exp_char = derived_capital_exp_char
                elif derived_capital_exp_char != capital_exp_char:
                    warn(f'Explicit exponent capitalization option passed by '
                         f'user ({capital_exp_char}) is not compatible with '
                         f'format mode flag \'{format_mode}\' passed in by '
                         f'user. Ignoring format mode flag capitalization and '
                         f'using explicit user capitalization option.')

                derived_percent_mode = format_mode == '%'
                if percent_mode is None:
                    percent_mode = derived_percent_mode
                elif derived_percent_mode != percent_mode:
                    if format_mode == 'f' or format_mode == 'F':
                        warn(f'Explicit percent mode option passed by user '
                             f'({percent_mode}) is not compatible with format'
                             f'mode flag \'{format_mode}\' passed in by user.'
                             f'Ignoring format mode flag and using explicit '
                             f'user percent mode.')
                        format_mode = '%'
                    else:
                        raise ValueError(f'Cannot use percent mode with format'
                                         f'mode flag \'{format_mode}\'')
            self.FORMAT_MODE = FormatMode.from_flag(format_mode)

        if capital_exp_char is not None:
            self.CAPITAL_EXP_CHAR = capital_exp_char

        if percent_mode:
            if self.FORMAT_MODE is not FormatMode.FIXEDPOINT:
                raise ValueError(f'Cannot use percent mode with format'
                                 f'mode \'{self.FORMAT_MODE}\'')
            self.PERCENT_MODE = percent_mode

        if exp is not None:
            self.EXP = exp

        if prefix_mode is not None:
            self.PREFIX_MODE = prefix_mode

        if extra_si_prefixes is not None:
            self.EXTRA_SI_PREFIXES.update(extra_si_prefixes)

        if include_c:
            self.EXTRA_SI_PREFIXES[-2] = 'c'

        if include_small_si_prefixes:
            self.EXTRA_SI_PREFIXES.update({-2: 'c', -1: 'd',
                                           +1: 'da', +2: 'h'})

        if extra_iec_prefixes:
            self.EXTRA_IEC_PREFIXES.update(extra_si_prefixes)


FORMAT_SPEC_GLOBAL_DEFAULTS = FormatSpecDefaultOptions()


def update_global_defaults(**kwargs):
    FORMAT_SPEC_GLOBAL_DEFAULTS.update(**kwargs)


class FormatSpec:
    def __init__(
            self,
            *,
            fill_mode: Union[str, FillMode] = None,
            sign_mode: Union[str, SignMode] = None,
            alternate_mode: bool = None,
            top_dig_place: int = None,
            thousands_separator: Union[str, GroupingSeparator] = None,
            decimal_separator: Union[str, DecimalSeparator] = None,
            thousandths_separator: Union[str, GroupingSeparator] = None,
            prec_mode: Union[str, PrecMode] = None,
            prec: int = None,
            format_mode: Union[str, FormatMode] = None,
            capital_exp_char: bool = None,
            percent_mode: bool = None,
            exp: int = None,
            prefix_mode: bool = None,
            extra_si_prefixes: Optional[dict[int, str]] = None,
            include_c: bool = None,
            include_small_si_prefixes: bool = None,
            extra_iec_prefixes: Optional[dict[int, str]] = None,
            default_options: Optional[FormatSpecDefaultOptions] = None):
        if default_options is None:
            default_options = FORMAT_SPEC_GLOBAL_DEFAULTS

        if fill_mode is None:
            fill_mode = default_options.FILL_MODE
        elif isinstance(fill_mode, str):
            fill_mode = FillMode.from_flag(fill_mode)
        self.fill_mode = fill_mode

        if sign_mode is None:
            sign_mode = default_options.SIGN_MODE
        elif isinstance(sign_mode, str):
            sign_mode = SignMode.from_flag(sign_mode)
        self.sign_mode = sign_mode

        if alternate_mode is None:
            alternate_mode = default_options.ALTERNATE_MODE
        self.alternate_mode = alternate_mode

        if top_dig_place is None:
            top_dig_place = default_options.TOP_DIG_PLACE
        self.top_dig_place = top_dig_place

        if thousands_separator is None:
            thousands_separator = default_options.THOUSANDS_SEPARATOR
        elif isinstance(thousands_separator, str):
            thousands_separator = GroupingSeparator.from_flag(
                thousands_separator)
        self.thousands_separator = thousands_separator

        if decimal_separator is None:
            decimal_separator = default_options.DECIMAL_SEPARATOR
        elif isinstance(decimal_separator, str):
            decimal_separator = DecimalSeparator.from_flag(decimal_separator)
        self.decimal_separator = decimal_separator

        if thousandths_separator is None:
            thousandths_separator = default_options.THOUSANDTHS_SEPARATOR
        elif isinstance(thousandths_separator, str):
            thousandths_separator = GroupingSeparator.from_flag(
                thousandths_separator)
        self.thousandths_separator = thousandths_separator

        if prec_mode is None:
            prec_mode = default_options.PREC_MODE
        elif isinstance(prec_mode, str):
            prec_mode = PrecMode.from_flag(prec_mode)

        if prec is None:
            prec = default_options.PREC

        if prec_mode is PrecMode.SIG_FIG:
            # Validate prec >= 1 for SIG_FIG mode
            if isinstance(prec, int):
                if prec < 1:
                    raise ValueError(
                        f'Precision must be >= 1 for sig fig format '
                        f'mode, not {prec}.')
        self.prec_mode = prec_mode
        self.prec = prec

        if format_mode is None:
            format_mode = default_options.FORMAT_MODE
        elif isinstance(format_mode, str):
            '''
            Validate consistency between format mode flag and capital_exp_char
            and percent_mode options
            '''
            derived_capital_exp_char = format_mode.isupper()
            if capital_exp_char is None:
                capital_exp_char = derived_capital_exp_char
            elif derived_capital_exp_char != capital_exp_char:
                warn(f'Explicit exponent capitalization option passed by user '
                     f'({capital_exp_char}) is not compatible with format'
                     f'mode flag \'{format_mode}\' passed in by user.'
                     f'Ignoring format mode flag capitalization and using '
                     f'explicit user capitalization option.')

            derived_percent_mode = format_mode == '%'
            if percent_mode is None:
                percent_mode = derived_percent_mode
            elif derived_percent_mode != percent_mode:
                if format_mode == 'f' or format_mode == 'F':
                    warn(f'Explicit percent mode option passed by user '
                         f'({percent_mode}) is not compatible with format'
                         f'mode flag \'{format_mode}\' passed in by user.'
                         f'Ignoring format mode flag and using explicit user '
                         f'percent mode.')
                    format_mode = '%'
                else:
                    raise ValueError(f'Cannot use percent mode with fomrat'
                                     f'mode flag \'{format_mode}\'')

            format_mode = FormatMode.from_flag(format_mode)
        self.format_mode = format_mode

        if capital_exp_char is None:
            capital_exp_char = default_options.CAPITAL_EXP_CHAR
        self.capital_exp_char = capital_exp_char

        if percent_mode is None:
            percent_mode = default_options.PERCENT_MODE
        self.percent_mode = percent_mode

        if exp is None:
            exp = default_options.EXP
        self.exp = exp

        if prefix_mode is None:
            prefix_mode = default_options.PREFIX_MODE
        self.prefix_mode = prefix_mode

        if extra_si_prefixes is None:
            extra_si_prefixes = default_options.EXTRA_SI_PREFIXES
        if extra_si_prefixes is None:
            '''
            This code block is avoided if the user modifies 
            DEF_EXTRA_SI_PREFIXES as a configuration option
            '''
            extra_si_prefixes = dict()
        self.extra_si_prefixes = extra_si_prefixes

        if include_c is None:
            include_c = default_options.INCLUDE_C
        if include_c:
            self.add_si_prefix(-2, 'c')

        if include_small_si_prefixes is None:
            include_small_si_prefixes = default_options.INCLUDE_SMALL_SI_PREFIXES
        if include_small_si_prefixes:
            self.add_si_prefixes({-2: 'c', -1: 'd', +1: 'da', +2: 'h'})

        if extra_iec_prefixes is None:
            extra_iec_prefixes = default_options.EXTRA_IEC_PREFIXES
        if extra_iec_prefixes is None:
            '''
            This code block is avoided if the user modifies 
            DEF_EXTRA_IEC_PREFIXES as a configuration option
            '''
            extra_iec_prefixes = dict()
        self.extra_iec_prefixes = extra_iec_prefixes

    def add_si_prefix(self, exp_val: int, si_prefix: str):
        self.extra_si_prefixes[exp_val] = si_prefix

    def add_si_prefixes(self, new_si_prefixes: dict[int, str]):
        self.extra_si_prefixes.update(new_si_prefixes)

    def add_iec_prefix(self, exp_val: int, iec_prefix: str):
        self.extra_iec_prefixes[exp_val] = iec_prefix

    def add_iec_prefixes(self, new_iec_prefixes: dict[int, str]):
        self.extra_iec_prefixes.update(new_iec_prefixes)


pattern = re.compile(r'''^
                         (?:(?P<fill>[ 0])=)?
                         (?P<sign>[+\- ])?
                         (?P<alternate>\#)?                         
                         (?P<top_dig_place>\d+)?
                         (?P<thousands_separator>[n,.s_])?                     
                         (?P<decimal_separator>[.,])?            
                         (?P<thousandths_separator>[ns_])?                  
                         (?:(?P<prec_mode>[.!])(?P<prec>-?\d+))?
                         (?P<format_mode>[fF%eErRbB])?
                         (?P<exp>[+-]\d+)?
                         (?P<prefix_mode>p)?
                         $''', re.VERBOSE)


def parse_format_spec(
        fmt: str,
        default_options: Optional[FormatSpecDefaultOptions] = None) \
        -> FormatSpec:
    # TODO: Catch more formatting errors as early as possible
    match = pattern.match(fmt)
    if match is None:
        raise ValueError(f'Invalid format specifier: \'{fmt}\'')

    fill = match.group('fill')
    sign_mode = match.group('sign')
    alternate_mode = match.group('alternate')
    top_dig_place = match.group('top_dig_place')
    if top_dig_place is not None:
        top_dig_place = int(top_dig_place)
    thousands_separator = match.group('thousands_separator')
    decimal_separator = match.group('decimal_separator')
    thousandths_separator = match.group('thousandths_separator')
    prec_mode = match.group('prec_mode')

    # TODO Think about default values here, force a default precision or number
    #  of sig figs?
    prec = match.group('prec')
    if prec is not None:
        prec = int(prec)

    format_mode = match.group('format_mode')
    if format_mode is not None:
        capital_exp_char = format_mode.isupper()
        percent_mode = format_mode == '%'
    else:
        capital_exp_char = None
        percent_mode = None

    exp = match.group('exp')
    if exp is not None:
        exp = int(exp)

    prefix_mode = match.group('prefix_mode')

    return FormatSpec(
        fill_mode=fill,
        sign_mode=sign_mode,
        alternate_mode=alternate_mode,
        top_dig_place=top_dig_place,
        thousands_separator=thousands_separator,
        decimal_separator=decimal_separator,
        thousandths_separator=thousandths_separator,
        prec_mode=prec_mode,
        prec=prec,
        format_mode=format_mode,
        capital_exp_char=capital_exp_char,
        percent_mode=percent_mode,
        exp=exp,
        prefix_mode=prefix_mode,
        default_options=default_options
    )
