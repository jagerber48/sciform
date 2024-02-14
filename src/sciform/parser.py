# ruff: noqa: ERA001

"""Parse formatted strings back into value/uncertainty pairs."""

from __future__ import annotations

import re
from decimal import Decimal
from typing import TYPE_CHECKING

from sciform import modes
from sciform import prefix as prefix_module
from sciform.global_configuration import get_global_options

if TYPE_CHECKING:  # pragma: no cover
    from sciform.format_utils import Number

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
    else:  # pragma: no cover
        msg = f'Unexpected ASCII base: "{base}"'
        raise ValueError(msg)
    exp_val = int(match.group("ascii_exp_val"))
    return base, exp_val


def _get_unicode_base_exp_val(match: re.Match) -> tuple[int, int]:
    base = int(match.group("uni_base"))
    exp_val = int(match.group("uni_exp_val").translate(superscript_translation))
    return base, exp_val


def _get_prefix_base_exp_val(prefix_exp: str) -> tuple[int, int]:
    candidate_base_exp_val_pairs = []
    global_options = get_global_options()

    si_translations = prefix_module.si_val_to_prefix_dict.copy()
    si_translations.update(global_options.extra_si_prefixes)
    for key, value in si_translations.items():
        if prefix_exp == value:
            candidate_base_exp_val_pairs.append((10, key))

    pp_translations = prefix_module.pp_val_to_prefix_dict.copy()
    pp_translations.update(global_options.extra_parts_per_forms)
    for key, value in pp_translations.items():
        if prefix_exp == value:
            candidate_base_exp_val_pairs.append((10, key))

    iec_translations = prefix_module.iec_val_to_prefix_dict.copy()
    iec_translations.update(global_options.extra_iec_prefixes)
    for key, value in iec_translations.items():
        if prefix_exp == value:
            candidate_base_exp_val_pairs.append((2, key))

    if len(candidate_base_exp_val_pairs) == 0:
        msg = f'Unrecognized prefix: "{prefix_exp}". Unable to parse input.'
        raise ValueError(msg)
    if len(set(candidate_base_exp_val_pairs)) > 1:
        candidate_exps = [
            candidate_pair[1] for candidate_pair in candidate_base_exp_val_pairs
        ]
        msg = (
            f'Multiple translations found for "{prefix_exp}": {candidate_exps}. '
            f"Unable to parse input."
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
    else:  # pragma: no cover
        msg = "Expected named match groups not found."
        raise ValueError(msg)
    return base, exp_val


def _infer_decimal_separator(
    val: str,
) -> modes.DecimalSeparators | None:
    val = val.replace(" ", "")
    val = val.replace("_", "")

    decimal_separator = None

    if "." in val and "," in val:
        """
        Both separators appear, determine which comes later and set that
        as the decimal separator.
        """
        if "." in val.split(",")[-1]:
            decimal_separator = "."
        else:
            decimal_separator = ","
    elif "." in val and "," not in val:
        if val.count(".") > 1:
            decimal_separator = ","
        else:
            upper, lower = val.split(".")
            if len(upper) > 3 or len(lower) != 3:
                """
                e.g. 1234.567 or 1.2
                In neither case can "." be an an upper separator. Lower
                separators can only appear if a decimal separator is present
                but only one separator is present so that is impossible.

                If len(upper) <= 3 and len(lower) == 3 then "." may be
                either an upper or decimal separator so we keep the
                decimal_passed that has been passed in.
                e.g. 12.456
                """
                decimal_separator = "."
    elif "," in val and "." not in val:
        if val.count(",") > 1:
            decimal_separator = "."
        else:
            upper, lower = val.split(",")
            if len(upper) > 3 or len(lower) != 3:
                # See comments above for logic
                decimal_separator = ","

    return decimal_separator


def _parse_decimal_separator(
    val: str,
    unc: str,
    decimal_separator: modes.DecimalSeparators | None,
) -> modes.DecimalSeparators:
    if decimal_separator is None:
        decimal_separator = get_global_options().decimal_separator

    val_decimal_separator = _infer_decimal_separator(val)
    if unc is not None:
        unc_decimal_separator = _infer_decimal_separator(unc)
    else:
        unc_decimal_separator = None
    if val_decimal_separator is not None:
        if (
            unc_decimal_separator is not None
            and unc_decimal_separator != val_decimal_separator
        ):
            msg = (
                f'Value "{val}" and uncertainty "{unc}" have different '
                f"decimal separators."
            )
            raise ValueError(msg)
        decimal_separator = val_decimal_separator
    elif unc_decimal_separator is not None:
        decimal_separator = unc_decimal_separator

    return decimal_separator


def _normalize_separators(
    input_str: str,
    decimal_separator: modes.DecimalSeparators,
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


def _extract_val_unc_base_exp(
    input_str: str,
) -> tuple[str, str | None, int, int]:
    if match := re.fullmatch(no_exp_pattern, input_str, re.VERBOSE):
        val, unc, base, exp_val = _parse_no_exp_pattern(match)
    elif match := re.fullmatch(optional_exp_pattern, input_str, re.VERBOSE):
        val, unc, base, exp_val = _parse_optional_exp_pattern(match)
    elif match := re.fullmatch(always_exp_pattern, input_str, re.VERBOSE):
        val, unc, base, exp_val = _parse_always_exp_pattern(match)
    else:
        msg = f'Input string "{input_str}" does not match any expected input format.'
        raise ValueError(msg)
    return val, unc, base, exp_val


def parse_val_unc_from_str(
    input_str: str,
    decimal_separator: modes.DecimalSeparators = None,
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
    val, unc, base, exp_val = _extract_val_unc_base_exp(input_str)

    decimal_separator = _parse_decimal_separator(val, unc, decimal_separator)

    val = _normalize_separators(val, decimal_separator)
    if unc is not None:
        unc = _normalize_separators(unc, decimal_separator)

    if (
        re.search(paren_pattern, input_str, re.VERBOSE)
        and re.match(finite_val_pattern, unc, re.VERBOSE)
        and "." in val
        and "." not in unc
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
        if num_missing_zeros < 0:
            msg = (
                f"Invalid value/uncertainty pair for parentheses uncertainty: "
                f'"{input_str}". If a decimal symbol appears in the value but not in '
                f"the uncertainty then the number of the digits in the uncertainty may "
                f"not exceed the number of digits in the fractional part of the value."
            )
            raise ValueError(msg)
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


def parse_val_unc_from_input(
    value: Number,
    uncertainty: Number | None,
    decimal_separator: modes.DecimalSeparators | None = None,
) -> tuple[Decimal, Decimal | None]:
    """
    Parse a user supplied value/uncertainty into a standard form of one or two Decimals.

    Values and uncertainties are passed in by users as either ints, floats, strings,
    or Decimals. In all cases these types are converted to Decimal via

      Decimal(str(value))

    For ints, numerical strings, and Decimals these two conversions are trivial.
    When floats are cast to a string they are converted to the shortest string
    representation which will round trip.

    User may pass in int, float, string, or Decimal inputs for both value and,
    optionally, the uncertainty.

    However, users may also pass in strings with more complicated structure than those
    strings which can be natively converted to float or Decimal. For example

    >>> from sciform.parser import parse_val_unc_from_input
    >>> val, unc = parse_val_unc_from_input("123 +/- 4", None)
    >>> print(val)
    123
    >>> print(unc)
    4

    If the value string contains information about both the value and the uncertainty
    then the uncertainty doesn't accept any value other than None, otherwise a
    ValueError is raised.

    parse_value_uncertainty accepts all the output formats the :mod:`sciform` can
    produce.

    >>> val, unc = parse_val_unc_from_input("123(4) k", None)
    >>> print(val)
    123000
    >>> print(unc)
    4000
    """
    if isinstance(value, (float, int)):
        value = Decimal(str(value))
    if isinstance(value, str):
        parsed_value, parsed_uncertainty = parse_val_unc_from_str(
            value,
            decimal_separator=decimal_separator,
        )
        if parsed_uncertainty is not None:
            if uncertainty is not None:
                msg = (
                    f'Value input string "{value}" already includes an '
                    f"uncertainty, ({parsed_uncertainty}). It is not "
                    f"possible to also pass in an uncertainty "
                    f"({uncertainty}) directly."
                )
                raise ValueError(msg) from None
            uncertainty = parsed_uncertainty
        value = parsed_value

    if uncertainty is not None:
        if isinstance(uncertainty, (float, int)):
            uncertainty = Decimal(str(uncertainty))
        if isinstance(uncertainty, str):
            uncertainty, _ = parse_val_unc_from_str(
                uncertainty,
                decimal_separator=decimal_separator,
            )

    value = value.normalize()
    if uncertainty is not None:
        uncertainty = uncertainty.normalize()

    return value, uncertainty
