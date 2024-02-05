"""InputOptions Dataclass which stores user input."""


from __future__ import annotations

from dataclasses import asdict, dataclass
from pprint import pformat
from typing import TYPE_CHECKING, Any, Literal

from sciform.options.validation import validate_options

if TYPE_CHECKING:  # pragma: no cover
    from sciform import modes


@dataclass(frozen=True)
class InputOptions:
    """
    Dataclass storing user input.

    Stores the user input to :class:`Formatter`, so any keyword
    arguments that can be passed into :class:`Formatter` are stored in
    :class:`InputOptions`. Any unpopulated options retain the ``None``
    value. At format time the :class:`InputOptions` are populated and
    replaced by a :class:`PopulatedOptions` instance which necessarily
    has all attributes populated with meaningful values.

    :class:`InputOptions` instances should only be accessed via the
    :class:`Formatter.input_options()` property. They should not be
    instantiated directly.

    >>> from sciform import Formatter
    >>> formatter = Formatter(
    ...     exp_mode="engineering",
    ...     round_mode="sig_fig",
    ...     ndigits=2,
    ...     superscript=True,
    ... )
    >>> print(formatter.input_options.round_mode)
    sig_fig
    >>> print(formatter.input_options.exp_format)
    None
    >>> print(formatter.input_options)
    InputOptions(
     'exp_mode': 'engineering',
     'round_mode': 'sig_fig',
     'ndigits': 2,
     'superscript': True,
    )
    >>> print(formatter.input_options.as_dict())
    {'exp_mode': 'engineering', 'round_mode': 'sig_fig', 'ndigits': 2, 'superscript': True}
    """  # noqa: E501

    exp_mode: modes.ExpMode | None = None
    exp_val: int | type(modes.AutoExpVal) | None = None
    round_mode: modes.RoundMode | None = None
    ndigits: int | type(modes.AutoDigits) | None = None
    upper_separator: modes.UpperSeparators | None = None
    decimal_separator: modes.DecimalSeparators | None = None
    lower_separator: modes.LowerSeparators | None = None
    sign_mode: modes.SignMode | None = None
    left_pad_char: modes.LeftPadChar | Literal[0] | None = None
    left_pad_dec_place: int | None = None
    exp_format: modes.ExpFormat | None = None
    extra_si_prefixes: dict[int, str] | None = None
    extra_iec_prefixes: dict[int, str] | None = None
    extra_parts_per_forms: dict[int, str] | None = None
    capitalize: bool | None = None
    superscript: bool | None = None
    nan_inf_exp: bool | None = None
    paren_uncertainty: bool | None = None
    pdg_sig_figs: bool | None = None
    left_pad_matching: bool | None = None
    paren_uncertainty_trim: bool | None = None
    pm_whitespace: bool | None = None

    add_c_prefix: bool = None
    add_small_si_prefixes: bool = None
    add_ppth_form: bool = None

    def __post_init__(self: InputOptions) -> None:
        validate_options(self)

    def as_dict(self: InputOptions) -> dict[str, Any]:
        """
        Return a dict representation of the InputOptions.

        This dict can be passed into :class:`Formatter` as ``**kwargs``,
        possibly after modification. This allows for the possibility of
        constructing new :class:`Formatter` instances based on old ones.
        Only explicitly populated attributes are included in the
        returned dictionary.
        """
        options_dict = asdict(self)
        for key in list(options_dict.keys()):
            if options_dict[key] is None:
                del options_dict[key]
        return options_dict

    def __str__(self: InputOptions) -> str:
        options_str = pformat(self.as_dict(), width=-1, sort_dicts=False)
        options_str = options_str.lstrip("{").rstrip("}")
        options_str = f"InputOptions(\n {options_str},\n)"
        return options_str
