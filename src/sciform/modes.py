from enum import Enum


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
            raise ValueError(f'Invalid format type flag {flag}.')


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


class GroupingMode(Enum):
    NO_GROUPING = 'no_grouping'
    COMMA = 'comma'
    UNDERSCORE = 'underscore'
    SPACE = 'space'

    @staticmethod
    def to_char(grouping_mode: 'GroupingMode') -> str:
        if grouping_mode is GroupingMode.NO_GROUPING:
            return ''
        elif grouping_mode is GroupingMode.COMMA:
            return ','
        elif grouping_mode is GroupingMode.UNDERSCORE:
            return '_'
        elif grouping_mode is GroupingMode.SPACE:
            return ' '
        else:
            raise ValueError(f'Invalid grouping mode: {grouping_mode}')

    @staticmethod
    def from_flag(flag: str):
        if flag == '':
            return GroupingMode.NO_GROUPING
        elif flag == ',':
            return GroupingMode.COMMA
        elif flag == '_':
            return GroupingMode.UNDERSCORE
        elif flag == 'v':
            return GroupingMode.SPACE
        else:
            raise ValueError(f'Invalid sign mode flag {flag}.')
