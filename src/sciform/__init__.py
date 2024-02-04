"""``sciform`` is used to convert python numbers into scientific formatted strings."""

from sciform.formatter import Formatter
from sciform.formatting import FormattedNumber
from sciform.global_configuration import (
    GlobalOptionsContext,
    get_default_global_options,
    get_global_options,
    reset_global_options,
    set_global_options,
)
from sciform.modes import AutoDigits, AutoExpVal
from sciform.options.input_options import InputOptions
from sciform.options.populated_options import PopulatedOptions
from sciform.scinum import SciNum

__all__ = [
    "Formatter",
    "FormattedNumber",
    "GlobalOptionsContext",
    "get_default_global_options",
    "get_global_options",
    "reset_global_options",
    "set_global_options",
    "AutoDigits",
    "AutoExpVal",
    "SciNum",
    "InputOptions",
    "PopulatedOptions",
]
