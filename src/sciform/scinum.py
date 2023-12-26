"""The SciNum class provides users access to sciform FSML."""

from __future__ import annotations

from decimal import Decimal
from typing import TYPE_CHECKING

from sciform.formatting import format_num, format_val_unc
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
    >>> snum = SciNum(12345.54321)
    >>> print(f"{snum:!3f}")
    12300
    >>> print(f"{snum:+2.3R}")
    + 12.346E+03
    >>> snum = SciNum(123456.654321, 0.0234)
    >>> print(f"{snum:#!2r()}")
    (0.123456654(23))e+06
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

    def __format__(self: SciNum, fmt: str) -> str:
        user_options = format_options_from_fmt_spec(fmt)
        rendered_options = user_options.render()
        if self.uncertainty is not None:
            return format_val_unc(self.value, self.uncertainty, rendered_options)
        return format_num(self.value, rendered_options)

    def __repr__(self: SciNum) -> str:
        if self.uncertainty is not None:
            return f"{self.__class__.__name__}({self.value}, {self.uncertainty})"
        return f"{self.__class__.__name__}({self.value})"
