from typing import Literal

_FILL_TYPES = Literal[0, '0', 'zero', ' ', 'space']

_SIGN_TYPES = Literal['-', 'negative', '+', 'always', ' ', 'space']

_UPPER_SEP_TYPES = Literal['', 'none', ',', 'comma', '.', 'point',
                           ' ', 'space', '_', 'underscore']

_DECIMAL_SEP_TYPES = Literal['.', 'point', ',', 'comma']

_LOWER_SEP_TYPES = Literal['', 'none', ' ', 'space',
                           '_', 'underscore']

_ROUND_TYPES = Literal['precision', 'sig_fig']

_FORMAT_TYPES = Literal['fixed_point', 'percent', 'scientific', 'engineering',
                        'engineering_shifted', 'binary', 'binary_iec']

AUTO = object()
