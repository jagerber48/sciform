.. _formatting_options:

##################
Formatting Options
##################

.. module:: sciform
   :noindex:

:mod:`sciform` provides a variety of options for converting floats into
formatted strings.
These options including control over the rounding strategy, scientific
notation formatting, separation characters and more.

Exponent Mode
=============

:mod:`sciform` supports a variety of exponent modes.
To display numbers across a wide range of magnitudes, scientific
formatting presents numbers in the form::

   num = mantissa * base**exp

Where exp is an integer and ``base`` is typically 10 or 2.
The different exponent modes control how ``mantissa``, ``base`` and
``exp`` are chosen for a given input float ``num``.

Fixed Point
-----------

Fixed point notation is standard notation in which a float is displayed
directly as a decimal number with no extra exponent.

>>> from sciform import Formatter, ExpMode, RoundMode
>>> sform = Formatter(exp_mode=ExpMode.FIXEDPOINT)
>>> print(sform(123.456))
123.456

Scientific Notation
-------------------

Scientific notation is used to display base-10 decimal numbers.
In scientific notation, the exponent is uniquely chosen so that the
mantissa ``m`` satisfies ``1 <= m < 10``.

>>> sform = Formatter(exp_mode=ExpMode.SCIENTIFIC)
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

>>> sform = Formatter(exp_mode=ExpMode.ENGINEERING)
>>> print(sform(123.456))
123.456e+00

Shifted Engineering Notation
----------------------------

Shifted engineering notation is the same as engineering notation except
the exponent is chosen so that the mantissa ``m`` satisfies
``0.1 <= m < 100``.

>>> sform = Formatter(exp_mode=ExpMode.ENGINEERING_SHIFTED)
>>> print(sform(123.456))
0.123456e+03

Binary
------

Binary formatting can be chosen to display a number in scientific
notation in base-2.

>>> sform = Formatter(exp_mode=ExpMode.BINARY)
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

>>> sform = Formatter(exp_mode=ExpMode.BINARY_IEC)
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

>>> sform = Formatter(exp_mode=ExpMode.SCIENTIFIC,
...                   exp=3)
>>> print(sform(123.456))
0.123456e+03

To explicitly force :mod:`sciform` to automatically select the exponent
then use the :class:`AutoExp` option by passing ``exp=AutoExp``.
This is the default value in the global configuration.

Exponent String Replacement
===========================

:mod:`sciform` provides a number of formatting options for replacing
decimal and binary exponent strings such as ``'e-03'`` or ``'b+10'``
with conventional strings such as ``'m'`` or ``'Ki'`` to succinctly
communicate the order of magnitude.
Decimal exponent strings can be replaced with either SI prefixes or
parts-per identifiers and binary exponent strings can be replaced with
IEC prefixes.
See :ref:`exp_replacements` for all default supported
replacements.
Furthermore, it is possible to customize :class:`Formatter`
objects or the global configuration settings to map additional
translations, in addition to those provided by default.

>>> sform = Formatter(exp_mode=ExpMode.ENGINEERING,
...                   prefix_exp=True)
>>> print(sform(4242.13))
4.24213 k
>>> sform = Formatter(exp_mode=ExpMode.BINARY_IEC,
...                   round_mode=RoundMode.SIG_FIG,
...                   precision=4,
...                   prefix_exp=True)
>>> print(sform(1300))
1.270 Ki
>>> sform = Formatter(exp_mode=ExpMode.ENGINEERING,
...                   parts_per_exp=True)
>>> print(sform(12.3e-6))
12.3 ppm

.. _extra_translations:

Extra Exponent Replacements
---------------------------

In addition to the default
:ref:`exponent replacements <exp_replacements>`, the user can include
some additional standard replacements.
Standard additional SI prefixes are::

   {-2: 'c', -1: 'd', +1: 'da', +2: 'h'}

Here the integer keys indicate the exponent and the string values
indicate the corresponding prefix.
These additional prefixes can be included using the
``add_small_si_prefixes`` options.
Furthermore, just the ``c`` prefix can be included using the
``add_c_prefix`` options.

>>> sform = Formatter(exp_mode=ExpMode.SCIENTIFIC,
...                   prefix_exp=True,
...                   add_c_prefix=True)
>>> print(sform(0.025))
2.5 c
>>> sform = Formatter(exp_mode=ExpMode.SCIENTIFIC,
...                   prefix_exp=True,
...                   add_small_si_prefixes=True)
>>> print(sform(25))
2.5 da

A non-standard parts-per-thousand form, ``ppth``, can be accessed with
the ``add_ppth_form`` option.

>>> sform = Formatter(exp_mode=ExpMode.ENGINEERING,
...                   parts_per_exp=True,
...                   add_ppth_form=True)
>>> print(sform(12.3e-3))
12.3 ppth

.. _rounding:

Rounding
========

:mod:`sciform` provides two rounding strategies: rounding based on
significant figures, and rounding based on digits past the decimal
point or "precision".
In both cases, the rounding applies to the mantissa determined after
identifying the appropriate exponent for display based on the selected
exponent mode.
In some cases, the rounding results in a modification to the chosen
exponent.
This is taken into account before the final presentation.

In both cases, if no explicit precision value or number of significant
figures is supplied then the number is displayed as if no rounding
occurs.
That is, all digits, down the least significant, are displayed.
To explicitly force this behavior use the :class:`AutoPrec` class by
passsing ``precision=AutoPrec``.
This is the default value in the global configuration.

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
>>> sform = Formatter(exp_mode=ExpMode.ENGINEERING,
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
>>> sform = Formatter(exp_mode=ExpMode.ENGINEERING,
...                   round_mode=RoundMode.PREC,
...                   precision=4)
>>> print(sform(12345.678))
12.3457e+03

For precision rounding, ``precision`` can be any integer.

>>> from sciform import RoundMode
>>> sform = Formatter(exp_mode=ExpMode.FIXEDPOINT,
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

Capitalization
==============

The capitalization of the exponent character can be controlled

>>> sform = Formatter(exp_mode=ExpMode.SCIENTIFIC,
...                   capitalize=True)
>>> print(sform(42))
4.2E+01
>>> sform = Formatter(exp_mode=ExpMode.BINARY,
...                   capitalize=True)
>>> print(sform(1024))
1B+10

The ``capitalize`` flag also controls the capitalization of ``nan`` and
``inf`` formatted floats:

>>> print(sform(float('nan')))
NAN
>>> print(sform(float('-inf')))
-INF

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

Percent Mode
============

The user can activate percent mode using the ``percent`` flag.
This flag is only valid for fixed point exponent mode.
In this case, the float is multipled by 100 and a % symbols is
appended to the end of the formatted string.

>>> sform = Formatter(round_mode=RoundMode.SIG_FIG,
...                   precision=3,
...                   percent=True)
>>> print(sform(0.12345))
12.3%
>>> print(sform(0.12345, 0.001))
(12.345 +/- 0.100)%

Superscript Exponent Format
===========================

The ``superscript_exp`` option can be chosen to present exponents in
standard superscript notation as opposed to e.g. ``e+02`` notation.

>>> sform = Formatter(exp_mode=ExpMode.SCIENTIFIC,
...                   superscript_exp=True)
>>> print(sform(789))
7.89×10²

Latex Format
============

The ``latex`` option can be chosen to convert strings into latex
parseable codes.

>>> sform = Formatter(exp_mode=ExpMode.SCIENTIFIC,
...                   exp=-1,
...                   upper_separator=GroupingSeparator.UNDERSCORE,
...                   latex=True)
>>> print(sform(12345))
123\_450\times 10^{-1}
>>> sform = Formatter(lower_separator=GroupingSeparator.UNDERSCORE,
...                   percent=True,
...                   latex=True)
>>> print(sform(0.12345678, 0.00000255))
\left(12.345\_678 \pm 0.000\_255\right)\%

The latex format makes the following changes:

* Convert standard exponent strings such as ``'e+02'`` into latex
  superscript strings like ``'\times 10^{+2}``
* Replace ``'('`` and ``')'`` by latex size-aware delimiters
  ``'\left('`` and ``'\right)'``.
* Replace ``'+/-'`` by ``'\pm'``
* Replace ``'_'`` by ``'\_'``
* Replace ``'%'`` by ``'\%'``

Note that use of ``latex`` renders the use of ``unicode_pm`` and
``superscript_exp`` meaningless.

Include Exponent on nan and inf
===============================

Python supports ``float('nan')``, ``float('inf')``, and
``float('-inf')``.
Typically these are formatted to ``'nan'``, ``'inf'``, and ``'-inf'`` or
``'NAN'``, ``'INF'``, and ``'-INF'`` respectively depending on
``capitalize``.
However, if ``nan_inf_exp=True`` (default ``False``), then, for
scientific, engineering, and binary exponent modes, these will instead
be formatted as, e.g. ``'(nan)e+00'``.

>>> sform = Formatter(exp_mode=ExpMode.SCIENTIFIC,
...                   nan_inf_exp=True,
...                   capitalize=True)
>>> print(sform(float('-inf')))
(-INF)E+00

.. _val_unc_formatting_options:

Value/Uncertainty Formatting Options
====================================

For value/uncertainty formatting the value + uncertainty pair are
formatted as follows.
First, significant figure rounding is applied to the uncertainty
according to the specified precision.
Next the value is rounded to the same position as the uncertainty.
The exponent is then determined using the exponent mode and the larger
of the value or uncertainty.
The value and the uncertainty are then formatted into a single string
according to the options below.

>>> sform = Formatter()
>>> print(sform(123.456, 0.789))
123.456 +/- 0.789

Particle Data Group Significant Figures
---------------------------------------

Typically value/uncertainty pairs are formatted with one or two
significant figures displayed for the uncertainty.
The Particle Data Group has
`published an algorithm <https://pdg.lbl.gov/2010/reviews/rpp2010-rev-rpp-intro.pdf>`_
for deciding when to
display uncertainty with one versus two significant figures.
The algorithm is as follows.

* Determine the three most significant digits of the uncertainty. E.g.
  if the uncertainty is 0.004857 then these digits would be 486
* If the value is between 100 and 354 (inclusive) then display the
  uncertainty with two significant digits. E.g. if the uncertainty is
  30.3 then display the uncertainy as 30
* If the value is between 355 and 954 (inclusive) then display the
  uncertainty with one signifcant digit. E.g. if the uncertainty is
  0.76932 then display the uncertainty as 0.8
* If the value is between 955 and 999 (inclusive) then display the
  uncertainty with two signficant digit, noting that this will involve
  rounding the three most significant digits up to 1000. E.g. if the
  uncertainty is 0.99 then display the uncertainty as 1.0.

:mod:`sciform` provides the ability to use this algorithm when
formatting value/uncertainty pairs by using significant figure rounding
mode with :class:`AutoPrec` precision and the ``pdg_sig_figs`` flag.

>>> from sciform import AutoPrec
>>> sform = Formatter(round_mode=RoundMode.SIG_FIG,
...                   precision=AutoPrec,
...                   pdg_sig_figs=True)
>>> print(sform(1, 0.0123))
1.00 +/- 0.01
>>> print(sform(1, 0.0483))
1.000 +/- 0.048
>>> print(sform(1, 0.0997))
1.00 +/- 0.10

Plus Minus Symbol Formatting
----------------------------

The user can enable (default) or disable white space around the plus/minus
symbol when formatting value/uncertainties.

>>> sform = Formatter()
>>> print(sform(123.456, 0.789))
123.456 +/- 0.789
>>> sform = Formatter(unc_pm_whitespace=False)
>>> print(sform(123.456, 0.789))
123.456+/-0.789

The user can also replace the ``'+/-'`` symbol with a unicode ``'±'``
symbol using the ``unicode_pm`` option.

>>> sform = Formatter(unicode_pm=True)
>>> print(sform(123.456, 0.789))
123.456 ± 0.789

Bracket Uncertainty
-------------------

Instead of displaying ``123.456 +/- 0.789``, there is a notation where
the uncertainty is shown in brackets after the value as
``123.456(789)``.
Here the ``(789)`` in parentheses is meant to be "matched up" with the
finaly three digits of the value so that the 9 in the uncertainty is
understood to appear in the thousandths place.
This format is described in the
`BIPM Guide Section 7.2.2 <https://www.bipm.org/documents/20126/2071204/JCGM_100_2008_E.pdf/cb0ef43f-baa5-11cf-3f85-4dcd86f77bd6#page=37>`_.
We call this format "bracket uncertainty" mode.
:mod:`sciform` provides this functionality via the ``bracket_unc``
option:

>>> sform = Formatter(bracket_unc=True)
>>> print(sform(123.456, 0.789))
123.456(789)

Or with other options:

>>> sform = Formatter(precision=2,
...                   bracket_unc=True)
>>> print(sform(123.456, 0.789))
123.46(79)
>>> sform = Formatter(precision=2,
...                   exp_mode=ExpMode.SCIENTIFIC,
...                   bracket_unc=True)
>>> print(sform(123.456, 0.789))
(1.2346(79))e+02

Remove Separators for Bracket Uncertainty
--------------------------------------------

In some cases using bracket uncertainty results in digits such that the
decimal point could appear in the uncertainty in the brackets.
For example: ``18.4 +/- 2.1 -> 18.4(2.1)``.
In such cases, there is no official guidance on if the decimal symbol
should be included in the bracket symbols or not.
That is, one may format ``18.4 +/- 2.1 -> 18.4 (21)``.
The interpretation here is that the uncertainty is 21 tenths, since the
digit of the value is in the tenths place.
Note that the author recommends keeping the decimal symbol because it
allows for rapid "lining up" of the decimal places by eye.

:mod:`sciform` allows the user to optionally remove the decimal symbol

>>> sform = Formatter(bracket_unc=True,
...                   bracket_unc_remove_seps=False)
>>> print(sform(18.4, 2.1))
18.4(2.1)
>>> sform = Formatter(bracket_unc=True,
...                   bracket_unc_remove_seps=True)
>>> print(sform(18.4, 2.1))
18.4(21)

Note that the ``bracket_unc_remove_seps`` removes *all* separator
symbols from the uncertainty in the brackets.

>>> sform = Formatter(upper_separator=GroupingSeparator.POINT,
...                   decimal_separator=GroupingSeparator.COMMA,
...                   lower_separator=GroupingSeparator.UNDERSCORE,
...                   bracket_unc=True,
...                   bracket_unc_remove_seps=False)
>>> print(sform(987654, 1234.4321))
987.654,000_0(1.234,432_1)
>>> sform = Formatter(upper_separator=GroupingSeparator.POINT,
...                   decimal_separator=GroupingSeparator.COMMA,
...                   lower_separator=GroupingSeparator.UNDERSCORE,
...                   bracket_unc=True,
...                   bracket_unc_remove_seps=True)
>>> print(sform(987654, 1234.4321))
987.654,000_0(12344321)

This latest example demonstrates that the bracket uncertainty mode can
become difficult to read in some cases.
Bracket uncertainty is most useful when the value is at least a few
orders of magnitude larger than the uncertainty and when the uncertainty
is displayed with a small number (e.g. 1 or 2) significant digits.

Match Value/Uncertainty Width
-----------------------------

If the user passes ``top_dig_place`` into a :class:`Formatter` then that
top digit place will be used to left pad both the value and the
uncertainty.
:mod:`sciform` provides additional control over the left padding of the
value and the uncertainty by allowing the user to left pad to the
maximum of (1) the specified ``top_dig_place``, (2) the most significant
digit of the value, and (3) the most significant digit of the
uncertainty.
This feature is accessed with the ``val_unc_match_widths`` option.

>>> sform = Formatter(fill_mode=FillMode.ZERO,
...                   top_dig_place=2,
...                   val_unc_match_widths=False)
>>> print(sform(12345, 1.23))
12345.00 +/- 001.23
>>> sform = Formatter(fill_mode=FillMode.ZERO,
...                   top_dig_place=2,
...                   val_unc_match_widths=True)
>>> print(sform(12345, 1.23))
12345.00 +/- 00001.23
