.. image:: https://www.repostatus.org/badges/latest/wip.svg
     :target: https://www.repostatus.org/#wip
     :alt: Project Status: WIP – Initial development is in progress, but there has not yet been a stable, usable release suitable for the public.
.. image:: https://img.shields.io/readthedocs/sciform?logo=readthedocs&link=https%3A%2F%2Fsciform.readthedocs.io%2Fen%2Fstable%2F
     :target: https://sciform.readthedocs.io/en/stable/
     :alt: Read the Docs
.. image:: https://img.shields.io/pypi/v/sciform?logo=pypi
     :target: https://pypi.org/project/sciform/
     :alt: PyPI - Version
.. image:: https://img.shields.io/pypi/pyversions/sciform?logo=python
     :target: https://pypi.org/project/sciform/
     :alt: PyPI - Python Version
.. image:: https://img.shields.io/codecov/c/github/jagerber48/sciform?logo=codecov
     :target: https://codecov.io/gh/jagerber48/sciform
     :alt: Codecov
.. image:: https://img.shields.io/github/actions/workflow/status/jagerber48/sciform/python-package.yml?logo=github%20actions
     :target: https://github.com/jagerber48/sciform/blob/main/.github/workflows/python-package.yml
     :alt: GitHub Workflow Status


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

``sciform`` is compatible with Python versions >=3.9.

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
now is a great time to
`post a discussion topic <https://github.com/jagerber48/sciform/discussions>`_
about it!

=====
Usage
=====

``sciform`` provides a wide variety of formatting options which can be
controlled when constructing ``Formatter`` objects which are then used
to format numbers into strings according to the selected options.

>>> from sciform import Formatter
>>> sform = Formatter(
...             round_mode='dec_place',
...             ndigits=6,
...             upper_separator=' ',
...             lower_separator=' ')
>>> print(sform(51413.14159265359))
51 413.141 593
>>> sform = Formatter(
...             round_mode='sig_fig',
...             ndigits=4,
...             exp_mode='engineering')
>>> print(sform(123456.78))
123.5e+03

Users can also format numbers by constructing ``SciNum`` objects and
using string formatting to format the ``SciNum`` instances according
to a custom FSML.

>>> from sciform import SciNum
>>> num = SciNum(123456)
>>> print(f'{num:_!2f}')
120_000

In addition to formatting individual numbers, ``sciform`` can be used
to format pairs of numbers as value/uncertainty pairs.
This can be done by passing two numbers into a ``Formatter`` call or by
using the ``SciNumUnc`` object.

>>> sform = Formatter(
...             ndigits=2,
...             upper_separator=' ',
...             lower_separator=' ')
>>> print(sform(123456.654321, 0.0034))
123 456.654 3 ± 0.003 4
>>> sform = Formatter(
...             ndigits=4,
...             exp_mode='engineering')
>>> print(sform(123456.654321, 0.0034))
(123.456654321 ± 0.000003400)e+03

>>> from sciform import SciNumUnc
>>> num = SciNumUnc(123456.654321, 0.0034)
>>> print(f'{num:_!2f}')
123_456.6543 ± 0.0034
>>> print(f'{num:_!2f()}')
123_456.6543(34)


================
Acknowledgements
================

``sciform`` was heavily motivated by the prefix formatting provided in
the `prefixed <https://github.com/Rockhopper-Technologies/prefixed>`_
package and the value ± uncertainty formatting in the
`uncertainties <https://github.com/lebigot/uncertainties>`_ package.
