Usage
#####

.. module:: sciform
   :noindex:

Formatting
==========

:mod:`sciform` provides two primary methods for formatting numbers into
scientific formatted strings.
The first is via the :class:`Formatter` object and the second is
using string formatting and the
:ref:`Format Specification Mini-Language (FSML) <fsml>` with the
:class:`SciNum` object.

Formatter
---------

The :class:`Formatter` object is initialized and configured using a
number of formatting options described in :ref:`formatting_options`.
The :class:`Formatter` object is then called with a number and returns
a corresponding formatted string.

>>> from sciform import Formatter
>>> sform = Formatter(
...     round_mode="dec_place", ndigits=6, upper_separator=" ", lower_separator=" "
... )
>>> print(sform(51413.14159265359))
51 413.141 593
>>> sform = Formatter(round_mode="sig_fig", ndigits=4, exp_mode="engineering")
>>> print(sform(123456.78))
123.5e+03

It is not necessary to provide input for all options.
At format time, any un-populated options will be populated with the
corresponding options from the global default options.
See :ref:`global_config` for details about how to view and modify the
global default options.

SciNum
------

The :mod:`sciform` :ref:`FSML <fsml>` can be accessed via the
:class:`SciNum` object.
Python numbers specified as :class:`string`, :class:`float`, or
:class:`Decimal` objects are cast to :class:`SciNum` objects which can
be formatted using the :mod:`sciform` :ref:`FSML <fsml>`.

>>> from sciform import SciNum
>>> num = SciNum(123456)
>>> print(f"{num:!2f}")
120000

Value/Uncertainty Formatting
----------------------------

One of the most important use cases for scientific formatting is
formatting a value together with its specified uncertainty, e.g.
``84.3 ± 0.2``.
:mod:`sciform` provides the ability to format pairs of numbers into
value/uncertainty strings.
:mod:`sciform` attempts to follow
`BIPM <https://www.bipm.org/documents/20126/2071204/JCGM_100_2008_E.pdf/cb0ef43f-baa5-11cf-3f85-4dcd86f77bd6>`_
or `NIST <https://www.nist.gov/pml/nist-technical-note-1297>`_
recommendations for conventions when possible.

Value/uncertainty pairs can be formatted either by passing two numbers
into a :class:`Formatter`, configured with the corresponding
:ref:`formatting_options` and :ref:`val_unc_formatting_options`, or by
using the :class:`SciNum` object.

>>> val = 84.3
>>> unc = 0.2
>>> sform = Formatter(ndigits=2)
>>> print(sform(val, unc))
84.30 ± 0.20
>>> from sciform import SciNum
>>> val_unc = SciNum(val, unc)
>>> print(f"{val_unc:!2}")
84.30 ± 0.20

Value/uncertainty pairs can also be formatted using a parentheses
notation in which the uncertainty is displayed in parentheses following
the value.

>>> print(f"{val_unc:!2()}")
84.30(20)

Value/uncertainty pairs are formatted according to the following
algorithm:

#. Rounding is always performed using significant figure rounding
   applied to the uncertainty.
   See :ref:`rounding` for more details about possible rounding options.
#. The value is rounded to the decimal place corresponding to the least
   significant digit of the rounded uncertainty.
#. The value for the exponent is resolved by using ``exp_mode`` and
   ``exp_val`` with the larger of the value or uncertainty.
#. The value and uncertainty mantissas are determined according to the
   value of the exponent determined in the previous step.
#. The value and uncertainty mantissas are formatted together with the
   exponent according to other user-selected display options.

.. _global_config:

Global Configuration
====================

It is possible to modify the global default configuration for
:mod:`sciform` to avoid repetition of verbose configuration options or
format specification strings.
When the user creates a :class:`Formatter` object or formats a string
using the :ref:`FSML <fsml>`, they typically do not specify settings for
all available options.
In these cases, the unspecified options resolve their values from the
global default settings at format time.

The global default settings can be viewed using
:func:`print_global_defaults()` (the settings shown here are the
package default settings):

>>> from sciform import print_global_defaults
>>> print_global_defaults()
{'exp_mode': 'fixed_point',
 'exp_val': AutoExpVal,
 'round_mode': 'sig_fig',
 'ndigits': AutoDigits,
 'upper_separator': '',
 'decimal_separator': '.',
 'lower_separator': '',
 'sign_mode': '-',
 'fill_char': ' ',
 'left_pad_dec_place': 0,
 'exp_format': 'standard',
 'extra_si_prefixes': {},
 'extra_iec_prefixes': {},
 'extra_parts_per_forms': {},
 'capitalize': False,
 'superscript': False,
 'latex': False,
 'nan_inf_exp': False,
 'paren_uncertainty': False,
 'pdg_sig_figs': False,
 'left_pad_matching': False,
 'paren_uncertainty_separators': True,
 'pm_whitespace': True}

The global default settings can be modified using the
:func:`set_global_defaults()` function.
Any options passed will overwrite the corresponding options in the
current global default settings and any unfilled options will remain
unchanged.

>>> from sciform import set_global_defaults
>>> set_global_defaults(
...     fill_char="0",
...     exp_mode="engineering_shifted",
...     ndigits=4,
...     decimal_separator=",",
... )
>>> print_global_defaults()
{'exp_mode': 'engineering_shifted',
 'exp_val': AutoExpVal,
 'round_mode': 'sig_fig',
 'ndigits': 4,
 'upper_separator': '',
 'decimal_separator': ',',
 'lower_separator': '',
 'sign_mode': '-',
 'fill_char': '0',
 'left_pad_dec_place': 0,
 'exp_format': 'standard',
 'extra_si_prefixes': {},
 'extra_iec_prefixes': {},
 'extra_parts_per_forms': {},
 'capitalize': False,
 'superscript': False,
 'latex': False,
 'nan_inf_exp': False,
 'paren_uncertainty': False,
 'pdg_sig_figs': False,
 'left_pad_matching': False,
 'paren_uncertainty_separators': True,
 'pm_whitespace': True}

The global default settings can be reset to the :mod:`sciform` defaults
using :func:`reset_global_defaults`.

>>> from sciform import reset_global_defaults
>>> reset_global_defaults()

The global default settings can be temporarily modified using the
:class:`GlobalDefaultsContext` context manager.
The context manager is configured using the same options as
:class:`Formatter`.
Within the context of :class:`GlobalDefaultsContext` manager, the
global defaults take on the specified input settings, but when the
context is exited, the global default settings revert to their previous
values.

>>> from sciform import GlobalDefaultsContext, SciNum
>>> snum = SciNum(0.0123)
>>> print(f"{snum:.2ep}")
1.23e-02
>>> with GlobalDefaultsContext(add_c_prefix=True):
...     print(f"{snum:.2ep}")
...
1.23 c
>>> print(f"{snum:.2ep}")
1.23e-02

Note that the :ref:`FSML <fsml>` does not provide complete control over
all possible format options.
For example, there is no code in the :ref:`FSML <fsml>` for configuring
the ``pdg_sig_figs`` option.
If the user wishes to configure these options, but also use the
:ref:`FSML <fsml>`, then they must do so by modifying the global default
settings.

.. _dec_and_float:

Note on Decimals and Floats
===========================

Numerical data can be stored in Python
`float <https://docs.python.org/3/library/functions.html#float>`_
or
`Decimal <https://docs.python.org/3/library/decimal.html>`_ objects.
:class:`float` instances represent numbers using binary which means
they are often only approximations of the decimal numbers users have in
mind when they use :class:`float`.
By contrast, :class:`Decimal` objects store sequences of integers
representing the decimal digits of the represented numbers so,
:class:`Decimal` instances are, therefore, exact representations of
decimal numbers.

Both of these representations have finite precision which can cause
unexpected issues when manipulating numerical data.
However, in the :class:`Decimal` class, the main issue is that
numbers may be truncated if their precision exceeds the configured
:class:`Decimal` precision, but the rounding will be as expected.
That said, the precision used for :class:`Decimal` numbers can
easily be modified if necessary.
:class:`float` instances, unfortunately, may exhibit more surprising
behavior, as will be explained below.
For these reasons, the :mod:`sciform` module uses :class:`Decimal`
representations in its internal formatting algorithms.

Note, however, that :class:`Decimal` arithmetic operations are less
performant that :class:`float` operations.
So, unless very high precision is needed at all steps of the
calculation, the suggested workflow is to store and manipulate numerical
data as :class:`float` instances, and only convert to :class:`Decimal`,
or format using :mod:`sciform`, as the final step when numbers are being
displayed for human readers.

Float issues
------------

Here I would like to highlight some important facts and possible issues
with :class:`float` objects that users should be aware of if they are
concerned with the exact decimal representation of their numerical data.

* Python uses
  `double-precision floating-point format <https://en.wikipedia.org/wiki/Double-precision_floating-point_format>`_
  for its :class:`float`.
  In this format, a :class:`float` occupies 64 bits of memory: 52 bits
  for the mantissa, 11 bits for the exponent and 1 bit for the sign.
* Any decimal with 15 digits between about ``± 1.8e+308`` can be
  uniquely represented by a :class:`float`.
  However, two decimals with more than 15 digits may map to the same
  :class:`float`.
  For example,
  ``float(8.000000000000001) == float(8.000000000000002)`` returns
  ``True``.
  See `"Decimal Precision of Binary Floating Point Numbers" <https://www.exploringbinary.com/decimal-precision-of-binary-floating-point-numbers/>`_
  for more details.

* If any :class:`float` is converted to a decimal with at least 17
  digits then it will be converted back to the same :class:`float`.
  See `"The Shortest Decimal String that Round-Trips: Examples" <https://www.exploringbinary.com/the-shortest-decimal-string-that-round-trips-examples/>`_
  for more details.
  However, many :class:`float` instances can be "round-tripped" with
  far fewer digits.
  The :func:`__repr__` for the python :class:`float` class converts the
  :class:`float` to a string decimal representation with the minimum
  number of digits such that it round trips to the same :class:`float`.
  For example we can see the exact decimal representation of the
  :class:`float` which ``0.1`` is mapped to:
  ``print(Decimal(float(0.1)))`` gives
  ``"0.1000000000000000055511151231257827021181583404541015625"``.
  However ``print(float(0.1))`` just gives ``"0.1"``.
  That is,
  ``0.1000000000000000055511151231257827021181583404541015625`` and
  ``0.1`` map to the same :class:`float` but the :class:`float`
  :func:`__repr__()` algorithm presents us with the shorter (more
  readable) decimal representation.

The `python documentation <https://docs.python.org/3/tutorial/floatingpoint.html#tut-fp-issues>`_
goes into some detail about possible issues one might encounter when
working with :class:`float` instances.
Here I would like to highlight two specific issues.

#. **Rounding**.
   `Python's round() function <https://docs.python.org/3/library/functions.html#round>`_
   uses a `"round-to-even" or "banker's rounding" <https://en.wikipedia.org/wiki/Rounding#Rounding_half_to_even>`_
   strategy in which ties are rounded so the least significant digit
   after rounding is always even.
   This ensures data sets with uniformly distributed digits are not
   biased by rounding.
   Rounding of :class:`float` instances may have surprising results.
   Consider the decimal numbers ``0.0355`` and ``0.00355``.
   If we round these to two significant figures using a "round-to-even"
   strategy, we expect the results ``0.036`` and ``0.0036``
   respectively.
   However, if we try to perform this rounding for :class:`float` we get
   an unexpected result. We see that ``round(0.00355, 4)`` gives
   ``0.0036`` as expected but ``round(0.0355, 3)`` gives ``0.035``.
   We can see the issue by looking at the decimal representations of the
   corresponding :class:`float` instances.
   ``print(Decimal(0.0355))`` gives
   ``"0.035499999999999996835864379818303859792649745941162109375"``
   which indeed should round down to ``0.035`` while
   ``print(Decimal(0.00355))`` gives
   ``"0.003550000000000000204003480774872514302842319011688232421875"``
   which should round to ``0.0036``.
   So, we see that the rounding behavior for :class:`float` may depend on
   digits of the decimal representation of the :class:`float` which are
   beyond the minimum number of digits necessary for the :class:`float`
   to round trip and, thus, beyond the number of digits that will be
   displayed by default.
#. **Representation of numbers with high precision**.
   Conservatively, :class:`float` provides 15 digits of precision.
   That is, any two decimal numbers (within the :class:`float` range)
   with 15 or fewer digits of precision are guaranteed to correspond to
   unique :class:`float` instances.
   Decimal numbers with 16 digits or more of precision may not
   correspond to unique :class:`float` instances.
   It is rare, in scientific applications, that we require more than 15
   digits of precision, but in some cases we do.
   One example is precision frequency metrology, such as that
   involved in atomic clocks.
   The relative uncertainty of primary frequency standards is
   approaching one part in 10\ :sup:`-16`.
   This means that measured quantities may require up to 16 digits to
   display.
   Indeed, consider
   `Metrologia 55 (2018) 188–200 <https://iopscience.iop.org/article/10.1088/1681-7575/aaa302>`_.
   In Table 2 the :sup:`87` Rb ground-state hyperfine splitting is cited
   as ``6 834 682 610.904 312 6 Hz`` with 17 digits. Suppose the last
   digit was a ``5`` instead of a ``6``. Python :class:`float` cannot
   tell the difference:
   ``float(6834682610.9043126) == float(6834682610.9043125)`` returns
   ``True``.

How :mod:`sciform` Handles Decimals and Floats
----------------------------------------------

To support predictable rounding and the representation of high precision
numbers, :mod:`sciform` casts the numbers it is presenting to
:class:`Decimal` objects during its formatting algorithm.
Numbers are input into :mod:`sciform` either as the input to a
:class:`Formatter` or when instantiating a :class:`SciNum` object.
In all cases the input will typically be a :class:`Decimal`,
:class:`float`, :class:`str`, or :class:`int`.
:class:`Decimal`, :class:`str` and :class:`int` are unambiguously
converted to :class:`Decimal` objects.
For :class:`float` inputs, the values are first cast to :class:`str`
instances to get their shortest round-trippable decimal representations.
These shortest round-trippable strings are then converted into
:class:`Decimal` instances.
For high precision applications it is recommended that users provide
input to :mod:`sciform` either as :class:`str` or :class:`Decimal`.
