from enum import Enum


AUTO = object()


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
    def from_flag(flag: str) -> 'FillMode':
        if flag == ' ':
            return FillMode.SPACE
        elif flag == '0':
            return FillMode.ZERO
        else:
            raise ValueError(f'Unhandled fill mode flag \'{flag}\'.')


class FormatMode(Enum):
    FIXEDPOINT = 'fixed_point'
    SCIENTIFIC = 'scientific'
    ENGINEERING = 'engineering'
    BINARY = 'binary'

    @staticmethod
    def from_flag(flag: str) -> 'FormatMode':
        if flag in ['f', 'F', '%']:
            return FormatMode.FIXEDPOINT
        elif flag in ['e', 'E']:
            return FormatMode.SCIENTIFIC
        elif flag in ['r', 'R']:
            return FormatMode.ENGINEERING
        elif flag in ['b', 'B']:
            return FormatMode.BINARY
        else:
            raise ValueError(f'Invalid format mode flag \'{flag}\'.')


class SignMode(Enum):
    ALWAYS = 'always'
    NEGATIVE = 'negative'
    SPACE = 'space'

    @staticmethod
    def from_flag(flag: str):
        if flag == '-':
            return SignMode.NEGATIVE
        elif flag == '+':
            return SignMode.ALWAYS
        elif flag == ' ':
            return SignMode.SPACE
        else:
            raise ValueError(f'Invalid sign mode flag {flag}.')


class PrecMode(Enum):
    SIG_FIG = 'sig_fig'
    PREC = 'prec'

    @staticmethod
    def from_flag(flag: str):
        if flag == '!':
            return PrecMode.SIG_FIG
        elif flag == '.':
            return PrecMode.PREC
        else:
            raise ValueError(f'Invalid precision type flag {flag}.')


class GroupingSeparator(Enum):
    NO_GROUPING = 'no_grouping'
    COMMA = 'comma'
    POINT = 'point'
    UNDERSCORE = 'underscore'
    SPACE = 'space'

    @staticmethod
    def to_char(grouping_separator: 'GroupingSeparator') -> str:
        if grouping_separator is GroupingSeparator.NO_GROUPING:
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
    def from_flag(flag: str):
        if flag == 'n':
            return GroupingSeparator.NO_GROUPING
        elif flag == ',':
            return GroupingSeparator.COMMA
        elif flag == '.':
            return GroupingSeparator.POINT
        elif flag == '_':
            return GroupingSeparator.UNDERSCORE
        elif flag == 's':
            return GroupingSeparator.SPACE
        else:
            raise ValueError(f'Invalid grouping separator flag '
                             f'\'{flag}\'.')


class DecimalSeparator(Enum):
    POINT = 'point'
    COMMA = 'comma'

    @staticmethod
    def to_char(decimal_separator: 'DecimalSeparator'):
        if decimal_separator is DecimalSeparator.POINT:
            return '.'
        elif decimal_separator is DecimalSeparator.COMMA:
            return ','
        else:
            raise ValueError(f'Invalid decimal separator: '
                             f'{decimal_separator}.')

    @staticmethod
    def from_flag(flag: str):
        if flag == '.':
            return DecimalSeparator.POINT
        elif flag == ',':
            return DecimalSeparator.COMMA
        else:
            raise ValueError(f'Invalid decimal separator flag {flag}.')
