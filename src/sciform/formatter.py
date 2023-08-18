from decimal import Decimal

from sciform.format_options import FormatOptions
from sciform.formatting import format_num, format_val_unc
from sciform.format_utils import Number


# TODO: Support SciNum/SciNumUnc input to formatter?


class Formatter:
    """
    :class:`Formatter` is used to convert numbers and pairs of numbers
    into formatted strings. Formatting options are configured using
    :class:`FormatOptions`. Any unpopulated format options will be
    populated from the global default options at format time. See
    :ref:`formatting_options` for more details on the available options.
    If no options are provided then the global default options are used
    for all options.

    >>> from sciform import FormatOptions, Formatter, ExpMode, RoundMode
    >>> sform = Formatter(FormatOptions(
    ...             exp_mode=ExpMode.ENGINEERING,
    ...             round_mode=RoundMode.SIG_FIG,
    ...             ndigits=4))
    >>> print(sform(12345.678))
    12.35e+03

    The Formatter can be called with two aguments for value/uncertainty
    formatting

    >>> sform = Formatter(FormatOptions(
    ...             exp_mode=ExpMode.ENGINEERING,
    ...             round_mode=RoundMode.SIG_FIG,
    ...             ndigits=2))
    >>> print(sform(12345.678, 3.4))
    (12.3457 +/- 0.0034)e+03

    :param format_options: :class:`FormatOptions` indicating which
      format options should be used for formatting.
    """
    def __init__(self, format_options=None):
        if format_options is None:
            format_options = FormatOptions()
        self.format_options = format_options

    def __call__(self, value: Number, uncertainty: Number = None, /):
        return self.format(value, uncertainty)

    def format(self, value: Number, uncertainty: Number = None, /):
        if uncertainty is None:
            return format_num(Decimal(str(value)), self.format_options)
        else:
            return format_val_unc(Decimal(str(value)),
                                  Decimal(str(uncertainty)),
                                  self.format_options)
