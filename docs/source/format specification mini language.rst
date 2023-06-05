.. _fsml:

Format Specification Mini Language
==================================

:class:`FormatOptions` can be applied to the formatting of an
:class:`sfloat` object
The ``sciform`` format specification mini language is given by::

    format_spec        ::=  [fill "="][sign]["#"][fill_top_digit][upper_separator][decimal_separator][lower_separator][round_mode precision][format_mode]["x" exp][prefix_mode]

    fill               ::=  "0" | " "
    sign               ::=  "+" | "-" | " "
    fill_top_digit     ::=  digit+
    upper_separator    ::=  "n" | "." | "," | "s" | "_"
    decimal_separator  ::=  "." | ","
    lower_separator    ::=  "n" | "s" | "_"
    round_mode         ::=  "!" | "."
    prec               ::=  -?digit+
    format_mode        ::=  "f" | "F" | "%" | "e" | "E" | "r" | "R" | "b" | "B" |
    exp                ::=  [+-]digit+
    prefix_mode        ::=  p


Details about the terms in the FSML are described below.

.. list-table:: ``sciform`` Format Specification Mini Language Terms
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
       notation (``r`` or ``R``), the alternate mode coerces the
       mantissa `m` to be ``0.1 <= m < 100`` rather than
       ``1 <= m < 1000``. In binary mode (``b`` or ``B``), the alternate
       flag coerces the mantissa to be between ``1 <= m < 1024`` rather
       than ``1 <= m < 2``.
   * - | fill_top_digit
       | (``\d+``)
     - Any non-negative integer, default (0). Indicates the decimal or
       binary place to which the formatted string should be padded. e.g.
       ``f'{sfloat(123):0=4}'`` will give ``'00123'``, i.e. padding to
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
     - Indicates whether the float will be rounded and displayed
       according to precision (digits past the decimal point) or
       significant figure. ``'.'`` indicates precision mode and ``'!'``
       indicates significant figure mode. E.g.
       ``f'{sfloat(123.456):.2f}'`` gives ``'123.46'`` while
       ``f'{sfloat(123.456):!2f}'`` gives ``'120'``.
   * - | prec
       | (``[+-]?\d+``)
     - Integer indicating the precision or number of significant figures
       to which the float shall be rounded and displayed. Can be
       negative for precision formatting mode. Must be greater than zero
       for significant figure mode. If no precision is supplied then an
       algorithm will be used to attempt to infer the least significant
       digit for the float and the precision will be chosen to match
       this least significant digit. This algorithm may have surprising
       behavior for floats with a large number (e.g. 15) of significant
       digits or due to the underlying binary nature of floats, e.g.
       ``0.1+0.2 = 0.30000000000000004``.
   * - | format_mode
       | (``'f'``, ``'F'``, ``'%'``, ``'e'``, ``'E'``, ``'r'``, ``'R'``,
         ``'b'``, ``'B'``)
     - Indicates which formatting mode should be used. In all cases the
       capitalization of the exponent symbol matches the capitalization
       of the format mode flag.

       * ``'f'`` and ``'F'`` indicate fixed point mode in which no
         exponent is used to display the number.
       * ``'%'`` mode is like fixed mode but the number is first
         multiplied by 100 and presented followed by a ``'%'``
         character.
       * ``'e'`` and ``'E'`` indicate scientific notation in which the
         exponent is chosen so that the mantissa satisfies
         ``1 <= m < 10``.
       * ``'r'`` and ``'R'`` indicate engineering notation in which the
         exponent is chosen so that the mantissa satisfies
         ``1 <= m <= 1000``. If the alternate mode is enabled then the
         mantissa satisfies ``0.1 <= m < 100``. In both cases the
         exponent is always an integer multiple of 3.
       * ``'b'`` and ``'B'`` indicate binary mode in which the number is
         presented as a mantissa and exponent in base 2. The mantissa
         satisfies ``1 <= m < 2``. If alternate mode is enabled the
         mantissa satisfies ``1 <= m < 1024 = 2^10``. In this case the
         exponent is always an integer multiple of 10.
   * - | exp
       | (``x[+-]\d+``)
     - Positive or negative integer that can be used to force the
       exponent to take a particular value. This flag is ignored in
       fixed format mode. If an explicit exponent is used in engineering
       mode or alternate binary mode which is incompatible with those
       modes (e.g. an exponent that is not a multiple of 3 for
       engineering notation), the exponent will be rounded down to the
       nearest compatible value.
   * - | prefix_mode
       | (``'p'``)
     -  Flag (default off) indicating whether exponent strings should be
        replaced with SI or IEC prefix characters. E.g.
        ``'123e+03' -> '123 k'`` or ``'857.2B+20' -> '857.2 Mi'``.
