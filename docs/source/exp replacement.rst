.. _exp_replacements:

Supported Exponent Replacements
###############################

:mod:`sciform` offers exponent replacement modes which provide
translations between exponent strings and conventional alphabetic
symbol representations.
For decimal exponents in engineering formats, SI prefix translations are
available according to the
`SI prefixes <https://www.nist.gov/pml/owm/metric-si-prefixes>`_.
It is also possible to convert decimal exponents into
`parts-per notation <https://en.wikipedia.org/wiki/Parts-per_notation>`_.
For binary formats, the IEC prefix translations are available matched to
integer multiples of 10 according to the
`IEC prefixes <https://physics.nist.gov/cuu/Units/binary.html>`_.

SI Prefixes
-----------

.. list-table:: SI Prefixes
   :widths: 15, 15, 15
   :header-rows: 1

   * - Exponent Value
     - Prefix Name
     - Prefix
   * - 10\ :sup:`+30`
     - Quetta
     - Q
   * - 10\ :sup:`+27`
     - Ronna
     - R
   * - 10\ :sup:`+24`
     - Yotta
     - Y
   * - 10\ :sup:`+21`
     - Zetta
     - Z
   * - 10\ :sup:`+18`
     - Exa
     - E
   * - 10\ :sup:`+15`
     - Peta
     - P
   * - 10\ :sup:`+12`
     - Tera
     - T
   * - 10\ :sup:`+9`
     - Giga
     - G
   * - 10\ :sup:`+6`
     - Mega
     - M
   * - 10\ :sup:`+3`
     - kilo
     - k
   * - 10\ :sup:`-3`
     - milli
     - m
   * - 10\ :sup:`-6`
     - micro
     - µ
   * - 10\ :sup:`-9`
     - nano
     - n
   * - 10\ :sup:`-12`
     - pico
     - p
   * - 10\ :sup:`-15`
     - femto
     - f
   * - 10\ :sup:`-18`
     - atto
     - a
   * - 10\ :sup:`-21`
     - zepto
     - z
   * - 10\ :sup:`-24`
     - yocto
     - y
   * - 10\ :sup:`-27`
     - ronto
     - r
   * - 10\ :sup:`-30`
     - quecto
     - q

Extra SI Prefixes
-----------------

The user can additionally add the following extra si prefixes using the
:ref:`extra_translations` options:

.. list-table:: Extra SI Prefixes
   :widths: 15, 15, 15
   :header-rows: 1

   * - Exponent Value
     - Prefix Name
     - Prefix
   * - 10\ :sup:`+2`
     - hecto
     - h
   * - 10\ :sup:`+1`
     - deca
     - da
   * - 10\ :sup:`-1`
     - deci
     - d
   * - 10\ :sup:`-2`
     - centi
     - c

Parts Per Forms
---------------

.. list-table:: Parts Per Forms
   :widths: 15, 15, 15
   :header-rows: 1

   * - Exponent Value
     - Prefix Name
     - Prefix
   * - 10\ :sup:`0`
     - unity
     - ``no symbol``
   * - 10\ :sup:`-6`
     - parts-per-million
     - ppm
   * - 10\ :sup:`-9`
     - parts-per-billion
     - ppb
   * - 10\ :sup:`-12`
     - parts-per-trillion
     - ppt
   * - 10\ :sup:`-15`
     - parts-per-quadrillion
     - ppq

The user can additionally add a parts-per-thousand form ``ppth``
corresponding to 10\ :sup:`-3` using the ``add_ppth_form`` option.
Note that the definitions here conform to the
`short scale <https://en.wikipedia.org/wiki/Long_and_short_scales>`_
naming convention for large numbers, but that some locales use the
`long scale <https://en.wikipedia.org/wiki/Long_and_short_scales>`_
naming convention for large numbers.
These two scales disagree on the numerical values for terms like
"billion" and "trillion".
For this reason, the usage of this notation is sometimes discouraged.
Note that it is possible, using the ``extra_parts_per_forms`` option to
override the standard mappings listed above.

>>> from sciform import Formatter
>>> formatter = Formatter(
...     exp_mode="engineering",
...     exp_format="parts_per",
...     extra_parts_per_forms={-9: None, -12: "ppb"},
... )
>>> print(formatter(33e-9))
33e-09
>>> print(formatter(33e-12))
33 ppb

IEC Prefixes
------------

.. list-table:: IEC Prefixes
   :widths: 15, 15, 15
   :header-rows: 1

   * - Exponent Value
     - Prefix Name
     - Prefix
   * - 2\ :sup:`+80`
     - yobi
     - Yi
   * - 2\ :sup:`+70`
     - zebi
     - Zi
   * - 2\ :sup:`+60`
     - exi
     - Ei
   * - 2\ :sup:`+50`
     - pebi
     - Pi
   * - 2\ :sup:`+40`
     - tebi
     - Ti
   * - 2\ :sup:`+30`
     - gibi
     - Gi
   * - 2\ :sup:`+20`
     - mebi
     - Mi
   * - 2\ :sup:`+10`
     - kibi
     - Ki
