import re

from sciform.format_utils import get_superscript_exp_str

times_str = "×"


def standard_exp_str_to_superscript_exp_str(match: re.Match) -> str:
    exp_symbol = match.group("exp_symbol")
    symbol_to_base_dict = {"e": 10, "b": 2}
    base = symbol_to_base_dict[exp_symbol.lower()]

    exp_val_str = match.group("exp_val")
    exp_val = int(exp_val_str)

    superscript_exp_str = get_superscript_exp_str(base, exp_val)
    return superscript_exp_str


def make_latex_superscript(match: re.Match) -> str:
    sup_trans = str.maketrans("⁺⁻⁰¹²³⁴⁵⁶⁷⁸⁹", "+-0123456789")
    exp_val_non_sup = match.group(0).translate(sup_trans)
    return fr"^{{{exp_val_non_sup}}}"


def sciform_to_latex(formatted_str: str) -> str:
    result_str = re.sub(
        r"((?P<exp_symbol>[eEbB])(?P<exp_val>[+-]\d+))$",
        standard_exp_str_to_superscript_exp_str,
        formatted_str,
    )

    result_str = re.sub(
        r"([a-zA-Zμ]+)",
        r"\\text{\1}",
        result_str,
    )

    replacements = (
        ("(", r"\left("),
        (")", r"\right)"),
        ("%", r"\%"),
        ("_", r"\_"),
        (" ", r"\:"),
        ("±", r"\pm"),
        ("×", r"\times"),
        ("μ", r"\textmu")
    )
    for old_chars, new_chars in replacements:
        result_str = result_str.replace(old_chars, new_chars)

    result_str = re.sub(
        r"([⁺⁻⁰¹²³⁴⁵⁶⁷⁸⁹]+)",
        make_latex_superscript,
        result_str,
    )

    return result_str
