from typing import Literal, TypeVar
from enum import Enum


class AutoExpVal:
    """
    Flag for auto-exponent calculation mode. Set ``exp_val=AutoExpVal`` or an
    integer.

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
    pass


class AutoDigits:
    """
    Flag for auto ndigits calculation mode. Set ``ndigits=AutoDigits``
    or an integer.

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
    pass


UserFillMode = Literal[' ', '0']

class FillMode(str, Enum):
    #: Fill with white space
    SPACE = ' '

    #: Fill with zeros
    ZERO = '0'


UserSignMode = Literal['-', '+', ' ']

class SignMode(str, Enum):
    #: Only include sign symbol on negative numbers
    NEGATIVE = '-'

    #: Always include sign symbol
    ALWAYS = '+'

    #: Include extra white space in front of positive numbers
    SPACE = ' '


UserUpperSeparators = Literal['', ',', '.', ' ', '_']
UserDecimalSeparators = Literal['.', ',']
UserLowerSeparators = Literal['', ' ', '_']

class Separator(str, Enum):
    #: No separator
    NONE = ''

    #: Comma separator (not valid as lower separator)
    COMMA = ','

    #: Point separator (not valid as lower separator)
    POINT = '.'

    #: Underscore separator
    UNDERSCORE = '_'

    #: White space separator
    SPACE = ' '

UpperSeparators = Literal[Separator.NONE,
                          Separator.COMMA,
                          Separator.POINT,
                          Separator.UNDERSCORE,
                          Separator.SPACE]
DecimalSeparators = Literal[Separator.POINT,
                            Separator.COMMA]
LowerSeparators = Literal[Separator.NONE,
                          Separator.UNDERSCORE,
                          Separator.SPACE]


UserRoundMode = Literal['sig_fig', 'dec_place']

class RoundMode(Enum):
    #: Significant figure rounding
    SIG_FIG = 'sig_fig'

    #: Decimal place rounding
    DEC_PLACE = 'dec_place'



UserExpMode = Literal['fixed_point', 'percent', 'scientific', 'engineering',
                      'engineering_shifted', 'binary', 'binary_iec']

class ExpMode(Enum):
    #: Fixed point
    FIXEDPOINT = 'fixed_point'

    #: Percent
    PERCENT = 'percent'

    #: Scientific
    SCIENTIFIC = 'scientific'

    #: Engineering
    ENGINEERING = 'engineering'

    #: Shifted Engineering
    ENGINEERING_SHIFTED = 'engineering_shifted'

    #: Binary
    BINARY = 'binary'

    #: Binary IEC
    BINARY_IEC = 'binary_iec'


UserExpFormat = Literal['standard', 'prefix', 'parts_per']

class ExpFormat(Enum):
    #: Standard Format
    STANDARD = 'standard'

    #: Prefix Format
    PREFIX = 'prefix'

    #: Parts-Per Format
    PARTS_PER = 'parts_per'


T = TypeVar('T', bound=Enum)

def mode_str_to_enum(mode_str: str, enum: type[T]) -> T:
    for member in enum:
        if mode_str == member.value:
            return member
    raise ValueError(f'String \'{mode_str}\' not found in {enum} values.')
