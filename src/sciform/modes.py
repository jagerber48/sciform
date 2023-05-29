from typing import get_args, Literal, Union
from enum import Enum

from sciform.types import (_FILL_TYPES,
                           _SIGN_TYPES,
                           _UPPER_SEP_TYPES,
                           _DECIMAL_SEP_TYPES,
                           _LOWER_SEP_TYPES,
                           _ROUND_TYPES,
                           _FORMAT_TYPES)


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

    @staticmethod
    def from_flag(flag: _FILL_TYPES) -> 'FillMode':
        if flag in [0, '0', 'zero']:
            return FillMode.ZERO
        elif flag in [' ', 'space']:
            return FillMode.SPACE
        else:
            raise ValueError(option_warn_str(flag, _FILL_TYPES))


class SignMode(Enum):
    NEGATIVE = 'negative'
    ALWAYS = 'always'
    SPACE = 'space'

    @staticmethod
    def from_flag(flag: _SIGN_TYPES):
        if flag in ['-', 'negative']:
            return SignMode.NEGATIVE
        elif flag in ['+', 'always']:
            return SignMode.ALWAYS
        elif flag in [' ', 'space']:
            return SignMode.SPACE
        else:
            raise ValueError(option_warn_str(flag, _SIGN_TYPES))


class GroupingSeparator(Enum):
    NONE = 'no_grouping'
    COMMA = 'comma'
    POINT = 'point'
    UNDERSCORE = 'underscore'
    SPACE = 'space'

    @staticmethod
    def to_char(
            grouping_separator: 'GroupingSeparator') -> str:
        if grouping_separator is GroupingSeparator.NONE:
            return ''
        elif grouping_separator is GroupingSeparator.COMMA:
            return ','
        elif grouping_separator is GroupingSeparator.POINT:
            return '.'
        elif grouping_separator is GroupingSeparator.UNDERSCORE:
            return '_'
        elif grouping_separator is GroupingSeparator.SPACE:
            return ' '
        else:
            raise ValueError(f'Invalid grouping separator: '
                             f'{grouping_separator}')

    @staticmethod
    def from_flag(flag: Union[_UPPER_SEP_TYPES,
                              _DECIMAL_SEP_TYPES,
                              _LOWER_SEP_TYPES]):
        if flag in ['', 'none']:
            return GroupingSeparator.NONE
        elif flag in [',', 'comma']:
            return GroupingSeparator.COMMA
        elif flag in ['.', 'point']:
            return GroupingSeparator.POINT
        elif flag in ['_', 'underscore']:
            return GroupingSeparator.UNDERSCORE
        elif flag in [' ', 'space']:
            return GroupingSeparator.SPACE
        else:
            raise ValueError(
                option_warn_str(flag,
                                Union[_UPPER_SEP_TYPES,
                                      _DECIMAL_SEP_TYPES,
                                      _LOWER_SEP_TYPES]
                                )
            )


class RoundMode(Enum):
    SIG_FIG = 'sig_fig'
    PREC = 'prec'

    @staticmethod
    def from_flag(flag: _ROUND_TYPES):
        if flag == 'sig_fig':
            return RoundMode.SIG_FIG
        elif flag == 'precision':
            return RoundMode.PREC
        else:
            raise ValueError(option_warn_str(flag, _ROUND_TYPES))


class FormatMode(Enum):
    FIXEDPOINT = 'fixed_point'
    PERCENT = 'percent'
    SCIENTIFIC = 'scientific'
    ENGINEERING = 'engineering'
    ENGINEERING_SHIFTED = 'engineering_shifted'
    BINARY = 'binary'
    BINARY_IEC = 'binary_iec'

    @staticmethod
    def from_flag(flag: _FORMAT_TYPES) -> 'FormatMode':
        if flag == 'fixed_point':
            return FormatMode.FIXEDPOINT
        elif flag == 'percent':
            return FormatMode.PERCENT
        elif flag == 'scientific':
            return FormatMode.SCIENTIFIC
        elif flag == 'engineering':
            return FormatMode.ENGINEERING
        elif flag == 'engineering_shifted':
            return FormatMode.ENGINEERING_SHIFTED
        elif flag == 'binary':
            return FormatMode.BINARY
        elif flag == 'binary_iec':
            return FormatMode.BINARY_IEC
        else:
            raise ValueError(option_warn_str(flag, _FORMAT_TYPES))
