"""Formatting utilities to target fixed overall string length."""

from dataclasses import asdict
from typing import Sequence

from sciform import modes
from sciform.format_utils import Number
from sciform.formatter import Formatter


def format_to_target_length(
    value: Number,
    uncertainty: Number = None,
    /,
    *,
    target_length: int,
    allowed_exp_modes: Sequence[modes.ExpMode] = ("fixed_point",),
    base_formatter: Formatter = None,
) -> str:
    """
    Format a number while adjusting sig_figs so that the result is a target length.

    :param value: (positional only) Value to be formatted.
    :type value: ``Decimal | float | int | str``
    :param uncertainty: (positional only) Optional uncertainty to be
      formatted.
    :type uncertainty: ``Decimal | float | int | str | None``
    :param target_length: (keyword only) Integer number of characters to
      target for output string. The output string will have a number of
      characters at least as large as target_length. However, in some
      cases, the output string must have a length exceeding
      target_length. E.g. 123456789 cannot be displayed with less than 9
      characters in fixed_point mode.
    :type target_length: ``int``
    :param allowed_exp_modes: (keyword only) Sequence of ``sciform``
      exponent modes. ``format_to_target_length()`` will attempt
      formatting using each of these modes and will select the mode
      which provides the best result. The best result is the one with
      the shortest length >= target_length. If there is a tie for
      shortest length then results with more significant figures are
      preferred. If there is still a tie then ``exp_modes`` which appear
      earlier in the ``allowed_exp_modes`` sequence are preferred. By
      default, only the ``"fixed_point"`` is allowed.
    :type allowed_exp_modes: ``Sequence[Literal["fixed_point", "percent",
          "scientific", "engineering", "engineering_shifted", "binary",
          "binary_iec"]]``
    :param base_formatter: (keyword only) Formatter object to use to
      format the input number(s). The ``round_mode`` will be overridden
      to ``"sig_fig"``, the ``exp_mode`` will be overridden to the values
      in ``allowed_exp_modes`` and the ``num_sig_figs`` will be
      overridden. If no base_formatter is supplied than a new
      ``Formatter()`` instance is created which uses the global
      ``sciform`` settings.
    :type base_formatter: ``Formatter``
    """
    """
    result_array is a list of tuples where each tuple is of the form
    (length, -num_sig_figs, exp_mode_number, result_str)
    At the end of the algorithm this list will be sorted and the
    result_str of the first entry will be returned. Only entries with
    length >= target_length will be included in this array. The sorting
    will prefer the shortest string with the most sig figs. If there is
    a tie then exponent modes with a lower exp_mode_number (the
    corresponding index for that exp_mode in allowed_exp_modes sequence)
    will be preferred.
    """
    result_array = []

    if base_formatter is None:
        base_formatter = Formatter()

    input_kwargs = asdict(base_formatter._user_options)  # noqa: SLF001

    for idx, exp_mode in enumerate(allowed_exp_modes):
        num_sig_figs = 1
        while True:
            # TODO: For large target_length the formatting throws a Decimal module error
            #   which arises due to rounding beyond the specified Decimal precision.
            #   This could be worked around by performing formatting in a local Decimal
            #   context with a precision which expands as necessary when large numbers
            #   of sig figs are requested.
            kwargs = input_kwargs.copy()
            kwargs["round_mode"] = "sig_fig"
            kwargs["exp_mode"] = exp_mode
            kwargs["ndigits"] = num_sig_figs

            formatter = Formatter(**kwargs)
            result = formatter(value, uncertainty)
            length = len(result)

            if length >= target_length:
                """
                Use -num_sig_figs instead of num_sig_figs as a hack so that sort
                prefers more (rather than less) sig figs!
                """
                result_tuple = (length, -num_sig_figs, idx, result)
                result_array.append(result_tuple)
                break

            num_sig_figs += 1

    sorted_results = sorted(result_array)
    best_result_tuple = sorted_results[0]
    best_result_str = best_result_tuple[3]

    return best_result_str
