from typing import Union, get_args
from dataclasses import dataclass, asdict
from pprint import pprint

from sciform.modes import (FillMode, SignMode, GroupingSeparator,
                           UpperGroupingSeparators, LowerGroupingSeparators,
                           DecimalGroupingSeparators, RoundMode, ExpMode,
                           AutoExp, AutoPrec)


@dataclass(frozen=True)
class RenderedFormatOptions:
    exp_mode: ExpMode
    exp: Union[int, type(AutoExp)]
    round_mode: RoundMode
    precision: Union[int, type(AutoPrec)]
    upper_separator: UpperGroupingSeparators
    decimal_separator: DecimalGroupingSeparators
    lower_separator: LowerGroupingSeparators
    sign_mode: SignMode
    fill_mode: FillMode
    top_dig_place: int
    prefix_exp: bool
    parts_per_exp: bool
    extra_si_prefixes: dict[int, str]
    extra_iec_prefixes: dict[int, str]
    extra_parts_per_forms: dict[int, str]
    capitalize: bool
    superscript_exp: bool
    latex: bool
    nan_inf_exp: bool
    bracket_unc: bool
    pdg_sig_figs: bool
    val_unc_match_widths: bool
    bracket_unc_remove_seps: bool
    unicode_pm: bool
    unc_pm_whitespace: bool


ExpReplaceDict = dict[int, Union[str, None]]


class FormatOptions:
    # TODO: __repr__
    """
    :class:`FormatOptions` stores all the configuration options used to
    format numbers and number/uncertainty pairs. See
    :ref:`formatting_options` for more details on the available options.
    :class:`FormatOptions` are used to create :class:`Formatter`
    instances and to modify the global default configuration.

    It is not necessary to provide input for all options. There are two
    mechanisms for filling of any un-supplied options. First, during
    initialization, the user can pass in another :class:`FormatOptions`
    instance as a ``template``. In this case any populated options for
    the ``template`` will be used to populate corresponding unpopulated
    options for the new :class:`FormatOptions`. Second, at format time
    any remaining unfilled options will be populated with the global
    default options. See :ref:`global_config` for details about how to
    view and modify the global default options.

    The following checks are performed when creating a new
    :class:`FormatOptions` object:

    * ``precision`` >= 1 for significant figure rounding mode
    * ``exp`` must be consistent with the exponent mode:

      * ``exp`` must be 0 for fixed point and percent modes
      * ``exp`` must be a multiple of 3 for engineering and shifted
        engineering modes
      * ``exp`` must be a multiple of 10 for binary iec mode

    * ``upper_separator`` may be any :class:`GroupingSeparator` but must
      be different from ``decimal_separator``
    * ``decimal_separator`` may only be :class:`GroupingSeparator.POINT`
      or :class:`GroupingSeparator.COMMA`
    * ``lower_separator`` may only be :class:`GroupingSeparator.NONE`,
      :class:`GroupingSeparator.SPACE`, or
      :class:`GroupingSeparator.UNDERSCORE`
    * Only one of ``prefix_exp`` and ``parts_per_exp`` may be selected.

    :param template: :class:`FormatOptions` instance to use to populate
      unfilled options.
    :param exp_mode: :class:`ExpMode` indicating the formatting
      mode to be used.
    :param exp: :class:`int` or :class:`AutoExp` indicating the value which
      should be used for the exponent. This parameter is ignored for the
      fixed point exponent mode. For engineering, engineering shifted,
      and binary iec modes, if this parameter is not consistent with the
      rules of that mode (e.g. if it is not a multiple of 3), then the
      exponent is rounded down to the nearest conforming value and a
      warning is printed.
    :param round_mode: :class:`RoundMode` indicating whether to round
      the number based on significant figures or digits past the
      decimal point
    :param precision: :class:`int` or :class:`AutoPrec` sentinel indicating
      how many significant figures or digits past the decimal point to
      include for rounding. Must be >= 1 for significant figure
      rounding. May be any integer for digits-past-the-decimal rounding.
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
      or :class:`GroupingSeparator.UNDERSCORE`.
    :param sign_mode: :class:`SignMode` indicating sign
      symbol behavior.
    :param fill_mode: :class:`FillMode` indicating whether
      to fill with zeros or spaces.
    :param top_dig_place: Positive ``int`` indicating the digits place
      to which the string will be left padded before the sign symbol. 0
      corresponds to the ones place, 1 corresponds to the tens place
      etc. E.g. ``top_dig_place=4`` will convert ``12`` into ``00012``.
    :param prefix_exp: :class:`bool` indicating if exponents should be
      replaced with either SI or IEC prefixes as appropriate.
    :param parts_per_exp: :class:`bool` indicating if "parts-per" exponent
      translations should be used.
    :param extra_si_prefixes: ``dict[int, Union[str, None]]`` mapping
      additional exponent values to si prefixes. Entries overwrite
      default values. A value of ``None`` means that exponent will not
      be converted.
    :param extra_iec_prefixes: ``dict[int, Union[str, None]]`` mapping
      additional exponent values to iec prefixes. Entries overwrite
      default values. A value of ``None`` means that exponent will not
      be converted.
    :param extra_parts_per_forms: ``dict[int, Union[str, None]]``
      mapping additional exponent values to "parts-per" forms. Entries
      overwrite default values. A value of ``None`` means that exponent
      will not be converted.
    :param capitalize: :class:`bool` indicating whether the exponentiation
      symbol should be upper- or lower-case.
    :param superscript_exp: :class:`bool` indicating if the exponent string
      should be converted into superscript notation. E.g. ``'1.23e+02'``
      is converted to ``'1.23×10²'``
    :param latex: :class:`bool` indicating if the resulting string should be
      converted into a latex parseable code, e.g.
      ``'\\left(1.23 \\pm 0.01\\right)\\times 10^{2}'``.
    :param nan_inf_exp: :class:`bool` indicating whether non-finite numbers
      such as ``float('nan')`` or ``float('inf')`` should be formatted
      with exponent symbols when exponent modes including exponent
      symbols are selected.
    :param bracket_unc: :class:`bool` indicating if bracket uncertainty mode
      (e.g. ``12.34(82)`` instead of ``12.34 +/- 0.82``) should be used.
    :param pdg_sig_figs: :class:`bool` indicating whether the
      particle-data-group conventions should be used to automatically
      determine the number of significant figures to use for
      uncertainty.
    :param val_unc_match_widths: :class:`bool` indicating if the value or
      uncertainty should be left padded to ensure they are both left
      padded to the same digits place.
    :param bracket_unc_remove_seps: :class:`bool` indicating if separator
      symbols should be removed from the uncertainty when using bracket
      uncertainty mode. E.g. expressing ``123.4 +/- 2.3`` as
      ``123.4(23)`` instead of ``123.4(2.3)``.
    :param unicode_pm: :class:`bool` indicating if the '+/-' separator should
      be replaced with the unicode plus minus symbol '±'.
    :param unc_pm_whitespace: :class:`bool` indicating if there should be
      whitespace surrounding the ``'+/-'`` symbols when formatting. E.g.
      ``123.4+/-2.3`` compared to ``123.4 +/- 2.3``.
    :param add_c_prefix: :class:`bool` (default ``False``) if ``True`` adds
      ``{-2: 'c'}`` to ``extra_si_prefixes``.
    :param add_small_si_prefixes: ``bool`` (default ``False``) if
      ``True`` adds ``{-2: 'c', -1: 'd', +1: 'da', +2: 'h'}`` to
      ``extra_si_prefixes``.
    :param add_ppth_form: :class:`bool` (default ``False``) if ``True`` adds
      ``{-3: 'ppth'}`` to ``extra_parts_per_forms``.
    """
    def __init__(
            self,
            *,
            template: Union['FormatOptions'] = None,
            exp_mode: ExpMode = None,
            exp: Union[int, type(AutoExp)] = None,
            round_mode: RoundMode = None,
            precision: Union[int, type(AutoPrec)] = None,
            upper_separator: UpperGroupingSeparators = None,
            decimal_separator: DecimalGroupingSeparators = None,
            lower_separator: LowerGroupingSeparators = None,
            sign_mode: SignMode = None,
            fill_mode: FillMode = None,
            top_dig_place: int = None,
            prefix_exp: bool = None,
            parts_per_exp: bool = None,
            extra_si_prefixes: ExpReplaceDict = None,
            extra_iec_prefixes: ExpReplaceDict = None,
            extra_parts_per_forms: ExpReplaceDict = None,
            capitalize: bool = None,
            superscript_exp: bool = None,
            latex: bool = None,
            nan_inf_exp: bool = None,
            bracket_unc: bool = None,
            pdg_sig_figs: bool = None,
            val_unc_match_widths: bool = None,
            bracket_unc_remove_seps: bool = None,
            unicode_pm: bool = None,
            unc_pm_whitespace: bool = None,
            add_c_prefix: bool = False,
            add_small_si_prefixes: bool = False,
            add_ppth_form: bool = False
    ):
        if round_mode is RoundMode.SIG_FIG:
            if isinstance(precision, int):
                if precision < 1:
                    raise ValueError(f'Precision must be >= 1 for sig fig '
                                     f'rounding, not {precision}.')

        if exp is not AutoExp and exp is not None:
            if exp_mode is ExpMode.FIXEDPOINT or exp_mode is ExpMode.PERCENT:
                if exp != 0:
                    raise ValueError(f'Exponent must must be 0, not '
                                     f'exp={exp}, for fixed point and percent '
                                     f'exponent modes.')
            elif (exp_mode is ExpMode.ENGINEERING
                  or exp_mode is ExpMode.ENGINEERING_SHIFTED):
                if exp % 3 != 0:
                    raise ValueError(f'Exponent must be a multiple of 3, not '
                                     f'exp={exp}, for engineering exponent '
                                     f'modes.')
            elif exp_mode is ExpMode.BINARY_IEC:
                if exp % 10 != 0:
                    raise ValueError(f'Exponent must be a multiple of 10, not '
                                     f'exp={exp}, for binary IEC '
                                     f'exponent mode.')

        if upper_separator is not None:
            if upper_separator not in get_args(UpperGroupingSeparators):
                raise ValueError(f'upper_separator must be in '
                                 f'{get_args(UpperGroupingSeparators)}, not '
                                 f'{upper_separator}.')
            if upper_separator is decimal_separator:
                raise ValueError(f'upper_separator and decimal_separator '
                                 f'({upper_separator}) cannot be equal.')

        if decimal_separator is not None:
            if decimal_separator not in get_args(DecimalGroupingSeparators):
                raise ValueError(f'upper_separator must be in '
                                 f'{get_args(DecimalGroupingSeparators)}, not '
                                 f'{upper_separator}.')

        if lower_separator is not None:
            if lower_separator not in get_args(LowerGroupingSeparators):
                raise ValueError(f'upper_separator must be in '
                                 f'{get_args(LowerGroupingSeparators)}, not '
                                 f'{upper_separator}.')

        if prefix_exp is not None and parts_per_exp is not None:
            if prefix_exp and parts_per_exp:
                raise ValueError('Only one of prefix exponent and parts-per '
                                 'exponent modes may be selected.')

        if add_c_prefix:
            if extra_si_prefixes is None:
                extra_si_prefixes = dict()
            if -2 not in extra_si_prefixes:
                extra_si_prefixes[-2] = 'c'

        if add_small_si_prefixes:
            if extra_si_prefixes is None:
                extra_si_prefixes = dict()
            if -2 not in extra_si_prefixes:
                extra_si_prefixes[-2] = 'c'
            if -1 not in extra_si_prefixes:
                extra_si_prefixes[-1] = 'd'
            if +1 not in extra_si_prefixes:
                extra_si_prefixes[+1] = 'da'
            if +2 not in extra_si_prefixes:
                extra_si_prefixes[+2] = 'h'

        if add_ppth_form:
            if extra_parts_per_forms is None:
                extra_parts_per_forms = dict()
            if -3 not in extra_parts_per_forms:
                extra_parts_per_forms[-3] = 'ppth'

        if template is None:
            self.exp_mode = exp_mode
            self.exp = exp
            self.round_mode = round_mode
            self.precision = precision
            self.upper_separator = upper_separator
            self.decimal_separator = decimal_separator
            self.lower_separator = lower_separator
            self.sign_mode = sign_mode
            self.fill_mode = fill_mode
            self.top_dig_place = top_dig_place
            self.prefix_exp = prefix_exp
            self.parts_per_exp = parts_per_exp
            self.extra_si_prefixes = extra_si_prefixes
            self.extra_iec_prefixes = extra_iec_prefixes
            self.extra_parts_per_forms = extra_parts_per_forms
            self.capitalize = capitalize
            self.superscript_exp = superscript_exp
            self.latex = latex
            self.nan_inf_exp = nan_inf_exp
            self.bracket_unc = bracket_unc
            self.pdg_sig_figs = pdg_sig_figs
            self.val_unc_match_widths = val_unc_match_widths
            self.bracket_unc_remove_seps = bracket_unc_remove_seps
            self.unicode_pm = unicode_pm
            self.unc_pm_whitespace = unc_pm_whitespace
        else:
            self.exp_mode = (template.exp_mode if exp_mode is None else exp_mode)
            self.exp = template.exp if exp is None else exp
            self.round_mode = template.round_mode if round_mode is None else round_mode
            self.precision = template.precision if precision is None else precision
            self.upper_separator = template.upper_separator if upper_separator is None else upper_separator
            self.decimal_separator = template.decimal_separator if decimal_separator is None else decimal_separator
            self.lower_separator = template.lower_separator if lower_separator is None else lower_separator
            self.sign_mode = template.sign_mode if sign_mode is None else sign_mode
            self.fill_mode = template.fill_mode if fill_mode is None else fill_mode
            self.top_dig_place = template.top_dig_place if top_dig_place is None else top_dig_place
            self.prefix_exp = template.prefix_exp if prefix_exp is None else prefix_exp
            self.parts_per_exp = template.parts_per_exp if parts_per_exp is None else parts_per_exp
            self.extra_si_prefixes = template.extra_si_prefixes if extra_si_prefixes is None else extra_si_prefixes
            self.extra_iec_prefixes = template.extra_iec_prefixes if extra_iec_prefixes is None else extra_iec_prefixes
            self.extra_parts_per_forms = template.extra_parts_per_forms if extra_parts_per_forms is None else extra_parts_per_forms
            self.capitalize = template.capitalize if capitalize is None else capitalize
            self.superscript_exp = template.superscript_exp if superscript_exp is None else superscript_exp
            self.latex = template.latex if latex is None else latex
            self.nan_inf_exp = template.nan_inf_exp if nan_inf_exp is None else nan_inf_exp
            self.bracket_unc = template.bracket_unc if bracket_unc is None else bracket_unc
            self.pdg_sig_figs = template.pdg_sig_figs if pdg_sig_figs is None else pdg_sig_figs
            self.val_unc_match_widths = template.val_unc_match_widths if val_unc_match_widths is None else val_unc_match_widths
            self.bracket_unc_remove_seps = template.bracket_unc_remove_seps if bracket_unc_remove_seps is None else bracket_unc_remove_seps
            self.unicode_pm = template.unicode_pm if unicode_pm is None else unicode_pm
            self.unc_pm_whitespace = template.unc_pm_whitespace if unc_pm_whitespace is None else unc_pm_whitespace

    def render(self) -> RenderedFormatOptions:
        gdf = get_global_defaults()
        rendered_format_options = RenderedFormatOptions(
          exp_mode=gdf.exp_mode if self.exp_mode is None else self.exp_mode,
          exp=gdf.exp if self.exp is None else self.exp,
          round_mode=gdf.round_mode if self.round_mode is None else self.round_mode,
          precision=gdf.precision if self.precision is None else self.precision,
          upper_separator=gdf.upper_separator if self.upper_separator is None else self.upper_separator,
          decimal_separator=gdf.decimal_separator if self.decimal_separator is None else self.decimal_separator,
          lower_separator=gdf.lower_separator if self.lower_separator is None else self.lower_separator,
          sign_mode=gdf.sign_mode if self.sign_mode is None else self.sign_mode,
          fill_mode=gdf.fill_mode if self.fill_mode is None else self.fill_mode,
          top_dig_place=gdf.top_dig_place if self.top_dig_place is None else self.top_dig_place,
          prefix_exp=gdf.prefix_exp if self.prefix_exp is None else self.prefix_exp,
          parts_per_exp=gdf.parts_per_exp if self.parts_per_exp is None else self.parts_per_exp,
          extra_si_prefixes=gdf.extra_si_prefixes if self.extra_si_prefixes is None else self.extra_si_prefixes,
          extra_iec_prefixes=gdf.extra_iec_prefixes if self.extra_iec_prefixes is None else self.extra_iec_prefixes,
          extra_parts_per_forms=gdf.extra_parts_per_forms if self.extra_parts_per_forms is None else self.extra_parts_per_forms,
          capitalize=gdf.capitalize if self.capitalize is None else self.capitalize,
          superscript_exp=gdf.superscript_exp if self.superscript_exp is None else self.superscript_exp,
          latex=gdf.latex if self.latex is None else self.latex,
          nan_inf_exp=gdf.nan_inf_exp if self.nan_inf_exp is None else self.nan_inf_exp,
          bracket_unc=gdf.bracket_unc if self.bracket_unc is None else self.bracket_unc,
          pdg_sig_figs=gdf.pdg_sig_figs if self.pdg_sig_figs is None else self.pdg_sig_figs,
          val_unc_match_widths=gdf.val_unc_match_widths if self.val_unc_match_widths is None else self.val_unc_match_widths,
          bracket_unc_remove_seps=gdf.bracket_unc_remove_seps if self.bracket_unc_remove_seps is None else self.bracket_unc_remove_seps,
          unicode_pm=gdf.unicode_pm if self.unicode_pm is None else self.unicode_pm,
          unc_pm_whitespace=gdf.unc_pm_whitespace if self.unc_pm_whitespace is None else self.unc_pm_whitespace
        )
        return rendered_format_options


DEFAULT_PKG_OPTIONS = RenderedFormatOptions(
    exp_mode=ExpMode.FIXEDPOINT,
    exp=AutoExp,
    round_mode=RoundMode.SIG_FIG,
    precision=AutoPrec,
    upper_separator=GroupingSeparator.NONE,
    decimal_separator=GroupingSeparator.POINT,
    lower_separator=GroupingSeparator.NONE,
    sign_mode=SignMode.NEGATIVE,
    fill_mode=FillMode.SPACE,
    top_dig_place=0,
    prefix_exp=False,
    parts_per_exp=False,
    extra_si_prefixes=dict(),
    extra_iec_prefixes=dict(),
    extra_parts_per_forms=dict(),
    capitalize=False,
    superscript_exp=False,
    latex=False,
    nan_inf_exp=False,
    bracket_unc=False,
    pdg_sig_figs=False,
    val_unc_match_widths=False,
    bracket_unc_remove_seps=False,
    unicode_pm=False,
    unc_pm_whitespace=True
)


GLOBAL_DEFAULT_OPTIONS = DEFAULT_PKG_OPTIONS


def get_global_defaults() -> RenderedFormatOptions:
    return GLOBAL_DEFAULT_OPTIONS


def print_global_defaults():
    """
    Print current global default formatting options as a dictionary.
    """
    pprint(asdict(get_global_defaults()), sort_dicts=False)


def set_global_defaults(format_options: FormatOptions):
    global GLOBAL_DEFAULT_OPTIONS
    GLOBAL_DEFAULT_OPTIONS = format_options.render()


def reset_global_defaults():
    """
    Reset global default options to package defaults.
    """
    global GLOBAL_DEFAULT_OPTIONS
    GLOBAL_DEFAULT_OPTIONS = DEFAULT_PKG_OPTIONS


def global_add_c_prefix():
    """
    Include ``c`` as a prefix for the exponent value -2. Has no effect
    if exponent value -2 is already mapped to a prefix string. To modify
    this mapping, first use :func:`global_reset_si_prefixes` or
    use :func:`set_global_defaults`.
    """
    set_global_defaults(FormatOptions(add_c_prefix=True))


def global_add_small_si_prefixes():
    """
    Include ``{-2: 'c', -1: 'd', +1: 'da', +2: 'h'}`` as prefix
    substitutions. Note, if any of these exponent values are mapped,
    then that mapping will NOT be overwritten. To modify existing
    mappings either first use :func:`global_reset_si_prefixes` or use
    :func:`set_global_defaults`.
    """
    set_global_defaults(FormatOptions(add_small_si_prefixes=True))


def global_add_ppth_form():
    """
    Include ``ppth`` as a "parts-per" form for the exponent value -3.
    Has no effect if exponent value -3 is already mapped to a
    "parts-per" format string. To modify this mapping, first use
    :func:`global_reset_parts_per_forms` or use
    :func:`set_global_defaults`.
    """
    set_global_defaults(FormatOptions(add_ppth_form=True))


def global_reset_si_prefixes():
    """
    Clear all extra SI prefix mappings.
    """
    set_global_defaults(FormatOptions(extra_si_prefixes=dict()))


def global_reset_iec_prefixes():
    """
    Clear all extra IEC prefix mappings.
    """
    set_global_defaults(FormatOptions(extra_iec_prefixes=dict()))


def global_reset_parts_per_forms():
    """
    Clear all extra "parts-per" forms.
    """
    set_global_defaults(FormatOptions(extra_parts_per_forms=dict()))


class GlobalDefaultsContext:
    """
    Temporarily update global default options. New settings are applied
    when the context is entered and original global settings are
    re-applied when the context is exited.
    """
    def __init__(self, format_options: FormatOptions):
        self.format_options = format_options
        self.initial_global_defaults = None

    def __enter__(self):
        global GLOBAL_DEFAULT_OPTIONS
        self.initial_global_defaults = GLOBAL_DEFAULT_OPTIONS
        GLOBAL_DEFAULT_OPTIONS = self.format_options.render()

    def __exit__(self, exc_type, exc_value, exc_tb):
        global GLOBAL_DEFAULT_OPTIONS
        GLOBAL_DEFAULT_OPTIONS = self.initial_global_defaults
