"""The SciNum class provides users access to sciform FSML."""

from __future__ import annotations

from typing import TYPE_CHECKING

from sciform.formatting import FormattedNumber, format_from_options
from sciform.fsml import format_options_from_fmt_spec
from sciform.parser import parse_val_unc_from_input

if TYPE_CHECKING:  # pragma: no cover
    from decimal import Decimal

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

    Formatted input can also be passed into :class:`SciNum`. For more
    details see :ref:`formatted_input`.

    >>> print(f'{SciNum("3.1415e+05"):#!2rp}')
    0.31 M
    >>> print(f'{SciNum("123456.654321 +/- 0.0234"):!2()}')
    123456.654(23)
    >>> print(f'{SciNum("123456.654321(23400)"):!2()}')
    123456.654(23)
    """

    def __init__(
        self: SciNum,
        value: Number,
        uncertainty: Number | None = None,
        /,
    ) -> None:
        val, unc = parse_val_unc_from_input(value, uncertainty)
        self.value: Decimal = val
        self.uncertainty: Decimal = unc

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

    def __eq__(self: SciNum, other: SciNum) -> bool:
        if self.value.is_nan():
            val_equal = other.value.is_nan()
        else:
            val_equal = self.value == other.value

        if self.uncertainty is None:
            unc_equal = other.uncertainty is None
        elif self.uncertainty.is_nan():
            unc_equal = other.uncertainty.is_nan()
        else:
            unc_equal = self.uncertainty == other.uncertainty

        total_equal = val_equal and unc_equal
        return total_equal
