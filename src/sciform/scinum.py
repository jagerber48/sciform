"""The SciNum class provides users access to sciform FSML."""

from __future__ import annotations

from decimal import Decimal
from typing import TYPE_CHECKING

from sciform.formatting import FormattedNumber, format_from_options
from sciform.fsml import format_options_from_fmt_spec

if TYPE_CHECKING:  # pragma: no cover
    from sciform.format_utils import Number


class SciNum:
    """
    Single number, or number and uncertainty, to be used with FSML.

    :class:`SciNum` objects represent single numbers, or
    number/uncertainty pairs to be formatted using the :mod:`sciform`
    format specification mini-language for scientific formatting of
    numbers. Any options not configured by the format specification will
    be populated with global default settings at format time.

    >>> from sciform import SciNum
    >>> num = SciNum(12345.54321)
    >>> print(f"{num:!3f}")
    12300
    >>> print(f"{num:+2.3R}")
    + 12.346E+03
    >>> num = SciNum(123456.654321, 0.0234)
    >>> print(f"{num:#!2r()}")
    0.123456654(23)e+06
    """

    def __init__(
        self: SciNum,
        value: Number,
        uncertainty: Number | None = None,
        /,
    ) -> None:
        self.value = Decimal(str(value))
        if uncertainty is None:
            self.uncertainty = uncertainty
        else:
            self.uncertainty = Decimal(str(uncertainty))

    def __format__(self: SciNum, fmt: str) -> FormattedNumber:
        input_options = format_options_from_fmt_spec(fmt)
        return format_from_options(
            self.value,
            self.uncertainty,
            input_options=input_options,
        )

    def __repr__(self: SciNum) -> str:
        if self.uncertainty is not None:
            return f"{self.__class__.__name__}({self.value}, {self.uncertainty})"
        return f"{self.__class__.__name__}({self.value})"
