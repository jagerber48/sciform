.. _formatting_options:

##################
Formatting Options
##################

.. module:: sciform
   :no-index:

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
>>> formatter = Formatter(exp_mode="fixed_point")
>>> print(formatter(123.456))
123.456
>>> print(formatter(123.456, 0.001))
123.456 ± 0.001

.. _percent_mode:

Percent
-------

Percent mode is similar to fixed point mode.
For percent mode, the number is multiplied by 100 and a ``%`` symbol is
appended to the end of the formatted string.

>>> formatter = Formatter(exp_mode="percent")
>>> print(formatter(0.12345))
12.345%
>>> print(formatter(0.12345, 0.001))
(12.3 ± 0.1)%

.. _scientific:

Scientific Notation
-------------------

Scientific notation is used to display base-10 decimal numbers.
In scientific notation, the exponent is uniquely chosen so that the
mantissa ``m`` satisfies ``1 <= m < 10``.

>>> formatter = Formatter(exp_mode="scientific")
>>> print(formatter(123.456))
1.23456e+02
>>> print(formatter(123.456, 0.001))
(1.23456 ± 0.00001)e+02

By default the exponent is expressed using ASCII characters, e.g.
``e+02``.
The sign symbol is always included and the exponent value is left padded
so that it is at least two digits wide.
These behaviors for ASCII exponents cannot be modified.
However the :ref:`superscript` mode can be used to represent the
exponent using Unicode superscript characters.

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

>>> formatter = Formatter(exp_mode="engineering")
>>> print(formatter(123.456))
123.456e+00
>>> print(formatter(123.456, 0.001))
(123.456 ± 0.001)e+00

.. _engineering_shifted:

Shifted Engineering Notation
----------------------------

Shifted engineering notation is the same as engineering notation except
the exponent is chosen so that the mantissa ``m`` satisfies
``0.1 <= m < 100``.

>>> formatter = Formatter(exp_mode="engineering_shifted")
>>> print(formatter(123.456))
0.123456e+03
>>> print(formatter(123.456, 0.001))
(0.123456 ± 0.000001)e+03

.. _binary:

Binary
------

Binary formatting can be chosen to display a number in scientific
notation in base-2.

>>> formatter = Formatter(exp_mode="binary")
>>> print(formatter(256))
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

>>> formatter = Formatter(exp_mode="binary_iec")
>>> print(formatter(2048))
2b+10

.. _fixed_exp:

Fixed Exponent
==============

The user can coerce the exponent for the formatting to a fixed value.

>>> formatter = Formatter(exp_mode="scientific", exp_val=3)
>>> print(formatter(123.456))
0.123456e+03

To explicitly force :mod:`sciform` to automatically select the exponent
then set ``exp_val="auto"``.
This is the default value in the global options.

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
objects or the global options settings to map additional translations,
in addition to those provided by default.

>>> formatter = Formatter(exp_mode="engineering", exp_format="prefix")
>>> print(formatter(4242.13))
4.24213 k
>>> formatter = Formatter(
...     exp_mode="binary_iec",
...     round_mode="sig_fig",
...     ndigits=4,
...     exp_format="prefix",
... )
>>> print(formatter(1300))
1.270 Ki
>>> formatter = Formatter(exp_mode="engineering", exp_format="parts_per")
>>> print(formatter(12.3e-6))
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

>>> formatter = Formatter(
...     exp_mode="scientific",
...     exp_format="prefix",
...     extra_si_prefixes={-2: "c"},
... )
>>> print(formatter(3e-2))
3 c

Passing ``None`` for the value for a corresponding exponent value will
force that exponent to not be translated.

>>> formatter = Formatter(exp_mode="engineering", exp_format="parts_per")
>>> print(formatter(3e-9))
3 ppb
>>> formatter = Formatter(
...     exp_mode="engineering",
...     exp_format="parts_per",
...     extra_parts_per_forms={-9: None},
... )
>>> print(formatter(3e-9))
3e-09

Keys into the extra translations dictionaries must be integers and
values must consist of only English alphabetic characters.

Two helper options exist to add additional SI prefix translations
corresponding to::

    {-2: 'c', -1: 'd', +1: 'da', +2: 'h'}

These SI prefixes are excluded by default because they do not correspond
to the integer-multiple-of-3 prefixes which are compatible with
engineering notation.
However, they can be easily be included using the ``add_c_prefix`` and
``add_small_si_prefixes`` options.

>>> formatter = Formatter(
...     exp_mode="scientific",
...     exp_format="prefix",
...     add_c_prefix=True,
... )
>>> print(formatter(0.025))
2.5 c
>>> formatter = Formatter(
...     exp_mode="scientific",
...     exp_format="prefix",
...     add_small_si_prefixes=True,
... )
>>> print(formatter(25))
2.5 da

A parts-per-thousand form, ``ppth``, can be accessed with
the ``add_ppth_form`` option.
Note that ``ppth`` is not a standard notation for "parts-per-thousand",
but it is one that the author has found useful.

>>> formatter = Formatter(
...     exp_mode="engineering",
...     exp_format="parts_per",
...     add_ppth_form=True,
... )
>>> print(formatter(12.3e-3))
12.3 ppth

Note that the helper flags will not overwrite value/string pairs already
specified in the extra translations dictionary:

>>> formatter = Formatter(
...     exp_mode="scientific",
...     exp_format="prefix",
...     add_c_prefix=True,
... )
>>> print(formatter(0.012))
1.2 c
>>> formatter = Formatter(
...     exp_mode="scientific",
...     exp_format="prefix",
...     extra_si_prefixes={-2: "zzz"},
...     add_c_prefix=True,
... )
>>> print(formatter(0.012))
1.2 zzz

Note that there is never *merging* of local and global extra
translations.
If any local extra translation settings are configured directly with
e.g. ``extra_si_prefixes`` or with a helper like
``add_small_si_prefixes`` then no global extra translations will be
used.

>>> from sciform import GlobalOptionsContext
>>> formatter = Formatter(
...     exp_mode="scientific",
...     exp_format="prefix",
...     extra_si_prefixes={-4: "zzz"},
... )
>>> with GlobalOptionsContext(add_c_prefix=True):
...     print(formatter(0.012))
1.2e-02
>>> formatter = Formatter(
...     exp_mode="scientific",
...     exp_format="prefix",
...     add_c_prefix=True,
... )
>>> with GlobalOptionsContext(extra_si_prefixes={1: "zzz"}):
...     print(formatter(12.4))
1.24e+01

If all local extra translation settings are left unset then all global
extra translation settings will be populated at format time.
This behavior is the same as the behavior for all other options.


.. _rounding:

Rounding
========

:mod:`sciform` provides four rounding strategies controlled by the
``round_mode`` and ``ndigits`` options.

* Significant figure rounding is selected by setting ``round_mode="sig_fig"``
  and passing in a positive :class:`int` for ``ndigits`` specifying the number
  of significant figures to which to round.
* Digits-past-the-deciaml rounding is selected by setting
  ``round_mode="dec_place"`` and passing an :class:`int` for ``ndigits``
  specifying the digit place to which to round.
* All digits rounding is selected by setting ``round_mode="all"``.
  In this mode "all" digits of the number are shown where the definition of
  "all" depends on the type of the numerical input data.
  See below for more details.
  In this mode the ``ndigits`` option has no effect.
* Particle data group (PDG) rounding is selected by setting
  ``round_mode="pdg"``.
  See below for the defintion of PDG rounding.
  In this mode the ``ndigits`` option has no effect.

Rounding always applies to the mantissa determined after identifying the
appropriate exponent for display based on ``exp_mode`` and ``exp_val``.
In some cases, the rounding results in a modification to the chosen
exponent.
This is taken into account before the final presentation.

>>> formatter = Formatter(
...     exp_mode="scientific",
...     round_mode="dec_place",
...     ndigits=2,
... )
>>> print(formatter(9.99))
9.99e+00
>>> formatter = Formatter(
...     exp_mode="scientific",
...     round_mode="dec_place",
...     ndigits=1,
... )
>>> print(formatter(9.99))
1.0e+01

By default, :mod:`sciform` uses
`"round-to-even" or "banker's rounding" <https://en.wikipedia.org/wiki/Rounding#Rounding_half_to_even>`_:

>>> formatter = Formatter(
...     round_mode="sig_fig",
...     ndigits=2,
... )
>>> print(formatter("2.45"))
2.4
>>> print(formatter("2.35"))
2.4

All :mod:`sciform` inputs are converted to :class:`Decimal` as the first step
for formatting before determining the mantissa and exponent and applying the
rounding algorithm.
This conversion can sometimes have surprising effects for rounding.
See :ref:`dec_and_float` for more details.

Note that for value/uncertainty formatting, if the uncertainty is finite and
non-zero, the rounding is applied to the uncertainty first then the value is
rounded to the same decimal place (as long as it is finite).

Significant Figures
-------------------

Significant figure rounding is selected by setting ``round_mode="sig_fig"`` and
``ndigits`` equal to a positive integer (zero excluded). In this mode, After the
exponent is first calculated, the digits place for the most-significant digit of
the mantissa is identified.
Then the mantissa is rounded to the specified number of significant figures
below that digits place.
E.g. for ``12345.678`` the most-significant digit appears in the
ten-thousands, or 10\ :sup:`4`, place.
To express this number to 4-significant digits means we should round it
to the tens, or 10\ :sup:`1`, place resulting in ``12350``.

>>> formatter = Formatter(
...     exp_mode="engineering",
...     round_mode="sig_fig",
...     ndigits=4,
... )
>>> print(formatter(12345.678))
12.35e+03

Note that 1001 rounded to 1, 2, or 3 significant figures results in
1000.
This demonstrates that we can't determine how many significant figures
a number was rounded to (or "how many significant figures a number has")
just by looking at the resulting string.

Digits-Past-the-Decimal Place
-----------------------------

Decimal place, or digits-past-the-decimal, rounding is selected by setting
``round_mode="dec_place"`` and ``ndigits`` equal to any integer.
In this mode ``ndigits`` specifies the decimal place to which the mantissa will
be rounded.
The convention for ``ndigits`` is the same as that for the built-in
`round function <https://docs.python.org/3/library/functions.html#round>`_.
E.g. ``ndigits=2`` means to round to two digits past the decimal place,
the hundredths or 10\ :sup:`-2` place, so that ``12.987`` would be
rounded to ``12.99``.

>>> formatter = Formatter(exp_mode="engineering", round_mode="dec_place", ndigits=4)
>>> print(formatter(12345.678))
12.3457e+03

Unlike the built in number formatting, it is possible for ``ndigits <= 0``:

>>> formatter = Formatter(
...     exp_mode="fixed_point",
...     round_mode="dec_place",
...     ndigits=-2,
... )
>>> print(formatter(12345.678))
12300

All Digits
----------

"All" digits rounding is selected by setting ``round_mode="all"``.
In this case, the ``ndigits`` option is ignored.
This mode attempts to display the input digits with full precision.
What exactly "full precision" means depends on the type of the input.
:class:`int`, :class:`str` and :class:`Decimal` inputs are converted to
:class:`Decimal` as the first step for formatting.
For these inputs the number of digits shown in ``"all"`` mode will be the
smaller of the number of significant digits in the number or the
:mod:`decimal` module precision (default 28).

:class:`float` inputs are first converted to :class:`str` before being converted
to :class:`Decimal`.
The string conversion converts the float into the shortest string representation
that will round trip to the same value as the input float.
For the 64-bit floats used in python this will be at most 17 digits, but it is
typically many fewer digits.
Unless the :mod:`decimal` module precision is decreased below 17 digits, then
the result of ``"all"`` rounding will print the same digits as present in the
string representation of the input :class:`float`.

>>> from decimal import Decimal
>>> formatter = Formatter(exp_mode="scientific", round_mode="all")
>>> float_num = 1/9
>>> dec_num = Decimal(float_num).normalize()
>>> print(float_num)
0.1111111111111111
>>> print(formatter(float_num))
1.111111111111111e-01
>>> print(dec_num)
0.1111111111111111049432054187
>>> print(formatter(dec_num))
1.111111111111111049432054187e-01

PDG Significant Figures
-----------------------

The PDG rounding is selected by setting ``round_mode="pdg"``.
In this case, the ``ndigits`` option is ignored.

Typically value/uncertainty pairs are formatted with one or two
significant figures displayed for the uncertainty.
The Particle Data Group has
`published an algorithm <https://pdg.lbl.gov/2010/reviews/rpp2010-rev-rpp-intro.pdf>`_
for deciding when to
display uncertainty with one versus two significant figures.
:mod:`sciform` can apply the PDG rounding algorithm either to value/uncertainty
pairs or to values alone.
The algorithm is as follows:

* Determine the three most significant digits of the number (without rounding).
  E.g. if the number is 0.004857 then these digits would be 485.
  Call 485 the scaled number.
* If the scaled number is between 100 and 354 (inclusive) then the
  number is rounded and displayed to one digit below its most
  significant digit.
  This means it will have two significant digit.
  E.g. if the uncertainty is 3.03 then it will appear as as 3.0
* If the scaled number is between 355 and 949 (inclusive) then the number is
  rounded and displayed to the same digit as the most significant digit.
  This means it will have one significant digit.
  E.g. if the uncertainty is 0.76932 then it will appear as 0.8
* If the scaled number is between 950 and 999 (inclusive) then the number is
  rounded and displayed to the same digit as the most significant digit.
  But 950 and above will always be rounded to 1000 if we round to the
  hundreds place.
  This means there will be two significant digits.
  E.g. if the number is 0.0099 then it will be displayed as 0.010.

The rationale for this algorithm is that it uses more significant digits in the
bottom section of an order-of-magnitude range where the fractional error
due to rounding is larger, but it saves ink in the upper section of an
order-of-magnitude range where the fractional error is not as large.
For a more thorough discussion see
`Significant digit 354 rule from Particle Data Group <https://stats.stackexchange.com/q/100502/260369>`_.

>>> formatter = Formatter(
...     round_mode="pdg",
... )
>>> print(formatter(0.0123))
0.012
>>> print(formatter(0.0483))
0.05
>>> print(formatter(0.0997))
0.10

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

>>> formatter = Formatter(upper_separator=",")
>>> print(formatter(12345678.987))
12,345,678.987

>>> formatter = Formatter(
...     upper_separator=" ",
...     decimal_separator=",",
...     lower_separator="_",
... )
>>> print(formatter(1234567.7654321))
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

>>> formatter = Formatter(sign_mode="-")
>>> print(formatter(42))
42
>>> formatter = Formatter(sign_mode="+")
>>> print(formatter(42))
+42
>>> formatter = Formatter(sign_mode=" ")
>>> print(formatter(42))
 42

Note that both :class:`float` ``nan`` and :class:`float` ``0`` have sign
bits which may be positive or negative.
:mod:`sciform` always ignores these sign bits and never puts a ``+`` or
``-`` symbol in front of either ``nan`` or ``0``.
In ``"+"`` or ``" "`` sign modes ``nan`` and ``0`` are always preceded
by a space.
The sign symbol for ``±inf`` is resolved the same as for
finite numbers.

>>> formatter = Formatter(sign_mode="-")
>>> print(formatter(float("-0")))
0
>>> print(formatter(float("-nan")))
nan
>>> print(formatter(float("+inf")))
inf
>>> formatter = Formatter(sign_mode="+")
>>> print(formatter(float("+0")))
 0
>>> print(formatter(float("+nan")))
 nan
>>> print(formatter(float("+inf")))
+inf
>>> formatter = Formatter(sign_mode=" ")
>>> print(formatter(float("-0")))
 0
>>> print(formatter(float("-nan")))
 nan
>>> print(formatter(float("-inf")))
-inf

Capitalization
==============

The capitalization of the exponent character can be controlled

>>> formatter = Formatter(exp_mode="scientific", capitalize=True)
>>> print(formatter(42))
4.2E+01
>>> formatter = Formatter(exp_mode="binary", capitalize=True)
>>> print(formatter(1024))
1B+10

The ``capitalize`` flag also controls the capitalization of ``nan`` and
``inf`` formatting:

>>> print(formatter(float("nan")))
NAN
>>> print(formatter(float("-inf")))
-INF

.. _left_padding:

Left Padding
============

The :ref:`rounding` options described above can be used to control how
many digits to the right of either the most-significant digit or the
decimal point are displayed.
It is also possible, using left padding options, to add digits to the
left of the most-significant digit.
The ``left_pad_char`` option can be used to select either whitespaces
``' '`` or zeros ``'0'`` as pad characters.
The ``left_pad_dec_place`` option is used to indicate to which decimal
place pad characters should be added.
E.g. ``left_pad_dec_place=4`` indicates pad characters should be
added up to the 10\ :sup:`4` (ten-thousands) decimal place.

>>> formatter = Formatter(left_pad_char="0", left_pad_dec_place=4)
>>> print(formatter(42))
00042

.. _superscript:

Superscript Exponent Format
===========================

The ``superscript`` option can be chosen to present exponents in
superscript notation as opposed to e.g. ``e+02`` notation.

>>> formatter = Formatter(exp_mode="scientific", superscript=True)
>>> print(formatter(789))
7.89×10²

Include Exponent on nan and inf
===============================

Python supports ``'nan'``, ``'inf'``, and
``'-inf'`` numbers which are simply formatted to ``'nan'``, ``'inf'``,
and ``'-inf'`` or ``'NAN'``, ``'INF'``, and ``'-INF'``, respectively,
depending on ``capitalize``.
However, if ``nan_inf_exp=True`` (default ``False``), then, for
scientific, percent, engineering, and binary exponent modes, these will
instead be formatted as, e.g. ``'(nan)e+00'``.

>>> formatter = Formatter(
...     exp_mode="scientific",
...     nan_inf_exp=False,
...     capitalize=True,
... )
>>> print(formatter(float("-inf")))
-INF
>>> formatter = Formatter(
...     exp_mode="scientific",
...     nan_inf_exp=True,
...     capitalize=True,
... )
>>> print(formatter(float("-inf")))
(-INF)E+00
>>> formatter = Formatter(
...     exp_mode="percent",
...     nan_inf_exp=False,
...     capitalize=True,
... )
>>> print(formatter(float("-inf")))
-INF
>>> formatter = Formatter(
...     exp_mode="percent",
...     nan_inf_exp=True,
...     capitalize=True,
... )
>>> print(formatter(float("-inf")))
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

>>> formatter = Formatter()
>>> print(formatter(123.456, 0.789))
123.456 ± 0.789

.. _paren_uncertainty:

Parentheses Uncertainty
-----------------------

The
`BIPM Guide Section 7.2.2 <https://www.bipm.org/documents/20126/2071204/JCGM_100_2008_E.pdf/cb0ef43f-baa5-11cf-3f85-4dcd86f77bd6#page=37>`_
Provides three example value/uncertainty formats::

  100,021 47 ± 0,000 35
  100,021 47(0,000 35)
  100,021 47(35)

In the first example the value and uncertainty are shown as regular
numbers separated by a ``±``.
In the second example the uncertainty is shown after the value inside
parentheses.
The third example is like the second but all leading zeros and separator
characters have been removed.
In the third example it is clear to see exactly which digits of the
value are uncertain and by how much.

:mod:`sciform` provides the ability to realize all three of these
formatting strategies by using the ``paren_uncertainty`` and
``paren_uncertainty_trim`` options.

>>> from sciform import Formatter, GlobalOptionsContext
>>> value = 100.02147
>>> uncertainty = 0.00035
>>>
>>> with GlobalOptionsContext(decimal_separator=",", lower_separator=" "):
...     formatter = Formatter(
...         paren_uncertainty=False,
...     )
...     print(formatter(value, uncertainty))
...
...     formatter = Formatter(
...         paren_uncertainty=True,
...         paren_uncertainty_trim=False,
...     )
...     print(formatter(value, uncertainty))
...
...     formatter = Formatter(
...         paren_uncertainty=True,
...         paren_uncertainty_trim=True,
...     )
...     print(formatter(value, uncertainty))
100,021 47 ± 0,000 35
100,021 47(0,000 35)
100,021 47(35)

``paren_uncertainty_trim`` modifies the uncertainty by eliminating any leading
zeros and all separators unless there are significant digits above and below
the decimal separator, in which case that separator is kept.

>>> value = 100.0215
>>> uncertainty = 1.2345
>>> formatter = Formatter(
...     paren_uncertainty=True,
...     paren_uncertainty_trim=False,
...     decimal_separator=",",
...     lower_separator=" ",
... )
>>> print(formatter(value, uncertainty))
100,021 5(1,234 5)
>>> formatter = Formatter(
...     paren_uncertainty=True,
...     paren_uncertainty_trim=True,
...     decimal_separator=",",
...     lower_separator=" ",
... )
>>> print(formatter(value, uncertainty))
100,021 5(1,2345)

Note that the BIPM guide does not show any examples where the digits of
the uncertainty span either a grouping or decimal separator.
This means there is no official guidance about

* Should ``18.4 ± 2.1`` be formatted as ``18.4(2.1)`` or ``18.4(21)``.
* Should ``18.456 4 ± 0.002 1`` be formatted as ``18.456 4(2 1)`` or
  ``18.456 4(21)``.

:mod:`sciform` formats the trimmed parentheses uncertainty mode by
never removing the decimal separator unless it is to the left of the
most significant digit of the uncertainty but to always remove all
upper and lower separator characters.
By contrast, the `siunitx <https://ctan.org/pkg/siunitx?lang=en>`_
LaTeX package always removes all separators characters, including the
decimal.

The default global options have ``paren_uncertainty=False`` and
``paren_uncertainty_trim=True``.

Here are examples demonstrating ``paren_uncertainty`` behavior when exponent
strings are present.

>>> formatter = Formatter(
...     exp_mode="engineering",
...     exp_format="standard",
...     paren_uncertainty=True,
... )
>>> print(formatter(523.4e-3, 1.2e-3))
523.4(1.2)e-03
>>> formatter = Formatter(
...     exp_mode="engineering",
...     exp_format="prefix",
...     paren_uncertainty=True,
... )
>>> print(formatter(523.4e-3, 1.2e-3))
523.4(1.2) m

The latter example is consistent with BIPM examples.

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

>>> formatter = Formatter(
...     left_pad_char="0",
...     left_pad_dec_place=2,
...     left_pad_matching=False,
... )
>>> print(formatter(12345, 1.23))
12345.00 ± 001.23
>>> formatter = Formatter(
...     left_pad_char="0",
...     left_pad_dec_place=2,
...     left_pad_matching=True,
... )
>>> print(formatter(12345, 1.23))
12345.00 ± 00001.23

Plus/Minus Symbol Whitespace
----------------------------

Depending on the value of ``pm_whitespace``, the ``±`` symbol will either have
one full space on either side of it or not.

>>> formatter = Formatter(pm_whitespace=True)
>>> print(formatter(2, 1))
2 ± 1
>>> formatter = Formatter(pm_whitespace=False)
>>> print(formatter(2, 1))
2±1
