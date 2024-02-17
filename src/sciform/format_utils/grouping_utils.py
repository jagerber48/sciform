"""Add separators to numerical strings."""

import re


def add_group_chars(
    num_str: str,
    group_char: str,
    *,
    reverse: bool = False,
    group_size: int = 3,
) -> str:
    """Add grouping characters to a string of numbers."""
    if reverse:
        num_str = num_str[::-1]

    result_str = ""
    group_counter = 0
    for digit in num_str:
        result_str += digit
        group_counter += 1
        if group_counter == group_size:
            result_str += group_char
            group_counter = 0
    result_str = result_str.rstrip(group_char)

    if reverse:
        result_str = result_str[::-1]

    return result_str


def add_separators(
    num_str: str,
    upper_separator: str = "",
    decimal_separator: str = ".",
    lower_separator: str = "",
    group_size: int = 3,
) -> str:
    """Add separators to a string of numbers."""
    match = re.match(
        r"(?P<sign>[+-])?(?P<spaces>\s*)(?P<integer>\d+)(\.(?P<fraction>\d+))?",
        num_str,
    )
    sign = match.group("sign") or ""
    spaces = match.group("spaces")
    integer_str = match.group("integer")
    fraction_str = match.group("fraction")

    integer_seps_str = add_group_chars(
        integer_str,
        upper_separator,
        reverse=True,
        group_size=group_size,
    )
    result_str = f"{sign}{spaces}{integer_seps_str}"

    if fraction_str is not None:
        fraction_seps_str = add_group_chars(
            fraction_str,
            lower_separator,
            reverse=False,
            group_size=group_size,
        )
        result_str += f"{decimal_separator}{fraction_seps_str}"

    return result_str
