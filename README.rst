=======
sciform
=======

Overview
--------

``sciform`` is used to convert python float objects into strings
according to a variety of user-selected scientific formatting options
including fixed-pointa and decimal and binary scientific and engineering
notations.
Where possible, formatting follows documented standards such as those
published by `BIPM <https://www.bipm.org/en/>`_ or
`IEC <https://iec.ch/homepage>`_.
``sciform`` provides certain options, such as engineering notation and
well-controlled significant figure rounding, which are not provided by
the python built-in
`format specification mini-language (FSML) <https://docs.python.org/3/library/string.html#format-specification-mini-language>`_.

Installation
------------

Install with pip::

   pip install sciform

Usage
=====

``sciform`` provides two primary methods for formatting floats into
scientific formatting strings.
The first is via the ``Formatter`` object and the second is using string
formatting and the custom FSML with the ``sfloat`` object.

>>> from sciform import Formatter, RoundMode, GroupingSeparator, FormatMode
>>> sform = Formatter(round_mode=RoundMode.PREC,
...                   precision=6,
...                   upper_separator=GroupingSeparator.SPACE,
...                   lower_separator=GroupingSeparator.SPACE)
>>> print(sform(3.14159265359))
3.141 593
>>> sform = Formatter(round_mode=RoundMode.SIG_FIG,
...                   precision=4,
...                   format_mode=FormatMode.ENGINEERING)
>>> print(sform(123456.78))
123.5e+03

>>> from sciform import sfloat
>>> num = sfloat(123456)
>>> print(f'{num:_!2f}')
120_000

OLD
===

Floats are formatted into strings of the form::

    mantissa [exp_str]

where ``exp_str`` can be of the form ``exp_symbol exp`` where
``exp_symbol`` is ``e``, ``E``, ``b``, or ``B``, and ``exp`` is an
integer like ``+03``.
``exp_str`` can also be a single SI or IEC "prefix" character like ``k``
``M`` or ``Mi``.

Example formatted floats are:

* ``'103.0400'``
* ``'1.03e+02'``
* ``'1.03E+03'``
* ``'1.03 k'``
* ``'1023b+10'``
* ``'1.00b+20'``
* ``'3.4 Mi'``

In this document, the terminology "precision" of a string representing a
float is number of digits that appear past the decimal point, e.g.
``1.030400`` has a precision of 6.
The number of "significant figures" or "sig figs" for a string
representing a float is the number of digits past the left-most non-zero
digit.
So `1.030400` has 7 sig figs. The string `1030` has a precision of 0 and
may have 3 or 4 sig figs.
When presenting a number to a certain number of sig figs, we first round
the number to the digit place corresponding to that number of sig figs
(based on the digit place of the most significant digit) then truncate
the number to that digit.
If that digit is the tens place or larger, then trailing zeros are added
until the ones place.

=======
Credits
=======
``sciform`` was heavily motivated by the float formatting provided in
the `prefixed <https://github.com/Rockhopper-Technologies/prefixed>`_
and the value +/- uncertainty formatting in the
`uncertainties <https://github.com/lebigot/uncertainties>`_ package.

===========================================
Built-in Format Specification Mini Language
===========================================

In Python, ``float`` objects can already be converted to string
representations using built in formatting.
For example, ``f'{0.00438:#.4g}'`` yeilds the string ``'0.004380'``.
Here the float ``0.00438`` has been formatted according to the format
specification string ``'#.4g'``.
The rules for constructing format specification strings are specified in
`the format specification mini lanuage (FSML)
<https://docs.python.org/3/library/string.html#format-specification-mini-language>`_
documentation.

The built-in FSML has a few short-comings making it non-ideal for all
scientific formatting tasks:

* The built-in FSML lacks certain features around rounding and
  presenting floats based on significant figures (as opposed to
  precision) which makes it challenging to apply certain formatting
  strategies.

  * It is possible to specify sig figs for formatting using the ``e``
    and ``g`` built in formatting modes, but it is impossible to format
    numbers according to a specific number of sig figs while also
    presenting the numbers in fixed point format.
    Specifically, it is impossible to coerce the string formatting to
    perform rounding "above the decimal point".
    There is no way to format ``123`` to yield ``'120'``. You can use
    ``f'{123:#.4g}'`` to get ``'123.0'`` (4 sig figs), but if you do
    ``f'{123:#.2g}'`` you get ``'1.2e+02'``.
    This is because built-in float formatting does not allow formatting
    to perform rounding/truncation *above* the decimal point.
  * The ``#`` option is necessary to format to a specified number of sig
    figs in ``g`` mode (which must be used if you want any possibility of
    fixed-point sig fig formatting) but, this option means mantissa with
    no fractional part will include a trailing decimal point, e.g.
    ``f'{123:#.3g}'`` gives ``123.`` which may be undesirable.

* While built-in formatting does provide a means to fill a string to a
  certain overall width (including all non-numeric symbols), it does not
  provide a means to fill a string up to a certain digit place, e.g. add
  zeros up to the hundreds place which may sometimes be desirable.
* In the sciences it is very common to display numbers in *engineering*
  notation in which the exponent is chosen so that it is an integer
  multiple of 3 and the mantissa is between ``0.1 <= m < 1000``.
  Built-in formatting has no functionality for this feature.
  See `NIST Guide to the SI 7.9
  <https://www.nist.gov/pml/special-publication-811/nist-guide-si-chapter-7-rules-and-style-conventions-expressing-values>`_
  for more details.
* The built-in formatting has limited functionality for customizing the
  separation and decimal characters used to display numbers.

While these shortcomings are all minor, and can be worked around with
simple helper functions, it would be most convenient if scientific float
formatting could be easily accessed in-line during string formatting
operations.
This motivated the development of the ``sciform`` FSML.

==============================================
``sciform`` Format Specification Mini Language
==============================================

``sciform`` introduces a new FSML based on the built-in FSML but which
avoids the shortcomings described above and includes a few additional
features.
These features include:

* Flexible significant figure formatting
* Engineering notation
* Binary (base-2) exponent formatting
* Flexible separator selection
* Explicit exponent value specification

The ``sciform`` FSML is based on the built-in FSML, but it is not fully
backwards compatible with it.
For the sake of simplicity, some format
specifications that are valid for the built-in FSML are invalid for the
``sciform`` FSML.
Also, a valid built-in format specification may give different results
when used as part of the built-in FSML compared to when used as part of
the ``sciform`` FSML.
These incompatibilities are captured in a section below.

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


where the terms are described in the table below.

The ``sciform`` FSML is accessed via the `sfloat` object.
Regular built-in floats are cast to ``sfloat`` objects which can be
formatted using the ``sciform`` FSML.::

    from sciform import sfloat

    num = sfloat(123456)
    print(f'{num:_!2f}')
    # 120_000

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
         satisfies ``1 <= m < 2`. If alternate mode is enabled the
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

===========
Prefix Mode
===========

Prefix mode offers a simple translation between exponent strings and
one or two letter prefixes.
For scientific and engineering formats the prefixes are matched to
integer multiple of 3 exponent according to the
`SI prefixes <https://www.nist.gov/pml/owm/metric-si-prefixes>`_.
For binary formats, the prefixes are matched to integer multiples of 10
according to the `IEC prefixes <https://physics.nist.gov/cuu/Units/binary.html>`_.

Supported translations:

.. list-table:: SI Prefixes
   :widths: 30, 15, 10
   :header-rows: 1

   * - Exponent Value
     - Prefix Name
     - Prefix
   * - 10\ :sup:`+30`
     - Quetta
     - Q
   * - 10\ :sup:`+27`
     - Ronna
     - R
   * - 10\ :sup:`+24`
     - Yotta
     - Y
   * - 10\ :sup:`+21`
     - Zetta
     - Z
   * - 10\ :sup:`+18`
     - Exa
     - E
   * - 10\ :sup:`+15`
     - Peta
     - P
   * - 10\ :sup:`+12`
     - Tera
     - T
   * - 10\ :sup:`+9`
     - Giga
     - G
   * - 10\ :sup:`+6`
     - Mega
     - M
   * - 10\ :sup:`+3`
     - kilo
     - k
   * - 10\ :sup:`-3`
     - milli
     - m
   * - 10\ :sup:`-6`
     - micro
     - μ
   * - 10\ :sup:`-9`
     - nano
     - n
   * - 10\ :sup:`-12`
     - pico
     - p
   * - 10\ :sup:`-15`
     - femto
     - f
   * - 10\ :sup:`-18`
     - atto
     - a
   * - 10\ :sup:`-21`
     - zepto
     - z
   * - 10\ :sup:`-24`
     - yocto
     - y
   * - 10\ :sup:`-27`
     - ronto
     - r
   * - 10\ :sup:`-30`
     - quecto
     - q

.. list-table:: IEC Prefixes
   :widths: 30, 15, 10
   :header-rows: 1

   * - Exponent Value
     - Prefix Name
     - Prefix
   * - 10\ :sup:`+80`
     - yobi
     - Yi
   * - 10\ :sup:`+70`
     - zebi
     - Zi
   * - 10\ :sup:`+60`
     - exi
     - Ei
   * - 10\ :sup:`+50`
     - pebi
     - Pi
   * - 10\ :sup:`+40`
     - tebi
     - Ti
   * - 10\ :sup:`+30`
     - gibi
     - Gi
   * - 10\ :sup:`+20`
     - mebi
     - Mi
   * - 10\ :sup:`+10`
     - kibi
     - Ki

Examples of prefix mode are:

- ``f'{sfloat(12.4e+06):rp}'`` gives ``'12 M'``
- ``f'{sfloat(1024*2**10):bp}'`` gives ``'1 Mi'``

===================================
Configuration options (forthcoming)
===================================

It is possible to modify the global default configuration for
``sciform`` to avoid repetition of verbose (and
difficult-to-parse-for-humans) format specification strings.

The global defaults can be accessed using ``get_global_defaults`` and
permanently modified using ``set_global_defaults``.
Any format calls will use the stored defaults for any settings which
have not been explicitly set by the user. The global defaults can also
be temporarily modified using the ``GlobalDefaultsContext`` context
manager. Within the scope of the context manager the new global
configuration will be used, but when the context manager scope exits,
the original configuration will be restored.

Modifying the global configuration allows the user to modify the mapping
between exponents and SI or IEC prefixes.
In particular, it is possible to include the ``c`` SI prefix (e.g.
1 cm = 10\ :sup:`-2` m) using the ``include_c`` kwarg as well as to
include all of the ``c``, ``d``, ``da``, and ``h`` SI prefixes corresponding to
10\ :sup:`-2`, 10\ :sup:`-1`, 10\ :sup:`+1`, and 10\ :sup:`+2`
respectively using the ``include_small_si_prefixes`` kwarg.

The user can format floats directly by constructing a ``Formatter``,
passing in the desired formatting settings, then calling its
``format()`` method on the float of interest.

In the future, configuration may be added for persistant class- and
instance-level default configuration options. However, it needs to be
decided how configuration will be shared between the different levels.
For example, if an ``sfloat`` object is instantiated which does not
specify behavior for the ``prefix`` field, but then the ``prefix`` field at
the global level is modified, should this ``sfloat`` instance adopt the
new global config?
Also, how should config conflicts be managed?
One idea is to resolve conflicts by deferring to the parent config.

============================================
Value + uncertainty formatting (forthcoming)
============================================

One of (if not the) most important use cases for scientific formatting
is formatting a value together with its specified uncertainty, e.g.
``84.3 +/- 0.2``. The ability to format pairs of floats as
value/uncertainty pairs will be supported by the forthcoming ``ufloat``
class.

Value/uncertainty formatting is not yet fully implemented or tested, but
it will support

* Selection of the exponent based on the value
* Selection of the least significant digit based on a user-requested
  number of sig figs to display for the uncertainty.
* Optional padding so that the value and uncertainty have the same
  width
* Short form "parentheses" uncertainty display, e.g.
  ``84.3 +/- 2= 84.3(2)``.

==================================================================
Incompatibilities With Built-in Format Specification Mini Language
==================================================================

The ``sciform`` FSML extends the functionality of the built-in FSML.
However, ``sciform`` FSML is not entirely backwards compatible with the
built-in FSML.
Certain allowed built-in format specifications are
illegal in ``sciform`` FSML and certain allowed built-in format
specifications give different results when used with ``sfloat`` rather
than ``float``.
These incompatibilities were intentionally introduced to simplify the
``sciform`` FSML by cutting out features less likely to be required for
scientific formatting.

* The built-in FSML accepts ``g``, ``G`` and ``n`` precision types
  These precision types are not supported by scientific formatting.
  These precision types offer automated formatting decisions which are
  not compatible with the explicit formatting options preferred by
  ``sciform``. These features include

  * Automated selection of fixed-point or scientific notation. For
    ``sciform``, the user must explicity indicate
    fixed point, scientific, or engineering notation by selecting one
    of the ``f``, ``F``, ``e``, ``E``, ``r`` or ``R`` flags.
  * Truncation of trailing zeros without the ``#`` option. For
    ``sciform``, trailing zeros are never truncated if they fall
    within the user-selected precision or sig figs.
  * Inclusion of a hanging decimal point, e.g. ``123.``. ``sciform``
    never includes a hanging decimal point.

* Python float formatting uses a pre-selected, hard-coded precion of 6
  for ``f``, ``F``, ``%``, ``e``, and ``E`` modes.
  When no precision or sig fig specification is provided, ``sciform``,
  instead, infers the precision or sig fig specification from the float
  by determining the least significant decimal digit required to
  represent it.
  Note that there may be surprising results for floats that require more
  decimals to represent than ``sys.float_info.dig`` such as ``0.1 * 3``.

  * ``f'{float(0.3):f}'`` yield ``0.300000`` while ``f'{sfloat(0.3):f}``
    yields ``0.3``.
* The built-in FSML supports left-aligned, right-aligned,
  center-aligned, and sign-aware string padding by any character.
  In the built-in FSML, the width field indicates the length to which
  the resulting string (including all punctuation such as ``+``, ``-``,
  ``.``, ``e``, etc.) should be filled to. ``sciform`` takes the
  perspective that these padding features are mostly tasks for string
  formatters, not number formatters. ``sciform`` only supports padding
  by a space ``' '`` or zero. For ``sciform``, the user specifies the
  digits place to which the number should be padded. For ``sciform``,
  the fill character may only be ``' '`` or ``'0'`` and must always be
  followed by the sign aware `=` flag. There is no ``0`` flag that may
  be placed before the width field to indicate sign-aware zero padding.

  * ``f'{float(12): =4}`` yields ``'  12'`` while ``f{sfloat(12): =4}``
    yeilds ``'   12'``. I.e. fill characters are padded up to the
    ``10^4`` digits place.

* The built-in FSML supports displaying negative zero, but also supports
  an option to coerce negative zero to be positive by including a
  ``'z'`` flag. ``sciform`` always coerces negative zero to be positive
  and therefore has no corresponding option to coerce negative zero to
  be positive.
