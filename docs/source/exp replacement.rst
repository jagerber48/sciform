.. _exp_replacements:

Supported Exponent Replacements
###############################

:mod:`sciform` offers exponent replacement modes which provide
translations between exponent strings and conventional string
representations.
For decimal exponents in scientific of engineering formats, SI prefix
translations are available matched to integer multiples of 3 according
to the
`SI prefixes <https://www.nist.gov/pml/owm/metric-si-prefixes>`_.
It is also possible to convert decimal exponents into
`parts-per notation <https://en.wikipedia.org/wiki/Parts-per_notation>`_.
For binary formats, the IEC prefix translations are available matched to
integer multiples of 10 according to the
`IEC prefixes <https://physics.nist.gov/cuu/Units/binary.html>`_.

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

.. list-table:: Parts Per Forms
   :widths: 15, 15, 15
   :header-rows: 1

   * - Exponent Value
     - Prefix Name
     - Prefix
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