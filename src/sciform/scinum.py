from decimal import Decimal
from typing import Union

from sciform.formatting import format_num, format_val_unc
from sciform.format_options import FormatOptions


class SciNum:
    """
    :class:`SciNum` objects are used in combination with the
    :mod:`sciform` format specification mini language for scientific
    formatting of input floats.

    >>> from sciform import SciNum
    >>> snum = SciNum(123456.654321)
    >>> print(f'{snum:,._.7f}')
    123,456.654_321_0
    """
    def __init__(self, value: Union[str, float, Decimal], /):
        self.value = Decimal(str(value))

    def __format__(self, fmt: str):
        return format_num(self.value,
                          FormatOptions.from_format_spec_str(fmt))


class SciNumUnc:
    """
    A :class:`SciNumUnc` objects stores a pair of numbers, a value and
    an uncertainty, for scientific formatting. This class is used in
    combination with the :mod:`sciform` format specification mini
    language to apply scientific formatting of input floats.

    >>> from sciform import SciNumUnc
    >>> snumunc = SciNumUnc(123456.654321, 0.000002)
    >>> print(f'{snumunc:,._!1f()}')
    123,456.654_321(2)
    """
    def __init__(self, value: Union[str, float, Decimal],
                 uncertainty: Union[str, float, Decimal], /):
        self.value = Decimal(str(value))
        self.uncertainty = Decimal(str(uncertainty))

    def __format__(self, format_spec: str):
        return format_val_unc(self.value,
                              self.uncertainty,
                              FormatOptions.from_format_spec_str(format_spec))
