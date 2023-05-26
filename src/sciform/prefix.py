import re


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
                         -6: 'u',
                         -9: 'n',
                         -12: 'p',
                         -15: 'f',
                         -18: 'a',
                         -21: 'z',
                         -24: 'y',
                         -27: 'r',
                         -30: 'q'}

iec_val_to_prefix_dict = {0: '',
                          10: 'K',
                          20: 'M',
                          30: 'G',
                          40: 'T',
                          50: 'P',
                          60: 'E'}


def replace_prefix(num_str: str):
    match = re.match(r'''
                         ^
                         (?P<before>.*?)
                         ((?P<exp_type>[eEbB])(?P<exp_val>[+-]?\d+))?
                         $
                      ''', num_str, re.VERBOSE)

    before = match.group('before')
    exp_type = match.group('exp_type')
    if not exp_type:
        return num_str
    exp_val = match.group('exp_val') or 0
    exp_val = int(exp_val)

    if exp_type in ['e', 'E']:
        val_to_prefix_dict = si_val_to_prefix_dict
    else:
        val_to_prefix_dict = iec_val_to_prefix_dict
    try:
        prefix = val_to_prefix_dict[exp_val]
        return f'{before} {prefix}'
    except KeyError:
        return num_str
