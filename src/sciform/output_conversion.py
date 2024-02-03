"""Convert sciform outputs into latex commands."""
from __future__ import annotations

import re
from typing import Literal, get_args

ascii_exp_pattern = re.compile(
    r"^(?P<mantissa>.*)(?P<ascii_base>[eEbB])(?P<exp>[+-]\d+)$",
)
ascii_base_dict = {"e": 10, "E": 10, "b": 2, "B": 2}

unicode_exp_pattern = re.compile(
    r"^(?P<mantissa>.*)×(?P<base>10|2)(?P<super_exp>[⁺⁻]?[⁰¹²³⁴⁵⁶⁷⁸⁹]+)$",
)
superscript_translation = str.maketrans("⁺⁻⁰¹²³⁴⁵⁶⁷⁸⁹", "+-0123456789")

output_formats = Literal["latex", "html", "ascii"]


def _make_exp_str(
    base: int,
    exp: int,
    output_format: output_formats,
    *,
    capitalize: bool = False,
) -> str:
    if output_format == "latex":
        return rf"\times{base}^{{{exp}}}"
    if output_format == "html":
        return f"×{base}<sup>{exp}</sup>"
    if output_format == "ascii":
        if base == 10:
            exp_str = f"e{exp:+03d}"
        elif base == 2:
            exp_str = f"b{exp:+03d}"
        else:
            msg = f"base must be 10 or 2, not {base}"
            raise ValueError(msg)
        if capitalize:
            exp_str = exp_str.upper()
        return exp_str
    msg = f"output_format must be in {get_args(output_formats)}, not {output_format}"
    raise ValueError(msg)


def _string_replacements(input_str: str, replacements: list[tuple[str, str]]) -> str:
    result_str = input_str
    for old_chars, new_chars in replacements:
        result_str = result_str.replace(old_chars, new_chars)
    return result_str


def convert_sciform_format(
    formatted_str: str,
    output_format: output_formats,
) -> str:
    r"""
    Convert sciform output to new format for different output contexts.

    convert_sciform_format() is used to convert a sciform output string
    into different formats for presentation in different contexts.
    Currently, LaTeX, HTML, and ASCII outputs are supported.

    LaTeX
    =====

    For LaTeX conversion the resulting string is a valid LaTeX command
    bracketed in "$" symbols to indicate it is in LaTeX math
    environment. The following transformations are applied.

    * The exponent is displayed using the LaTeX math superscript
      construction, e.g. "10^{-3}"
    * Any strings of alphabetic characters (plus ``"μ"``) are wrapped in
      the LaTeX math-mode text environment, e.g.
      ``"nan"`` -> ``r"\text{nan}"`` or ``"k"`` -> ``r"\text{k}"``.
    * The following character replacments are made:

      * ``"%"`` -> ``r"\%"``
      * ``"_"`` -> ``r"\_"``
      * ``" "`` -> ``r"\:"``
      * ``"±"`` -> ``r"\pm"``
      * ``"×"`` -> ```r"\times"``
      * ``"μ"`` -> ``r"\textmu"``

    >>> from sciform.output_conversion import convert_sciform_format
    >>> print(convert_sciform_format("(7.8900 ± 0.0001)×10²", "latex"))
    $(7.8900\:\pm\:0.0001)\times10^{2}$
    >>> print(convert_sciform_format("16.18033E+03", "latex"))
    $16.18033\times10^{3}$

    HTML
    ====

    In HTML mode superscripts are representing using e.g.
    "<sup>-3</sup>".

    >>> from sciform.output_conversion import convert_sciform_format
    >>> print(convert_sciform_format("(7.8900 ± 0.0001)×10²", "html"))
    (7.8900 ± 0.0001)×10<sup>2</sup>
    >>> print(convert_sciform_format("16.18033E+03", "html"))
    16.18033×10<sup>3</sup>

    ASCII
    =====

    In the ASCII mode exponents are always represented as e.g. "e-03".
    Also, "±" is replaced by "+/-" and "μ" is replaced by "u".

    >>> from sciform.output_conversion import convert_sciform_format
    >>> print(convert_sciform_format("(7.8900 ± 0.0001)×10²", "ascii"))
    (7.8900 +/- 0.0001)e+02
    >>> print(convert_sciform_format("16.18033E+03", "ascii"))
    16.18033E+03
    """
    if match := re.match(ascii_exp_pattern, formatted_str):
        mantissa = match.group("mantissa")
        ascii_base = match.group("ascii_base")
        base = ascii_base_dict[ascii_base]
        exp = int(match.group("exp"))
        exp_str = _make_exp_str(
            base,
            exp,
            output_format,
            capitalize=ascii_base.isupper(),
        )
        main_str = mantissa
        suffix_str = exp_str
    elif match := re.match(unicode_exp_pattern, formatted_str):
        mantissa = match.group("mantissa")
        base = int(match.group("base"))
        super_exp = match.group("super_exp")
        exp = int(super_exp.translate(superscript_translation))
        exp_str = _make_exp_str(base, exp, output_format)
        main_str = mantissa
        suffix_str = exp_str
    else:
        main_str = formatted_str
        suffix_str = ""

    if output_format == "latex":
        main_str = re.sub(
            r"([a-zA-Zμ]+)",
            r"\\text{\1}",
            main_str,
        )

        replacements = [
            ("%", r"\%"),
            ("_", r"\_"),
            (" ", r"\:"),
            ("±", r"\pm"),
            ("×", r"\times"),
            ("μ", r"\textmu"),
        ]
        main_str = _string_replacements(main_str, replacements)
        return f"${main_str}{suffix_str}$"

    if output_format == "html":
        return f"{main_str}{suffix_str}"
    if output_format == "ascii":
        replacements = [
            ("±", "+/-"),
            ("μ", "u"),
        ]
        main_str = _string_replacements(main_str, replacements)
        return f"{main_str}{suffix_str}"
    msg = f"output_format must be in {get_args(output_formats)}, not {output_format}"
    raise ValueError(msg)
