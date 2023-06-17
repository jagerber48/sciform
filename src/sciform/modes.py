from typing import get_args, Literal
from enum import Enum


class AutoExp:
    pass


class AutoPrec:
    pass


def option_warn_str(value, options: type(Literal)):
    return f'Flag \'{value}\' not in {get_args(options)}.'


class FillMode(Enum):
    #: Fill with white space
    SPACE = 'space'

    #: Fill with zeros
    ZERO = 'zero'

    @staticmethod
    def to_char(fill_mode: 'FillMode') -> str:
        if fill_mode is FillMode.SPACE:
            return ' '
        elif fill_mode is FillMode.ZERO:
            return '0'
        else:
            raise ValueError(f'Unhandled fill mode \'{fill_mode}\'.')


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

    #: Digits-past-the-decimal rounding
    PREC = 'prec'


class ExpMode(Enum):
    #: Fixed point
    FIXEDPOINT = 'fixed_point'

    #: Percentage
    PERCENT = 'percent'  # TODO: This should be an option, not an exp mode.

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
