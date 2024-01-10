"""Main Formatter class."""

from __future__ import annotations

from decimal import Decimal
from typing import TYPE_CHECKING

from sciform.formatting import format_num, format_val_unc
from sciform.user_options import UserOptions

if TYPE_CHECKING:  # pragma: no cover
    from sciform import modes
    from sciform.format_utils import Number


class Formatter:
    """
    Class to format numbers and pairs of numbers into strings.

    :class:`Formatter` is used to convert numbers and pairs of numbers
    into formatted strings according to a variety of formatting options.
    See :ref:`formatting_options` for more details on the available
    options. Any options which are unpopulated (have the value ``None``)
    will be populated at format time by the corresponding values in the
    globally configured default options. See :ref:`global_config` for
    details about how to view and modify the global default options.

    >>> from sciform import Formatter
    >>> sform = Formatter(exp_mode="engineering", round_mode="sig_fig", ndigits=4)
    >>> print(sform(12345.678))
    12.35e+03

    The Formatter can be called with two aguments for value/uncertainty
    formatting

    >>> sform = Formatter(exp_mode="engineering", round_mode="sig_fig", ndigits=2)
    >>> print(sform(12345.678, 3.4))
    (12.3457 ± 0.0034)e+03
    """

    def __init__(  # noqa: PLR0913
        self: Formatter,
        *,
        exp_mode: modes.UserExpMode | None = None,
        exp_val: int | type(modes.AutoExpVal) | None = None,
        round_mode: modes.UserRoundMode | None = None,
        ndigits: int | type(modes.AutoDigits) | None = None,
        upper_separator: modes.UserUpperSeparators | None = None,
        decimal_separator: modes.UserDecimalSeparators | None = None,
        lower_separator: modes.UserLowerSeparators | None = None,
        sign_mode: modes.UserSignMode | None = None,
        fill_char: modes.UserFillChar | None = None,
        left_pad_dec_place: int | None = None,
        exp_format: modes.UserExpFormat | None = None,
        extra_si_prefixes: dict[int, str] | None = None,
        extra_iec_prefixes: dict[int, str] | None = None,
        extra_parts_per_forms: dict[int, str] | None = None,
        capitalize: bool | None = None,
        superscript: bool | None = None,
        latex: bool | None = None,
        nan_inf_exp: bool | None = None,
        paren_uncertainty: bool | None = None,
        pdg_sig_figs: bool | None = None,
        left_pad_matching: bool | None = None,
        paren_uncertainty_separators: bool | None = None,
        pm_whitespace: bool | None = None,
        add_c_prefix: bool = False,
        add_small_si_prefixes: bool = False,
        add_ppth_form: bool = False,
    ) -> None:
        r"""
        Create a new ``Formatter``.

        The following checks are performed when creating a new
        :class:`Formatter` object:

        * ``ndigits`` >= 1 for significant figure rounding mode
        * ``exp_val`` must be consistent with the exponent mode. If
          ``exp_val`` is specified (i.e. not ``None``) and ``exp_val``
          is not ``AutoExpVal`` then

          * ``exp_val`` must be 0 for fixed point and percent modes
          * ``exp_val`` must be a multiple of 3 for engineering and
            shifted engineering modes
          * ``exp_val`` must be a multiple of 10 for binary iec mode

        * ``upper_separator`` may be any of ``['', ',', '.', ' ', '_']``
          but must be different from ``decimal_separator``
        * ``decimal_separator`` may be any of ``['.', ',']``
        * ``lower_separator`` may be any of ``['', ' ', '_']``

        :param exp_mode: Specify the formatting mode.
        :type exp_mode: ``Literal['fixed_point', 'percent',
          'scientific', 'engineering', 'engineering_shifted', 'binary',
          'binary_iec'] | None``
        :param exp_val: Indicates how the exponent value should be
          chosen. If an integer is specified, the value must be 0 for
          fixed point and percent modes, an integer multiple of 3 for
          engineering and engineering shifted modes, and an integer
          multiple of 10 for binary IEC mode.
        :type exp_val: ``int | type[AutoExpVal] | None``
        :param round_mode: Indicate how to round numbers during
          formatting.
        :type round_mode: ``Literal['sig_fig', 'dec_place'] | None``
        :param ndigits: Indicate how the many significant digits or the
          decimal place to use for rounding. Must be >= 1 for
          significant figure rounding. Can be any integer for decimal
          place rounding.
        :type ndigits: ``int | type[AutoDigits] | None``
        :param upper_separator: Separator character to be used to group
          digits above the decimal symbol.
        :type upper_separator: ``Literal['', ',', '.', ' ', '_'] | None``
        :param decimal_separator: Separator character to be used as the
          decimal symbol. Note that ``decimal_separator`` cannot be the
          same as ``upper_separator``
        :type decimal_separator: ``Literal['.', ','] | None``
        :param lower_separator: Separator character to be used to group
          digits below the decimal symbol.
        :type lower_separator: ``Literal['', ' ', '_'] | None``
        :param sign_mode: Indicate sign symbol behavior.
        :type sign_mode: ``Literal['-', '+', ' '] | None``
        :param fill_char: Indicate whether to fill with zeros or spaces.
        :type fill_char: ``Literal[' ', '0'] | None``
        :param left_pad_dec_place: Positive ``int`` indicating the
          decimal place to which the string will be left padded before
          the sign symbol. 0 corresponds to the ones place, 1
          corresponds to the tens place etc. E.g.
          ``left_pad_dec_place=4`` will convert ``12`` into
          ``00012``.
        :type left_pad_dec_place: ``int | None``
        :param exp_format: Indicate how exponents should be presented.
        :type exp_format: ``Literal['standard', 'prefix', 'parts_per'] | None``
        :param extra_si_prefixes: Dictionary mapping additional exponent
          values to si prefixes. Entries overwrite default values. A
          value of ``None`` means that exponent will not be converted.
        :type extra_si_prefixes: ``dict[int, Union[str, None]] | None``
        :param extra_iec_prefixes: Dictionary mapping additional
          exponent values to iec prefixes. Entries overwrite default
          values. A value of ``None`` means that exponent will not be
          converted.
        :type extra_iec_prefixes: ``dict[int, Union[str, None]] | None``
        :param extra_parts_per_forms: Dictionary mapping additional
          exponent values to "parts-per" forms. Entries overwrite
          default values. A value of ``None`` means that exponent will
          not be converted.
        :type extra_parts_per_forms: ``dict[int, Union[str, None]] | None``
        :param capitalize: Flag indicating whether the exponentiation
          symbol should be upper- or lower-case.
        :type capitalize: ``bool | None``
        :param superscript: Flag indicating if the exponent string
          should be converted into superscript notation. E.g.
          ``'1.23e+02'`` is converted to ``'1.23×10²'``
        :type superscript: ``bool | None``
        :param latex: Flag indicating if the resulting string should be
          converted into a latex parseable code, e.g.
          ``'\\left(1.23 \\pm 0.01\\right)\\times 10^{2}'``.
        :type latex: ``bool | None``
        :param nan_inf_exp: Flag indicating whether non-finite numbers
          such as ``float('nan')`` or ``float('inf')`` should be
          formatted with exponent symbols when exponent modes including
          exponent symbols are selected.
        :type nan_inf_exp: ``bool | None``
        :param paren_uncertainty: Flag indicating if parentheses
          uncertainty mode (e.g. ``12.34(82)`` instead of
          ``12.34 ± 0.82``) should be used.
        :type paren_uncertainty: ``bool | None``
        :param pdg_sig_figs: Flag indicating whether the
          particle-data-group conventions should be used to
          automatically determine the number of significant figures to
          use for uncertainty. Ignored for single value formatting.
        :type pdg_sig_figs: ``bool | None``
        :param left_pad_matching: Flag indicating if the value or
          uncertainty should be left padded to ensure they are both left
          padded to the same digits place.
        :type left_pad_matching: ``bool | None``
        :param paren_uncertainty_separators: Flag indicating if
          separator symbols should be included in the uncertainty when
          using parentheses uncertainty mode. E.g. expressing
          ``123.4 ± 2.3`` either as ``123.4(2.3)`` or ``123.4(23)``.
        :type paren_uncertainty_separators: ``bool | None``
        :param pm_whitespace: Flag indicating if there should be
          whitespace surrounding the ``'±'`` symbols when formatting.
          E.g. ``123.4±2.3`` compared to ``123.4 ± 2.3``.
        :type pm_whitespace: ``bool | None``
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
        """  # noqa: RUF002
        self._user_options = UserOptions(
            exp_mode=exp_mode,
            exp_val=exp_val,
            round_mode=round_mode,
            ndigits=ndigits,
            upper_separator=upper_separator,
            decimal_separator=decimal_separator,
            lower_separator=lower_separator,
            sign_mode=sign_mode,
            fill_char=fill_char,
            left_pad_dec_place=left_pad_dec_place,
            exp_format=exp_format,
            extra_si_prefixes=extra_si_prefixes,
            extra_iec_prefixes=extra_iec_prefixes,
            extra_parts_per_forms=extra_parts_per_forms,
            capitalize=capitalize,
            superscript=superscript,
            latex=latex,
            nan_inf_exp=nan_inf_exp,
            paren_uncertainty=paren_uncertainty,
            pdg_sig_figs=pdg_sig_figs,
            left_pad_matching=left_pad_matching,
            paren_uncertainty_separators=paren_uncertainty_separators,
            pm_whitespace=pm_whitespace,
            add_c_prefix=add_c_prefix,
            add_small_si_prefixes=add_small_si_prefixes,
            add_ppth_form=add_ppth_form,
        )

    def __call__(
        self: Formatter,
        value: Number,
        uncertainty: Number | None = None,
        /,
    ) -> str:
        """
        Format a value or value/uncertainty pair.

        :param value: Value to be formatted.
        :type value: ``Decimal | float | int | str``
        :param uncertainty: Optional uncertainty to be formatted.
        :type uncertainty: ``Decimal | float | int | str | None``
        """
        rendered_options = self._user_options.render()
        if uncertainty is None:
            output = format_num(Decimal(str(value)), rendered_options)
        else:
            output = format_val_unc(
                Decimal(str(value)),
                Decimal(str(uncertainty)),
                rendered_options,
            )
        return output
