Usage
#####

Formatting
==========

.. module:: sciform
   :noindex:

:mod:`sciform` provides two primary methods for formatting floats into
scientific formatting strings.
The first is via the :class:`Formatter` object and the second is
using string formatting and the
:ref:`Format Specification Mini Language (FSML) <fsml>` with the
:class:`sfloat` object.

Formatter
---------

The :class:`Formatter` object is initialized with user-selected
formatting options and then used to format floats. Additional details
about formatting options at :ref:`formatting_options`.

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

sfloat
------

The :mod:`sciform` :ref:`FSML <fsml>` is accessed via the
:class:`sfloat` object.
Regular built-in floats are cast to :class:`sfloat` objects which can be
formatted using the :mod:`sciform` :ref:`FSML <fsml>`.

>>> from sciform import sfloat
>>> num = sfloat(123456)
>>> print(f'{num:_!2f}')
120_000

Global Configuration
====================

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

