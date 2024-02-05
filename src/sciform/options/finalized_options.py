"""
Rendered format options used in sciform backend formatting algorithm.

:class:`InputOptions` are converted into :class:`FinalizedOptions`
internally at format time.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

from sciform.options.validation import validate_options

if TYPE_CHECKING:  # pragma: no cover
    from sciform import modes


@dataclass(frozen=True)
class FinalizedOptions:
    """Rendered options: All options populated and using Enum instead of Literal."""

    exp_mode: modes.ExpModeEnum
    exp_val: int | type(modes.AutoExpVal)
    round_mode: modes.RoundModeEnum
    ndigits: int | type(modes.AutoDigits)
    upper_separator: modes.UpperSeparatorEnums
    decimal_separator: modes.DecimalSeparatorEnums
    lower_separator: modes.LowerSeparatorEnums
    sign_mode: modes.SignModeEnum
    left_pad_char: modes.LeftPadCharEnum
    left_pad_dec_place: int
    exp_format: modes.ExpFormatEnum
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

    def __post_init__(self: FinalizedOptions) -> None:
        validate_options(self)
