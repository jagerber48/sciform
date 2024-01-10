.. _formatting_options:

##################
Formatting Options
##################

.. module:: sciform
   :noindex:

:mod:`sciform` provides a variety of options for converting numbers into
formatted strings.
These options include control over the rounding strategy, scientific
notation formatting, separation characters and more.

.. _exp_mode:

Exponent Mode
=============

:mod:`sciform` supports a variety of exponent modes.
To display numbers across a wide range of magnitudes, scientific
formatting presents numbers in the form::

   num = mantissa * base**exp

Where exp is an integer and ``base`` is 10 or 2.
The different exponent modes control how ``mantissa``, ``base`` and
``exp`` are chosen for a given input number ``num``.

.. _fixed_point:

Fixed Point
-----------

Fixed point notation is standard notation in which a number is displayed
directly with no extra exponent.

>>> from sciform import Formatter
>>> sform = Formatter(exp_mode="fixed_point")
>>> print(sform(123.456))
123.456
>>> print(sform(123.456, 0.001))
123.456 ± 0.001

.. _percent_mode:

Percent
-------

Percent mode is similar to fixed point mode.
For percent mode, the number is multiplied by 100 and a ``%`` symbol is
appended to the end of the formatted string.

>>> sform = Formatter(exp_mode="percent")
>>> print(sform(0.12345))
12.345%
>>> print(sform(0.12345, 0.001))
(12.3 ± 0.1)%

.. _scientific:

Scientific Notation
-------------------

Scientific notation is used to display base-10 decimal numbers.
In scientific notation, the exponent is uniquely chosen so that the
mantissa ``m`` satisfies ``1 <= m < 10``.

>>> sform = Formatter(exp_mode="scientific")
>>> print(sform(123.456))
1.23456e+02
>>> print(sform(123.456, 0.001))
(1.23456 ± 0.00001)e+02

Note that, for all exponent modes, the exponent integer is always
displayed with a sign symbol (+ or -) and is left padded with a zero so
that it is at least two digits wide.
There are no options to modify this behavior for standard exponent
display.
The :ref:`superscript` or :ref:`latex_format` options can be used as
alternatives.

.. _engineering:

Engineering Notation
--------------------

Engineering notation is similar to scientific notation except the
exponent is chosen to be an integer multiple of 3.
In standard engineering notation, the mantissa ``m`` satisfies
``1 <= m < 1000``.
Engineering notation is compatible with the SI prefixes which are
defined for any integer multiple of 3 exponent, e.g.::

   369,000,00 Hz = 369e+06 Hz = 369 MHz

Here it may be more convenient to display the number with an exponent of
6 for rapid identification of the "Mega" order of magnitude, as opposed
to an exponent of 8 which would be chosen for standard scientific
notation.

>>> sform = Formatter(exp_mode="engineering")
>>> print(sform(123.456))
123.456e+00
>>> print(sform(123.456, 0.001))
(123.456 ± 0.001)e+00

.. _engineering_shifted:

Shifted Engineering Notation
----------------------------

Shifted engineering notation is the same as engineering notation except
the exponent is chosen so that the mantissa ``m`` satisfies
``0.1 <= m < 100``.

>>> sform = Formatter(exp_mode="engineering_shifted")
>>> print(sform(123.456))
0.123456e+03
>>> print(sform(123.456, 0.001))
(0.123456 ± 0.000001)e+03

.. _binary:

Binary
------

Binary formatting can be chosen to display a number in scientific
notation in base-2.

>>> sform = Formatter(exp_mode="binary")
>>> print(sform(256))
1b+08

Here ``b`` exponent symbol indicates base-2 instead of base-10.
For binary formatting, the mantissa ``m`` satisfies ``1 <= m < 2``.

.. _binary_iec:

Binary IEC
----------

Binary IEC mode is similar to engineering notation, except in base-2.
In this mode number are expressed in base-2 exponent notation, but the
exponent is constrained to be a multiple of 10, consistent with the
IEC binary prefixes.
The mantissa ``m`` satisfies ``1 <= m < 1024``.

>>> sform = Formatter(exp_mode="binary_iec")
>>> print(sform(2048))
2b+10

.. _fixed_exp:

Fixed Exponent
==============

The user can coerce the exponent for the formatting to a fixed value.

>>> sform = Formatter(exp_mode="scientific", exp_val=3)
>>> print(sform(123.456))
0.123456e+03

To explicitly force :mod:`sciform` to automatically select the exponent
then use the :class:`AutoExpVal` option by passing
``exp_val=AutoExpVal``.
This is the default value in the global configuration.

Note that the forced exponent must be consistent with the requested
exponent mode.
For fixed point and percent modes an explicit fixed exponent must equal
0.
For engineering and shifted engineering modes an explicit fixed exponent
must be an integer multiple of 3.
For binary IEC mode an explicit fixed exponent must be an integer
multiple of 10.
Because of this constrained behavior, it is recommended to only use a
fixed exponent with the scientific or binary exponent modes.

.. _exp_str_replacement:

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

>>> sform = Formatter(exp_mode="engineering", exp_format="prefix")
>>> print(sform(4242.13))
4.24213 k
>>> sform = Formatter(
...     exp_mode="binary_iec",
...     round_mode="sig_fig",
...     ndigits=4,
...     exp_format="prefix",
... )
>>> print(sform(1300))
1.270 Ki
>>> sform = Formatter(exp_mode="engineering", exp_format="parts_per")
>>> print(sform(12.3e-6))
12.3 ppm

.. _extra_translations:

Extra Exponent Replacements
---------------------------

In addition to the default
:ref:`exponent replacements <exp_replacements>`, The user can modify the
available exponent replacements using a number of options.
The SI prefix, IEC prefix, and parts-per replacements can be modified
using the ``extra_si_prefixes``, ``extra_iec_prefixes`` and
``extra_parts_per_forms`` options, respectively, and passing in
dictionaries with keys corresponding to integer exponents and values
corresponding to translated strings.
The entries in these dictionaries overwrite any default translation
mappings.

>>> sform = Formatter(
...     exp_mode="scientific",
...     exp_format="prefix",
...     extra_si_prefixes={-2: "c"},
... )
>>> print(sform(3e-2))
3 c

Passing ``None`` for the value for a corresponding exponent value will
force that exponent to not be translated.

>>> sform = Formatter(exp_mode="engineering", exp_format="parts_per")
>>> print(sform(3e-9))
3 ppb
>>> sform = Formatter(
...     exp_mode="engineering",
...     exp_format="parts_per",
...     extra_parts_per_forms={-9: None},
... )
>>> print(sform(3e-9))
3e-09

Two helper options exist to add additional SI prefix translations
corresponding to::

    {-2: 'c', -1: 'd', +1: 'da', +2: 'h'}

These SI prefixes are excluded by default because they do not correspond
to the integer-multiple-of-3 prefixes which are compatible with
engineering notation.
However, they can be easily be included using the ``add_c_prefix`` and
``add_small_si_prefixes`` options.

>>> sform = Formatter(
...     exp_mode="scientific",
...     exp_format="prefix",
...     add_c_prefix=True,
... )
>>> print(sform(0.025))
2.5 c
>>> sform = Formatter(
...     exp_mode="scientific",
...     exp_format="prefix",
...     add_small_si_prefixes=True,
... )
>>> print(sform(25))
2.5 da

A parts-per-thousand form, ``ppth``, can be accessed with
the ``add_ppth_form`` option.
Note that ``ppth`` is not a standard notation for "parts-per-thousand",
but it is one that the author has found useful.

>>> sform = Formatter(
...     exp_mode="engineering",
...     exp_format="parts_per",
...     add_ppth_form=True,
... )
>>> print(sform(12.3e-3))
12.3 ppth

Note that the helper flags will not overwrite value/string pairs already
specified in the extra translations dictionary:

>>> sform = Formatter(
...     exp_mode="scientific",
...     exp_format="prefix",
...     add_c_prefix=True,
... )
>>> print(sform(0.012))
1.2 c
>>> sform = Formatter(
...     exp_mode="scientific",
...     exp_format="prefix",
...     extra_si_prefixes={-2: 'zzz'},
...     add_c_prefix=True,
... )
>>> print(sform(0.012))
1.2 zzz

Note that there is never *merging* of local and global extra
translations.
If any local extra translation settings are configured directly with
e.g. ``extra_si_prefixes`` or with a helper like
``add_small_si_prefixes`` then no global extra translations will be
used.

>>> from sciform import GlobalDefaultsContext
>>> sform = Formatter(
...     exp_mode="scientific",
...     exp_format="prefix",
...     extra_si_prefixes={-4: "zzz"},
... )
>>> with GlobalDefaultsContext(add_c_prefix=True):
...     print(sform(0.012))
1.2e-02
>>> sform = Formatter(
...     exp_mode="scientific",
...     exp_format="prefix",
...     add_c_prefix=True,
... )
>>> with GlobalDefaultsContext(extra_si_prefixes={1: 'zzz'}):
...     print(sform(12.4))
1.24e+01

If all local extra translation settings are left unset then all global
extra translation settings will be populated at format time.
This behavior is the same as the behavior for all other options.


.. _rounding:

Rounding
========

:mod:`sciform` provides two rounding strategies: rounding based on
significant figures, and rounding based on decimal places.
In both cases, the rounding applies to the mantissa determined after
identifying the appropriate exponent for display based on the selected
exponent mode.
In some cases, the rounding results in a modification to the chosen
exponent (e.g. when presenting ``9.99`` in scientific exponent mode with
two digits past the decimal point :mod:`sciform` displays
``"9.99e+00"``, but with one digit past the decimal point :mod:`sciform`
displays ``"1.0e+01"``).
This is taken into account before the final presentation.

If the user does not specify the number of significant digits or the
digits place to which to round, then the decimal numbers are displayed
with full precision.
To explicitly request this behavior, the user may use the
:class:`AutoDigits` sentinel by passing ``ndigits=AutoDigits``.
This is the default value in the global configuration.

Note that surprising behavior may be observed if using :class:`float`
inputs.
A :class:`float` input is handled by first being converted to a string
to realize the minimum number decimal digits necessary for the
:class:`float` to round trip and is then cast to :class:`Decimal`
instance before determining the mantissa and exponent and applying the
rounding algorithm.
See :ref:`dec_and_float` for more details.

Significant Figures
-------------------

For significant figure rounding, first the digits place for the
most-significant digit is identified, then the number is rounded to
the specified number of significant figures below that digits place.
E.g. for ``12345.678`` the most-significant digit appears in the
ten-thousands, or 10\ :sup:`4`, place.
To express this number to 4-significant digits means we should round it
to the tens, or 10\ :sup:`1`, place resulting in ``12350``.

Note that 1001 rounded to 1, 2, or 3 significant figures results in
1000.
This demonstrates that we can't determine how many significant figures
a number was rounded to (or "how many significant figures a number has")
just by looking at the resulting string.

>>> sform = Formatter(
...     exp_mode="engineering",
...     round_mode="sig_fig",
...     ndigits=4,
... )
>>> print(sform(12345.678))
12.35e+03

Here the ``ndigits`` input is used to indicate how many significant
figures should be included.
for significant figure rounding, ``ndigits`` must be an integer
greater than or equal 1.

Decimal Place
-------------

For decimal place rounding we specify the decimal place to which we want
to round using ``ndigits``.
The convention for ``ndigits`` is the same as that for the built-in
`round function <https://docs.python.org/3/library/functions.html#round>`_.
E.g. ``ndigits=2`` means to round to two digits past the decimal place,
the hundredths or 10\ :sup:`-2` place, so that ``12.987`` would be
rounded to ``12.99``.

>>> sform = Formatter(exp_mode="engineering", round_mode="dec_place", ndigits=4)
>>> print(sform(12345.678))
12.3457e+03

It is possible for ``ndigits <= 0``:

>>> sform = Formatter(
...     exp_mode="fixed_point",
...     round_mode="dec_place",
...     ndigits=-2,
... )
>>> print(sform(12345.678))
12300

Automatic Rounding
------------------

If the user does not specify ``ndigits`` or the user uses
:class:`AutoDigits` by passing ``ndigits=AutoDigits``, then
:mod:`sciform` will automatically determine how rounding should be
performed.

For single value formatting the auto rounding mode will display the
input number with full precision.
For :class:`str`, :class:`int` and :class:`Decimal` inputs this is
unambiguous.
For :class:`float` inputs the :class:`float` is first converted to a
string and then converted to a decimal.
This means that the :class:`float` will be rounded to the minimum
necessary precision for it to "round-trip".
See :ref:`dec_and_float` for more details.

For value/uncertainty formatting, if ``ndigits=AutoDigits`` and
``pdg_sig_figs=False``, then the rounding strategy described in the
previous paragraph is used to round the uncertainty and the value is
rounded to the same decimal place as the uncertainty.
See :ref:`pdg_sig_figs` for more details.

.. _separators:

Separators
==========

:mod:`sciform` provides support for some customization for separator
characters within formatting strings.
Different locales use different conventions for the symbol separating
the integral and fractional part of a number, called the decimal symbol.
:mod:`sciform` supports using a period ``'.'`` or comma ``','`` as the
decimal symbol.

Additionally, :mod:`sciform` also supports including separation
characters between groups of three digits both above the decimal symbol
and below the decimal symbol.
``''``, ``','``, ``'.'``, ``' '``, ``'_'`` can all be used as
"upper" separator characters and ``''``, ``' '``, and ``'_'`` can
all be used as "lower" separator characters.
Note that the upper separator character must be different than the
decimal separator.

>>> sform = Formatter(upper_separator=",")
>>> print(sform(12345678.987))
12,345,678.987

>>> sform = Formatter(
...     upper_separator=" ",
...     decimal_separator=",",
...     lower_separator="_",
... )
>>> print(sform(1234567.7654321))
1 234 567,765_432_1

NIST discourages the use of ``','`` or ``'.'`` as thousands separators
because they can be confused with the decimal separators depending on
the locality. See
`NIST Guide to the SI 10.5.3 <https://www.nist.gov/pml/special-publication-811/nist-guide-si-chapter-10-more-printing-and-using-symbols-and-numbers#1053>`_.

.. _sign_mode:

Sign Mode
=========

:mod:`sciform` provides control over the symbol used to indicate whether
a number is positive or negative.
In all cases a ``'-'`` sign is used for negative numbers.
By default, positive numbers are formatted with no sign symbol.
However, :mod:`sciform` includes a mode where positive numbers are
always presented with a ``'+'`` symbol.
:mod:`sciform` also provides a mode where positive numbers include an
extra whitespace in place of a sign symbol.
This mode may be useful to match string lengths when positive and
negatives numbers are being presented together, but without explicitly
including a ``'+'`` symbol.
Note that ``0`` is always considered positive.

>>> sform = Formatter(sign_mode="-")
>>> print(sform(42))
42
>>> sform = Formatter(sign_mode="+")
>>> print(sform(42))
+42
>>> sform = Formatter(sign_mode=" ")
>>> print(sform(42))
 42

Capitalization
==============

The capitalization of the exponent character can be controlled

>>> sform = Formatter(exp_mode="scientific", capitalize=True)
>>> print(sform(42))
4.2E+01
>>> sform = Formatter(exp_mode="binary", capitalize=True)
>>> print(sform(1024))
1B+10

The ``capitalize`` flag also controls the capitalization of ``nan`` and
``inf`` formatting:

>>> print(sform(float("nan")))
NAN
>>> print(sform(float("-inf")))
-INF

.. _left_filling:

Left Filling
============

The :ref:`rounding` options described above can be used to control how
many digits to the right of either the most-significant digit or the
decimal point are displayed.
It is also possible, using "fill" options, to add digits to the left of
the most-significant digit.
The ``fill_char`` option can be used to select either whitespaces
``' '`` or zeros ``'0'`` as fill characters.
The ``left_pad_dec_place`` option is used to indicate to which decimal
place fill characters should be added.
E.g. ``left_pad_dec_place=4`` indicates fill characters should be
added up to the 10\ :sup:`4` (ten-thousands) decimal place.

>>> sform = Formatter(fill_char="0", left_pad_dec_place=4)
>>> print(sform(42))
00042

.. _superscript:

Superscript Exponent Format
===========================

The ``superscript`` option can be chosen to present exponents in
superscript notation as opposed to e.g. ``e+02`` notation.

>>> sform = Formatter(exp_mode="scientific", superscript=True)
>>> print(sform(789))
7.89×10²

.. _latex_format:

Latex Format
============

The ``latex`` option can be chosen to convert strings into latex
parseable codes.

>>> sform = Formatter(
...     exp_mode="scientific",
...     exp_val=-1,
...     upper_separator="_",
...     latex=True,
... )
>>> print(sform(12345))
123\_450\times 10^{-1}
>>> sform = Formatter(
...     exp_mode="percent",
...     lower_separator="_",
...     latex=True,
... )
>>> print(sform(0.12345678, 0.00000255))
\left(12.345\_678 \pm 0.000\_255\right)\%

The latex format makes the following changes:

* Convert standard exponent strings such as ``'e+02'`` into latex
  superscript strings like ``'\times 10^{+2}``
* Replace ``'('`` and ``')'`` by latex size-aware delimiters
  ``'\left('`` and ``'\right)'``.
* Replace ``'±'`` by ``'\pm'``
* Replace ``'_'`` by ``'\_'``
* Replace ``'%'`` by ``'\%'``
* Exponent replacements such as ``'M'``, ``'Ki'``, or ``'ppb'`` and
  non-finite numbers such as ``'nan'``, ``'NAN'``, ``'inf'``, and
  ``'INF'`` are wrapped in ``'\text{}'``.

Note that use of ``latex`` renders the use of the ``superscript``
option meaningless.

Include Exponent on nan and inf
===============================

Python supports ``'nan'``, ``'inf'``, and
``'-inf'`` numbers which are simply formatted to ``'nan'``, ``'inf'``,
and ``'-inf'`` or ``'NAN'``, ``'INF'``, and ``'-INF'``, respectively,
depending on ``capitalize``.
However, if ``nan_inf_exp=True`` (default ``False``), then, for
scientific, percent, engineering, and binary exponent modes, these will
instead be formatted as, e.g. ``'(nan)e+00'``.

>>> sform = Formatter(
...     exp_mode="scientific",
...     nan_inf_exp=False,
...     capitalize=True,
... )
>>> print(sform(float("-inf")))
-INF
>>> sform = Formatter(
...     exp_mode="scientific",
...     nan_inf_exp=True,
...     capitalize=True,
... )
>>> print(sform(float("-inf")))
(-INF)E+00
>>> sform = Formatter(
...     exp_mode="percent",
...     nan_inf_exp=False,
...     capitalize=True,
... )
>>> print(sform(float("-inf")))
-INF
>>> sform = Formatter(
...     exp_mode="percent",
...     nan_inf_exp=True,
...     capitalize=True,
... )
>>> print(sform(float("-inf")))
(-INF)%

.. _val_unc_formatting_options:

Value/Uncertainty Formatting Options
====================================

For value/uncertainty formatting, the value + uncertainty pair are
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
123.456 ± 0.789

.. _pdg_sig_figs:

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
* If the scaled uncertainty is between 100 and 354 (inclusive) then the
  uncertainty is rounded and displayed to one digit below its most
  significant digit.
  This means it will have two significant digit.
  E.g. if the uncertainty is 3.03 then it will appear as as 3.0
* If the scaled uncertainty is between 355 and 949 (inclusive) then the
  uncertainty is rounded and displayed to the same digit as the most
  significant digit.
  This means it will have one significant digit.
  E.g. if the uncertainty is 0.76932 then it will appear as 0.8
* If the scaled uncertainty is between 950 and 999 (inclusive) then the
  uncertainty is rounded and displayed to the same digit as the most
  significant digit.
  But 950 and above will always be rounded to 1000 if we round to the
  hundreds place.
  This means there will be two significant digits.
  E.g. if the uncertainty is 0.0099 then it will be displayed as 0.010.

:mod:`sciform` provides the ability to use this algorithm when
formatting value/uncertainty pairs by using significant figure rounding
mode and the ``pdg_sig_figs`` flag.

>>> from sciform import AutoDigits
>>> sform = Formatter(
...     round_mode="sig_fig",
...     pdg_sig_figs=True,
... )
>>> print(sform(1, 0.0123))
1.000 ± 0.012
>>> print(sform(1, 0.0483))
1.00 ± 0.05
>>> print(sform(1, 0.0997))
1.00 ± 0.10

If ``pdg_sig_figs=True`` then ``ndigits`` is ignored for
value/uncertainty formatting.
``pdg_sig_figs`` is always ignored in favor of ``ndigits`` for single
value formatting.

.. _paren_uncertainty:

Parentheses Uncertainty
-----------------------

Instead of displaying ``123.456 ± 0.789``, there is a notation where
the uncertainty is shown in parentheses after the value as
``123.456(789)``.
Here the ``(789)`` in parentheses is meant to be "matched up" with the
final three digits of the value so that the 9 in the uncertainty is
understood to appear in the thousandths place.
This format is described in the
`BIPM Guide Section 7.2.2 <https://www.bipm.org/documents/20126/2071204/JCGM_100_2008_E.pdf/cb0ef43f-baa5-11cf-3f85-4dcd86f77bd6#page=37>`_.
We call this format "parentheses uncertainty" mode.
:mod:`sciform` provides this functionality via the ``paren_uncertainty``
option:

>>> sform = Formatter(paren_uncertainty=True)
>>> print(sform(123.456, 0.789))
123.456(789)

Or with other options:

>>> sform = Formatter(ndigits=2, paren_uncertainty=True)
>>> print(sform(123.456, 0.789))
123.46(79)
>>> sform = Formatter(
...     ndigits=2,
...     exp_mode="scientific",
...     paren_uncertainty=True,
... )
>>> print(sform(123.456, 0.789))
(1.2346(79))e+02

When ``paren_uncertainty=True`` is used with the prefix or parts-per
exponent formats, if the exponent string is replaced, then the enclosing
parentheses around the value/uncertainty pair are omitted.
This is consistent with
`BIPM Guide Section 7.2.2 <https://www.bipm.org/documents/20126/2071204/JCGM_100_2008_E.pdf/cb0ef43f-baa5-11cf-3f85-4dcd86f77bd6#page=37>`_.

>>> sform = Formatter(
...     exp_mode="engineering",
...     exp_format="prefix",
...     paren_uncertainty=True,
... )
>>> print(sform(523.4e-3, 1.2e-3))
523.4(1.2) m

Parentheses Uncertainty Separators
----------------------------------

In some cases using parentheses uncertainty results in digits such that
a decimal point could appear in the uncertainty in the parentheses.
For example: ``18.4 ± 2.1 -> 18.4(2.1)``.
In such cases, there is no official guidance on if the decimal symbol
should be included in the uncertainty or not.
That is, one may format ``18.4 ± 2.1 -> 18.4(21)``.
The interpretation here is that the uncertainty is 21 tenths, since the
least significant digit of the value is in the tenths place.
The author's preference is to keep the decimal symbol because it allows
for rapid "lining up" of the decimal places by eye and it is similar to
`BIPM Guide Section 7.2.2 <https://www.bipm.org/documents/20126/2071204/JCGM_100_2008_E.pdf/cb0ef43f-baa5-11cf-3f85-4dcd86f77bd6#page=37>`_.
example 3 in which the entire uncertainty number is shown in
parentheses.

:mod:`sciform` allows the user to optionally include or exclude
separator symbols from the uncertainty in parentheses using the
``paren_uncertainty_separatros`` option:

>>> sform = Formatter(
...     paren_uncertainty=True,
...     paren_uncertainty_separators=True,
... )
>>> print(sform(18.4, 2.1))
18.4(2.1)
>>> sform = Formatter(
...     paren_uncertainty=True,
...     paren_uncertainty_separators=False,
... )
>>> print(sform(18.4, 2.1))
18.4(21)

Note that the ``paren_uncertainty_separators`` removes *all* separator
symbols from the uncertainty in the parentheses.

>>> sform = Formatter(
...     upper_separator=".",
...     decimal_separator=",",
...     lower_separator="_",
...     paren_uncertainty=True,
...     paren_uncertainty_separators=True,
... )
>>> print(sform(987654, 1234.4321))
987.654,000_0(1.234,432_1)
>>> sform = Formatter(
...     upper_separator=".",
...     decimal_separator=",",
...     lower_separator="_",
...     paren_uncertainty=True,
...     paren_uncertainty_separators=False,
... )
>>> print(sform(987654, 1234.4321))
987.654,000_0(12344321)

This latest example demonstrates that the parentheses uncertainty mode
can become difficult to read in some cases.
Parentheses uncertainty is most useful when the value is at least a few
orders of magnitude larger than the uncertainty and when the uncertainty
is displayed with a small number (e.g. 1 or 2) of significant digits.

Match Value/Uncertainty Width
-----------------------------

If the user passes ``left_pad_dec_place`` into a :class:`Formatter`,
then that decimal place will be used for left padding both the value and
the uncertainty.
:mod:`sciform` provides additional control over the left padding of the
value and the uncertainty by allowing the user to left pad to the
maximum of (1) the specified ``left_pad_dec_place``, (2) the most
significant digit of the value, and (3) the most significant digit of
the uncertainty.
This feature is accessed with the ``left_pad_matching`` option.

>>> sform = Formatter(
...     fill_char="0",
...     left_pad_dec_place=2,
...     left_pad_matching=False,
... )
>>> print(sform(12345, 1.23))
12345.00 ± 001.23
>>> sform = Formatter(
...     fill_char="0",
...     left_pad_dec_place=2,
...     left_pad_matching=True,
... )
>>> print(sform(12345, 1.23))
12345.00 ± 00001.23
