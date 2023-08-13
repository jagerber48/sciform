from typing import Literal
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


class AutoRound:
    """
    Flag for auto ndigits calculation mode. Set ``ndigits=AutoRound``
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


class FillMode(Enum):
    #: Fill with white space
    SPACE = 'space'

    #: Fill with zeros
    ZERO = 'zero'

    def to_char(self) -> str:
        if self is FillMode.SPACE:
            return ' '
        elif self is FillMode.ZERO:
            return '0'
        else:
            raise ValueError(f'Invalid fill mode: {self}')


class SignMode(Enum):
    #: Only include sign symbol on negative numbers
    NEGATIVE = 'negative'

    #: Always include sign symbol
    ALWAYS = 'always'

    #: Include extra white space in front of positive numbers
    SPACE = 'space'


class GroupingSeparator(Enum):
    #: No separator
    NONE = 'no_grouping'

    #: Comma separator (not valid as lower separator)
    COMMA = 'comma'

    #: Point separator (not valid as lower separator)
    POINT = 'point'

    #: Underscore separator
    UNDERSCORE = 'underscore'

    #: White space separator
    SPACE = 'space'

    def to_char(self) -> str:
        if self is GroupingSeparator.NONE:
            return ''
        elif self is GroupingSeparator.COMMA:
            return ','
        elif self is GroupingSeparator.POINT:
            return '.'
        elif self is GroupingSeparator.UNDERSCORE:
            return '_'
        elif self is GroupingSeparator.SPACE:
            return ' '
        else:
            raise ValueError(f'Invalid grouping separator: '
                             f'{self}')


UpperGroupingSeparators = Literal[GroupingSeparator.NONE,
                                  GroupingSeparator.COMMA,
                                  GroupingSeparator.POINT,
                                  GroupingSeparator.UNDERSCORE,
                                  GroupingSeparator.SPACE]

DecimalGroupingSeparators = Literal[GroupingSeparator.POINT,
                                    GroupingSeparator.COMMA]

LowerGroupingSeparators = Literal[GroupingSeparator.NONE,
                                  GroupingSeparator.UNDERSCORE,
                                  GroupingSeparator.SPACE]


class RoundMode(Enum):
    #: Significant figure rounding
    SIG_FIG = 'sig_fig'

    #: Digit place
    DIG_PLACE = 'dig_place'


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
