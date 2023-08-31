import re

from sciform.format_options import FormatOptions
from sciform.modes import (FillMode, SignMode, GroupingSeparator, RoundMode,
                           ExpMode, ExpFormat)


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

fill_mode_mapping = {' ': FillMode.SPACE,
                     '0': FillMode.ZERO,
                     None: None}

sign_mode_mapping = {'-': SignMode.NEGATIVE,
                     '+': SignMode.ALWAYS,
                     ' ': SignMode.SPACE,
                     None: None}

separator_mapping = {'n': GroupingSeparator.NONE,
                     ',': GroupingSeparator.COMMA,
                     '.': GroupingSeparator.POINT,
                     's': GroupingSeparator.SPACE,
                     '_': GroupingSeparator.UNDERSCORE,
                     None: None}

round_mode_mapping = {'!': RoundMode.SIG_FIG,
                      '.': RoundMode.DEC_PLACE,
                      None: None}


def format_options_from_fmt_spec(fmt_spec: str) -> 'FormatOptions':
    match = pattern.match(fmt_spec)
    if match is None:
        raise ValueError(f'Invalid format specifier: \'{fmt_spec}\'')

    fill_mode_flag = match.group('fill_mode')
    if fill_mode_flag is not None:
        fill_mode = fill_mode_mapping[fill_mode_flag]
    else:
        fill_mode = None

    sign_mode_flag = match.group('sign_mode')
    if sign_mode_flag is not None:
        sign_mode = sign_mode_mapping[sign_mode_flag]
    else:
        sign_mode = None

    alternate_mode = match.group('alternate_mode')
    alternate_mode = alternate_mode is not None

    top_dig_place = match.group('top_dig_place')
    if top_dig_place is not None:
        top_dig_place = int(top_dig_place)
        val_unc_match_widths = True
    else:
        top_dig_place = None
        val_unc_match_widths = None

    upper_separator_flag = match.group('upper_separator')
    upper_separator = separator_mapping[upper_separator_flag]

    decimal_separator_flag = match.group('decimal_separator')
    decimal_separator = separator_mapping[decimal_separator_flag]

    lower_separator_flag = match.group('lower_separator')
    lower_separator = separator_mapping[lower_separator_flag]

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
            exp_mode = ExpMode.FIXEDPOINT
        elif exp_mode == '%':
            exp_mode = ExpMode.PERCENT
        elif exp_mode in ['e', 'E']:
            exp_mode = ExpMode.SCIENTIFIC
        elif exp_mode in ['r', 'R']:
            if alternate_mode:
                exp_mode = ExpMode.ENGINEERING_SHIFTED
            else:
                exp_mode = ExpMode.ENGINEERING
        elif exp_mode in ['b', 'B']:
            if alternate_mode:
                exp_mode = ExpMode.BINARY_IEC
            else:
                exp_mode = ExpMode.BINARY
    else:
        capitalize = None

    exp_val = match.group('exp_val')
    if exp_val is not None:
        exp_val = int(exp_val)

    prefix_exp = match.group('prefix_mode')
    if prefix_exp is not None:
        exp_format = ExpFormat.PREFIX
    else:
        exp_format = None

    bracket_unc = match.group('bracket_unc')
    if bracket_unc is not None:
        bracket_unc = True
    else:
        bracket_unc = None

    return FormatOptions(
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
