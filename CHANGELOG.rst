0.25.2 (2023-08-11)
-------------------

* Update roadmap

0.25.1 (2023-08-10)
-------------------

* Refactor ``get_pdg_round_digit()`` into a dedicated function.

0.25.0 (2023-08-02)
------------------

* **[BREAKING]** ``template`` option removed from ``FormatOptions``
  constructor.
  New ``FormatOptions`` instances can be constructed from two existing
  ``FormatOptions`` instances using the ``merge()`` method.
* Minor documentation improvements.

0.24.0 (2023-07-30)
-------------------

* **[BREAKING]** percent mode is now accessed via an exponent mode,
  ``ExpMode.PERCENT``.
  There is no longer a ``percent`` keyword argument.

0.23.0 (2023-07-29)
-------------------

* **[BREAKING]** Users now construct ``FormatOptions`` objects which
  they pass into ``Formatter`` objects and global configuration
  functions.
  ``Formatter`` and global configuration functions no longer accept bare
  keyword arguments to indicate formatting options.
* **[BREAKING]** ``Formatter`` now resolves un-filled format options
  from the global defaults at format time instead of initialization
  time.
  This is consistent with the previous behavior for ``SciNum`` and
  ``SciNumUnc`` objects.
* Change ``pyproject.toml`` description


0.22.2 (2023-07-27)
-------------------

* Add ``.readthedocs.yaml`` and update documentation
  ``requirements.txt`` for reproducible documentation builds.

0.22.1 (2023-07-27)
-------------------

* Fix a date typo in the changelog for the entry for version ``0.22.0``.

0.22.0 (2023-07-27)
-------------------

* **[BREAKING]** Rename ``sfloat`` to ``SciNum`` and ``vufloat`` to
  ``SciNumUnc``
* **[BREAKING]** ``SciNum`` instances do not support arithmetic
  operations the same way ``sfloat`` instances did.
  This functionality was removed for two reasons.
  First, ``SciNum`` uses ``Decimal`` to store its value instead of
  ``float`` and configuring ``SciNum`` to behave as a subclass of
  ``Decimal`` would require added complexity.
  Second, A decision has been made to keep the ``sciform`` module
  focussed solely on formatting individual numbers or pairs of numbers
  for early releases.
  Convenience functionality outside of this narrow scope will be
  considered at a later time.
* Favor ``Decimal`` methods over ``float`` methods in internal
  formatting algorithm code.
* Documentation

   * Remove ``float``-based language fom documentation.
   * Include a discussion in the documentation about ``Decimal`` versus
     ``float`` considerations that may be important for users.
   * Various minor revisions and edits. Notably a typo in the version
     ``0.21.0`` changelog entry that reversed the meaning of a sentence
     was corrected.
   * Add "under construction" message to README.

0.21.0 (2023-07-22)
-------------------

* Use ``Decimal`` under the hood for numerical formatting instead of
  ``float``. ``Decimal`` instances support higher precision than
  ``float`` and more reliable rounding behavior.
* Update particle data group uncertainty rounding unit tests since edge
  cases are now handled property as a result of adopting ``Decimal``.
* Minor cleanup of ``sfloat`` arithemetic functions.

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
* Link to test cases on examples page.

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
