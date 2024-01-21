"""Enums and Literals for the various formatting options."""

from __future__ import annotations

from enum import Enum
from typing import Literal, TypeVar


class SentinelMeta(type):
    """Sentinel metaclass, __repr__ returns class name."""

    def __repr__(cls: SentinelMeta) -> str:
        return cls.__name__


class AutoExpVal(metaclass=SentinelMeta):
    """
    Flag for auto-exponent calculation mode.

      * For scientific exponent mode the base-10 exponent is selected so
        that the mantissa ``m`` satisfies ``1 <= m < 10``.
      * For engineering exponent mode the base-10 exponent is chosen so
        that it is an integer multiple of 3 and the mantissa ``m``
        satisfies ``1 <= m < 1000``.
      * For shifted engineering exponent mode the base-10 exponent is
        chosen so that it is an integer multiple of 3 and the mantissa
        ``m`` satisfies ``0.1 <= m < 100``.
      * For binary exponent mode the base-2 exponent is chosen so that
        the mantissa ``m`` satisfies ``1 <= m < 2``.
      * For binary IEC exponent mode the base-2 exponent is chosen so
        that the mantissa ``m`` satisfies ``1 <= m < 1024 = 2**10``.
    """


class AutoDigits(metaclass=SentinelMeta):
    """
    Flag for auto ndigits calculation mode.

    In both sig fig and ndigits round modes this auto ndigits
    option chooses the ndigits so that the least significant digit of
    the input number will be displayed.
    For example the number 123.456789 would be displayed with either 9
    significant figures or 6 digits past the decimal point so that in
    either case all digits are shown.

    When used with sig fig rounding and in combination with the
    ``pdg_sig_figs`` option, the number of significant figures will be
    chosen to be one or two in accordance with the Particle Data Group
    algorithm.
    """


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


RoundMode = Literal["sig_fig", "dec_place"]


class RoundModeEnum(str, Enum):
    """Round mode Enum."""

    SIG_FIG = "sig_fig"
    DEC_PLACE = "dec_place"


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


T = TypeVar("T", bound=Enum)


def mode_str_to_enum(mode_str: str, enum: type[T]) -> T:
    """Convert a string to its corresponding Enum member."""
    for member in enum:
        if mode_str == member.value:
            return member
    msg = f"String '{mode_str}' not found in {enum} values."
    raise ValueError(msg)
