.. _prefixes:

Supported Prefixes
##################

:mod:`sciform` offers a prefix mode which provides a simple translation
between exponent strings and one or two letter prefixes.
For scientific and engineering formats the prefixes are matched to
integer multiple of 3 exponent according to the
`SI prefixes <https://www.nist.gov/pml/owm/metric-si-prefixes>`_.
For binary formats, the prefixes are matched to integer multiples of 10
according to the `IEC prefixes <https://physics.nist.gov/cuu/Units/binary.html>`_.

.. list-table:: SI Prefixes
   :widths: 30, 15, 10
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
     - μ
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

.. list-table:: IEC Prefixes
   :widths: 30, 15, 10
   :header-rows: 1

   * - Exponent Value
     - Prefix Name
     - Prefix
   * - 10\ :sup:`+80`
     - yobi
     - Yi
   * - 10\ :sup:`+70`
     - zebi
     - Zi
   * - 10\ :sup:`+60`
     - exi
     - Ei
   * - 10\ :sup:`+50`
     - pebi
     - Pi
   * - 10\ :sup:`+40`
     - tebi
     - Ti
   * - 10\ :sup:`+30`
     - gibi
     - Gi
   * - 10\ :sup:`+20`
     - mebi
     - Mi
   * - 10\ :sup:`+10`
     - kibi
     - Ki
