"""SciNum and SciNumUnc classes give users access to sciform FSML."""

from __future__ import annotations

from decimal import Decimal
from typing import TYPE_CHECKING

from sciform.formatting import format_num, format_val_unc
from sciform.fsml import format_options_from_fmt_spec

if TYPE_CHECKING:  # pragma: no cover
    from sciform.format_utils import Number


class SciNum:
    """
    Single number to be used with FSML.

    :class:`SciNum` objects are used in combination with the
    :mod:`sciform` format specification mini-language for scientific
    formatting of numbers. Any options not configured by the format
    specification will be populated with global default settings at
    format time.

    >>> from sciform import SciNum
    >>> snum = SciNum(12345.54321)
    >>> print(f"{snum:!3f}")
    12300
    >>> print(f"{snum:+2.3R}")
    + 12.346E+03
    """

    def __init__(self: SciNum, value: Number, /) -> None:
        self.value = Decimal(str(value))

    def __format__(self: SciNum, fmt: str) -> str:
        user_options = format_options_from_fmt_spec(fmt)
        rendered_options = user_options.render()
        return format_num(self.value, rendered_options)

    def __repr__(self: SciNum) -> str:
        return f"{self.__class__.__name__}({self.value})"


class SciNumUnc:
    """
    Value/uncertainty pair to be used with FSML.

    A :class:`SciNumUnc` objects stores a pair of numbers, a value and
    an uncertainty, for scientific formatting. This class is used in
    combination with the :mod:`sciform` format specification mini
    language to apply scientific formatting to the value/uncertainty
    pair. Any options not configured by the format specification will be
    populated with global default settings at format time.

    >>> from sciform import SciNumUnc
    >>> snumunc = SciNumUnc(123456.654321, 0.00000234)
    >>> print(f"{snumunc:!2f()}")
    123456.6543210(23)
    """

    def __init__(self: SciNumUnc, value: Number, uncertainty: Number, /) -> None:
        self.value = Decimal(str(value))
        self.uncertainty = Decimal(str(uncertainty))

    def __format__(self: SciNumUnc, fmt: str) -> str:
        user_options = format_options_from_fmt_spec(fmt)
        rendered_options = user_options.render()
        return format_val_unc(self.value, self.uncertainty, rendered_options)

    def __repr__(self: SciNumUnc) -> str:
        return f"{self.__class__.__name__}({self.value}, {self.uncertainty})"
