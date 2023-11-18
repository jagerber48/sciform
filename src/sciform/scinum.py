from decimal import Decimal

from sciform.formatting import format_num, format_val_unc
from sciform.format_utils import Number
from sciform.fsml import format_options_from_fmt_spec


class SciNum:
    """
    :class:`SciNum` objects are used in combination with the
    :mod:`sciform` format specification mini-language for scientific
    formatting of numbers. Any options not configured by the format
    specification will be populated with global default settings at
    format time.

    >>> from sciform import SciNum
    >>> snum = SciNum(123456.654321)
    >>> print(f'{snum:,._.7f}')
    123,456.654_321_0
    """
    def __init__(self, value: Number, /):
        self.value = Decimal(str(value))

    def __format__(self, fmt: str):
        user_options = format_options_from_fmt_spec(fmt)
        rendered_options = user_options.render()
        return format_num(self.value,
                          rendered_options)

    def __repr__(self):
        return f'{self.__class__.__name__}({self.value})'


class SciNumUnc:
    """
    A :class:`SciNumUnc` objects stores a pair of numbers, a value and
    an uncertainty, for scientific formatting. This class is used in
    combination with the :mod:`sciform` format specification mini
    language to apply scientific formatting to the value/uncertainty
    pair. Any options not configured by the format specification will be
    populated with global default settings at format time.

    >>> from sciform import SciNumUnc
    >>> snumunc = SciNumUnc(123456.654321, 0.000002)
    >>> print(f'{snumunc:,._!1f()}')
    123,456.654_321(2)
    """
    def __init__(self, value: Number,
                 uncertainty: Number, /):
        self.value = Decimal(str(value))
        self.uncertainty = Decimal(str(uncertainty))

    def __format__(self, fmt: str):
        user_options = format_options_from_fmt_spec(fmt)
        rendered_options = user_options.render()
        return format_val_unc(self.value,
                              self.uncertainty,
                              rendered_options)

    def __repr__(self):
        return f'{self.__class__.__name__}({self.value}, {self.uncertainty})'
