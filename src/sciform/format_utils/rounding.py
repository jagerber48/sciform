"""Rounding utilities."""

from __future__ import annotations

from decimal import Decimal

from sciform.format_utils.numbers import (
    get_bottom_dec_place,
    get_top_dec_place,
)
from sciform.options.option_types import (
    AutoDigits,
    RoundModeEnum,
)


def get_pdg_round_digit(num: Decimal) -> int:
    """
    Determine the PDG rounding decimal place to which to round.

    Calculate the appropriate decimal place to which to round  according
    to the particle data group 3-5-4 rounding rules.

    See
    https://pdg.lbl.gov/2010/reviews/rpp2010-rev-rpp-intro.pdf
    Section 5.2
    """
    top_dec_place = get_top_dec_place(num)

    # Bring num to be between 100 and 1000.
    num_top_three_digs = num * Decimal(10) ** (Decimal(2) - Decimal(top_dec_place))
    num_top_three_digs.quantize(1)
    new_top_dec_place = get_top_dec_place(num_top_three_digs)
    num_top_three_digs = num_top_three_digs * 10 ** (2 - new_top_dec_place)
    if 100 <= num_top_three_digs <= 354:
        round_digit = top_dec_place - 1
    elif 355 <= num_top_three_digs <= 949:
        round_digit = top_dec_place
    elif 950 <= num_top_three_digs <= 999:
        """
        Here we set the round digit equal to the top digit. But since
        the top three digits are >= 950 this means they will be rounded
        up to 1000. So with round digit set to the top digit this will
        correspond to displaying two digits of uncertainty: "10".
        e.g. 123.45632 +/- 0.987 would be rounded as 123.5 +/- 1.0.
        """
        round_digit = top_dec_place
    else:  # pragma: no cover
        raise ValueError

    return round_digit


def get_round_dec_place(
    num: Decimal,
    round_mode: RoundModeEnum,
    ndigits: int | type(AutoDigits),
    *,
    pdg_sig_figs: bool = False,
) -> int:
    """Get the decimal place to which to round."""
    # TODO: Handle nan and inf
    if round_mode is RoundModeEnum.SIG_FIG:
        if pdg_sig_figs:
            round_digit = get_pdg_round_digit(num)
        elif ndigits is AutoDigits:
            round_digit = get_bottom_dec_place(num)
        else:
            round_digit = get_top_dec_place(num) - (ndigits - 1)
    elif round_mode is RoundModeEnum.DEC_PLACE:
        round_digit = get_bottom_dec_place(num) if ndigits is AutoDigits else -ndigits
    else:
        msg = f"Unhandled round mode: {round_mode}."
        raise ValueError(msg)
    return round_digit


def round_val_unc(
    val: Decimal,
    unc: Decimal,
    ndigits: int | type[AutoDigits],
    *,
    use_pdg_sig_figs: bool = False,
) -> tuple[Decimal, Decimal, int]:
    """Simultaneously round the value and uncertainty."""
    if unc.is_finite() and unc != 0:
        round_digit = get_round_dec_place(
            unc,
            RoundModeEnum.SIG_FIG,
            ndigits,
            pdg_sig_figs=use_pdg_sig_figs,
        )
        unc_rounded = round(unc, -round_digit)
    else:
        round_digit = get_round_dec_place(
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
