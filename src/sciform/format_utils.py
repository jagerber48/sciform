"""Various formatting utilities."""

from __future__ import annotations

import re
from decimal import Decimal
from math import floor, log2
from typing import Literal, Union, cast

from sciform.modes import (
    AutoDigits,
    AutoExpVal,
    DecimalSeparatorEnums,
    ExpFormatEnum,
    ExpModeEnum,
    RoundModeEnum,
    SeparatorEnum,
    SignModeEnum,
)
from sciform.prefix import (
    iec_val_to_prefix_dict,
    pp_val_to_prefix_dict,
    si_val_to_prefix_dict,
)

Number = Union[Decimal, float, int, str]


def get_top_digit(num: Decimal) -> int:
    """Get the decimal place of a decimal's most significant digit."""
    if not num.is_finite() or num == 0:
        return 0
    _, digits, exp = num.as_tuple()
    return len(digits) + exp - 1


def get_top_digit_binary(num: Decimal) -> int:
    """Get the decimal place of a decimal's most significant digit."""
    if not num.is_finite() or num == 0:
        return 0
    return floor(log2(abs(num)))


def get_bottom_digit(num: Decimal) -> int:
    """Get the decimal place of a decimal's least significant digit."""
    if not num.is_finite():
        return 0
    _, _, exp = num.as_tuple()
    return exp


def get_fixed_exp(
    input_exp: int | type(AutoExpVal),
) -> Literal[0]:
    """Get the exponent for fixed or percent format modes."""
    if input_exp is not AutoExpVal and input_exp != 0:
        msg = "Cannot set non-zero exponent in fixed point or percent exponent mode."
        raise ValueError(msg)
    return 0


def get_scientific_exp(
    num: Decimal,
    input_exp: int | type(AutoExpVal),
) -> int:
    """Get the exponent for scientific formatting mode."""
    return get_top_digit(num) if input_exp is AutoExpVal else input_exp


def get_engineering_exp(
    num: Decimal,
    input_exp: int | type(AutoExpVal),
    *,
    shifted: bool = False,
) -> int:
    """Get the exponent for engineering formatting modes."""
    if input_exp is AutoExpVal:
        exp_val = get_top_digit(num)
        exp_val = exp_val // 3 * 3 if not shifted else (exp_val + 1) // 3 * 3
    else:
        if input_exp % 3 != 0:
            msg = (
                f"Exponent must be an integer multiple of 3 in engineering modes, not "
                f"{input_exp}."
            )
            raise ValueError(msg)
        exp_val = input_exp
    return exp_val


def get_binary_exp(
    num: Decimal,
    input_exp: int | type(AutoExpVal),
    *,
    iec: bool = False,
) -> int:
    """Get the exponent for binary formatting modes."""
    if input_exp is AutoExpVal:
        exp_val = get_top_digit_binary(num)
        if iec:
            exp_val = (exp_val // 10) * 10
    else:
        if iec and input_exp % 10 != 0:
            msg = (
                f"Exponent must be an integer multiple of 10 in binary IEC mode, not "
                f"{input_exp}."
            )
            raise ValueError(msg)
        exp_val = input_exp
    return exp_val


def get_mantissa_exp_base(
    num: Decimal,
    exp_mode: ExpModeEnum,
    input_exp: int | type(AutoExpVal),
) -> tuple[Decimal, int, int]:
    """Get mantissa, exponent, and base for formatting a decimal number."""
    if exp_mode is ExpModeEnum.BINARY or exp_mode is ExpModeEnum.BINARY_IEC:
        base = 2
    else:
        base = 10

    if num == 0 or not num.is_finite():
        mantissa = Decimal(num)
        exp = 0 if input_exp is AutoExpVal else input_exp
    else:
        if exp_mode is ExpModeEnum.FIXEDPOINT or exp_mode is ExpModeEnum.PERCENT:
            exp = get_fixed_exp(input_exp)
        elif exp_mode is ExpModeEnum.SCIENTIFIC:
            exp = get_scientific_exp(num, input_exp)
        elif exp_mode is ExpModeEnum.ENGINEERING:
            exp = get_engineering_exp(num, input_exp)
        elif exp_mode is ExpModeEnum.ENGINEERING_SHIFTED:
            exp = get_engineering_exp(num, input_exp, shifted=True)
        elif exp_mode is ExpModeEnum.BINARY:
            exp = get_binary_exp(num, input_exp)
        elif exp_mode is ExpModeEnum.BINARY_IEC:
            exp = get_binary_exp(num, input_exp, iec=True)
        else:
            msg = f"Unhandled exponent mode {exp_mode}."
            raise ValueError(msg)
        mantissa = num * Decimal(base) ** Decimal(-exp)
    mantissa = mantissa.normalize()
    return mantissa, exp, base


def get_standard_exp_str(base: int, exp_val: int, *, capitalize: bool = False) -> str:
    """Get standard (eg. 'e+02') exponent string."""
    base_exp_symbol_dict = {10: "e", 2: "b"}
    exp_symbol = base_exp_symbol_dict[base]
    if capitalize:
        exp_symbol = exp_symbol.capitalize()
    return f"{exp_symbol}{exp_val:+03d}"


def get_superscript_exp_str(base: int, exp_val: int) -> str:
    """Get superscript (e.g. '×10⁺²') exponent string."""
    sup_trans = str.maketrans("+-0123456789", "⁺⁻⁰¹²³⁴⁵⁶⁷⁸⁹")
    exp_val_str = f"{exp_val}".translate(sup_trans)
    return f"×{base}{exp_val_str}"


def get_prefix_dict(
    exp_format: ExpFormatEnum,
    base: Literal[10, 2],
    extra_si_prefixes: dict[int, str],
    extra_iec_prefixes: dict[int, str],
    extra_parts_per_forms: dict[int, str],
) -> dict[int, str]:
    """Resolve dictionary of prefix translations."""
    if exp_format is ExpFormatEnum.PREFIX:
        if base == 10:
            prefix_dict = si_val_to_prefix_dict.copy()
            prefix_dict.update(extra_si_prefixes)
        elif base == 2:
            prefix_dict = iec_val_to_prefix_dict.copy()
            prefix_dict.update(extra_iec_prefixes)
        else:
            msg = f"Unhandled base {base}"
            raise ValueError(msg)
    elif exp_format is ExpFormatEnum.PARTS_PER:
        prefix_dict = pp_val_to_prefix_dict.copy()
        prefix_dict.update(extra_parts_per_forms)
    else:
        msg = f"Unhandled ExpFormat, {exp_format}."
        raise ValueError(msg)

    return prefix_dict


def get_exp_str(  # noqa: PLR0913
    *,
    exp_val: int,
    exp_mode: ExpModeEnum,
    exp_format: ExpFormatEnum,
    extra_si_prefixes: dict[int, str],
    extra_iec_prefixes: dict[int, str],
    extra_parts_per_forms: dict[int, str],
    capitalize: bool,
    superscript: bool,
) -> str:
    """Get formatting exponent string."""
    if exp_mode is ExpModeEnum.FIXEDPOINT:
        return ""
    if exp_mode is ExpModeEnum.PERCENT:
        return "%"

    if exp_mode is ExpModeEnum.BINARY or exp_mode is ExpModeEnum.BINARY_IEC:
        base = 2
    else:
        base = 10
    base = cast(Literal[10, 2], base)

    if exp_format is ExpFormatEnum.PREFIX or exp_format is ExpFormatEnum.PARTS_PER:
        text_exp_dict = get_prefix_dict(
            exp_format,
            base,
            extra_si_prefixes,
            extra_iec_prefixes,
            extra_parts_per_forms,
        )
        if exp_val in text_exp_dict and text_exp_dict[exp_val] is not None:
            exp_str = f" {text_exp_dict[exp_val]}"
            exp_str = exp_str.rstrip(" ")
            return exp_str

    if superscript:
        return get_superscript_exp_str(base, exp_val)

    return get_standard_exp_str(base, exp_val, capitalize=capitalize)


def get_sign_str(num: Decimal, sign_mode: SignModeEnum) -> str:
    """Get the format sign string."""
    if num < 0:
        # Always return "-" for negative numbers.
        sign_str = "-"
    elif num > 0:
        # Return "+", " ", or "" for positive numbers.
        if sign_mode is SignModeEnum.ALWAYS:
            sign_str = "+"
        elif sign_mode is SignModeEnum.SPACE:
            sign_str = " "
        elif sign_mode is SignModeEnum.NEGATIVE:
            sign_str = ""
        else:
            msg = f"Invalid sign mode {sign_mode}."
            raise ValueError(msg)
    elif sign_mode is SignModeEnum.ALWAYS or sign_mode is SignModeEnum.SPACE:
        # For anything else (typically 0, possibly nan) return " " in "+" and " " modes
        sign_str = " "
    else:
        # Otherwise return the empty string.
        sign_str = ""

    return sign_str


def get_pdg_round_digit(num: Decimal) -> int:
    """
    Determine the PDG rounding digit place to which to round.

    Calculate the appropriate digit place to round to according to the
    particle data group 3-5-4 rounding rules.

    See
    https://pdg.lbl.gov/2010/reviews/rpp2010-rev-rpp-intro.pdf
    Section 5.2
    """
    top_digit = get_top_digit(num)

    # Bring num to be between 100 and 1000.
    num_top_three_digs = num * Decimal(10) ** (Decimal(2) - Decimal(top_digit))
    num_top_three_digs.quantize(1)
    new_top_digit = get_top_digit(num_top_three_digs)
    num_top_three_digs = num_top_three_digs * 10 ** (2 - new_top_digit)
    if 100 <= num_top_three_digs <= 354:
        round_digit = top_digit - 1
    elif 355 <= num_top_three_digs <= 949:
        round_digit = top_digit
    elif 950 <= num_top_three_digs <= 999:
        """
        Here we set the round digit equal to the top digit. But since
        the top three digits are >= 950 this means they will be rounded
        up to 1000. So with round digit set to the top digit this will
        correspond to displaying two digits of uncertainty: "10".
        e.g. 123.45632 +/- 0.987 would be rounded as 123.5 +/- 1.0.
        """
        round_digit = top_digit
    else:  # pragma: no cover
        raise ValueError

    return round_digit


def get_round_digit(
    num: Decimal,
    round_mode: RoundModeEnum,
    ndigits: int | type(AutoDigits),
    *,
    pdg_sig_figs: bool = False,
) -> int:
    """Get the digit place to which to round."""
    if round_mode is RoundModeEnum.SIG_FIG:
        if pdg_sig_figs:
            round_digit = get_pdg_round_digit(num)
        elif ndigits is AutoDigits:
            round_digit = get_bottom_digit(num)
        else:
            round_digit = get_top_digit(num) - (ndigits - 1)
    elif round_mode is RoundModeEnum.DEC_PLACE:
        round_digit = get_bottom_digit(num) if ndigits is AutoDigits else -ndigits
    else:
        msg = f"Unhandled round mode: {round_mode}."
        raise ValueError(msg)
    return round_digit


def get_pad_str(left_pad_char: str, top_digit: int, top_padded_digit: int) -> str:
    """Get the string padding from top_digit place to top_padded_digit place."""
    if top_padded_digit > top_digit:
        pad_len = top_padded_digit - max(top_digit, 0)
        pad_str = left_pad_char * pad_len
    else:
        pad_str = ""
    return pad_str


def format_num_by_top_bottom_dig(
    num: Decimal,
    target_top_digit: int,
    target_bottom_digit: int,
    sign_mode: SignModeEnum,
    left_pad_char: str,
) -> str:
    """Format a number according to specified top and bottom digit places."""
    print_prec = max(0, -target_bottom_digit)
    abs_mantissa_str = f"{abs(num):.{print_prec}f}"

    sign_str = get_sign_str(num, sign_mode)

    num_top_digit = get_top_digit(num)
    pad_str = get_pad_str(left_pad_char, num_top_digit, target_top_digit)
    return f"{sign_str}{pad_str}{abs_mantissa_str}"


def round_val_unc(
    val: Decimal,
    unc: Decimal,
    ndigits: int | type[AutoDigits],
    *,
    use_pdg_sig_figs: bool = False,
) -> tuple[Decimal, Decimal, int]:
    """Simultaneously round the value and uncertainty."""
    if unc.is_finite() and unc != 0:
        round_digit = get_round_digit(
            unc,
            RoundModeEnum.SIG_FIG,
            ndigits,
            pdg_sig_figs=use_pdg_sig_figs,
        )
        unc_rounded = round(unc, -round_digit)
    else:
        round_digit = get_round_digit(
            val,
            RoundModeEnum.SIG_FIG,
            ndigits,
            pdg_sig_figs=False,
        )
        unc_rounded = unc
    if val.is_finite():
        val_rounded = round(val, -round_digit)
    else:
        val_rounded = val
    return val_rounded, unc_rounded, round_digit


def get_val_unc_exp(
    val: Decimal,
    unc: Decimal,
    exp_mode: ExpModeEnum,
    input_exp: int,
) -> int:
    """Get exponent for value/uncertainty formatting."""
    if val.is_finite() and unc.is_finite():
        if abs(val) >= unc:
            exp_driver_val = val
        else:
            exp_driver_val = unc
    elif val.is_finite():
        exp_driver_val = val
    else:
        exp_driver_val = unc

    _, exp_val, _ = get_mantissa_exp_base(
        exp_driver_val,
        exp_mode=exp_mode,
        input_exp=input_exp,
    )

    return exp_val


def get_val_unc_top_digit(
    val_mantissa: Decimal,
    unc_mantissa: Decimal,
    input_top_digit: int | AutoDigits,
    *,
    left_pad_matching: bool,
) -> int | AutoDigits:
    """Get top digit place for value/uncertainty formatting."""
    if left_pad_matching:
        val_top_digit = get_top_digit(val_mantissa)
        unc_top_digit = get_top_digit(unc_mantissa)
        new_top_digit = max(
            input_top_digit,
            val_top_digit,
            unc_top_digit,
        )
    else:
        new_top_digit = input_top_digit
    return new_top_digit


def get_val_unc_mantissa_strs(
    val_mantissa_exp_str: str,
    unc_mantissa_exp_str: str,
) -> tuple[str, str]:
    """Break val/unc mantissa/exp strings into mantissa strings and an exp string."""
    # Optional parentheses needed to handle (nan)e+00 case
    mantissa_exp_pattern = re.compile(
        r"^\(?(?P<mantissa_str>.*?)\)?(?P<exp_str>[eEbB].*?)?$",
    )
    val_match = mantissa_exp_pattern.match(val_mantissa_exp_str)
    val_mantissa_str = val_match.group("mantissa_str")

    unc_match = mantissa_exp_pattern.match(unc_mantissa_exp_str)
    unc_mantissa_str = unc_match.group("mantissa_str")

    return val_mantissa_str, unc_mantissa_str


def construct_val_unc_str(  # noqa: PLR0913
    val_mantissa_str: str,
    unc_mantissa_str: str,
    val_mantissa: Decimal,
    unc_mantissa: Decimal,
    decimal_separator: DecimalSeparatorEnums,
    *,
    paren_uncertainty: bool,
    pm_whitespace: bool,
    paren_uncertainty_trim: bool,
) -> str:
    """Construct the value/uncertainty part of the formatted string."""
    if not paren_uncertainty:
        pm_symb = "±"
        if pm_whitespace:
            pm_symb = f" {pm_symb} "
        val_unc_str = f"{val_mantissa_str}{pm_symb}{unc_mantissa_str}"
    else:
        if (
            paren_uncertainty_trim
            and unc_mantissa.is_finite()
            and val_mantissa.is_finite()
            and 0 < unc_mantissa < abs(val_mantissa)
        ):
            """
            Don't strip the unc_mantissa_str if val_mantissa is non-finite.
            Don't strip the unc_mantissa_str if unc_mantissa == 0 (because then the
              empty string would remain).
            Don't left strip the unc_mantissa_str if unc_mantissa >= val_mantissa
            """
            for separator in SeparatorEnum:
                if separator != decimal_separator:
                    unc_mantissa_str = unc_mantissa_str.replace(separator, "")
            unc_mantissa_str = unc_mantissa_str.lstrip("0" + decimal_separator)
        val_unc_str = f"{val_mantissa_str}({unc_mantissa_str})"
    return val_unc_str


def construct_val_unc_exp_str(  # noqa: PLR0913
    *,
    val_unc_str: str,
    exp_val: int,
    exp_mode: ExpModeEnum,
    exp_format: ExpFormatEnum,
    extra_si_prefixes: dict[int, str | None],
    extra_iec_prefixes: dict[int, str | None],
    extra_parts_per_forms: dict[int, str | None],
    capitalize: bool,
    superscript: bool,
    paren_uncertainty: bool,
) -> str:
    """Combine the val_unc_str into the final val_unc_exp_str."""
    exp_str = get_exp_str(
        exp_val=exp_val,
        exp_mode=exp_mode,
        exp_format=exp_format,
        capitalize=capitalize,
        superscript=superscript,
        extra_si_prefixes=extra_si_prefixes,
        extra_iec_prefixes=extra_iec_prefixes,
        extra_parts_per_forms=extra_parts_per_forms,
    )

    if exp_str == "":
        val_unc_exp_str = val_unc_str
    elif paren_uncertainty:
        # No parentheses for paren_uncertainty, e.g. 123(4)e+03
        val_unc_exp_str = f"{val_unc_str}{exp_str}"
    else:
        # Wrapping parentheses for ± uncertainty, e.g. (123 ± 4)e+03
        val_unc_exp_str = f"({val_unc_str}){exp_str}"

    return val_unc_exp_str
