from typing import Union
from math import isfinite

from sciform.modes import (SignMode, FillMode, UpperGroupingSeparators,
                           DecimalGroupingSeparators, LowerGroupingSeparators,
                           FormatMode, RoundMode, AutoExp, AutoPrec)
from sciform.format_options import FormatOptions
from sciform.format_utils import (get_mantissa_exp_base, get_exp_str,
                                  get_top_and_bottom_digit,
                                  get_round_digit,
                                  format_float_by_top_bottom_dig)
from sciform.grouping import add_separators
from sciform.prefix import replace_prefix


def format_float(num: float, options: FormatOptions) -> str:
    format_mode = options.format_mode
    round_mode = options.round_mode
    precision = options.precision
    top_padded_digit = options.top_dig_place
    sign_mode = options.sign_mode
    capital_exp_char = options.capital_exp_char
    fill_char = FillMode.to_char(options.fill_mode)
    if not isfinite(num):
        if capital_exp_char:
            return str(num).upper()
        else:
            return str(num).lower()

    if format_mode is FormatMode.PERCENT:
        num *= 100

    exp = options.exp
    mantissa, temp_exp, base = get_mantissa_exp_base(num, format_mode, exp)

    top_digit, bottom_digit = get_top_and_bottom_digit(mantissa)
    round_digit = get_round_digit(top_digit, bottom_digit,
                                  precision, round_mode)

    mantissa_rounded = round(mantissa, -round_digit)

    '''
    Repeat mantissa + exponent discovery after rounding in case rounding
    altered the required exponent.
    '''
    rounded_num = mantissa_rounded * base**temp_exp
    mantissa, exp, base = get_mantissa_exp_base(rounded_num, format_mode, exp)

    top_digit, bottom_digit = get_top_and_bottom_digit(mantissa)
    round_digit = get_round_digit(top_digit, bottom_digit,
                                  precision, round_mode)

    mantissa_rounded = round(mantissa, -round_digit)
    if mantissa_rounded == 0:
        exp = 0

    exp_str = get_exp_str(exp, format_mode, capital_exp_char)

    if mantissa_rounded == -0.0:
        mantissa_rounded = abs(mantissa_rounded)
    mantissa_str = format_float_by_top_bottom_dig(mantissa_rounded,
                                                  top_padded_digit,
                                                  round_digit, sign_mode,
                                                  fill_char)

    # TODO: Think about the interaction between separators and fill
    #  characters
    upper_separator = options.upper_separator.to_char()
    decimal_separator = options.decimal_separator.to_char()
    lower_separator = options.lower_separator.to_char()
    mantissa_str = add_separators(mantissa_str,
                                  upper_separator,
                                  decimal_separator,
                                  lower_separator,
                                  group_size=3)

    full_str = f'{mantissa_str}{exp_str}'

    if options.use_prefix:
        full_str = replace_prefix(full_str,
                                  options.extra_si_prefixes,
                                  options.extra_iec_prefixes)

    if format_mode is FormatMode.PERCENT:
        full_str = full_str + '%'

    return full_str


class Formatter:
    """
    Formatter object use to convert floats into formatting strings. See
    :ref:`formatting_options` for more details on the different options.
    Any options which are not provided by the user will be filled with
    the corresponding values from the global default configuration.

    >>> from sciform import Formatter, FormatMode, RoundMode
    >>> sform = Formatter(format_mode=FormatMode.ENGINEERING,
    ...                   round_mode=RoundMode.SIG_FIG,
    ...                   precision=4)
    >>> print(sform(12345.678))
    12.35e+03

    The following checks are performed when creating a
    :class:`Formatter` object:

    * precision >= 1 for significant figure rounding mode
    * exp must be consistent with the format mode:

      * exp must be 0 for fixed point and percent modes
      * exp must be a multiple of 3 for engineering and shifted
        engineering modes
      * exp must be a multiple of 10 for binary iec mode

    * upper_separator must be different than decimal_separator
    * decimal_separator may only be GroupingSeparator.POINT or
      GroupingSeparator.COMMA
    * lower_separator may only be GroupingSeparator.NONE,
      GroupingSeparator.SPACE, or GroupingSeparator.UNDERSCORE.

    :param fill_mode: :class:`FillMode` indicating whether
      to fill with zeros or spaces.
    :param sign_mode: :class:`SignMode` indicating sign
      symbol behavior.
    :param top_dig_place: Positive ``int`` indicating the digits place
      to which the string will be left padded before the sign symbol.
      e.g. top_dig_place=4 will convert ``12`` into ``00012``.
    :param upper_separator: :class:`GroupingSeparator` indicating the
      character to be used to group digits above the decimal symbol.
    :param decimal_separator: :class:`GroupingSeparator` indicating
      the character to be used as the decimal symbol.
      :class:`GroupingSeparator.POINT` or
      :class:`GroupingSeparator.COMMA`. Note that ``decimal_separator``
      cannot be the same as ``upper_separator``
    :param lower_separator: :class:`GroupingSeparator` indicating the
      character to be used to group digits below the decimal symbol.
      :class:`GroupingSeparator.NONE`, :class:`GroupingSeparator.SPACE`,
      :class:`GroupingSeparator.UNDERSCORE`.
    :param round_mode: :class:`RoundMode` indicating whether to round
      the number based on significant figures or digits past the
      decimal point
    :param precision: ``int`` indicating how many significant figures or
      digits past the decimal point to include for rounding. Must be
      >= 1 for significant figure rounding. May be positive, negative,
      or zero for digits past the decimal rounding.
    :param format_mode: :class:`FormatMode` indicating the formatting
      mode to be used.
    :param capital_exp_char: ``bool`` indicating whether the exponentiation
      symbol should be upper- or lower-case.
    :param exp: ``int`` indicating the value which should be used for the
      exponent. This parameter is ignored for fixed point and percent
      format modes. For engineering, engineering shifted, and binary
      iec modes, if this parameter is not consistent with the rules of
      that mode (e.g. if it is not a multiple of 3), then the exponent
      is rounded down to the nearest conforming value and a warning is
      printed.
    :param extra_si_prefixes: ``dict[int, str]`` mapping additional
      exponent values to si prefixes.
    :param extra_iec_prefixes: ``dict[int, str]`` mapping additional
      exponent values to iec prefixes
    :param add_c_prefix: ``bool`` if ``True`` adds ``{-2: 'c'}`` to
      ``extra_si_prefixes``.
    :param add_small_si_prefixes: ``bool`` if ``True`` adds
      ``{-2: 'c', -1: 'd', +1: 'da', +2: 'h'}`` to
      ``extra_si_prefixes``.
    """
    def __init__(
            self,
            *,
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
            defaults=None,
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

    def __call__(self, num: float):
        return self.format(num)

    def format(self, num: float):
        return format_float(num, self.options)

    @classmethod
    def _from_options(cls, options: FormatOptions):
        return cls(fill_mode=options.fill_mode,
                   sign_mode=options.sign_mode,
                   top_dig_place=options.top_dig_place,
                   upper_separator=options.upper_separator,
                   decimal_separator=options.decimal_separator,
                   lower_separator=options.lower_separator,
                   round_mode=options.round_mode,
                   precision=options.precision,
                   format_mode=options.format_mode,
                   capital_exp_char=options.capital_exp_char,
                   exp=options.exp,
                   use_prefix=options.use_prefix,
                   extra_si_prefixes=options.extra_si_prefixes,
                   extra_iec_prefixes=options.extra_iec_prefixes)

    @classmethod
    def from_format_spec_str(cls, fmt: str):
        options = FormatOptions.from_format_spec_str(fmt)
        return cls._from_options(options=options)
