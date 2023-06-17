from typing import Union

from sciform.modes import (SignMode, FillMode, UpperGroupingSeparators,
                           DecimalGroupingSeparators, LowerGroupingSeparators,
                           FormatMode, RoundMode, AutoExp, AutoPrec)
from sciform.format_options import FormatOptions
from sciform.formatting import format_float, format_val_unc


class Formatter:
    """
    Formatter object used to convert floats and pairs of floats into
    formatted strings. See :ref:`formatting_options` for more details on
    the available options. Any options which are not provided by the
    user will be filled with the corresponding values from the global
    default configuration.

    >>> from sciform import Formatter, FormatMode, RoundMode
    >>> sform = Formatter(format_mode=FormatMode.ENGINEERING,
    ...                   round_mode=RoundMode.SIG_FIG,
    ...                   precision=4)
    >>> print(sform(12345.678))
    12.35e+03

    The Formatter can be called with two aguments for value/uncertainty
    formatting

    >>> sform = Formatter(format_mode=FormatMode.ENGINEERING,
    ...                   round_mode=RoundMode.SIG_FIG,
    ...                   precision=2)
    >>> print(sform(12345.678, 3.4))
    (12.3457 +/- 0.0034)e+03

    The following checks are performed when creating a
    :class:`Formatter` object:

    * precision >= 1 for significant figure rounding mode
    * exp must be consistent with the format mode:

      * exp must be 0 for fixed point and percent modes
      * exp must be a multiple of 3 for engineering and shifted
        engineering modes
      * exp must be a multiple of 10 for binary iec mode

    * upper_separator must be different from decimal_separator
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
    :param capitalize: ``bool`` indicating whether the exponentiation
      symbol should be upper- or lower-case.
    :param exp: ``int`` indicating the value which should be used for the
      exponent. This parameter is ignored for fixed point and percent
      format modes. For engineering, engineering shifted, and binary
      iec modes, if this parameter is not consistent with the rules of
      that mode (e.g. if it is not a multiple of 3), then the exponent
      is rounded down to the nearest conforming value and a warning is
      printed.
    :param nan_inf_exp: ``bool`` indicating whether non-finite floats
      such as ``float('nan')`` or ``float('inf')`` should be formatted
      with exponent symbols when exponent format modes are selected.
    :param use_prefix: ``bool`` indicating if exponents should be
      replaced with either SI or IEC prefixes as appropriate.
    :param extra_si_prefixes: ``dict[int, str]`` mapping additional
      exponent values to si prefixes.
    :param extra_iec_prefixes: ``dict[int, str]`` mapping additional
      exponent values to iec prefixes
    :param add_c_prefix: ``bool`` (default ``False``) if ``True`` adds
      ``{-2: 'c'}`` to ``extra_si_prefixes``.
    :param add_small_si_prefixes: ``bool`` (default ``False``) if
      ``True`` adds ``{-2: 'c', -1: 'd', +1: 'da', +2: 'h'}`` to
      ``extra_si_prefixes``.
    :param bracket_unc: ``bool`` indicating if bracket uncertainty mode
      (e.g. ``12.34(82)`` instead of ``12.34 +/- 0.82``) should be used.
    :param val_unc_match_widths: ``bool`` indicating if the value or
      uncertainty should be left padded to ensure they are both left
      padded to the same digits place.
    :param bracket_unc_remove_seps: ``bool`` indicating if separator
      symbols should be removed from the uncertainty when using bracket
      uncertainty mode. E.g. expressing ``123.4 +/- 2.3`` as
      ``123.4(23)`` instead of ``123.4(2.3)``.
    :param unc_pm_whitespace: ``bool`` indicating if there should be
      whitespace surrounding the ``'+/-'`` symbols when formatting. E.g.
      ``123.4+/-2.3`` compared to ``123.4 +/- 2.3``.
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

    def __call__(self, val: float, unc: float = None, /):
        return self.format(val, unc)

    def format(self, val: float, unc: float = None, /):
        if unc is None:
            return format_float(val, self.options)
        else:
            return format_val_unc(val, unc, self.options)

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
                   capitalize=options.capitalize,
                   exp=options.exp,
                   nan_inf_exp=options.nan_inf_exp,
                   use_prefix=options.use_prefix,
                   extra_si_prefixes=options.extra_si_prefixes,
                   extra_iec_prefixes=options.extra_iec_prefixes,
                   bracket_unc=options.bracket_unc,
                   val_unc_match_widths=options.val_unc_match_widths,
                   bracket_unc_remove_seps=options.bracket_unc_remove_seps,
                   unc_pm_whitespace=options.unc_pm_whitespace)

    @classmethod
    def from_format_spec_str(cls, fmt: str):
        options = FormatOptions.from_format_spec_str(fmt)
        return cls._from_options(options=options)
