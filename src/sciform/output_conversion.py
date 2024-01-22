"""Convert sciform outputs into latex commands."""

import re

from sciform.format_utils import get_superscript_exp_str

times_str = "×"


def standard_exp_str_to_superscript_exp_str(match: re.Match) -> str:
    """Convert matched ascii exp_str to unicode superscript exp_str."""
    exp_symbol = match.group("exp_symbol")
    symbol_to_base_dict = {"e": 10, "b": 2}
    base = symbol_to_base_dict[exp_symbol.lower()]

    exp_val_str = match.group("exp_val")
    exp_val = int(exp_val_str)

    superscript_exp_str = get_superscript_exp_str(base, exp_val)
    return superscript_exp_str


def make_latex_superscript(match: re.Match) -> str:
    """Convert matched superscript exp_str to latex exp_str."""
    sup_trans = str.maketrans("⁺⁻⁰¹²³⁴⁵⁶⁷⁸⁹", "+-0123456789")
    exp_val_non_sup = match.group(0).translate(sup_trans)
    return rf"^{{{exp_val_non_sup}}}"


def sciform_to_latex(formatted_str: str) -> str:
    r"""
    Convert a sciform output string into a latex string.

    conversion proceeds by

    1. If an exponent string is present and in ascii format
       (e.g. ``"e+03"``) then convert it to superscript notation
       (e.g. ``"×10³"``).
    2. Bundle any unicode superscript substrings into latex
       superscripts, e.g. ``"⁻²"`` -> ``r"^{-2}"``.
    3. Wrap any strings of alphabetic characters (plus ``"μ"``) in latex
       text environment, e.g. ``"nan"`` -> ``r"\text{nan}"`` or
       ``"k"`` -> ``r"\text{k}"``.
    4. Make the following character replacments:

      * ``"%"`` -> ``r"\%"``
      * ``"_"`` -> ``r"\_"``
      * ``" "`` -> ``r"\:"``
      * ``"±"`` -> ``r"\pm"``
      * ``"×"`` -> ```r"\times"``
      * ``"μ"`` -> ``r"\textmu"``

    >>> from sciform import sciform_to_latex
    >>> print(sciform_to_latex("(7.8900 ± 0.0001)×10²"))
    (7.8900\:\pm\:0.0001)\times10^{2}
    >>> print(sciform_to_latex("16.18033E+03"))
    16.18033\times10^{3}
    """
    result_str = re.sub(
        r"((?P<exp_symbol>[eEbB])(?P<exp_val>[+-]\d+))$",
        standard_exp_str_to_superscript_exp_str,
        formatted_str,
    )

    result_str = re.sub(
        r"([⁺⁻⁰¹²³⁴⁵⁶⁷⁸⁹]+)",
        make_latex_superscript,
        result_str,
    )

    result_str = re.sub(
        r"([a-zA-Zμ]+)",
        r"\\text{\1}",
        result_str,
    )

    replacements = (
        ("%", r"\%"),
        ("_", r"\_"),
        (" ", r"\:"),
        ("±", r"\pm"),
        ("×", r"\times"),
        ("μ", r"\textmu"),
    )
    for old_chars, new_chars in replacements:
        result_str = result_str.replace(old_chars, new_chars)

    return result_str
