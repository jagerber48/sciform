Changelog
=========

This project adheres to `Semantic Versioning <https://semver.org/>`_.

----

Unreleased
----------

* Any unreleased changes can be viewed in the latest version
  documentation
  `changelog <https://sciform.readthedocs.io/en/latest/project.html#changelog>`_.

----

0.35.0 (2024-02-16)
-------------------

Added
^^^^^

* The ``Formatter`` formatting method and the ``SciNum`` constructor now
  accept formatted inputs for the value and optional uncertainty inputs.
  E.g. ``formatter("123.456(7)e-03")`` or ``SciNum("24 +/- 2")`` are now
  valid inputs.
  [`#104 <https://github.com/jagerber48/sciform/issues/104>`_]
* Added the ``paren_uncertainties_trim`` option.
  The previous behavior was ``paren_uncertainties_trim=True``.
  Now ``paren_uncertainties_trim=False`` allows a more verbose
  presentation of the uncertainty in ``paren_uncertainty`` mode in which
  leading zeros and separator characters are **not** stripped from the
  string.
  E.g. ``paren_uncertainties_trim=True`` will give

    123.002 3(21)

  while ``paren_uncertainties_trim=False`` will give

    123.002 3(0.002 1)

* Added ``value`` and ``uncertainty`` attributes to the
  ``FormattedNumber`` class.
* Added badge for Zenodo.

Removed
^^^^^^^

* **[BREAKING]** Removed the ``paren_uncertainties_separators`` option.
  This option made it possible (when ``False``) to optionally strip all
  separator characters, including the decimal separator, from the
  uncertainty in ``paren_uncertainty`` mode.
  This lead to the possibility of value/uncertainty pairs like

    123 456.789 8 ± 123.456 7

  being represented as

    123 456.789 8(1234567)

  ``sciform`` will now display this as

    123 456.789 8(123.456 7)

  if ``paren_uncertainty_strip=False`` or

    123 456.789 8(123.4567)

  if ``paren_uncertainty_strip=True``, but always retaining the decimal
  separator.
  In most cases many fewer significant digits of the uncertainty are
  displayed and the resulting outputs don't look as egregious when the
  decimal separator is stripped.
  Nonetheless, given that more outputs look better when the decimal is
  retained and that there is no official BIPM guidance on how
  parentheses should handle cases when the uncertainty digits span
  decimal or other separator characters, ``sciform`` will not presently
  provide an option to strip the decimal separator character.

Changed
^^^^^^^

* Previously, when using ``paren_uncertainty=True``, redundant
  parentheses were included around the value and uncertainty numbers if
  there was an ASCII exponent (e.g. ``e+02``) or in percent formatting
  mode.
  E.g. outputs would look like ``(32.4(1.2))e+02`` or ``(32.4(1.2))%``.
  Now these redundant parentheses are excluded so outputs look like
  ``32.4(1.2)e+02`` or ``32.4(1.2)%``.
  This is consistent with how the
  `uncertainties <https://uncertainties-python-package.readthedocs.io/en/latest/>`_
  package handles these cases.
  The extra parentheses were originally included for increased clarity,
  but the extra parentheses only clutter the output and there is
  sufficient clarity without them.
  This change eliminates an issue where the redundant parentheses were
  erroneously included or excluded after LaTeX/HTML/ASCII output
  conversion.
  [`#145 <https://github.com/jagerber48/sciform/issues/145>`_]

Fixed
^^^^^

* Previously, when formatting individual ``Decimal`` input values, the
  values were always normalized at an early stage in formatting.
  This meant that even if ``ndigits=AutoDigits`` then ``Decimal("1.0")``
  would be formatted the same as ``Decimal("1.00")``.
  However, for value/uncertainty formatting, ``Decimal`` input to the
  uncertainty was not necessarily normalized at an early stage.
  This meant that with ``ndigits=AutoDigits``, an uncertainty of
  ``Decimal("1.0")`` would be formatted to the tenths decimal place
  while an uncertainty of ``Decimal("1.00")`` would be formatted to the
  hundredths place.
  This behavior was inconsistent and undocumented.
  Now all ``Decimal`` inputs are immediately normalized before any
  formatting.
  [`#148 <https://github.com/jagerber48/sciform/issues/148>`_]
* Fixed the behavior around the sign symbols for zero and non-finite
  inputs.
  Previously ``0`` was treated as positive for the sake of resolving
  its sign symbol, the sign of infinite numbers was preserved but
  ``+inf`` did not respect the ``"+"`` and ``" "`` sign modes, and
  ``nan`` never had a sign but also never had an extra character added
  for ``"+"`` or ``" "`` sign modes.
  Now both ``0`` and ``nan`` are treated as having no sign.
  In both ``"+"`` and ``" "`` sign modes ``0`` and ``nan`` are prepended
  by a space.
  The sign of infinite numbers is retained as before, but now formatting
  of these numbers respects the sign mode.
  [`#147 <https://github.com/jagerber48/sciform/issues/147>`_]

----

0.34.1 (2024-02-10)
-------------------

Added
^^^^^

* Updated the readme to reflect completion of the PyOpenSci review.

----

0.34.0 (2024-02-04)
-------------------

Added
^^^^^

* The ``Formatter`` now exposes the ``input_options`` and
  ``populated_options`` attributes.
  The ``input_options`` attribute holds an ``InputOptions`` object which
  stores a record of the input options passed into the ``Formatter``.
  The ``populated_options`` attribute returns a ``PopulatedOptions``
  object which shows the complete set of populated options which will be
  used for formatting after merging with the global options.
  Note that the ``populated_options`` attribute is re-calculated each
  time it is access so that it reflects the current global options.
  Both the ``InputOptions`` and ``PopulatedOptions`` objects can be used
  to provide string representations of the options, or provide
  programmatic access to the options via either attribute access or the
  ``as_dict()`` methods.
  [`#110 <https://github.com/jagerber48/sciform/issues/110>`_]
* The ``PopulatedOptions`` used during formatting of a given
  ``FormattedNumber`` instance are stored on that instance for future
  reference.
* Added ``get_default_global_options()``.
* Now integer ``0`` can be passed into ``left_pad_char`` to get the same
  behavior as string ``"0"``.
* Added tests for docstrings.

Changed
^^^^^^^

* **[BREAKING]** Renamed functions for configuring global options:

  * ``set_global_defaults()`` -> ``set_global_options()``
  * ``reset_global_defaults()`` -> ``reset_global_options()``
  * ``GlobalDefaultsContext()`` -> ``GlobalOptionsContext()``

* Refactored backend options handling code.
  Previously, ``UserOptions`` were rendered into ``RenderedOptions``.
  During rendering the global options were appropriately merged in and
  some string literal options were replaced with enums for internal use.
  These two classes were private.
  Now there are ``InputOptions`` (which try to faithfully record user
  input), ``PopulatedOptions`` (which capture the result of merging
  the global options into the input options, but still using
  user-friendly string representations of all options), and
  ``FinalizedOptions`` (which use the internal enum representations of
  certain options).
  The ``InputOptions`` and ``PopulatedOptions`` are now public while the
  ``FinalizedOptions`` is still private to shield the enum
  representations from the users.
  This sizable refactor was precipitated by the publicizing of the
  options.
  [`#110 <https://github.com/jagerber48/sciform/issues/110>`_]

Removed
^^^^^^^

* **[BREAKING]** Removed ``print_global_defaults()`` in favor of
  ``get_global_defaults()`` which now returns a ``PopulatedOptions``
  object which can be printed by the user if desired.

Fixed
^^^^^

* Fixed a bug where ``SciNum`` formatting resulted in ``str`` objects
  instead of ``FormattedNumber`` objects.

----

0.33.0 (2024-01-31)
-------------------

Added
^^^^^

* Added the ``FormattedNumber`` class.
  This class is a subclass of ``str`` and is now returned by the
  ``Formatter`` instead of ``str``.
  The ``FormattedNumber`` class allows post-conversion to ASCII, HTML,
  and LaTeX formats.
  [`#114 <https://github.com/jagerber48/sciform/issues/114>`_]
* Added separate flags for code coverage reports for each python
  version.

Changed
^^^^^^^

* In addition to removing the ``latex`` option from the ``Formatter`` in
  favor of the introduction of the ``FormattedNumber`` class, the
  LaTeX conversion algorithm has been slightly modified.

    * Left and right parentheses are no longer converted to ``"\left("``
      and ``"\right)"`` due to introducing strange spacing issues.
      See
      `Spacing around \\left and \\right <https://tex.stackexchange.com/questions/2607/spacing-around-left-and-right>`_.
    * Previously spaces within the ``sciform`` output were handled
      inconsistently and occasionally required confusing extra handling.
      Now any spaces in the input string are directly and explicitly
      converted into math mode medium spaces: ``"\:"``.
    * ``"μ"`` is now included in the math mode ``\text{}`` environment
      and converted to ``"\textmu"``.

* **[BREAKING]** Renamed ``fill_char`` to ``left_pad_char``.
  [`#126 <https://github.com/jagerber48/sciform/issues/126>`_]
* Slimmed down ``[dev]`` optional dependencies and created
  ``[examples]`` optional dependencies.
  The former includes development tools, while the latter includes
  the heavy-weight requirements needed to run all the examples,
  including, e.g. ``jupyter``, ``scipy``, etc.
* Cleaned up and improved github actions for testing and
  linting/formatting.
  [`#136 <https://github.com/jagerber48/sciform/issues/136>`_]

    * Use ``unittest`` and ``coverage`` instead of ``pytest``.
    * The requirements to run the automation match the ``[dev]``
      optional dependencies.
    * Cache ``pip`` requirements to avoid unnecessarily downloading
      dependencies.
    * Remove a defunct ``blackdoc`` test.
      Hopefully this can be replaced when ``ruff`` provides
      functionality for formatting ``.rst`` files.

Fixed
^^^^^

* Fixed a bug where value/uncertainty pairs formatted in the
  ``"parts_per"`` format with zero exponent would appear with redundant
  parentheses, e.g. ``"(1.2 ± 0.1)"``.
  [`#130 <https://github.com/jagerber48/sciform/issues/130>`_]

Removed
^^^^^^^

* **[BREAKING]** Removed the ``latex`` option in favor of the
  introduction of the ``FormattedNumber.as_latex()`` method.
  This removal simplifies the formatting algorithm by separating LaTeX
  formatting from other tasks like exponent string resolution.
  The ``latex`` option also introduced a potential confusion with the
  ``superscript`` option, which had no effect when ``latex=True``.

----

0.32.3 (2024-01-11)
-------------------

Added
^^^^^

* Added more PyPi classifiers.

0.32.2 (2024-01-11)
-------------------

Added
^^^^^

* Expanded the "Under Construction" section of the readme and the
  "How to Contribute" section of the project page.
  Changes included adding links to the ``sciform`` feedback survey.
* Added examples in the documentation demonstrating how ``sciform``
  formatting can be mapped over collections of numbers.
  [`#120 <https://github.com/jagerber48/sciform/issues/120>`_]

Changed
^^^^^^^

* Refactor backend mode literal (used for typing) and enum (used
  internally for tracking options) object names so that e.g.
  ``SignMode`` -> ``SignModeEnum`` and ``UserSignMode`` -> ``SignMode``.
  [`#111 <https://github.com/jagerber48/sciform/issues/111>`_]

----

0.32.0 (2024-01-10)
-------------------

Added
^^^^^

* Previously it was impossible to configure ``pdg_sig_figs=True``
  together with ``ndigits!=AutoDigits``.
  This combinations resulted in an exception.
  Now behavior has been defined and implemented for this combination.
  For single value formatting the value of ``pdg_sig_figs`` is always
  ignored.
  For value/uncertainty formatting ``ndigits`` is ignored if
  ``pdg_sig_figs=True``.
  The behavior for ``pdg_sig_figs=False`` is unchanged.
  [`#73 <https://github.com/jagerber48/sciform/issues/73>`_]

Removed
^^^^^^^

* **[BREAKING]** Removed ``global_add_c_prefix``,
  ``global_add_small_si_prefixes``, ``global_add_ppth_form``,
  ``global_reset_si_prefixes``, ``global_reset_iec_prefixes``, and
  ``global_reset_parts_per_forms``.
  These options are redundant with ``set_global_defaults`` and
  ``GlobalDefaultsContext`` and make the extra translations dictionaries
  more confusing to understand.
  [`#97 <https://github.com/jagerber48/sciform/issues/97>`_]

Changed
^^^^^^^

* **[BREAKING]** Previously ``12.3`` would format as ``"12.3e+00"``
  when using parts per formatting mode.
  Now, when using parts per formatting mode, the ``e+00`` exponent is
  translated to be an empty string so that ``12.3`` would format as
  ``"12.3"``.
  [`#99 <https://github.com/jagerber48/sciform/issues/99>`_]

----

0.31.1 (2024-01-06)
-------------------

Removed
^^^^^^^

* **[BREAKING]** Removed the ``SciNumUnc`` class. Now the ``SciNum``
  class can be used with an optional second positional argument to
  specify the uncertainty associated with a number.

* **[BREAKING]** Remove separator configuration from the FSML.
  These options made the FSML to cumbersome and led to confusing
  (if not incorrect) conflicts with the round mode symbol.
  Now all separator configuration needs to be done by setting the
  global format options or using the global format options context
  manager.
  [`#29 <https://github.com/jagerber48/sciform/issues/29>`_]

Added
^^^^^

* Added annotated examples demonstrating the FSML.
* Added more documentation for contributing developers.
* Added `pre-commit <https://pre-commit.com/>`_ configuration.

Changed
^^^^^^^

* **[BREAKING]** Renamed multiple options.

    * ``top_dig_place`` renamed to ``left_pad_dec_place``.
    * ``superscript_exp`` renamed to ``superscript``.
    * ``bracket_unc`` renamed to ``paren_uncertainty``.
    * ``bracket_unc_remove_seps`` renamed to
      ``paren_uncertainty_separators``. This change is associated with a
      a reversal of the Boolean logic on the option.
    * ``val_unc_match_widths`` renamed to ``left_pad_matching``.
    * ``unc_pm_whitespace`` renamed to ``pm_whitespace``.

* **[BREAKING]** Previously specifying any left pad decimal place using
  the ``sciform`` FSML resulted in setting ``left_pad_matching=True`` so
  that ``print(f"{SciNum(123.456, 0.789):0}")`` resulted in
  ``"123.456 ± 000.789"``.
  Now the FSML has no impact on ``left_pad_matching``.
  Now, similar to many other options, the global setting for
  ``left_pad_matching`` will always be used when formatting using the
  FSML.
  Under the default global options (``left_pad_matching=False``)
  ``print(f"{SciNum(123.456, 0.789):0}")`` results in
  ``"123.456 ± 0.789"``.
* Implemented `ruff <https://docs.astral.sh/ruff/>`_ linting and
  formatting in codebase and integration automation.
* Refactored code for adding separators.
* Refactored formatting and formatting utilities to simplify functions
  and make the algorithm easier to follow.
* More aggressively filter JetBrains ``.idea/`` folder from version control.

Fixed
^^^^^

* Fixed a bug involving removing separators in parentheses uncertainty
  mode when at least one of the value and uncertainty were non-finite.

----

0.30.1 (2023-11-24)
-------------------

Fixed
^^^^^

* Fixed Changelog.

----

0.30.0 (2023-11-24)
-------------------

Changed
^^^^^^^

* **[BREAKING]** Remove the ``FormatOptions`` class from the user
  interface. Now users configure ``Formatter`` instances by passing the
  formatting keyword arguments into the ``Formatter`` constructor
  directly. Global configuration via ``set_global_defaults()`` or the
  ``GlobalDefaultsContext`` is also done by passing formatting keywords
  directly. This change reduces the amount of boilerplate code and
  keystrokes needed to use ``sciform``.
* **[BREAKING]** Options such as ``exp_mode`` and ``exp_format`` were
  previously configured using ``Enum`` objects such as ``ExpMode`` or
  ``ExpFormat``. Now these options are configured using string literals.
  This change also reduces the amount of boilerplate code and keystrokes
  needed to use ``sciform``.
* Clean up ``print_global_defaults`` output. This is the start of an
  effort to improve interface for getting and printing current format
  options.

Added
^^^^^

* Added code of conduct.
* Added contributing guidelines.
* Added Python 3.12 to automated testing.

Fixed
^^^^^

* Cleaned up API documentation.
* Fixed a bug where the ``repr`` for ``FormatOptions`` would return a
  string containing information about the global format options rather
  than about the specific ``FormatOptions`` instance.
  [`#75 <https://github.com/jagerber48/sciform/issues/75>`_]
* Fixed an issue that was causing Github actions code coverage report to
  not actually check code coverage.
  [`#84 <https://github.com/jagerber48/sciform/issues/84>`_]

Removed
^^^^^^^

* **[BREAKING]** Removed the ``unicode_pm`` feature which allowed
  toggling between using ``'+/-'`` or ``'±'`` in value/uncertainty
  strings. Previously ``unicode_pm`` defaulted to ``False`` so that
  ``'+/-'`` was the default behavior. Now the default behavior is to use
  ``'±'`` and there is no way to change to the old ``'+/-'`` behavior.
  [`#10 <https://github.com/jagerber48/sciform/discussions/10>`_]

----

0.29.1 (2023-10-22)
-------------------

Fixed
^^^^^

* Fixed a bug where bracket uncertainties erroneously appeared as
  empty parentheses for zero or non-finite uncertainties.
  [`#66 <https://github.com/jagerber48/sciform/issues/66>`_]
* Fixed a bug where the exponent value was erroneously calculated
  from the uncertainty rather than the value when the value was
  negative (but larger in magnitude than the uncertainty).
  [`#68 <https://github.com/jagerber48/sciform/issues/68>`_]
* Fixed a bug where certain leading digits were erroneously not
  stripped from the uncertainty when using bracket uncertainty with
  negative values.
  [`#68 <https://github.com/jagerber48/sciform/issues/68>`_]
* Fixed a bug where the value was erroneously being rounded
  according to the PDG rounding rules when ``pdg_sig_figs=True``,
  the uncertainty was zero or non-finite, and the value was
  positive. [`#71 <https://github.com/jagerber48/sciform/issues/71>`_]
* Fixed a bug where a spurious error was raised when
  ``pdg_sig_figs=True``, the uncertainty was zero or non-finite, and
  the value was zero or negative.
  [`#65 <https://github.com/jagerber48/sciform/issues/65>`_]

Changed
^^^^^^^

* Replace ``-e .`` with ``.`` in ``requirements.txt``. There is no need
  to install ``sciform`` in editable mode for code automation routines.

----

0.29.0 (2023-09-05)
-------------------

Changed
^^^^^^^

* Previously, when using ``bracket_unc=True`` with any exponent string
  (such as ``e-06``, ``μ`` or ``ppm``), the value and uncertainty were
  always wrapped in parentheses, e.g. ``(1.03(25))e-06``,
  ``(1.03(25)) μ`` or ``(1.03(25)) ppm``.
  Now, when using ``bracket_unc=True`` with prefix or parts-per exponent
  format modes, if the exponent is replaced with an alphabetic
  replacement, then the value and uncertainty are no longer wrapped in
  parentheses, e.g. ``1.03(25) μ`` and ``1.03(25) ppm``.
  This is consistent with
  `BIPM Guide Section 7.2.2 <https://www.bipm.org/documents/20126/2071204/JCGM_100_2008_E.pdf/cb0ef43f-baa5-11cf-3f85-4dcd86f77bd6#page=37>`_.
  Specifically, any time ``bracket_unc=False`` the value and uncertainty
  are always wrapped in parentheses, and any time notation like ``e+02``
  or ``b+02`` is used to indicate the exponent then the value and
  uncertainty are always wrapped in parentheses.

Fixed
^^^^^

* Correct ``fit_plot_with_sciform.py`` example script to use new
  ``exp_format=ExpFormat.PREFIX`` instead of old ``prefix_exp=True``.

Improved
^^^^^^^^

* Documentation improvements including typos and neatening up changelog.

----

0.28.2 (2023-08-31)
-------------------

Improved
^^^^^^^^

* General wording and grammar improvements throughout documentation.
* Include more usage examples in the examples documentation in addition
  to referring the reader to the test suite.

Fixed
^^^^^

* Fixed a bug when using ``pdg_sig_figs`` with uncertainties larger than
  about 1000 by cleaning up ``Decimal`` math.
* Previously, when formatting using the format specification
  mini-language, if the prefix exponent format flag was omitted then the
  exponent format was forced to ``ExpFormat.STANDARD`` rather than
  ``None``.
  This meant that it was impossible, using the format specification
  mini-language combined with global configuration options, to set
  ``ExpFormat.PARTS_PER``.
  Now when the prefix flag is omitted ``exp_format`` is set to ``None``
  so that it will be populated by the global default option.
  In the future a flag may be added to select "parts-per" formatting
  using the format specification mini-language.

----

0.28.1 (2023-08-28)
-------------------

* Make ``FormatOptions`` inputs ``Optional`` so that ``None`` inputs
  pass type checks.
* Write format-specification mini-language documentation to refer to
  existing format options documentation to avoid documentation
  duplication.
* Setup test coverage analysis automation and upload report to
  `codecov <https://codecov.io/gh/jagerber48/sciform>`_.
* Add package status badges to readme.
* Test against Python 3.11.
* List supported Python versions in ``pyproject.toml`` classifiers.

----

0.28.0 (2023-08-27)
-------------------

* **[BREAKING]** Replace ``prefix_exp`` and ``parts_per_exp`` options
  with an ``exp_format`` option which can be configured to
  ``ExpFormat.STANDARD``, ``ExpFormat.PREFIX`` or
  ``ExpFormat.PARTS_PER``.
* Previously formatting a non-finite number in percent mode would always
  display a ``'%'`` symbol, e.g. ``'(nan)%'``.
  Now the brackets and ``'%'`` symbol will be omitted unless
  ``nan_inf_exp=True``.
* In ``latex=True`` mode there is now a space between the number and a
  prefix or parts-per translated exponent.
  For value/uncertainty formatting the space is still absent.
  For ``latex=False`` there is still always a space for number and
  value/uncertainty formatting before the translated exponent string.
* In ``latex=True`` mode ``'nan'`` and ``'inf'`` strings are now wrapped
  in ``'\text{}'``.
* Refactored code for resolving exponent strings.
* Added more unit tests to reach 100% test coverage. Mostly added test
  cases for invalid internal inputs.
* Raise ``NotImplementedError`` when attempting value/uncertainty
  formatting with binary exponent modes.
  Rounding and truncating are not properly implemented in binary mode
  yet.

----

0.27.4 (2023-08-25)
-------------------

* Setup github action to automatically build and publish on release.

----

0.27.3 (2023-08-23)
-------------------

* Added ``Unreleased`` section to changelog.
* Removed ``version`` from source code.
  Project version is now derived from a git version tag using
  ``setuptools_scm``.
* Stopped encouraging ``import FormatOptions as Fo``.

----

0.27.2 (2023-08-20)
-------------------

* Add ``__repr__()`` for ``FormatOptions`` and
  ``RenderedFormatOptions``.

----

0.27.1 (2023-08-18)
-------------------

* Add ``examples/`` folder to hold example scripts used in the
  documentation as well as the input data for these scripts and their
  outputs which appear in the documentation.
* Remove extra ``readthedocs.yaml`` file.

----

0.27.0 (2023-08-18)
-------------------

* **[BREAKING]** Rename ``AutoRound`` to ``AutoDigits``. This is
  because, e.g., ``ndigits=AutoDigits`` sounds more correct than
  ``ndigits=AutoRound``. Furthermore, ``AutoRound`` could likely be
  confused as being an option for ``round_mode``, which it is not.

----

0.26.2 (2023-08-18)
-------------------

* Fix a bug where illegal options combinations could be realized at
  format time when certain global default objects were merged into
  certain user specified options.
  The bug is fixed by re-checking the options combinations after merging
  in the global defaults but before formatting.

----

0.26.1 (2023-08-18)
-------------------

* Add unit tests, increase test coverage.

----

0.26.0 (2023-08-15)
-------------------

* **[BREAKING]** Rename some format options to make their usage more
  clear.

   * ``exp`` to ``exp_val``
   * ``precision`` to ``ndigits``
   * ``RoundMode.PREC`` to ``RoundMode.DEC_PLACE``
   * ``AutoExp`` to ``AutoExpVal``
   * ``AutoPrec`` to ``AutoRound``

* Raise more exceptions for incorrect options combinations.

   * Raise an exception when using ``pdg_sig_figs`` with a user-supplied
     ``exp_val``.
   * Raise exceptions instead of warnings for invalid user-supplied
     ``exp_val`` in ``get_mantissa_base_exp()``.

* Minor refactor to ``GlobalDefaultsContext``.
* Documentation:

   * Update documentation to reflect name changes above.
   * Better centralization of ``float``/``Decimal`` information.
   * Better explanations of ``AutoExpVal`` and ``AutoRound`` behavior.
   * More accurate descriptions of some invalid options combinations.

----

0.25.2 (2023-08-11)
-------------------

* Update roadmap

----

0.25.1 (2023-08-10)
-------------------

* Refactor ``get_pdg_round_digit()`` into a dedicated function.

----

0.25.0 (2023-08-02)
-------------------

* **[BREAKING]** ``template`` option removed from ``FormatOptions``
  constructor.
  New ``FormatOptions`` instances can be constructed from two existing
  ``FormatOptions`` instances using the ``merge()`` method.
* Minor documentation improvements.

----

0.24.0 (2023-07-30)
-------------------

* **[BREAKING]** percent mode is now accessed via an exponent mode,
  ``ExpMode.PERCENT``.
  There is no longer a ``percent`` keyword argument.

----

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

----

0.22.2 (2023-07-27)
-------------------

* Add ``.readthedocs.yaml`` and update documentation
  ``requirements.txt`` for reproducible documentation builds.

----

0.22.1 (2023-07-27)
-------------------

* Fix a date typo in the changelog for the entry for version ``0.22.0``.

----

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

----

0.21.0 (2023-07-22)
-------------------

* Use ``Decimal`` under the hood for numerical formatting instead of
  ``float``. ``Decimal`` instances support higher precision than
  ``float`` and more reliable rounding behavior.
* Update particle data group uncertainty rounding unit tests since edge
  cases are now handled property as a result of adopting ``Decimal``.
* Minor cleanup of ``sfloat`` arithmetic functions.

----

0.20.1 (2023-06-24)
-------------------

* Refactor unit tests to use lists and tuples instead of dicts. Literal
  dicts allow the possibility for defining the same key (test case) with
  different values, only the latest of which will actually be tested.
  The refactoring ensures all elements of the test lists will be tested.
* Refactor ``sfloat`` and ``vufloat`` ``__format__()`` functions to call
  ``format_float()`` and ``format_val_unc()`` directly instead of
  creating a ``Formatter`` object first.

----

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

----

0.19.0 (2023-06-22)
-------------------

* Add python-package.yaml github workflows. Allows automated testing,
  doc testing, and flake8 scans during github pull requests.
* Minor flake8 cleanup

----

0.18.1 (2023-06-21)
-------------------

* Documentation improvements

----

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

----

0.17.1 (2023-06-19)
-------------------

* Code restructure to make formatting algorithm easier to follow
  including more verbose clarifying comments.
* Minor documentation cleanup

----

0.17.0 (2023-06-19)
-------------------

* Add parts-per notation feature, documentation, and tests.
* **[BREAKING]** Rename ``use_prefix`` option to ``prefix_exp``.
* Fix typos in binary IEC prefixes table.
* Fix some cross links in documentation.

----

0.16.0 (2023-06-18)
-------------------

* Add ``latex`` option with documentation and tests.
* Refactor exponent string conversion.
* Percent mode for non-finite numbers.

----

0.15.2 (2023-06-18)
-------------------

* Fix a bug involving space filling and separators.

----

0.15.1 (2023-06-17)
-------------------

* Changelog formatting typo.

----

0.15.0 (2023-06-17)
-------------------

* Add ``superscript_exp`` option with documentation and tests.
* Forbid percent mode unless using fixed point exponent mode.
* Add PyPi link to readme.

----

0.14.0 (2023-06-17)
-------------------

* Add Changelog.
* Add ``unicode_pm`` option with documentation and tests.
