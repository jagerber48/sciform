.. _fsml:

Format Specification Mini Language
##################################

.. module:: sciform
   :noindex:

Specification
=============

:mod:`sciform` :ref:`formatting options <formatting_options>` can be
applied to the formatting of :class:`SciNum` or :class:`SciNumUnc`
instances by using string formatting analogous to the built-in
formatting for :class:`float` and :class:`Decimal` objects.
The :mod:`sciform` format specification mini language is given by::

    format_spec        ::=  [fill "="][sign]["#"][fill_top_digit][upper_separator][decimal_separator][lower_separator][round_mode precision][exp_mode]["x" exp]["p"]["()"]

    fill               ::=  "0" | " "
    sign               ::=  "+" | "-" | " "
    fill_top_digit     ::=  digit+
    upper_separator    ::=  "n" | "." | "," | "s" | "_"
    decimal_separator  ::=  "." | ","
    lower_separator    ::=  "n" | "s" | "_"
    round_mode         ::=  "!" | "."
    precision          ::=  [+-]?digit+
    exp_mode           ::=  "f" | "F" | "%" | "e" | "E" | "r" | "R" | "b" | "B" |
    exp                ::=  [+-]?digit+

Details about the terms in the FSML are described below.

.. list-table:: :mod:`sciform` Format Specification Mini Language Terms
   :widths: 15 30
   :header-rows: 1

   * - Format Specification
     - Description
   * - | fill
       | (``'0='``, ``' ='``)
     - Fill characters will be padded between the most signifant digit
       and the sign symbol until the digit corresponding to the
       ``fill_top_digit`` is filled.
   * - | sign
       | (``'-'``, ``'+'``, ``' '``)
     - ``'-'`` will include a sign symbol only for negative numbers.
       ``'+'`` will include a sign symbol for all numbers. ``' '`` will
       include a minus symbol for negative numbers and a space for
       positive numbers. Zero is always considered to be positive.
   * - | alternate mode
       | (``'#'``)
     - Alternate mode is enabled (disabled by default) if the ``'#'``
       flag is included in the format specification. In engineering
       mode (``r`` or ``R``), the alternate mode engages
       :ref:`engineering_shifted` mode. In binary mode (``b`` or ``B``),
       the alternate mode engages :ref:`binary_iec` mode.
   * - | fill_top_digit
       | (``\d+``)
     - Any non-negative integer, default (0). Indicates the decimal or
       binary place to which the formatted string should be padded. e.g.
       ``f'{SciNum(123):0=4}'`` will give ``'00123'``, i.e. padding to
       the ``10^4`` place.
   * - | upper_separator
       | (``'n'``, ``','``, ``'.'``, ``'s'``, ``'_'``)
     - Indicates the character to use as the separator between groups of
       three digits above the decimal point. For base 10 formats this is
       the "thousands" separator. ``'n'`` is no separator, ``'s'`` is a
       single-whitespace separator and ``','``, ``'.'``, and ``'_'`` are
       comma, period, and underscore separators. Note
       that NIST discourages the use of ``','`` or ``'.'`` as thousands
       seperators because they can be confused with the decimal
       separators depending on the locality. See
       `NIST Guide to the SI 10.5.3 <https://www.nist.gov/pml/special-publication-811/nist-guide-si-chapter-10-more-printing-and-using-symbols-and-numbers#1053>`_.
   * - | decimal_separator
       | (``'.'``, ``','``)
     - Symbol to use as the decimal separator. Note that the decimal
       separator must be different than the upper separator.
   * - | lower_separator
       | (``'n'``, ``'s'``, ``'_'``)
     - Indicates the character to use as the separator between groups of
       three digits below the decimal point. ``'n'`` is no separator,
       ``'s'`` is a single-whitespace separator and ``'_'`` is an
       underscore separators.
   * - | round_mode
       | (``'!'``, ``'.'``)
     - Indicates whether the number will be rounded and displayed
       according to precision ``'.'`` (digits past the decimal point) or
       significant figures ``'!'``. E.g. ``f'{SciNum(123.456):.2f}'``
       gives ``'123.46'`` while ``f'{SciNum(123.456):!2f}'`` gives
       ``'120'``.
   * - | precision
       | (``[+-]?\d+``)
     - Integer indicating the precision or number of significant figures
       to which the number shall be rounded and displayed. Can be any
       integer for digits-past-the-decimal rounding mode. Must be
       greater than zero for significant figure mode. If no precision is
       supplied then the number will be displayed without any rounding.
   * - | exp_mode
       | (``'f'``, ``'F'``, ``'%'``, ``'e'``, ``'E'``, ``'r'``, ``'R'``,
         ``'b'``, ``'B'``)
     - Indicates which exponent mode should be used. In all cases the
       capitalization of the exponent symbol matches the capitalization
       of the exponent mode flag.

       * ``'f'`` and ``'F'`` indicate :ref:`fixed_point` mode in which
         no exponent is used to display the number.
       * ``'%'`` uses :ref:`fixed_point` exponent mode but also engages
         :ref:`percent_mode` which multiplies the number by 100 prior to
         formatting and appends a ``'%'`` character.
       * ``'e'`` and ``'E'`` indicate :ref:`scientific` exponent mode in
         which the exponent is chosen so that the mantissa satisfies
         ``1 <= m < 10``.
       * ``'r'`` and ``'R'`` indicate :ref:`engineering` exponent mode
         in which the exponent is chosen to be a multiple of 3 and so
         that the mantissa ``m`` satisfies ``1 <= m <= 1000``. If the
         alternate mode is enabled then :ref:`engineering_shifted`
         exponent mode is used in which the exponent is a multiple of 3
         but the mantissa satisfies ``0.1 <= m < 100``.
       * ``'b'`` and ``'B'`` indicate :ref:`binary` exponent mode in
         which the number is presented as a mantissa and exponent in
         base 2. The mantissa satisfies ``1 <= m < 2``. If alternate
         mode is enabled then :ref:`binary_iec` exponent mode is
         engaged so that the exponent is a multiple of 10 and the
         mantissa satisfies ``1 <= m < 1024 = 2^10``.
   * - | exp
       | (``x[+-]\d+``)
     - Positive or negative integer that can be used to force the
       exponent to take a particular value. This flag is ignored in
       fixed exponent mode. If an explicit exponent is used in
       engineering mode or alternate binary mode which is incompatible
       with those modes (e.g. an exponent that is not a multiple of 3
       for engineering notation), the exponent will be rounded down to
       the nearest compatible value.
   * - | prefix mode
       | (``'p'``)
     -  Flag (default off) indicating whether exponent strings should be
        replaced with SI or IEC prefix characters. E.g.
        ``'123e+03' -> '123 k'`` or ``'857.2B+20' -> '857.2 Mi'``.
   * - | bracket uncertainty
       | (``'()'``)
     - Flag (default off) indicating if :ref:`bracket_uncertainty` mode
       should be used so that uncertainty appears in parentheses rather
       than after a plus/minus symbol. E.g.
       ``'1.0 +/- 0.5' -> '1.0(5)'``.



Incompatibilities With Built-in Format Specification Mini Language
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
  These precision types are not supported by :mod:`sciform`.
  These precision types offer automated formatting decisions which are
  not compatible with the explicit formatting options preferred by
  :mod:`sciform`. The built-in automation features include

  * Automated selection of fixed-point or scientific notation. For
    :mod:`sciform`, the user must explicity indicate the exponent mode.
  * Truncation of trailing zeros without the ``#`` option. For
    :mod:`sciform`, trailing zeros are never truncated if they fall
    within the user-selected precision or significant figures.
  * Inclusion of a hanging decimal point, e.g. ``123.``.
    :mod:`sciform` never includes a hanging decimal point.

* For :class:`float` instances, Python formatting uses a default precion
  of 6 for ``f``, ``F``, ``%``, ``e``, and ``E`` modes if no explicit
  precision is supplied.
  :mod:`sciform`, instead, always converts inputs to :class:`Decimal`
  objects and displays exactly as many digits as necessary to represent
  the :class:`Decimal`.
  Specifically, for :class:`float` input, the :class:`float` is first
  cast to a string, which returns the shortest round-trippable decimal
  representation of the :class:`float`.
  E.g. ``f'{float(0.3):f}'`` yields ``0.300000`` while
  ``f'{SciNum(0.3):f}`` yields ``0.3``.

* The built-in FSML supports left-aligned, right-aligned,
  center-aligned, and sign-aware string padding by any character. In the
  built-in FSML, the width field indicates the minimum length to which
  the resulting string (including all punctuation such as ``+``, ``-``,
  ``.``, ``e``, etc.) should be filled to. ``sciform`` takes the
  perspective that these padding features are mostly tasks for string
  formatters, not number formatters. For :mod:`sciform`, the user
  specifies the digits place to which the number should be padded.
  The fill character may only be ``' '`` or ``'0'`` and must always be
  followed by the sign aware `=` flag. There is no ``0`` flag, as in the
  built-in FSML, that may be placed before the width field to indicate
  sign-aware zero padding. E.g. ``f'{float(12): =4}`` yields ``'  12'``
  while ``f{SciNum(12): =4}`` yeilds ``'   12'``, fill characters are
  padded up to the ``10^4`` digits place.

* The built-in FSML supports displaying negative zero, but also supports
  an option to coerce negative zero to be positive by including a
  ``'z'`` flag. :mod:`sciform` always coerces negative zero to be
  positive and therefore has no corresponding option to coerce negative
  zero to be positive.
