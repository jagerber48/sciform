import re
from copy import copy


si_val_to_prefix_dict = {30: 'Q',
                         27: 'R',
                         24: 'Y',
                         21: 'Z',
                         18: 'E',
                         15: 'P',
                         12: 'T',
                         9: 'G',
                         6: 'M',
                         3: 'k',
                         0: '',
                         -3: 'm',
                         -6: 'μ',
                         -9: 'n',
                         -12: 'p',
                         -15: 'f',
                         -18: 'a',
                         -21: 'z',
                         -24: 'y',
                         -27: 'r',
                         -30: 'q'}

iec_val_to_prefix_dict = {0: '',
                          10: 'Ki',
                          20: 'Mi',
                          30: 'Gi',
                          40: 'Ti',
                          50: 'Pi',
                          60: 'Ei',
                          70: 'Zi',
                          80: 'Yi'}


def replace_prefix(num_str: str, extra_si_prefixes: dict[int, str] = None,
                   extra_iec_prefixes: dict[int, str] = None):
    match = re.match(r'''
                         ^
                         (?P<before>.*?)
                         ((?P<exp_type>[eEbB])(?P<exp_val>[+-]?\d+))?
                         $
                      ''', num_str, re.VERBOSE)

    before = match.group('before')
    exp_type = match.group('exp_type')
    if exp_type is None:
        return num_str
    exp_val = match.group('exp_val') or 0
    exp_val = int(exp_val)
    if exp_val == 0:
        return before

    if exp_type in ['e', 'E']:
        val_to_prefix_dict = copy(si_val_to_prefix_dict)
        if extra_si_prefixes is not None:
            val_to_prefix_dict.update(extra_si_prefixes)
    else:
        val_to_prefix_dict = copy(iec_val_to_prefix_dict)
        if extra_iec_prefixes is not None:
            val_to_prefix_dict.update(extra_iec_prefixes)
    try:
        prefix = val_to_prefix_dict[exp_val]
        return f'{before} {prefix}'
    except KeyError:
        return num_str
