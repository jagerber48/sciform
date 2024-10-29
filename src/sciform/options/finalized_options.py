"""
Rendered format options used in sciform backend formatting algorithm.

:class:`InputOptions` are converted into :class:`FinalizedOptions`
internally at format time.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

if TYPE_CHECKING:  # pragma: no cover
    from sciform.options import option_types


@dataclass(frozen=True)
class FinalizedOptions:
    """Rendered options: All options populated and using Enum instead of Literal."""

    exp_mode: option_types.ExpModeEnum
    exp_val: int | option_types.ExpValEnum
    round_mode: option_types.RoundModeEnum
    ndigits: int
    upper_separator: option_types.UpperSeparatorEnums
    decimal_separator: option_types.DecimalSeparatorEnums
    lower_separator: option_types.LowerSeparatorEnums
    sign_mode: option_types.SignModeEnum
    left_pad_char: option_types.LeftPadCharEnum
    left_pad_dec_place: int
    exp_format: option_types.ExpFormatEnum
    extra_si_prefixes: dict[int, str]
    extra_iec_prefixes: dict[int, str]
    extra_parts_per_forms: dict[int, str]
    capitalize: bool
    superscript: bool
    nan_inf_exp: bool
    paren_uncertainty: bool
    left_pad_matching: bool
    paren_uncertainty_trim: bool
    pm_whitespace: bool
