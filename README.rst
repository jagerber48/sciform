#######
sciform
#######

|  **Repository:** `<https://github.com/jagerber48/sciform>`_
|  **Documentation:** `<https://sciform.readthedocs.io/en/stable/>`_
|  **PyPi:** `<https://pypi.org/project/sciform/>`_

========
Overview
========

``sciform`` is used to convert python numbers into strings according to
a variety of user-selected scientific formatting options including
decimal, binary, fixed-point, scientific and engineering formats.
Where possible, formatting follows documented standards such as those
published by `BIPM <https://www.bipm.org/en/>`_ or
`IEC <https://iec.ch/homepage>`_.
``sciform`` provides certain options, such as engineering notation,
well-controlled significant figure rounding, and separator customization
which are not provided by the python built-in
`format specification mini-language (FSML) <https://docs.python.org/3/library/string.html#format-specification-mini-language>`_.

============
Installation
============

Install with pip::

   pip install sciform

==================
Under Construction
==================

The ``sciform`` package is still in early stages of development.
The API is not stable.
Class and function names and usages have undergone changes and may
continue to change until version ``1.0.0`` is released.
API changes will be announced after new releases in the
`changelog <https://sciform.readthedocs.io/en/stable/project.html#changelog>`_.
If you have an idea or opinion about how ``sciform`` should be designed,
now is a great to
`post a discussion topic <https://github.com/jagerber48/sciform/discussions>`_
about it!

=====
Usage
=====

``sciform`` provides two primary methods for formatting numbers into
scientific formatted strings.
The first is via the ``Formatter`` object and the second is using string
formatting and the custom FSML with the ``SciNum`` object.

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

>>> from sciform import SciNum
>>> num = SciNum(123456)
>>> print(f'{num:_!2f}')
120_000

``sciform`` can also be used to format pairs of value/uncertainty
numbers using the ``Formatter`` or ``SciNumUnc`` objects.

>>> sform = Formatter(precision=2,
...                   upper_separator=GroupingSeparator.SPACE,
...                   lower_separator=GroupingSeparator.SPACE)
>>> print(sform(123456.654321, 0.0034))
123 456.654 3 +/- 0.003 4
>>> sform = Formatter(precision=4,
...                   exp_mode=ExpMode.ENGINEERING)
>>> print(sform(123456.654321, 0.0034))
(123.456654321 +/- 0.000003400)e+03

>>> from sciform import SciNumUnc
>>> num = SciNumUnc(123456.654321, 0.0034)
>>> print(f'{num:_!2f}')
123_456.6543 +/- 0.0034


================
Acknowledgements
================

``sciform`` was heavily motivated by the prefix formatting provided in
the `prefixed <https://github.com/Rockhopper-Technologies/prefixed>`_
package and the value +/- uncertainty formatting in the
`uncertainties <https://github.com/lebigot/uncertainties>`_ package.
