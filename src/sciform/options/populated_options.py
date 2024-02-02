"""InputOptions Dataclass which stores user input."""


from __future__ import annotations

from dataclasses import asdict, dataclass
from pprint import pformat
from typing import TYPE_CHECKING, Any

from sciform.options.validation import validate_options

if TYPE_CHECKING:
    from sciform import modes


@dataclass(frozen=True)
class PopulatedOptions:
    """Dataclass storing user input."""

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
    paren_uncertainty_separators: bool
    pm_whitespace: bool

    def __post_init__(self: PopulatedOptions) -> None:
        validate_options(self)

    def as_dict(self: PopulatedOptions) -> dict[str, Any]:
        """Return a dict representation of the inputs used to construct InputOptions."""
        return asdict(self)

    def __str__(self: PopulatedOptions) -> str:
        return pformat(self.as_dict(), sort_dicts=False)
