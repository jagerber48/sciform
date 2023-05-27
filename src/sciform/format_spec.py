from typing import Optional, Union
import re
from warnings import warn

from sciform.modes import (FillMode, FormatMode, PrecMode, SignMode,
                           GroupingSeparator, DecimalSeparator, AUTO)


class FormatSpec:
    def __init__(
            self,
            *,
            fill_mode: Union[str, FillMode],
            sign_mode: Union[str, SignMode],
            alternate_mode: bool,
            top_dig_place: int,
            thousands_separator: Union[str, GroupingSeparator],
            decimal_separator: Union[str, DecimalSeparator],
            thousandths_separator: Union[str, GroupingSeparator],
            prec_mode: Union[str, PrecMode],
            prec: Union[int, type(AUTO)],
            format_mode: Union[str, FormatMode],
            capital_exp_char: bool,
            percent_mode: bool,
            exp: Union[int, type(AUTO)],
            prefix_mode: bool,
            extra_si_prefixes: dict[int, str],
            include_c: bool,
            include_small_si_prefixes: bool,
            extra_iec_prefixes: dict[int, str]):

        if isinstance(fill_mode, str):
            fill_mode = FillMode.from_flag(fill_mode)
        self.fill_mode = fill_mode

        if isinstance(sign_mode, str):
            sign_mode = SignMode.from_flag(sign_mode)
        self.sign_mode = sign_mode

        self.alternate_mode = alternate_mode

        self.top_dig_place = top_dig_place

        if isinstance(thousands_separator, str):
            thousands_separator = GroupingSeparator.from_flag(
                thousands_separator)
        self.thousands_separator = thousands_separator

        if isinstance(decimal_separator, str):
            decimal_separator = DecimalSeparator.from_flag(decimal_separator)
        self.decimal_separator = decimal_separator

        if isinstance(thousandths_separator, str):
            thousandths_separator = GroupingSeparator.from_flag(
                thousandths_separator)
        self.thousandths_separator = thousandths_separator

        if isinstance(prec_mode, str):
            prec_mode = PrecMode.from_flag(prec_mode)

        if prec_mode is PrecMode.SIG_FIG:
            # Validate prec >= 1 for SIG_FIG mode
            if isinstance(prec, int):
                if prec < 1:
                    raise ValueError(
                        f'Precision must be >= 1 for sig fig format '
                        f'mode, not {prec}.')
        self.prec_mode = prec_mode
        self.prec = prec

        if isinstance(format_mode, str):
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

        self.capital_exp_char = capital_exp_char

        self.percent_mode = percent_mode

        self.exp = exp

        self.prefix_mode = prefix_mode

        self.extra_si_prefixes = extra_si_prefixes
        if include_c:
            self.add_si_prefix(-2, 'c')
        if include_small_si_prefixes:
            self.add_si_prefixes({-2: 'c', -1: 'd',
                                  +1: 'da', +2: 'h'})

        self.extra_iec_prefixes = extra_iec_prefixes

    def add_si_prefix(self, exp_val: int, si_prefix: str):
        self.extra_si_prefixes[exp_val] = si_prefix

    def add_si_prefixes(self, new_si_prefixes: dict[int, str]):
        self.extra_si_prefixes.update(new_si_prefixes)

    def add_iec_prefix(self, exp_val: int, iec_prefix: str):
        self.extra_iec_prefixes[exp_val] = iec_prefix

    def add_iec_prefixes(self, new_iec_prefixes: dict[int, str]):
        self.extra_iec_prefixes.update(new_iec_prefixes)

    @classmethod
    def from_template(
            cls,
            *,
            template: 'FormatSpec',
            fill_mode: Union[str, FillMode] = None,
            sign_mode: Union[str, SignMode] = None,
            alternate_mode: bool = None,
            top_dig_place: int = None,
            thousands_separator: Union[str, GroupingSeparator] = None,
            decimal_separator: Union[str, DecimalSeparator] = None,
            thousandths_separator: Union[str, GroupingSeparator] = None,
            prec_mode: Union[str, PrecMode] = None,
            prec: Optional[int] = None,
            format_mode: Union[str, FormatMode] = None,
            capital_exp_char: bool = None,
            percent_mode: bool = None,
            exp: Optional[int] = None,
            prefix_mode: bool = None,
            extra_si_prefixes: dict[int, str] = None,
            include_c: bool = False,
            include_small_si_prefixes: bool = False,
            extra_iec_prefixes: dict[int, str] = None) -> 'FormatSpec':
        return FormatSpec(
            fill_mode=fill_mode or template.fill_mode,
            sign_mode=sign_mode or template.sign_mode,
            alternate_mode=alternate_mode or template.alternate_mode,
            top_dig_place=(template.top_dig_place if top_dig_place is None
                           else top_dig_place),
            thousands_separator=(thousands_separator
                                 or template.thousands_separator),
            decimal_separator=decimal_separator or template.decimal_separator,
            thousandths_separator=(thousandths_separator
                                   or template.thousandths_separator),
            prec_mode=prec_mode or template.prec_mode,
            prec=template.prec if prec is None else prec,
            format_mode=format_mode or template.format_mode,
            capital_exp_char=capital_exp_char or template.capital_exp_char,
            percent_mode=percent_mode or template.percent_mode,
            exp=template.exp if exp is None else exp,
            prefix_mode=prefix_mode or template.prefix_mode,
            extra_si_prefixes=extra_si_prefixes or template.extra_si_prefixes,
            include_c=include_c,
            include_small_si_prefixes=include_small_si_prefixes,
            extra_iec_prefixes=extra_iec_prefixes)

    def update(
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
            prec: Optional[int] = None,
            format_mode: Union[str, FormatMode] = None,
            capital_exp_char: bool = None,
            percent_mode: bool = None,
            exp: Optional[int] = None,
            prefix_mode: bool = None,
            extra_si_prefixes: dict[int, str] = None,
            include_c: bool = False,
            include_small_si_prefixes: bool = False,
            extra_iec_prefixes: dict[int, str] = None):
        self.fill_mode = fill_mode or self.fill_mode
        self.sign_mode = sign_mode or self.sign_mode
        self.alternate_mode = alternate_mode or self.alternate_mode
        self.top_dig_place = (self.top_dig_place if top_dig_place is None
                              else top_dig_place)
        self.thousands_separator = (thousands_separator
                                    or self.thousands_separator)
        self.decimal_separator = (decimal_separator
                                  or self.decimal_separator)
        self.thousandths_separator = (thousandths_separator
                                      or self.thousandths_separator)

        if prec_mode is PrecMode.SIG_FIG:
            # Validate prec >= 1 for SIG_FIG mode
            if isinstance(prec, int):
                if prec < 1:
                    raise ValueError(
                        f'Precision must be >= 1 for sig fig format '
                        f'mode, not {prec}.')
        self.prec_mode = prec_mode or self.prec_mode
        self.prec = self.prec if prec is None else prec

        format_mode = format_mode or self.format_mode

        if isinstance(format_mode, str):
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

        self.capital_exp_char = capital_exp_char or self.capital_exp_char

        percent_mode = percent_mode or self.percent_mode
        if (percent_mode
                and self.format_mode is not FormatMode.FIXEDPOINT):
            raise ValueError(f'Cannot use percent mode with fomrat'
                             f'mode \'{self.format_mode}\'')
        self.percent_mode = percent_mode

        self.exp = self.exp if exp is None else exp

        self.prefix_mode = prefix_mode or self.prefix_mode
        self.extra_si_prefixes = (extra_si_prefixes
                                  or self.extra_si_prefixes)
        if include_c:
            self.add_si_prefix(-2, 'c')
        if include_small_si_prefixes:
            self.add_si_prefixes({-2: 'c', -1: 'd',
                                  +1: 'da', +2: 'h'})

        self.extra_iec_prefixes = extra_iec_prefixes


FMT_SPEC_PKG_DEFAULTS = FormatSpec(
    fill_mode=FillMode.SPACE,
    sign_mode=SignMode.NEGATIVE,
    alternate_mode=False,
    top_dig_place=0,
    thousands_separator=GroupingSeparator.NO_GROUPING,
    decimal_separator=DecimalSeparator.POINT,
    thousandths_separator=GroupingSeparator.NO_GROUPING,
    prec_mode=PrecMode.SIG_FIG,
    prec=AUTO,
    format_mode=FormatMode.FIXEDPOINT,
    capital_exp_char=False,
    percent_mode=False,
    exp=AUTO,
    prefix_mode=False,
    extra_si_prefixes=dict(),
    include_c=False,
    include_small_si_prefixes=False,
    extra_iec_prefixes=dict()
)


FMT_SPEC_GLOBAL_DEFAULTS = FormatSpec.from_template(
    template=FMT_SPEC_PKG_DEFAULTS)


def get_global_defaults():
    return FMT_SPEC_GLOBAL_DEFAULTS


def update_global_defaults(new_fmt_spec: Optional[FormatSpec] = None,
                           **kwargs):
    global FMT_SPEC_GLOBAL_DEFAULTS
    if new_fmt_spec is not None:
        FMT_SPEC_GLOBAL_DEFAULTS = new_fmt_spec
    FMT_SPEC_GLOBAL_DEFAULTS.update(**kwargs)


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
        format_spec_template: Optional[FormatSpec] = None) \
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

    if format_spec_template is None:
        format_spec_template = FMT_SPEC_GLOBAL_DEFAULTS

    return FormatSpec.from_template(
        template=format_spec_template,
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
    )
