"""``sciform`` is used to convert python numbers into scientific formatted strings."""

from sciform.formatter import Formatter
from sciform.global_configuration import (
    GlobalOptionsContext,
    get_global_options,
    reset_global_options,
    set_global_options,
)
from sciform.modes import AutoDigits, AutoExpVal
from sciform.scinum import SciNum

__all__ = [
    "Formatter",
    "GlobalOptionsContext",
    "get_global_options",
    "reset_global_options",
    "set_global_options",
    "AutoDigits",
    "AutoExpVal",
    "SciNum",
]
