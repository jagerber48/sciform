.. image:: https://www.repostatus.org/badges/latest/wip.svg
     :target: https://www.repostatus.org/#wip
     :alt: Project Status: WIP – Initial development is in progress, but there has not yet been a stable, usable release suitable for the public.
.. image:: https://tinyurl.com/y22nb8up
     :target: https://github.com/pyOpenSci/software-review/issues/121
     :alt: pyOpenSci
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
.. image:: https://zenodo.org/badge/645611310.svg
     :target: https://zenodo.org/doi/10.5281/zenodo.10645272
     :alt: Zenodo


#######
sciform
#######

|  **Repository:** `<https://github.com/jagerber48/sciform>`_
|  **Documentation:** `<https://sciform.readthedocs.io/en/stable/>`_
|  **PyPi:** `<https://pypi.org/project/sciform/>`_

We would greatly appreciate you taking the time to fill out the
`User Experience Survey <https://forms.gle/TkkKgywYyEMKu9U37>`_ to help
improve ``sciform``.

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

Install the latest stable version from
`PyPi <https://pypi.org/project/sciform/>`_ with::

   python -m pip install sciform

or install the latest development version from
`GitHub <https://github.com/jagerber48/sciform>`_ with::

   python -m pip install git+https://github.com/jagerber48/sciform.git

``sciform`` is compatible with Python versions >=3.9.

=====
Usage
=====

Here we provide a few key usage examples.
For many more details see
`Usage <https://sciform.readthedocs.io/en/stable/usage.html>`_.

``sciform`` provides a wide variety of formatting options which can be
controlled when constructing ``Formatter`` objects which are then used
to format numbers into strings according to the selected options.

>>> from sciform import Formatter
>>> formatter = Formatter(
...     round_mode="dec_place", ndigits=6, upper_separator=" ", lower_separator=" "
... )
>>> print(formatter(51413.14159265359))
51 413.141 593
>>> formatter = Formatter(round_mode="sig_fig", ndigits=4, exp_mode="engineering")
>>> print(formatter(123456.78))
123.5e+03

Users can also format numbers by constructing ``SciNum`` objects and
using string formatting to format the ``SciNum`` instances according
to a custom FSML.

>>> from sciform import SciNum
>>> num = SciNum(12345)
>>> print(f"{num:!2f}")
12000
>>> print(f"{num:!2r}")
12e+03

In addition to formatting individual numbers, ``sciform`` can be used
to format pairs of numbers as value/uncertainty pairs.
This can be done by passing two numbers into a ``Formatter`` call or by
using the ``SciNum`` object.

>>> formatter = Formatter(ndigits=2, upper_separator=" ", lower_separator=" ")
>>> print(formatter(123456.654321, 0.00345))
123 456.654 3 ± 0.003 4
>>> formatter = Formatter(ndigits=4, exp_mode="engineering")
>>> print(formatter(123456.654321, 0.00345))
(123.456654321 ± 0.000003450)e+03

>>> num = SciNum(123456.654321, 0.00345)
>>> print(f"{num:!2f}")
123456.6543 ± 0.0034
>>> print(f"{num:!2f()}")
123456.6543(34)

Note that the above examples demonstrate that ``sciform`` uses
`"round-to-even" <https://en.wikipedia.org/wiki/Rounding#Rounding_half_to_even>`_
rounding.

>>> print(f"{SciNum(865):!2}")
860
>>> print(f"{SciNum(875):!2}")
880

See `Formatting Options <https://sciform.readthedocs.io/en/stable/options.html>`_,
`Format Specification Mini-Language <https://sciform.readthedocs.io/en/stable/fsml.html>`_
for more details and
`Examples <https://sciform.readthedocs.io/en/stable/examples.html>`_ for
more examples.

==============
Project Status
==============

``sciform`` adheres to `semantic versioning <https://semver.org/>`_.
The major version for ``sciform`` is still ``0`` indicating that
``sciform`` is still in the development stage which means there may be
backwards-incompatible changes to the interface (e.g. function or object
behaviors and names) without a corresponding major version bump.
All changes are announced after new releases in the
`changelog <https://sciform.readthedocs.io/en/stable/project.html#changelog>`_.
Backwards incompatible changes are indicated with the **[BREAKING]**
flag.

We are very excited to get your feedback to help stabilize the interface
and make ``sciform`` a more useful tool.
You can provide your feedback on your experience with ``sciform`` by
filling out
`the user experience survey <https://forms.gle/TkkKgywYyEMKu9U37>`_.
Now is a great time to share your ``sciform`` ideas or issues by
opening a
`discussion <https://github.com/jagerber48/sciform/discussions>`_ or
`issue <https://github.com/jagerber48/sciform/issues>`_.
If you would like to contribute to ``sciform`` then please see
`How to Contribute <https://sciform.readthedocs.io/en/stable/project.html#how-to-contribute>`_.

``sciform`` has undergone
`peer review <https://www.pyopensci.org/about-peer-review/index.html>`_
by the `PyOpenSci <https://www.pyopensci.org/>`_ community and been
accepted into the PyOpenSci ecosystem.
You can view the review
`here <https://github.com/pyOpenSci/software-submission/issues/121>`_.

================
Acknowledgements
================

``sciform`` was heavily motivated by the prefix formatting provided in
the `prefixed <https://github.com/Rockhopper-Technologies/prefixed>`_
package and the value ± uncertainty formatting in the
`uncertainties <https://github.com/lebigot/uncertainties>`_ package.
