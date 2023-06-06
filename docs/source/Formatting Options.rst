.. _formatting_options:

==================
Formatting Options
==================

:mod:`sciform` provides a variety of options for converting floats into
formatted strings.
These options including control over the rounding strategy, scientific
notation formatting, separation characters and more.

Format Mode
===========

:mod:`sciform` supports a variety of format modes.
To display numbers across a wide range of magnitudes, scientific
formatting presents numbers in the form::

   num = mantissa * base**exp

Where exp is an integer and ``base`` is typically 10 or 2.
The different formatting modes control how ``mantissa``, ``base`` and
``exp`` are chosen for a given input float ``num``.

Fixed Point
--------------

Fixed point notation is standard notation in which a float is displayed
directly as a decimal number with no extra exponent.

>>> from sciform import Formatter, FormatMode, RoundMode
>>> sform = Formatter(format_mode=FormatMode.FIXEDPOINT)
>>> print(sform(123.456))
123.456

Scientific Notation
-------------------

Scientific notation is used to display base-10 decimal numbers.
In scientific notation, the exponent is uniquely chosen so that the
mantissa ``m`` satisfies ``1 <= m < 10``.

>>> sform = Formatter(format_mode=FormatMode.SCIENTIFIC)
>>> print(sform(123.456))
1.23456e+02

Engineering Notation
--------------------

Engineering notation is similar to scientific notation except the
exponent is chosen to be an integer multiple of 3.
In standard engineering notation, the mantissa ``m`` satisfies
``1 <= m < 1000``.
Engineering notation is compatible with the SI prefixes which are
defined for any integer mulitple of 3 exponent, e.g.::

   369,000,00 Hz = 369e+06 Hz = 369 MHz

Here it may be more convenient to display the number with an exponent of
6 for rapid identification of the "Mega" order of magnitude, as opposed
to an exponent of 8 which would be chosen for standard scientific
notation.

>>> sform = Formatter(format_mode=FormatMode.ENGINEERING)
>>> print(sform(123.456))
123.456e+00

Shifted Engineering Notation
----------------------------

Shifted engineering notation is the same as engineering notation except
the exponent is chosen so that the mantissa ``m`` satisfies
``0.1 <= m < 100``.

>>> sform = Formatter(format_mode=FormatMode.ENGINEERING_SHIFTED)
>>> print(sform(123.456))
0.123456e+03

Binary
------

Binary formatting can be chosen to display a number in scientific
notation in base-2.

>>> sform = Formatter(format_mode=FormatMode.BINARY)
>>> print(sform(256))
1b+08

Here ``b`` exponent symbol indicates base-2 instead of base-10.
For binary formatting, the mantissa ``m`` satisfies ``1 <= m < 2``.

Binary IEC
----------

Binary IEC mode is similar to engineering notation, except in base-2.
In this mode number are expressed in base-2 exponent notation, but the
exponent is constrained to be a multiple of 10, consistent with the
IEC binary prefixes.
The mantissa ``m`` satisfies ``1 <= m < 1024``.

Binary formatting can be chosen to display a number in scientific
notation in base-2.

>>> sform = Formatter(format_mode=FormatMode.BINARY_IEC)
>>> print(sform(2048))
2b+10

Here ``b`` exponent symbol indicates base-2 instead of base-10.

Fixed Exponent
==============

The user can coerce the exponent for the formatting to a fixed value.
The requested exponent is ignored in fixed point mode.
If a fixed exponent is requested for engineering, shifted engineering,
or binary IEC mode, then the requested exponent is rounded down to the
nearest multiple of 3 or 10.

>>> sform = Formatter(format_mode=FormatMode.SCIENTIFIC,
...                   exp=3)
>>> print(sform(123.456))
0.123456e+03

Prefix Mode
===========

Prefix mode enables the replacement of certain base-10 and binary
exponents by alphabetic scientific SI or IEC prefixes outlined in
:ref:`Supported Prefixes <prefixes>`.
Furthermore, it is possible to customize :class:`Formatter`
objects or the global configuration settings to map additional prefix
translations, in addition to those provided by default.

.. todo::
   * prefix mode coerces scientific notation into engineering notation
   * prefix mode coerces binary notation into binary iec notation
   * handles values larger and smaller than largest and smallest
     supported translations

>>> sform = Formatter(format_mode=FormatMode.ENGINEERING,
...                   use_prefix=True)
>>> print(sform(4242.13))
4.24213 k

>>> sform = Formatter(format_mode=FormatMode.BINARY_IEC,
...                   round_mode=RoundMode.SIG_FIG,
...                   precision=4,
...                   use_prefix=True)
>>> print(sform(1300))
1.270 Ki

.. _rounding:

Rounding
========

:mod:`sciform` provides two rounding strategies: rounding based on
significant figures, and rounding based on digits past the decimal
point or "precision".
In both cases, the rounding applies to the mantissa determined after
identifying the appropriate exponent for display based on the selected
format mode.
In some cases, the rounding results in a modification to the chosen
exponent.
This is taken into account before the final presentation.

Significant Figures
-------------------

For significant figure rounding, first the digits place for the
most-significant digit is identified.
e.g. for ``12345.678`` the most-significant digit appears in the
ten-thousands, or 10\ :sup:`4`, place.
To express this number to 4-significant digits means we should round it
to the tens, or 10\ :sup:`1`, place resulting in ``12350``.

Note that 1000 rounded to 2 significant figures is, of course, still
1000.
This demonstrates that we can't determine how many significant figures
a number was rounded to just by looking at the resulting string.

>>> from sciform import RoundMode
>>> sform = Formatter(format_mode=FormatMode.ENGINEERING,
...                   round_mode=RoundMode.SIG_FIG,
...                   precision=4)
>>> print(sform(12345.678))
12.35e+03

Here ``precision`` input is used to indicate how many significant
figures should be included.
for significant figure rounding, ``precision`` must be an integer
greater than or equal 1.

Precision
---------

Precision simply indicates the number of digits to be displayed past the
decimal point.
So, e.g., a precision of 2 indicates rounding to the hundredths, or
10\ :sup:`-2`, place.
Most of the built-in string formatting mini-language is based on
precision presentation.

>>> from sciform import RoundMode
>>> sform = Formatter(format_mode=FormatMode.ENGINEERING,
...                   round_mode=RoundMode.PREC,
...                   precision=4)
>>> print(sform(12345.678))
12.3457e+03

For precision rounding, ``precision`` can be any integer.

>>> from sciform import RoundMode
>>> sform = Formatter(format_mode=FormatMode.FIXEDPOINT,
...                   round_mode=RoundMode.PREC,
...                   precision=-2)
>>> print(sform(12345.678))
12300

Separators
==========

:mod:`sciform` provides support for some customization for separator
characters within formatting strings.
Different locales use different conventions for the symbol separating
the integral and fractional part of a float number, called the decimal
symbol.
:mod:`sciform` supports using a period ``'.'`` or comma ``','`` as the
decimal symbol.

Additionally, :mod:`sciform` also supports including separation characters
between groups of three digits both above the decimal symbol and below
the decimal symbols.
No separator, ``','``, ``'.'``, ``' '``, ``'_'`` can all be used as
"upper" separator characters and no separator, ``' '``, and ``'_'`` can
all be used as "lower" separator characters.
Note that the upper separator character must be different than the
decimal separator.

>>> from sciform import GroupingSeparator
>>> sform = Formatter(upper_separator=GroupingSeparator.COMMA)
>>> print(sform(12345678.987))
12,345,678.987

>>> from sciform import GroupingSeparator
>>> sform = Formatter(upper_separator=GroupingSeparator.SPACE,
...                   decimal_separator=GroupingSeparator.COMMA,
...                   lower_separator=GroupingSeparator.UNDERSCORE)
>>> print(sform(1234567.7654321))
1 234 567,765_432_1

Sign Mode
=========

:mod:`sciform` provides control over the symbol used to indicate whether a
float is positive or negative.
In all cases a ``'-'`` sign is used for negative numbers.
By default, positive numbers are formatted with no sign symbol.
However, :mod:`sciform` includes a mode where positive numbers are always
presented with a ``'+'`` symbol.
:mod:`sciform` also provides a mode where positive numbers include an extra
whitespace in place of a sign symbol.
This mode may be useful to match string lengths when positive and
negatives numbers are being presented together, but without explicitly
including a ``'+'`` symbol.
Note that ``0`` is always considered positive.

>>> from sciform import SignMode
>>> sform = Formatter(sign_mode=SignMode.NEGATIVE)
>>> print(sform(42))
42
>>> sform = Formatter(sign_mode=SignMode.ALWAYS)
>>> print(sform(42))
+42
>>> sform = Formatter(sign_mode=SignMode.SPACE)
>>> print(sform(42))
 42

Exponent Character Capitalization
=================================

The capitalization of the exponent character can be controlled

>>> sform = Formatter(format_mode=FormatMode.SCIENTIFIC,
...                   capital_exp_char=True)
>>> print(sform(42))
4.2E+01
>>> sform = Formatter(format_mode=FormatMode.BINARY,
...                   capital_exp_char=True)
>>> print(sform(1024))
1B+10

Left Filling
============

The :ref:`rounding` options described above can be used to control how
many digits to the left of either the most-significant digit or the
decimal point are displayed.
It is also possible, using "fill" options, to add digits to the left of
the most-significant digit.
The ``fill_mode`` can be used to select either whitespaces ``' '`` or
zeros ``'0'`` as fill characters.
The ``top_dig_place`` option is used to indicate to which digit fill
characters should be added.
E.g. ``top_dig_place=4`` indicates fill characters should be added up
to the 10\ :sup:`4` (ten-thousands) place.

>>> from sciform import FillMode
>>> sform = Formatter(fill_mode=FillMode.ZERO,
...                   top_dig_place=4)
>>> print(sform(42))
00042

Extra Prefixes
==============

In addition to the :ref:`default prefixes <prefixes>`, the user can include some
additional standard prefixes as well as user-supplied prefixes.
Standard additional SI prefixes are::

   {-2: 'c', -1: 'd', +1: 'da', +2: 'h'}

Here the integer keys indicate the exponent and the string values
indicate the corresponding prefix.
These additional prefixes can be included using the
``add_small_si_prefixes`` options.
Furthermore, just the ``c`` prefix can be included using the
``add_c_prefix`` options.

>>> sform = Formatter(format_mode=FormatMode.SCIENTIFIC,
...                   use_prefix=True,
...                   add_c_prefix=True)
>>> print(sform(0.025))
2.5 c
>>> sform = Formatter(format_mode=FormatMode.SCIENTIFIC,
...                   use_prefix=True,
...                   add_small_si_prefixes=True)
>>> print(sform(25))
2.5 da
