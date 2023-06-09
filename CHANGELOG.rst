0.20.1 (2023-06-24)
-------------------

* Refactor unit tests to use lists and tuples instead of dicts. Literal
  dicts allow the possibility for defining the same key (test case) with
  different values, only the latest of which will actually be tested.
  The refactoring ensures all elements of the test lists will be tested.
* Refactor ``sfloat`` and ``vufloat`` ``__format__()`` functions to call
  ``format_float()`` and ``format_val_unc()`` directly instead of
  creating a ``Formatter`` object first.

0.20.0 (2023-06-22)
-------------------

* Support passing ``None`` as a value into ``extra_si_prefixes``,
  ``extra_iec_prefixes``, or ``extra_parts_per_forms`` to prevent
  translation of a certain exponent value. This may be useful for
  suppressing ``ppb`` or similar local-dependent "parts per"
  translations.
* **[BREAKING]** Change the bracket uncertainty flag in the
  `FSML <fsml>`_ from ``'S'`` to ``'()'``.
* When an exponent translation mode is used in combination with Latex
  mode, the translated exponent will now be wrapped in a Latex text
  mode: e.g. ``\text{Mi}``.
* Link to test cases on examples page

0.19.0 (2023-06-22)
-------------------

* Add python-package.yaml github workflows. Allows automated testing,
  doc testing, and flake8 scans during github pull requests.
* Minor flake8 cleanup

0.18.1 (2023-06-21)
-------------------

* Documentation improvements

0.18.0 (2023-06-19)
-------------------

* Add Particle Data Group significant figure auto selection feature,
  documentation, and tests.
* **[BREAKING]** Use the larger of value or uncertainty to resolve the
  exponent when formatting value/uncertainty pairs. The previous
  behavior was to always use the value to resolve the exponent, but this
  behavior was not convenient for the important use case of zero value
  with non-zero uncertainty.
* Expose ``AutoPrec`` and ``AutoExp`` sentinel classes so that users can
  explicitly indicate automatic precision and exponent selection.

0.17.1 (2023-06-19)
-------------------

* Code restructure to make formatting algorithm easier to follow
  including more verbose clarifying comments.
* Minor documentation cleanup

0.17.0 (2023-06-19)
-------------------

* Add parts-per notation feature, documentation, and tests.
* **[BREAKING]** Rename ``use_prefix`` option to ``prefix_exp``.
* Fix typos in binary IEC prefixes table.
* Fix some cross links in documentation.

0.16.0 (2023-06-18)
-------------------

* Add ``latex`` option with documentation and tests.
* Refactor exponent string conversion.
* Percent mode for non-finite numbers.

0.15.2 (2023-06-18)
-------------------

* Fix a bug involving space filling and separators.

0.15.1 (2023-06-17)
-------------------

* Changelog formatting typo.

0.15.0 (2023-06-17)
-------------------

* Add ``superscript_exp`` option with documentation and tests.
* Forbid percent mode unless using fixed point exponent mode.
* Add PyPi link to readme.

0.14.0 (2023-06-17)
-------------------

* Add Changelog.
* Add ``unicode_pm`` option with documentation and tests.
