"""Enums and Literals for the various formatting options."""

from __future__ import annotations

from enum import Enum
from typing import Literal, TypeVar

LeftPadChar = Literal[" ", "0"]


class LeftPadCharEnum(str, Enum):
    """Left pad character mode Enum."""

    SPACE = " "
    ZERO = "0"


SignMode = Literal["-", "+", " "]


class SignModeEnum(str, Enum):
    """Sign mode Enum."""

    NEGATIVE = "-"
    ALWAYS = "+"
    SPACE = " "


UpperSeparators = Literal["", ",", ".", " ", "_"]
DecimalSeparators = Literal[".", ","]
LowerSeparators = Literal["", " ", "_"]


class SeparatorEnum(str, Enum):
    """Separator type Enum."""

    NONE = ""
    COMMA = ","
    POINT = "."
    UNDERSCORE = "_"
    SPACE = " "


UpperSeparatorEnums = Literal[
    SeparatorEnum.NONE,
    SeparatorEnum.COMMA,
    SeparatorEnum.POINT,
    SeparatorEnum.UNDERSCORE,
    SeparatorEnum.SPACE,
]
DecimalSeparatorEnums = Literal[SeparatorEnum.POINT, SeparatorEnum.COMMA]
LowerSeparatorEnums = Literal[
    SeparatorEnum.NONE,
    SeparatorEnum.UNDERSCORE,
    SeparatorEnum.SPACE,
]


RoundMode = Literal["sig_fig", "dec_place", "all", "pdg"]


class RoundModeEnum(str, Enum):
    """Round mode Enum."""

    SIG_FIG = "sig_fig"
    DEC_PLACE = "dec_place"
    ALL = "all"
    PDG = "pdg"


ExpMode = Literal[
    "fixed_point",
    "percent",
    "scientific",
    "engineering",
    "engineering_shifted",
    "binary",
    "binary_iec",
]


class ExpModeEnum(str, Enum):
    """Exponent mode Enum."""

    FIXEDPOINT = "fixed_point"
    PERCENT = "percent"
    SCIENTIFIC = "scientific"
    ENGINEERING = "engineering"
    ENGINEERING_SHIFTED = "engineering_shifted"
    BINARY = "binary"
    BINARY_IEC = "binary_iec"


ExpFormat = Literal["standard", "prefix", "parts_per"]


class ExpFormatEnum(str, Enum):
    """Exponent format Enum."""

    STANDARD = "standard"
    PREFIX = "prefix"
    PARTS_PER = "parts_per"


ExpVal = Literal["auto"]


class ExpValEnum(str, Enum):
    """Exponent value Enum."""

    AUTO = "auto"


T = TypeVar("T", bound=Enum)


def mode_str_to_enum(mode_str: str, enum: type[T]) -> T:
    """Convert a string to its corresponding Enum member."""
    for member in enum:
        if mode_str == member.value:
            return member
    msg = f"String '{mode_str}' not found in {enum} values."
    raise ValueError(msg)
