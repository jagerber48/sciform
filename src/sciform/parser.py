# ruff: noqa: ERA001

"""Parse formatted strings back into value/uncertainty pairs."""

from __future__ import annotations

import re
from decimal import Decimal

from sciform import modes
from sciform import prefix as prefix_module

# language=pythonverboseregexp
upper_grouping_pattern = r"((_\d{3})*|(\ \d{3})*|(\.\d{3})*|(,\d{3})*|(\d{3})*)"
# language=pythonverboseregexp
lower_grouping_pattern = r"((\d{3}_)*|(\d{3}\ )*|(\d{3})*)"

# language=pythonverboseregexp
finite_val_pattern = rf"""
(
  [ +-]?  # Sign
  \ *  # Leading zeros or spaces
  (\d{{1,3}}){upper_grouping_pattern}  # Leading digit groups
  (  # Start of optional fractional part
    ((?<!,\d{{3}}),|(?<!\.\d{{3}})\.)  # decimal_separator != upper_separator
    {lower_grouping_pattern}(\d{{1,3}})  # Trailing digit groups
  )?  # End of optional fractional part
)
"""
# language=pythonverboseregexp
non_finite_val_pattern = r"(nan|NAN|([ +-]?(inf|INF)))"
# language=pythonverboseregexp
any_val_pattern = rf"({finite_val_pattern}|{non_finite_val_pattern})"

# language=pythonverboseregexp
pm_pattern = rf"""
(
  (?P<pm_val>{any_val_pattern})  # Value
  (\ (±|\+/-)\ |(±|\+/-))  # +/- symbol (optional whitespace)
  (?P<pm_unc>{any_val_pattern})  # Uncertainty
)
"""
# language=pythonverboseregexp
paren_pattern = rf"""
((?P<paren_val>{any_val_pattern})\((?P<paren_unc>{any_val_pattern})\))
"""

# language=pythonverboseregexp
ascii_exp_pattern = r"(?P<ascii_exp>(?P<ascii_base>[eEbB])(?P<ascii_exp_val>[+-]\d+))"
# language=pythonverboseregexp
uni_exp_pattern = r"(?P<uni_exp>×(?P<uni_base>10|2)(?P<uni_exp_val>[⁺⁻]?[⁰¹²³⁴⁵⁶⁷⁸⁹]+))"
# language=pythonverboseregexp
prefix_exp_pattern = r"(\ (?P<prefix_exp>[a-zA-zμ]+))"
# language=pythonverboseregexp
percent_exp_pattern = r"(?P<percent_exp>%)"
# language=pythonverboseregexp
any_exp_pattern = rf"""
(
  {ascii_exp_pattern}
  |{uni_exp_pattern}
  |{prefix_exp_pattern}
  |{percent_exp_pattern}
)
"""

# language=pythonverboseregexp
no_exp_pattern = rf"^{pm_pattern}|(?P<non_finite_val>{non_finite_val_pattern})$"
# language=pythonverboseregexp
optional_exp_pattern = rf"""
^((?P<val>{finite_val_pattern})|{paren_pattern})(?P<exp>{any_exp_pattern})?$
"""
# language=pythonverboseregexp
always_exp_pattern = rf"""
^
(
  \((?P<non_finite_val>{non_finite_val_pattern})\)
  |\({pm_pattern}\)
)
(?P<exp>{any_exp_pattern})
$
"""

superscript_translation = str.maketrans("⁺⁻⁰¹²³⁴⁵⁶⁷⁸⁹", "+-0123456789")


def _get_ascii_base_exp_val(match: re.Match) -> tuple[int, int]:
    base = match.group("ascii_base")
    if base.lower() == "e":
        base = 10
    elif base.lower() == "b":
        base = 2
    else:
        raise ValueError
    exp_val = int(match.group("ascii_exp_val"))
    return base, exp_val


def _get_unicode_base_exp_val(match: re.Match) -> tuple[int, int]:
    base = int(match.group("uni_base"))
    exp_val = int(match.group("uni_exp_val").translate(superscript_translation))
    return base, exp_val


def _get_prefix_base_exp_val(prefix_exp: str) -> tuple[int, int]:
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
        msg = f'Unrecognized prefix: "{prefix_exp}". Unable to parse input.'
        raise ValueError(msg)
    if len(set(candidate_base_exp_val_pairs)) > 1:
        msg = (
            f'Multiple translations found for prefix "{prefix_exp}". Unable to '
            f"parse input."
        )
        raise ValueError(msg)
    base, exp_val = candidate_base_exp_val_pairs[0]
    return base, exp_val


def _extract_exp_base_exp_val(
    match: re.Match,
) -> tuple[int, int]:
    if match.group("ascii_exp"):
        base, exp_val = _get_ascii_base_exp_val(match)
    elif match.group("uni_exp"):
        base, exp_val = _get_unicode_base_exp_val(match)
    elif prefix_exp := match.group("prefix_exp"):
        base, exp_val = _get_prefix_base_exp_val(prefix_exp)
    elif match.group("percent_exp"):
        base = 10
        exp_val = -2
    else:
        raise ValueError
    return base, exp_val


def _extract_decimal_separator(
    val: str,
    decimal_separator: modes.DecimalSeparators,
) -> modes.DecimalSeparators:
    val = val.replace(" ", "")
    val = val.replace("_", "")
    if "." not in val and "," not in val:
        # Ambiguous, must fall back to default.
        pass
    elif "." in val and "," in val:
        if re.match(r"^[^.]+,[^.]+\..*$", val):
            # If a decimal point appears after a comma it must be the decimal separator.
            decimal_separator = "."
        else:
            decimal_separator = ","
    elif "." in val and "," not in val:
        upper, lower = val.split(".")
        if len(upper) <= 3 and len(lower) == 3:
            """
            If there are 1, 2, or 3 digits before the separator and 3 after then it is
            ambiguous whether the separator is an upper or decimal separator.
            e.g 12,456 could be 12000 + 456, or 12 + 0.456. Must fall back on the
            default.
            """
            pass  # noqa: PIE790
        else:
            """
            Otherwise the separator must be the decimal separator, e.g. 1234.45 must be
            1234 + 0.45.
            """
            decimal_separator = "."
    elif "," in val and "." not in val:
        upper, lower = val.split(",")
        if len(upper) <= 3 and len(lower) == 3:
            # See comments above for logic
            pass
        else:
            # See comments above for logic
            decimal_separator = ","
    else:
        raise ValueError
    return decimal_separator


def _normalize_separators(
    input_str: str,
    decimal_separator: modes.DecimalSeparators = ".",
) -> str:
    for separator in modes.SeparatorEnum:
        if separator != decimal_separator:
            input_str = input_str.replace(separator, "")
    input_str = input_str.replace(",", ".")
    return input_str


def _parse_no_exp_pattern(match: re.Match) -> tuple[str, str | None, int, int]:
    if val := match.group("non_finite_val"):
        unc = None
    else:
        val = match.group("pm_val")
        unc = match.group("pm_unc")
    base = 10
    exp_val = 0
    return val, unc, base, exp_val


def _parse_optional_exp_pattern(match: re.Match) -> tuple[str, str | None, int, int]:
    if match.group("exp"):
        base, exp_val = _extract_exp_base_exp_val(match)
    else:
        base = 10
        exp_val = 0
    if val := match.group("val"):
        unc = None
    else:
        val = match.group("paren_val")
        unc = match.group("paren_unc")
    return val, unc, base, exp_val


def _parse_always_exp_pattern(match: re.Match) -> tuple[str, str | None, int, int]:
    base, exp_val = _extract_exp_base_exp_val(match)
    if val := match.group("non_finite_val"):
        unc = None
    else:
        val = match.group("pm_val")
        unc = match.group("pm_unc")
    return val, unc, base, exp_val


def parse_val_unc_from_str(
    input_str: str,
    decimal_separator: modes.DecimalSeparators = ".",
) -> tuple[Decimal, Decimal | None]:
    """
    Parse a formatted string back into numbers representing the value and uncertainty.

    First the input string is matched to one of three regex patterns.

      * A pattern which can never have an exponent attached such as
        "nan" or "123.000 ± 0.456".
      * A pattern which can optional have an exponent attached such as
        "123", "123e+01", "123.000(456)", or "123.000(456)e+01".
      * A pattern which must always have an exponent attached such as
        (INF)e+00, or "(123.000 ± 0.456)e+01"

    Whichever pattern is matched is then parsed to extract the value,
    uncertainty, and exponent base and value (if no exponent information
    is available then base is set to 10 and value is set to 0).

    Next, grouping separators such as "_" or " " are stripped from the
    value and uncertainty strings. An algorithm is then run to detect
    whether "." or "," is the decimal separator. If the decimal
    separator can be resolved then the other one is removed and the
    decimal separator is changed from "," to "." if necessary. Note that
    for some inputs it is impossible to resolve whether "." or "," is
    the decimal separator. In these cases the code must fall back on the
    `decimal_separator` input parameter.

    If the uncertainty string arose from a trimmed parentheses
    value/uncertainty string then the uncertainty string is un-trimmed.
    E.g. 124.456(7) results in value string "123.456" and uncertainty
    string "7". The uncertainty string must be expanded to "0.007".

    Finally, the value and uncertainty strings are converted to decimals
    and multiplied by the extracted exponents.
    """
    if match := re.fullmatch(no_exp_pattern, input_str, re.VERBOSE):
        val, unc, base, exp_val = _parse_no_exp_pattern(match)
    elif match := re.fullmatch(optional_exp_pattern, input_str, re.VERBOSE):
        val, unc, base, exp_val = _parse_optional_exp_pattern(match)
    elif match := re.fullmatch(always_exp_pattern, input_str, re.VERBOSE):
        val, unc, base, exp_val = _parse_always_exp_pattern(match)
    else:
        raise ValueError

    if val.lower() not in ("nan", "inf"):
        decimal_separator = _extract_decimal_separator(val, decimal_separator)
        val = _normalize_separators(val, decimal_separator)
    elif unc is not None and unc.lower() not in ("nan", "inf"):
        decimal_separator = _extract_decimal_separator(unc, decimal_separator)
        unc = _normalize_separators(unc, decimal_separator)

    if (
        unc is not None
        and "." in val
        and "." not in unc
        and unc.lower() not in ("nan", "inf")
    ):
        """
        Looking for cases like 123.456(7). At this point we would have
        val = "123.456" and unc = "7". We can see that unc has resulted
        from a trimmed parentheses value/uncertainty notation. We must
        un-trim it by prepending enough zeros to that the least
        significant decimal place of unc matches that of val.
        """
        val_frac_part = val.split(".")[1]
        num_missing_zeros = len(val_frac_part) - len(unc)
        unc = "0." + "0" * num_missing_zeros + unc

    base = Decimal(base)
    exp_val = Decimal(exp_val)
    val = Decimal(val)
    if val.is_finite():
        val *= base**exp_val

    if unc is not None:
        unc = Decimal(unc)
        if unc.is_finite():
            unc *= base**exp_val

    return val, unc
