from decimal import Decimal
from typing import Optional, Union

from sciform import modes
from sciform.user_options import UserOptions
from sciform.formatting import format_num, format_val_unc
from sciform.format_utils import Number


# TODO: Support SciNum/SciNumUnc input to formatter?


class Formatter:
    """
    :class:`Formatter` is used to convert numbers and pairs of numbers
    into formatted strings according to a variety of formatting options.
    See :ref:`formatting_options` for more details on the available
    options. Any options which are unpopulated (have the value ``None``)
    will be populated at format time by the corresponding values in the
    globally configured default options. See :ref:`global_config` for
    details about how to view and modify the global default options.

    >>> from sciform import Formatter
    >>> sform = Formatter(exp_mode='engineering',
    ...                   round_mode='sig_fig',
    ...                   ndigits=4)
    >>> print(sform(12345.678))
    12.35e+03

    The Formatter can be called with two aguments for value/uncertainty
    formatting

    >>> sform = Formatter(exp_mode='engineering',
    ...                   round_mode='sig_fig',
    ...             ndigits=2)
    >>> print(sform(12345.678, 3.4))
    (12.3457 ± 0.0034)e+03

    The following checks are performed when creating a new
    :class:`Formatter` object:

    * ``ndigits`` >= 1 for significant figure rounding mode
    * ``exp_val`` must be consistent with the exponent mode. If
      ``exp_val`` is specified (i.e. not ``None``) and ``exp_val`` is
      not ``AutoExpVal`` then

      * ``exp_val`` must be 0 for fixed point and percent modes
      * ``exp_val`` must be a multiple of 3 for engineering and shifted
        engineering modes
      * ``exp_val`` must be a multiple of 10 for binary iec mode

    * ``upper_separator`` may be any of ``['', ',', '.', ' ', '_']`` but
      must be different from ``decimal_separator``
    * ``decimal_separator`` may be any of ``['.', ',']``
    * ``lower_separator`` may be any of ``['', ' ', '_']``
    * if ``pdg_sig_figs=True`` then ``ndigits=None`` or
      ``ndigits=AutoDigits``.

    :param exp_mode: Specify the formatting mode.
    :type exp_mode: ``Literal['fixed_point', 'percent', 'scientific',
      'engineering', 'engineering_shifted', 'binary', 'binary_iec']``
    :param exp_val: Indicates how the exponent value should be chosen.
      If an integer is specified, the value must be 0 for fixed point
      and percent modes, an integer multiple of 3 for engineering and
      engineering shifted modes, and an integer multiple of 10 for
      binary IEC mode.
    :type exp_val: ``Union[int, type[AutoExpVal]]``
    :param round_mode: Indicate how to round numbers during formatting.
    :type round_mode: ``Literal['sig_fig', 'dec_place']``
    :param ndigits: Indicate how the many significant digits or the
      decimal place to use for rounding. Must be >= 1 for significant
      figure rounding. Can be any integer for decimal place rounding.
    :type ndigits: ``Union[int, type[AutoDigits]]``
    :param upper_separator: Separator character to be used to group
      digits above the decimal symbol.
    :type upper_separator: ``Literal['', ',', '.', ' ', '_']``
    :param decimal_separator: Separator character to be used as the
      decimal symbol. Note that ``decimal_separator`` cannot be the same
      as ``upper_separator``
    :type decimal_separator: ``Literal['.', ',']``
    :param lower_separator: Separator character to be used to group
      digits below the decimal symbol.
    :type lower_separator: ``Literal['', ' ', '_']``
    :param sign_mode: :class:`SignMode` indicating sign symbol behavior.
    :type sign_mode: ``Literal['-', '+', ' ']``
    :param fill_mode: :class:`FillMode` indicating whether to fill with
      zeros or spaces.
    :type fill_mode: ``Literal[' ', '0']``
    :param top_dig_place: Positive ``int`` indicating the digits place
      to which the string will be left padded before the sign symbol. 0
      corresponds to the ones place, 1 corresponds to the tens place
      etc. E.g. ``top_dig_place=4`` will convert ``12`` into ``00012``.
    :type top_dig_place: ``int``
    :param exp_format: :class:`ExpFormat` indicating how exponents
      should be presented.
    :type exp_format: ``Literal['standard', 'prefix', 'parts_per']``
    :param extra_si_prefixes: Dictionary mapping additional exponent
      values to si prefixes. Entries overwrite default values. A value
      of ``None`` means that exponent will not be converted.
    :type extra_si_prefixes: ``dict[int, Union[str, None]]``
    :param extra_iec_prefixes: Dicitonary mapping additional exponent
      values to iec prefixes. Entries overwrite default values. A value
      of ``None`` means that exponent will not be converted.
    :type extra_iec_prefixes: ``dict[int, Union[str, None]]``
    :param extra_parts_per_forms: Dictionary mapping additional exponent
      values to "parts-per" forms. Entries overwrite default values. A
      value of ``None`` means that exponent will not be converted.
    :type extra_parts_per_forms: ``dict[int, Union[str, None]]``
    :param capitalize: Flag indicating whether the exponentiation symbol
      should be upper- or lower-case.
    :type capitalize: ``bool``
    :param superscript_exp: Flag indicating if the exponent string
      should be converted into superscript notation. E.g. ``'1.23e+02'``
      is converted to ``'1.23×10²'``
    :type superscript_exp: ``bool``
    :param latex: Flag indicating if the resulting string should be
      converted into a latex parseable code, e.g.
      ``'\\left(1.23 \\pm 0.01\\right)\\times 10^{2}'``.
    :type latex: ``bool``
    :param nan_inf_exp: Flag indicating whether non-finite numbers such
      as ``float('nan')`` or ``float('inf')`` should be formatted with
      exponent symbols when exponent modes including exponent symbols
      are selected.
    :type nan_inf_exp: ``bool``
    :param bracket_unc: Flag indicating if bracket uncertainty mode
      (e.g. ``12.34(82)`` instead of ``12.34 ± 0.82``) should be
      used.
    :type bracket_unc: ``bool``
    :param pdg_sig_figs: Flag indicating whether the particle-data-group
      conventions should be used to automatically determine the number
      of significant figures to use for uncertainty.
    :type pdg_sig_figs: ``bool``
    :param val_unc_match_widths: Flag indicating if the value or
      uncertainty should be left padded to ensure they are both left
      padded to the same digits place.
    :type val_unc_match_widths: ``bool``
    :param bracket_unc_remove_seps: Flag indicating if separator symbols
      should be removed from the uncertainty when using bracket
      uncertainty mode. E.g. expressing ``123.4 ± 2.3`` as
      ``123.4(23)`` instead of ``123.4(2.3)``.
    :type bracket_unc_remove_seps: ``bool``
    :param unc_pm_whitespace: Flag indicating if there should be
      whitespace surrounding the ``'±'`` symbols when formatting. E.g.
      ``123.4±2.3`` compared to ``123.4 ± 2.3``.
    :type unc_pm_whitespace: ``bool``
    :param add_c_prefix: (default ``False``) If ``True``, adds
      ``{-2: 'c'}`` to ``extra_si_prefixes``.
    :type add_c_prefix: ``bool``
    :param add_small_si_prefixes: (default ``False``) If ``True``, adds
      ``{-2: 'c', -1: 'd', +1: 'da', +2: 'h'}`` to
      ``extra_si_prefixes``.
    :type add_small_si_prefixes: ``bool``
    :param add_ppth_form: (default ``False``) if ``True``, adds
      ``{-3: 'ppth'}`` to ``extra_parts_per_forms``.
    :type add_ppth_form: ``bool``
    """
    def __init__(
            self,
            exp_mode: Optional[modes.UserExpMode] = None,
            exp_val: Optional[Union[int, type(modes.AutoExpVal)]] = None,
            round_mode: Optional[modes.UserRoundMode] = None,
            ndigits: Optional[Union[int, type(modes.AutoDigits)]] = None,
            upper_separator: Optional[modes.UserUpperSeparators] = None,
            decimal_separator: Optional[modes.UserDecimalSeparators] = None,
            lower_separator: Optional[modes.UserLowerSeparators] = None,
            sign_mode: Optional[modes.UserSignMode] = None,
            fill_mode: Optional[modes.UserFillMode] = None,
            top_dig_place: Optional[int] = None,
            exp_format: Optional[modes.UserExpFormat] = None,
            extra_si_prefixes: Optional[dict[int, str]] = None,
            extra_iec_prefixes: Optional[dict[int, str]] = None,
            extra_parts_per_forms: Optional[dict[int, str]] = None,
            capitalize: Optional[bool] = None,
            superscript_exp: Optional[bool] = None,
            latex: Optional[bool] = None,
            nan_inf_exp: Optional[bool] = None,
            bracket_unc: Optional[bool] = None,
            pdg_sig_figs: Optional[bool] = None,
            val_unc_match_widths: Optional[bool] = None,
            bracket_unc_remove_seps: Optional[bool] = None,
            unc_pm_whitespace: Optional[bool] = None,
            add_c_prefix: bool = False,
            add_small_si_prefixes: bool = False,
            add_ppth_form: bool = False,
    ):
        self._user_options = UserOptions(
            exp_mode=exp_mode,
            exp_val=exp_val,
            round_mode=round_mode,
            ndigits=ndigits,
            upper_separator=upper_separator,
            decimal_separator=decimal_separator,
            lower_separator=lower_separator,
            sign_mode=sign_mode,
            fill_mode=fill_mode,
            top_dig_place=top_dig_place,
            exp_format=exp_format,
            extra_si_prefixes=extra_si_prefixes,
            extra_iec_prefixes=extra_iec_prefixes,
            extra_parts_per_forms=extra_parts_per_forms,
            capitalize=capitalize,
            superscript_exp=superscript_exp,
            latex=latex,
            nan_inf_exp=nan_inf_exp,
            bracket_unc=bracket_unc,
            pdg_sig_figs=pdg_sig_figs,
            val_unc_match_widths=val_unc_match_widths,
            bracket_unc_remove_seps=bracket_unc_remove_seps,
            unc_pm_whitespace=unc_pm_whitespace,
            add_c_prefix=add_c_prefix,
            add_small_si_prefixes=add_small_si_prefixes,
            add_ppth_form=add_ppth_form
        )

    def __call__(self, value: Number, uncertainty: Number = None, /):
        rendered_options = self._user_options.render()
        if uncertainty is None:
            return format_num(Decimal(str(value)), rendered_options)
        else:
            return format_val_unc(Decimal(str(value)),
                                  Decimal(str(uncertainty)),
                                  rendered_options)

    # TODO: print_options and print_resolved_options?
