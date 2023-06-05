Usage
=====

``sciform`` provides two primary methods for formatting floats into
scientific formatting strings.
The first is via the ``sciform.Formatter`` object and the second is
using string formatting and the
:ref:`Format Specification Mini Language <fsml>` with the
``sciform.sfloat`` object.

Formatter
---------

:class:`~sciform.Formatter` object is initialized with user-selected
formatting options and then used to format floats:

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

The ``kwargs`` passed into the :class:`~sciform.Formatter` constructor
are used to generate a :class:`~sciform.FormatOptions` object which
controls the string formatting.


The ``sciform`` FSML is accessed via the `sfloat` object.
Regular built-in floats are cast to ``sfloat`` objects which can be
formatted using the ``sciform`` FSML.

>>> from sciform import sfloat
>>> num = sfloat(123456)
>>> print(f'{num:_!2f}')
120_000