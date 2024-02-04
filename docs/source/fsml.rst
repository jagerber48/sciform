.. _fsml:

Format Specification Mini-Language
##################################

.. module:: sciform
   :noindex:

Specification
=============

Instead of explicitly constructing :class:`Formatter` instances, users
can construct :class:`SciNum` instances and format them using string
formatting with format specification strings from the :mod:`sciform`
format specification mini-language (FSML).
This is analogous to how python :class:`int`, :class:`float`, and
:class:`Decimal` instances can be formatted using the built-in
`format specification mini-language <https://docs.python.org/3/library/string.html#format-specification-mini-language>`_.
The :mod:`sciform` format specification mini-language is given by::

    format_spec        ::=  [left_pad_char "="][sign]["#"][left_pad_dec_place][round_mode ndigits][exp_mode]["x" exp_val]["p"]["()"]

    left_pad_char      ::=  "0" | " "
    sign               ::=  "+" | "-" | " "
    left_pad_dec_place ::=  digit+
    round_mode         ::=  "!" | "."
    ndigits            ::=  [+-]?digit+
    exp_mode           ::=  "f" | "F" | "%" | "e" | "E" | "r" | "R" | "b" | "B" |
    exp_val            ::=  [+-]?digit+

Below is are two simple FSML usage examples.
See :ref:`FSML examples <fsml_examples>` for more complicated FSML
usage examples.


>>> from sciform import SciNum
>>> print(f"{SciNum(123456):!4f}")
123500

In this example ``!4`` indicates the number should be formatted with
four significant figures and ``f`` indicates the number should be
formatted in fixed point mode.

>>> print(f"{SciNum(12345, 789):!1r}")
(12.3 ± 0.8)e+03

In this example ``!1`` indicates the number will be formatted so that
the uncertainty has one significant digit (and the value will be rounded
and displayed accordingly).
The ``r`` indicates that the number will be formatted using engineering
notation.

See below for details about how the terms in the FSML correspond to
formatting options.
Further details about the options can be found at
:ref:`formatting_options`.

.. list-table:: :mod:`sciform` Format Specification Mini-Language Terms
   :widths: 15 30
   :header-rows: 1

   * - Format Specification
     - Description
   * - | left_pad_char
       | (``'0='``, ``' ='``)
     - Configure ``left_pad_char`` to be ``'0'`` or ``' '``. See
       :ref:`left_padding`.
   * - | sign
       | (``'-'``, ``'+'``, ``' '``)
     - Configure ``sign_mode`` to be ``'-'``, ``'+'``, or ``' '``. See
       :ref:`sign_mode`.
   * - | alternate mode
       | (``'#'``)
     - The alternate mode flag indicates to use
       :ref:`engineering_shifted` mode when the exponent mode flag is
       ``'r'`` or ``'R'`` or to use :ref:`binary_iec` mode when the
       exponent mode flag is ``'b'`` or ``'B'``.
   * - | left_pad_dec_place
       | (``\d+``)
     - Sets ``left_pad_dec_place`` to any non-negative integer.
       See :ref:`left_padding`.
   * - | round_mode
       | (``'!'``, ``'.'``)
     - Sets ``round_mode`` to ``'sig_fig'`` or ``'dec_place'``.
       See :ref:`rounding`.
   * - | ndigits
       | (``[+-]?\d+``)
     - Sets ``ndigits`` to an integer to control rounding.
       See :ref:`rounding`.
   * - | exp_mode
       | (``'f'``, ``'F'``, ``'%'``, ``'e'``, ``'E'``, ``'r'``, ``'R'``,
         ``'b'``, ``'B'``)
     - Sets ``exponent_mode``.
       If this flag is capitalized then ``capitalize`` is set to
       ``True``.
       See :ref:`exp_mode`.

       * ``'f'`` and ``'F'`` set :ref:`fixed_point` exponent mode.
       * ``'%'`` sets :ref:`percent_mode` exponent mode.
       * ``'e'`` and ``'E'`` set :ref:`scientific` exponent mode.
       * ``'r'`` and ``'R'`` set :ref:`engineering` or
         :ref:`engineering_shifted` exponent modes depending on if the
         alternate mode flag is used..
       * ``'b'`` and ``'B'`` set :ref:`binary` or :ref:`binary_iec`
         exponent modes depending on if the alternate mode flag is used.
   * - | exp_val
       | (``x[+-]\d+``)
     - Sets ``exp_val`` to an integer.
       See :ref:`fixed_exp`.
   * - | prefix mode
       | (``'p'``)
     - Sets ``exp_format`` to :class:`'prefix'`.
       See :ref:`exp_str_replacement`.
   * - | parentheses uncertainty
       | (``'()'``)
     - Sets ``paren_uncertainty=True``.
       See :ref:`paren_uncertainty`.


Incompatibilities With Built-in Format Specification Mini-Language
==================================================================

The :mod:`sciform` FSML extends the functionality of the
`built-in FSML <https://docs.python.org/3/library/string.html#format-specification-mini-language>`_.
However, :mod:`sciform` FSML is not entirely backwards compatible with
the built-in FSML.
Certain allowed built-in format specifications are illegal in the
:mod:`sciform` FSML and certain allowed built-in format specifications
give different results when used with :class:`SciNum` rather than
:class:`float` or :class:`Decimal` objects.
These incompatibilities were intentionally introduced to simplify the
:class:`sciform` FSML by cutting out features less likely to be required
for scientific formatting.

* The built-in FSML accepts ``g``, ``G`` and ``n`` precision types
  (exponent modes).
  These precision types are not supported by :mod:`sciform`.
  These precision types offer automated formatting decisions which are
  not compatible with the explicit formatting options preferred by
  :mod:`sciform`. The built-in automation features include

  * Automated selection of fixed-point or scientific notation.
    For :mod:`sciform`, the exponent mode is either explicitly indicated
    by the user or resolved from the global options.
  * Truncation of trailing zeros without the ``#`` option.
    For :mod:`sciform`, trailing zeros are never truncated if they fall
    within the user-selected decimal place or significant figures
    rounding.
  * Inclusion of a hanging decimal point, e.g. ``123.``.
    :mod:`sciform` never includes a hanging decimal point.

* For :class:`float` instances, Python formatting uses a default
  precision of 6 for ``f``, ``F``, ``%``, ``e``, and ``E`` modes if no
  explicit precision (``ndigits``) is supplied.
  :mod:`sciform`, instead, converts :class:`float` instances into
  :class:`str` and then :class:`Decimal` so that they are displayed with
  as many digits as necessary to "round-trip" when no ``ndigits`` is
  supplied.
  E.g. ``f'{float(0.3):f}'`` yields ``0.300000`` while
  ``f'{SciNum(0.3):f}`` yields ``0.3``.

* The built-in FSML supports left-aligned, right-aligned,
  center-aligned, and sign-aware string padding by any character.
  In the built-in FSML, the width field indicates the minimum length to
  which the resulting string (including all punctuation such as ``+``,
  ``-``, ``.``, ``e``, etc.) should be filled.
  :mod:`sciform` takes the stance that these padding features are tasks
  better suited for string, as opposed to number, formatters.
  For :mod:`sciform`, the user specifies the digits place to which the
  number should be padded.
  The pad character may only be ``' '`` or ``'0'`` and must always be
  followed by the sign aware `=` flag.
  There is no ``0`` flag, as in the built-in FSML, that may be placed
  before the width field to indicate sign-aware zero padding.
  E.g. ``f'{float(12): =4}`` yields ``'  12'`` while
  ``f{SciNum(12): =4}`` yields ``'   12'``, fill characters are padded
  up to the 10\ :sup:`4` digits place.

* The built-in FSML supports configuring a thousands separator (what
  :mod:`sciform` calls the ``upper_separator``).
  :mod:`sciform` has more numerous options for grouping separators such
  that it would be cumbersome to include all grouping separator options
  in the :mod:`sciform` FSML and awkward to only include a subset.
  Therefore no grouping separators can be configured using the
  :mod:`sciform` FSML, and these instead need to be configured as
  global options.

* The built-in FSML supports displaying negative zero, but also supports
  an option to coerce negative zero to be positive by including a
  ``'z'`` flag.
  :mod:`sciform` always coerces negative zero to be positive and
  therefore has no corresponding option to coerce negative zero to be
  positive.
