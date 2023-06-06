Usage
=====

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