Usage
#####

Formatting
==========

.. module:: sciform
   :noindex:

:mod:`sciform` provides two primary methods for formatting floats into
scientific formatting strings.
The first is via the :class:`Formatter` object and the second is
using string formatting and the
:ref:`Format Specification Mini Language (FSML) <fsml>` with the
:class:`sfloat` object.

Formatter
---------

The :class:`Formatter` object is initialized with user-selected
formatting options and then used to format floats. Additional details
about formatting options at :ref:`formatting_options`.

>>> from sciform import Formatter, RoundMode, GroupingSeparator, FormatMode
>>> sform = Formatter(round_mode=RoundMode.PREC,
...                   precision=6,
...                   upper_separator=GroupingSeparator.SPACE,
...                   lower_separator=GroupingSeparator.SPACE)
>>> print(sform(3.14159265359))
3.141 593

>>> sform = Formatter(round_mode=RoundMode.SIG_FIG,
...                   precision=4,
...                   format_mode=FormatMode.ENGINEERING)
>>> print(sform(123456.78))
123.5e+03

sfloat
------

The :mod:`sciform` :ref:`FSML <fsml>` is accessed via the
:class:`sfloat` object.
Regular built-in floats are cast to :class:`sfloat` objects which can be
formatted using the :mod:`sciform` :ref:`FSML <fsml>`.

>>> from sciform import sfloat
>>> num = sfloat(123456)
>>> print(f'{num:_!2f}')
120_000

Global Configuration
====================

It is possible to modify the global default configuration for
:mod:`sciform` to avoid repetition of verbose configuration options or
format specification strings.
When the user creates a :class:`Formatter` object or formats a string
using the :ref:`FSML <fsml>`, they typically do not specify settings for
available options.
In thes cases, the unspecified options extract their settings from the
global default settings.

The global default settings can be viewed using
:func:`print_global_defaults()`:

>>> from sciform import print_global_defaults
>>> print_global_defaults()
{'fill_mode': <FillMode.SPACE: 'space'>,
 'sign_mode': <SignMode.NEGATIVE: 'negative'>,
 'top_dig_place': 0,
 'upper_separator': <GroupingSeparator.NONE: 'no_grouping'>,
 'decimal_separator': <GroupingSeparator.POINT: 'point'>,
 'lower_separator': <GroupingSeparator.NONE: 'no_grouping'>,
 'round_mode': <RoundMode.SIG_FIG: 'sig_fig'>,
 'precision': <class 'sciform.modes.AutoPrec'>,
 'format_mode': <FormatMode.FIXEDPOINT: 'fixed_point'>,
 'capital_exp_char': False,
 'exp': <class 'sciform.modes.AutoExp'>,
 'use_prefix': False,
 'extra_si_prefixes': {},
 'extra_iec_prefixes': {},
 'bracket_unc': False,
 'val_unc_match_widths': False,
 'bracket_unc_remove_dec_symb': False,
 'unc_pm_whitespace': True,
 'nan_include_exp': False,
 'val_unc_nan_include_exp': <class 'sciform.modes.AutoValUncNanIncludeExp'>}

The global default settings can be modified using
:func:`set_global_defaults()` with the same keyword arguments passed
into :class:`Formatter`.
Any explicit options passed in will be updated while any unspecified
options will retain their existing values.
The same checks applied when constructing a :class:`Formatter` are
applied to setting global default settings.

>>> from sciform import (set_global_defaults, FillMode, FormatMode,
...                      GroupingSeparator)
>>> set_global_defaults(fill_mode=FillMode.ZERO,
...                    format_mode=FormatMode.ENGINEERING_SHIFTED,
...                    precision=4,
...                    decimal_separator=GroupingSeparator.COMMA)
>>> print_global_defaults()
{'fill_mode': <FillMode.ZERO: 'zero'>,
 'sign_mode': <SignMode.NEGATIVE: 'negative'>,
 'top_dig_place': 0,
 'upper_separator': <GroupingSeparator.NONE: 'no_grouping'>,
 'decimal_separator': <GroupingSeparator.COMMA: 'comma'>,
 'lower_separator': <GroupingSeparator.NONE: 'no_grouping'>,
 'round_mode': <RoundMode.SIG_FIG: 'sig_fig'>,
 'precision': 4,
 'format_mode': <FormatMode.ENGINEERING_SHIFTED: 'engineering_shifted'>,
 'capital_exp_char': False,
 'exp': <class 'sciform.modes.AutoExp'>,
 'use_prefix': False,
 'extra_si_prefixes': {},
 'extra_iec_prefixes': {},
 'bracket_unc': False,
 'val_unc_match_widths': False,
 'bracket_unc_remove_dec_symb': False,
 'unc_pm_whitespace': True,
 'nan_include_exp': False,
 'val_unc_nan_include_exp': <class 'sciform.modes.AutoValUncNanIncludeExp'>}

The global default settings can be reset to the :mod:`sciform` defaults
using :func:`reset_global_defaults`.

>>> from sciform import reset_global_defaults
>>> reset_global_defaults()

There are also helper function for managing supported SI and IEC
prefixes:

* :func:`global_add_c_prefix()` add ``{-2: 'c'}`` to the
  ``extra_si_prefixes`` dictionary if there is not already a prefix
  assigned to ``-2``.
* :func:`global_add_small_si_prefixes()` adds any of ``{-2: 'c',
  -1: 'd', +1: 'da', +2: 'h'}`` to the ``extra_si_prefixes`` that do not
  already have assigned prefixes.
* :func:`global_reset_si_prefixes()` resets ``extra_si_prefixes`` to be
  empty.
* :func:`global_reset_iec_prefixes()` resets ``extra_iec_prefixes`` to
  be empty.

The global default settings can be temporarily modified using the
:class:`GlobalDefaultsContext` context manager.
This context manager accepts the same keyword arguments as
:class:`Formatter`.
Within the context of :class:`GlobalDefaultsContext` manager, the
global defaults take on the specified in put settings, but when the
context is exited, the global default settings revert to their previous
values.

>>> from sciform import GlobalDefaultsContext, sfloat
>>> snum = sfloat(0.0123)
>>> print(f'{snum:.2ep}')
1.23e-02
>>> with GlobalDefaultsContext(add_c_prefix=True):
...     print(f'{snum:.2ep}')
1.23 c

:class:`sfloat` objects load global settings when being *formatted*,
not initialized.
In contrast, :class:`Formatter` settings are configured and frozen when
the class is initialized.
Thus changing global default settings with :func:`set_global_defaults`
or with the :class:`GlobalDefaultsContext` will not change the behavior
of any :class:`Formatter` that was intantiated before the change, but it
will change :class:`sfloat` formatting.
Global configuration settings are, thus, most useful for controlling the
behavior of :class:`sfloat` formatting.
Global configuration settings (1) allow :class:`sfloat` format
specification strings to be shortened and simplified and (2) provide the
only means to modify the prefixes available for :class:`sfloat`
formatting.
