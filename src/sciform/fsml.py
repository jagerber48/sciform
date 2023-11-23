import re

from sciform.user_options import UserOptions


pattern = re.compile(r'''^
                         (?:(?P<fill_mode>[ 0])=)?
                         (?P<sign_mode>[-+ ])?
                         (?P<alternate_mode>\#)?
                         (?P<top_dig_place>\d+)?
                         (?P<upper_separator>[n,.s_])?
                         (?P<decimal_separator>[.,])?
                         (?P<lower_separator>[ns_])?
                         (?:(?P<round_mode>[.!])(?P<ndigits>[+-]?\d+))?
                         (?P<exp_mode>[fF%eErRbB])?
                         (?:x(?P<exp_val>[+-]?\d+))?
                         (?P<prefix_mode>p)?
                         (?P<bracket_unc>\(\))?
                         $''', re.VERBOSE)


def format_options_from_fmt_spec(fmt_spec: str) -> UserOptions:
    match = pattern.match(fmt_spec)
    if match is None:
        raise ValueError(f'Invalid format specifier: \'{fmt_spec}\'')

    fill_mode = match.group('fill_mode')
    sign_mode = match.group('sign_mode')

    alternate_mode = match.group('alternate_mode')
    alternate_mode = alternate_mode is not None

    top_dig_place = match.group('top_dig_place')
    if top_dig_place is not None:
        top_dig_place = int(top_dig_place)
        val_unc_match_widths = True
    else:
        top_dig_place = None
        val_unc_match_widths = None

    upper_separator = match.group('upper_separator')
    if upper_separator is not None:
        upper_separator = upper_separator.replace('n', '')
        upper_separator = upper_separator.replace('s', ' ')

    decimal_separator = match.group('decimal_separator')

    lower_separator = match.group('lower_separator')
    if lower_separator is not None:
        lower_separator = lower_separator.replace('n', '')
        lower_separator = lower_separator.replace('s', ' ')

    round_mode_mapping = {'!': 'sig_fig',
                          '.': 'dec_place',
                          None: None}

    round_mode_flag = match.group('round_mode')
    round_mode = round_mode_mapping[round_mode_flag]

    ndigits = match.group('ndigits')
    if ndigits is not None:
        ndigits = int(ndigits)
    else:
        ndigits = None

    exp_mode = match.group('exp_mode')
    if exp_mode is not None:
        capitalize = exp_mode.isupper()
        if exp_mode in ['f', 'F']:
            exp_mode = 'fixed_point'
        elif exp_mode == '%':
            exp_mode = 'percent'
        elif exp_mode in ['e', 'E']:
            exp_mode = 'scientific'
        elif exp_mode in ['r', 'R']:
            if alternate_mode:
                exp_mode = 'engineering_shifted'
            else:
                exp_mode = 'engineering'
        elif exp_mode in ['b', 'B']:
            if alternate_mode:
                exp_mode = 'binary_iec'
            else:
                exp_mode = 'binary'
    else:
        capitalize = None

    exp_val = match.group('exp_val')
    if exp_val is not None:
        exp_val = int(exp_val)

    prefix_exp = match.group('prefix_mode')
    if prefix_exp is not None:
        exp_format = 'prefix'
    else:
        exp_format = None

    bracket_unc = match.group('bracket_unc')
    if bracket_unc is not None:
        bracket_unc = True
    else:
        bracket_unc = None

    return UserOptions(
        fill_mode=fill_mode,
        sign_mode=sign_mode,
        top_dig_place=top_dig_place,
        upper_separator=upper_separator,
        decimal_separator=decimal_separator,
        lower_separator=lower_separator,
        round_mode=round_mode,
        ndigits=ndigits,
        exp_mode=exp_mode,
        exp_val=exp_val,
        exp_format=exp_format,
        capitalize=capitalize,
        bracket_unc=bracket_unc,
        val_unc_match_widths=val_unc_match_widths
    )
