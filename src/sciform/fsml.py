"""Parse Format Specification Mini Language."""

from __future__ import annotations

import re

from sciform.options.input_options import InputOptions

pattern = re.compile(
    r"""^
                         (?:(?P<left_pad_char>[ 0])=)?
                         (?P<sign_mode>[-+ ])?
                         (?P<alternate_mode>\#)?
                         (?P<left_pad_dec_place>\d+)?
                         (?:(?P<round_mode>[.!])(?P<ndigits>[+-]?\d+))?
                         (?P<exp_mode>[fF%eErRbB])?
                         (?:x(?P<exp_val>[+-]?\d+))?
                         (?P<prefix_mode>p)?
                         (?P<paren_uncertainty>\(\))?
                         $""",
    re.VERBOSE,
)


def parse_exp_mode(
    exp_mode: str | None,
    *,
    alternate_mode: bool,
) -> tuple[str | None, bool]:
    """Pase the exp_mode."""
    if exp_mode is not None:
        capitalize = exp_mode.isupper()
        if exp_mode in ["f", "F"]:
            exp_mode = "fixed_point"
        elif exp_mode == "%":
            exp_mode = "percent"
        elif exp_mode in ["e", "E"]:
            exp_mode = "scientific"
        elif exp_mode in ["r", "R"]:
            if alternate_mode:
                exp_mode = "engineering_shifted"
            else:
                exp_mode = "engineering"
        elif exp_mode in ["b", "B"]:
            if alternate_mode:
                exp_mode = "binary_iec"
            else:
                exp_mode = "binary"
    else:
        capitalize = None
    return exp_mode, capitalize


def format_options_from_fmt_spec(fmt_spec: str) -> InputOptions:
    """Resolve InputOptions from format specification string."""
    match = pattern.match(fmt_spec)
    if match is None:
        msg = f"Invalid format specifier: '{fmt_spec}'"
        raise ValueError(msg)

    left_pad_char = match.group("left_pad_char")
    sign_mode = match.group("sign_mode")

    alternate_mode = match.group("alternate_mode")
    alternate_mode = alternate_mode is not None

    left_pad_dec_place = match.group("left_pad_dec_place")
    if left_pad_dec_place is not None:
        left_pad_dec_place = int(left_pad_dec_place)

    round_mode_mapping = {"!": "sig_fig", ".": "dec_place", None: None}

    round_mode_flag = match.group("round_mode")
    round_mode = round_mode_mapping[round_mode_flag]

    ndigits = match.group("ndigits")
    if ndigits is not None:
        ndigits = int(ndigits)
    else:
        ndigits = None

    exp_mode = match.group("exp_mode")
    exp_mode, capitalize = parse_exp_mode(
        exp_mode,
        alternate_mode=alternate_mode,
    )

    exp_val = match.group("exp_val")
    if exp_val is not None:
        exp_val = int(exp_val)

    prefix_exp = match.group("prefix_mode")
    if prefix_exp is not None:
        exp_format = "prefix"
    else:
        exp_format = None

    paren_uncertainty = match.group("paren_uncertainty")
    if paren_uncertainty is not None:
        paren_uncertainty = True
    else:
        paren_uncertainty = None

    return InputOptions(
        left_pad_char=left_pad_char,
        sign_mode=sign_mode,
        left_pad_dec_place=left_pad_dec_place,
        round_mode=round_mode,
        ndigits=ndigits,
        exp_mode=exp_mode,
        exp_val=exp_val,
        exp_format=exp_format,
        capitalize=capitalize,
        paren_uncertainty=paren_uncertainty,
    )
