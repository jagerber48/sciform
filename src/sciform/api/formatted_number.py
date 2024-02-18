"""FormattedNumber class represents sciform output data."""

from __future__ import annotations

from typing import TYPE_CHECKING

from sciform.formatting.output_conversion import convert_sciform_format

if TYPE_CHECKING:  # pragma: no cover
    from typing import Self

    from sciform.format_utils import Number
    from sciform.options.populated_options import PopulatedOptions


class FormattedNumber(str):
    """
    Representation of a formatted value of value/uncertainty pair.

    The :class:`FormattedNumber` class is returned by ``sciform``
    formatting methods. In most cases it behaves like a regular python
    string, but it provides functionality for post-converting the string
    to various other formats such as latex or html. This allows the
    formatted number to be displayed in a range of contexts other than
    e.g. text terminals.

    The :class:`FormattedNumber` class should never be instantiated
    directly.
    """

    __slots__ = {
        "value": "The value that was formatted to generate the "
        ":class:`FormattedNumber`.",
        "uncertainty": "The uncertainty that was formatted to generate the "
        ":class:`FormattedNumber`.",
        "populated_options": "Record of the :class:`PopulatedOptions` used to "
        "generate the :class:`FormattedNumber`.",
    }

    def __new__(
        cls: type[Self],
        formatted_str: str,
        value: Number,
        uncertainty: Number | None,
        populated_options: PopulatedOptions,
    ) -> Self:
        """Get a new string."""
        obj = super().__new__(cls, formatted_str)
        obj.value = value
        obj.uncertainty = uncertainty
        obj.populated_options = populated_options
        return obj

    def as_str(self: FormattedNumber) -> str:
        """Return the string representation of the formatted number."""
        return self.__str__()

    def as_ascii(self: FormattedNumber) -> str:
        """Return the ascii representation of the formatted number."""
        return convert_sciform_format(self, "ascii")

    def as_html(self: FormattedNumber) -> str:
        """Return the html representation of the formatted number."""
        return convert_sciform_format(self, "html")

    def as_latex(self: FormattedNumber, *, strip_math_mode: bool = False) -> str:
        """Return the latex representation of the formatted number."""
        latex_repr = convert_sciform_format(self, "latex")
        if strip_math_mode:
            latex_repr = latex_repr.strip("$")
        return latex_repr

    def _repr_html_(self: FormattedNumber) -> str:
        """Hook for HTML display."""  # noqa: D401
        return self.as_html()

    def _repr_latex_(self: FormattedNumber) -> str:
        """Hook for LaTeX display."""  # noqa: D401
        return self.as_latex()
