from typing import get_args, Literal
from enum import Enum


AUTO = object()


def option_warn_str(value, options: type(Literal)):
    return f'Flag \'{value}\' not in {get_args(options)}.'


class FillMode(Enum):
    SPACE = 'space'
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
    NEGATIVE = 'negative'
    ALWAYS = 'always'
    SPACE = 'space'


class GroupingSeparator(Enum):
    NONE = 'no_grouping'
    COMMA = 'comma'
    POINT = 'point'
    UNDERSCORE = 'underscore'
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
    SIG_FIG = 'sig_fig'
    PREC = 'prec'


class FormatMode(Enum):
    FIXEDPOINT = 'fixed_point'
    PERCENT = 'percent'
    SCIENTIFIC = 'scientific'
    ENGINEERING = 'engineering'
    ENGINEERING_SHIFTED = 'engineering_shifted'
    BINARY = 'binary'
    BINARY_IEC = 'binary_iec'
