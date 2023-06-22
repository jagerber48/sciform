sciform
#######

|  **Repository:** `<https://github.com/jagerber48/sciform>`_
|  **Documentation:** `<https://sciform.readthedocs.io/en/stable/>`_
|  **PyPi:** `<https://pypi.org/project/sciform/>`_

Overview
--------

``sciform`` is used to convert python float objects into strings
according to a variety of user-selected scientific formatting options
including decimal, binary, fixed-point, scientific and engineering
formats.
Where possible, formatting follows documented standards such as those
published by `BIPM <https://www.bipm.org/en/>`_ or
`IEC <https://iec.ch/homepage>`_.
``sciform`` provides certain options, such as engineering notation,
well-controlled significant figure rounding, and separator customization
which are not provided by the python built-in
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

>>> from sciform import Formatter, RoundMode, GroupingSeparator, ExpMode
>>> sform = Formatter(round_mode=RoundMode.PREC,
...                   precision=6,
...                   upper_separator=GroupingSeparator.SPACE,
...                   lower_separator=GroupingSeparator.SPACE)
>>> print(sform(51413.14159265359))
51 413.141 593
>>> sform = Formatter(round_mode=RoundMode.SIG_FIG,
...                   precision=4,
...                   exp_mode=ExpMode.ENGINEERING)
>>> print(sform(123456.78))
123.5e+03

>>> from sciform import sfloat
>>> num = sfloat(123456)
>>> print(f'{num:_!2f}')
120_000

``sciform`` can also be used to format pairs of value/uncertainty floats
using the ``Formatter`` or ``vufloat`` objects.

>>> sform = Formatter(round_mode=RoundMode.SIG_FIG,
...                   precision=2,
...                   upper_separator=GroupingSeparator.SPACE,
...                   lower_separator=GroupingSeparator.SPACE)
>>> print(sform(123456.654321, 0.0034))
123 456.654 3 +/- 0.003 4
>>> sform = Formatter(round_mode=RoundMode.SIG_FIG,
...                   precision=4,
...                   exp_mode=ExpMode.ENGINEERING)
>>> print(sform(123456.654321, 0.0034))
(123.456654321 +/- 0.000003400)e+03

>>> from sciform import vufloat
>>> num = vufloat(123456.654321, 0.0034)
>>> print(f'{num:_!2f}')
123_456.6543 +/- 0.0034blah


================
Acknowledgements
================

``sciform`` was heavily motivated by the prefix formatting provided in
the `prefixed <https://github.com/Rockhopper-Technologies/prefixed>`_
package and the value +/- uncertainty formatting in the
`uncertainties <https://github.com/lebigot/uncertainties>`_ package.
