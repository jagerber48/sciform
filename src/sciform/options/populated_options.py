"""InputOptions Dataclass which stores user input."""


from __future__ import annotations

from dataclasses import asdict, dataclass
from pprint import pformat
from typing import TYPE_CHECKING, Any

from sciform.options.validation import validate_options

if TYPE_CHECKING:  # pragma: no cover
    from sciform import modes


@dataclass(frozen=True)
class PopulatedOptions:
    """
    Dataclass storing fully populated formatting options.

    User input options during :class:`Formatter` initialization are
    stored in :class:`InputOptions` instances. But
    :class:`InputOptions` instances don't necessarily have all options
    populated as required for the formatting algorithm. At formatting
    time the unpopulated options are populated from the global options.
    The new resulting options object with all options populated is a
    :class:`PopulatedOptions` instances. Note that the global options
    are stored as a :class:`PopulatedOptions` instance.

    :class:`PopulatedOptions` instances should only be accessed via the
    :class:`Formatter.populated_options()` property. They should not be
    instantiated directly.

    >>> from sciform import Formatter
    >>> formatter = Formatter(
    ...     exp_mode="engineering",
    ...     round_mode="sig_fig",
    ...     ndigits=2,
    ...     superscript=True,
    ... )
    >>> print(formatter.populated_options.round_mode)
    sig_fig
    >>> print(formatter.populated_options.exp_format)
    standard
    >>> print(formatter.populated_options)
    PopulatedOptions(
     'exp_mode': 'engineering',
     'exp_val': AutoExpVal,
     'round_mode': 'sig_fig',
     'ndigits': 2,
     'upper_separator': '',
     'decimal_separator': '.',
     'lower_separator': '',
     'sign_mode': '-',
     'left_pad_char': ' ',
     'left_pad_dec_place': 0,
     'exp_format': 'standard',
     'extra_si_prefixes': {},
     'extra_iec_prefixes': {},
     'extra_parts_per_forms': {},
     'capitalize': False,
     'superscript': True,
     'nan_inf_exp': False,
     'paren_uncertainty': False,
     'pdg_sig_figs': False,
     'left_pad_matching': False,
     'paren_uncertainty_trim': True,
     'pm_whitespace': True,
    )
    >>> print(formatter.populated_options.as_dict())
    {'exp_mode': 'engineering', 'exp_val': AutoExpVal, 'round_mode': 'sig_fig', 'ndigits': 2, 'upper_separator': '', 'decimal_separator': '.', 'lower_separator': '', 'sign_mode': '-', 'left_pad_char': ' ', 'left_pad_dec_place': 0, 'exp_format': 'standard', 'extra_si_prefixes': {}, 'extra_iec_prefixes': {}, 'extra_parts_per_forms': {}, 'capitalize': False, 'superscript': True, 'nan_inf_exp': False, 'paren_uncertainty': False, 'pdg_sig_figs': False, 'left_pad_matching': False, 'paren_uncertainty_trim': True, 'pm_whitespace': True}

    Note that :class:`PopulatedOptions` lacks the ``add_c_prefix``,
    ``add_small_si_prefixes`` and ``add_ppth_form`` options present
    in :class:`InputOptions`. These options are helper functions which
    modify the corresponding exponent replacement dictionaries.

    >>> formatter = Formatter(
    ...     exp_mode="engineering",
    ...     exp_format="prefix",
    ...     add_c_prefix=True,
    ... )
    >>> print(formatter.input_options)
    InputOptions(
     'exp_mode': 'engineering',
     'exp_format': 'prefix',
     'add_c_prefix': True,
    )
    >>> print(formatter.input_options.extra_si_prefixes)
    None
    >>> print(formatter.populated_options.extra_si_prefixes)
    {-2: 'c'}

    """  # noqa: E501

    exp_mode: modes.ExpMode
    exp_val: int | type(modes.AutoExpVal)
    round_mode: modes.RoundMode
    ndigits: int | type(modes.AutoDigits)
    upper_separator: modes.UpperSeparators
    decimal_separator: modes.DecimalSeparators
    lower_separator: modes.LowerSeparators
    sign_mode: modes.SignMode
    left_pad_char: modes.LeftPadChar
    left_pad_dec_place: int
    exp_format: modes.ExpFormat
    extra_si_prefixes: dict[int, str]
    extra_iec_prefixes: dict[int, str]
    extra_parts_per_forms: dict[int, str]
    capitalize: bool
    superscript: bool
    nan_inf_exp: bool
    paren_uncertainty: bool
    pdg_sig_figs: bool
    left_pad_matching: bool
    paren_uncertainty_trim: bool
    pm_whitespace: bool

    def __post_init__(self: PopulatedOptions) -> None:
        validate_options(self)

    def as_dict(self: PopulatedOptions) -> dict[str, Any]:
        """
        Return a dict representation of the PopulatedOptions.

        This dict can be passed into :class:`Formatter` as ``**kwargs``,
        possibly after modification. This allows for the possibility of
        constructing new :class:`Formatter` instances based on old ones.
        """
        return asdict(self)

    def __str__(self: PopulatedOptions) -> str:
        options_str = pformat(self.as_dict(), width=-1, sort_dicts=False)
        options_str = options_str.lstrip("{").rstrip("}")
        options_str = f"PopulatedOptions(\n {options_str},\n)"
        return options_str
