from __future__ import annotations

import re
from decimal import Decimal

from sciform import modes
from sciform import prefix as prefix_module

finite_val_pattern = r"(?:[-+]?[\d.,_ ]*\d)"
non_finite_val_pattern = r"(?:[+-]?(?:nan|NAN|inf|INF))"
any_val_pattern = rf"(?:{finite_val_pattern}|{non_finite_val_pattern})"
pm_pattern = rf"(?:(?P<pm_val>{any_val_pattern})(?: ± |±)(?P<pm_unc>{any_val_pattern}))"
paren_pattern = rf"(?:(?P<paren_val>{any_val_pattern})\((?P<paren_unc>{any_val_pattern})\))"

ascii_exp_pattern = r"(?P<ascii_exp>(?P<ascii_base>[eEbB])(?P<ascii_exp_val>[+-]\d+))"
uni_exp_pattern = r"(?P<uni_exp>×(?P<uni_base>10|2)(?P<uni_exp_val>[⁺⁻]?[⁰¹²³⁴⁵⁶⁷⁸⁹]+))"
prefix_exp_pattern = r"(?:\ (?P<prefix_exp>[a-zA-zμ]+))"
percent_exp_pattern = r"(?P<percent_exp>%)"
any_exp_pattern = rf"(?:{ascii_exp_pattern}|{uni_exp_pattern}|{prefix_exp_pattern}|{percent_exp_pattern})"

no_exp_pattern = rf"^{pm_pattern}|(?P<non_finite_val>{non_finite_val_pattern})$"
optional_exp_pattern = rf"^(?:(?P<val>{finite_val_pattern})|{paren_pattern})(?P<exp>{any_exp_pattern})?$"
always_exp_pattern = rf"^(?:\((?P<non_finite_val>{non_finite_val_pattern})\)|\({pm_pattern}\))(?P<exp>{any_exp_pattern})$"

superscript_translation = str.maketrans("⁺⁻⁰¹²³⁴⁵⁶⁷⁸⁹", "+-0123456789")


def extract_exp_base_exp_val(
    match: re.Match,
) -> tuple[int, int]:
    if match.group("ascii_exp"):
        base = match.group("ascii_base")
        if base.lower() == "e":
            base = 10
        elif base.lower() == "b":
            base = 2
        else:
            raise ValueError
        exp_val = int(match.group("ascii_exp_val"))
    elif match.group("uni_exp"):
        base = int(match.group("uni_base"))
        exp_val = int(match.group("uni_exp_val").translate(superscript_translation))
    elif prefix_exp := match.group("prefix_exp"):
        candidate_base_exp_val_pairs = []
        for key, value in prefix_module.si_val_to_prefix_dict.items():
            if prefix_exp == value:
                candidate_base_exp_val_pairs.append((10, key))
        for key, value in prefix_module.pp_val_to_prefix_dict.items():
            if prefix_exp == value:
                candidate_base_exp_val_pairs.append((10, key))
        for key, value in prefix_module.iec_val_to_prefix_dict.items():
            if prefix_exp == value:
                candidate_base_exp_val_pairs.append((2, key))
        if len(candidate_base_exp_val_pairs) == 0:
            raise ValueError
        if len(candidate_base_exp_val_pairs) > 1:
            print("Multiple candidate translations found, using the first one.")
        base, exp_val = candidate_base_exp_val_pairs[0]
    elif match.group("percent_exp"):
        base = 10
        exp_val = -2
    else:
        raise ValueError
    return base, exp_val


def strip_separators(
    input_str: str,
    decimal_separator: modes.DecimalSeparators = ".",
) -> str:
    for separator in modes.SeparatorEnum:
        if separator != decimal_separator:
            input_str = input_str.replace(separator, "")
    return input_str


def extract_val_unc(
    input_str: str,
    decimal_separator: modes.DecimalSeparators = ".",
) -> tuple[Decimal, Decimal | None]:
    if match := re.fullmatch(no_exp_pattern, input_str):
        if val := match.group("non_finite_val"):
            unc = None
        else:
            val = match.group("pm_val")
            unc = match.group("pm_unc")
        base = 10
        exp_val = 0
    elif match := re.fullmatch(optional_exp_pattern, input_str):
        if match.group("exp"):
            base, exp_val = extract_exp_base_exp_val(match)
        else:
            base = 10
            exp_val = 0
        if val := match.group("val"):
            unc = None
        else:
            val = match.group("paren_val")
            unc = match.group("paren_unc")
            if decimal_separator in val and decimal_separator not in unc:
                if unc.lower() != "nan" and "inf" not in unc.lower():
                    val = strip_separators(val, decimal_separator)
                    unc = strip_separators(unc, decimal_separator)
                    val_frac_part = val.split(decimal_separator)[1]
                    num_missing_zeros = len(val_frac_part) - len(unc)
                    unc = "0." + "0"*num_missing_zeros + unc

    elif match := re.fullmatch(always_exp_pattern, input_str):
        base, exp_val = extract_exp_base_exp_val(match)
        if val := match.group("non_finite_val"):
            unc = None
        else:
            val = match.group("pm_val")
            unc = match.group("pm_unc")
    else:
        raise ValueError

    val = strip_separators(val, decimal_separator)
    if unc is not None:
        unc = strip_separators(unc, decimal_separator)

    val = Decimal(val)

    if unc is not None:
        unc = Decimal(unc)

    base = Decimal(base)
    exp_val = Decimal(exp_val)

    if val.is_finite():
        val *= base**exp_val
    if unc is not None and unc.is_finite():
        unc *= base**exp_val

    return val, unc
