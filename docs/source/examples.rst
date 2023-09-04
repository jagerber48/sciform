Examples
########

.. module:: sciform
   :noindex:

Test Cases
==========

The :mod:`sciform`
`test suite <https://github.com/jagerber48/sciform/tree/main/tests>`_
contains hundreds of example formatting test cases which showcase the
many available formatting options.

Formatter
=========

Here are a small selection of examples which demonstrate some of the
available formatting options.

>>> from sciform import (FormatOptions, Formatter, ExpMode, RoundMode,
...                      SignMode, GroupingSeparator, ExpFormat)
>>> num = 12345.54321
>>> sform = Formatter(FormatOptions(
...             exp_mode=ExpMode.SCIENTIFIC,
...             round_mode=RoundMode.SIG_FIG,
...             ndigits=4))
>>> print(sform(num))
1.235e+04
>>> sform = Formatter(FormatOptions(
...             exp_mode=ExpMode.ENGINEERING,
...             round_mode=RoundMode.DEC_PLACE,
...             ndigits=10,
...             sign_mode=SignMode.SPACE,
...             superscript_exp=True))
>>> print(sform(num))
 12.3455432100×10³
>>> sform = Formatter(FormatOptions(
...             exp_mode=ExpMode.FIXEDPOINT,
...             upper_separator=GroupingSeparator.SPACE,
...             decimal_separator=GroupingSeparator.COMMA,
...             lower_separator=GroupingSeparator.UNDERSCORE,
...             sign_mode=SignMode.ALWAYS))
>>> print(sform(num))
+12 345,543_21

>>> num = 0.076543
>>> sform = Formatter(FormatOptions(
...             exp_mode=ExpMode.SCIENTIFIC,
...             exp_val=-3,
...             exp_format=ExpFormat.PARTS_PER,
...             add_ppth_form=True))
>>> print(sform(num))
76.543 ppth
>>> sform = Formatter(FormatOptions(
...             exp_mode=ExpMode.SCIENTIFIC,
...             exp_val=-2,
...             exp_format=ExpFormat.PREFIX,
...             add_c_prefix=True))
>>> print(sform(num))
7.6543 c
>>> sform = Formatter(FormatOptions(
...             exp_mode=ExpMode.SCIENTIFIC,
...             exp_val=-6,
...             exp_format=ExpFormat.PREFIX))
>>> print(sform(num))
76543 μ
>>> sform = Formatter(FormatOptions(
...             exp_mode=ExpMode.PERCENT))
>>> print(sform(num))
7.6543%

>>> num = 3141592.7
>>> unc = 1618
>>> sform = Formatter()
>>> print(sform(num, unc))
3141593 +/- 1618
>>> sform = Formatter(FormatOptions(
...             exp_mode=ExpMode.ENGINEERING,
...             exp_format=ExpFormat.PREFIX,
...             pdg_sig_figs=True,
...             unicode_pm=True,
...             unc_pm_whitespace=False))
>>> print(sform(num, unc))
(3.1416±0.0016) M

>>> num = 314159.27
>>> unc = 1618
>>> sform = Formatter(FormatOptions(
...             exp_mode=ExpMode.ENGINEERING_SHIFTED,
...             pdg_sig_figs=True,
...             bracket_unc=True))
>>> print(sform(num, unc))
(0.3142(16))e+06

SciNum, SciNumUnc, and Global Options
=====================================

Here are a small selection of examples which demonstrate some of the
available string formatting options.
Note that many options are not available through the :ref:`fsml`, so
these options must be selected by configuring the global default options
during formatting.
Here this is done using the :class:`GlobalDefaultsContext` context
manager, but this could have been done using :func:`set_global_defaults`
instead.

>>> from sciform import SciNum, SciNumUnc, GlobalDefaultsContext
>>> snum = SciNum(12345.54321)
>>> print(f'{snum:!4e}')
1.235e+04
>>> print(f'{snum: .10r}')
 12.3455432100e+03
>>> print(f'{snum:+s,_}')
+12 345,543_21

>>> snum = SciNum(0.076543)
>>> with GlobalDefaultsContext(FormatOptions(
...         exp_format=ExpFormat.PARTS_PER,
...         add_ppth_form=True)):
...     print(f'{snum:ex-3}')
76.543 ppth
>>> with GlobalDefaultsContext(FormatOptions(
...             exp_format=ExpFormat.PREFIX,
...             add_c_prefix=True)):
...     print(f'{snum:ex-2}')
7.6543 c
>>> with GlobalDefaultsContext(FormatOptions(
...             exp_mode=ExpMode.SCIENTIFIC,
...             exp_val=-6,
...             exp_format=ExpFormat.PREFIX)):
...     print(f'{snum:ex-6}')
76543 μ
>>> print(f'{snum:%}')
7.6543%

>>> num_unc = SciNumUnc(3141592.7, 1618)
>>> print(f'{num_unc}')
3141593 +/- 1618
>>> with GlobalDefaultsContext(FormatOptions(
...             pdg_sig_figs=True,
...             unicode_pm=True,
...             unc_pm_whitespace=False)):
...     print(f'{num_unc:rp}')
(3.1416±0.0016) M

>>> num_unc = SciNumUnc(314159.27, 1618)
>>> with GlobalDefaultsContext(FormatOptions(
...             pdg_sig_figs=True)):
...     print(f'{num_unc:#r()}')
(0.3142(16))e+06

Plotting and Tabulating Fit Data
================================

We are given 3 data sets:

.. collapse:: Data

   .. literalinclude:: ../../examples/data/fit_data.json
      :language: json

We want to perform quadratic fits to these data sets, visualize
the results, and print the best fit parameters including the uncertainty
reported by the fit routine.
For these tasks we will require the ``numpy``, ``scipy``,
``matplotlib``, and ``tabulate`` packages.

Without ``sciform``
-------------------

Without ``sciform`` we can perform the fit and plot the data and best
fit lines and print out a table of best fit parameters and
uncertainties:

.. collapse:: Code

   .. literalinclude:: ../../examples/fit_plot_no_sciform.py
      :language: python

This produces the plot:

.. image:: ../../examples/outputs/fit_plot_no_sciform.png
  :width: 400

And the table:

.. literalinclude:: ../../examples/outputs/fit_plot_no_sciform_table.txt
   :language: python

This plot and table suffer from a number of shortcomings which impede
human readability.

- In the table, the exponents for the values and uncertainties differ,
  making it hard to identify the significant digits of the value.
- The number of digits displayed for the values is not correlated with
  the uncertainty for that value. For example, the ``y0`` values are
  shown with precision to the 10\ :sup:`+8` place, but the uncertainty
  indicates precision down to the 10\ :sup:`+3` place.
- In the table, the exponents vary from one dataset to the next. It is
  hard to see these differences at a glance.
- The tick labels on the plot are illegible because each value has so
  many digits.

Of course, even without :mod:`sciform`, it would be possible to make
manual adjustments to the plot and the table to improve these data
visualizations.
However, :mod:`sciform` will allow us to make the required changes in a
general and automated way.

With ``sciform``
----------------

We can address these problems using :mod:`sciform` by:

#. Using prefix scientific notation to label the plot axes.
   This will greatly reduce the number of symbols needed for each tick
   value.
#. Using value/uncertainty formatting in the table to collapse the value
   and error column pairs into individual columns.
   This will make obvious the relative scale between the uncertainty and
   the value.
   Using ``sciform``, the significant digits displayed for the value
   will always match the precision of the uncertainty.
   We will use bracket uncertainty format.
#. Using engineering notation for the value/uncertainty in the table. This
   will make the relative scale between different rows obvious.

To do this we import :mod:`sciform` and make some helper functions for
displaying the plot axes as described:

.. collapse:: Code

    .. literalinclude:: ../../examples/fit_plot_with_sciform.py
      :language: python

This produces the plot:

.. image:: ../../examples/outputs/fit_plot_with_sciform.png
  :width: 400

and the table:

.. literalinclude:: ../../examples/outputs/fit_plot_with_sciform_table.txt
   :language: python

We can see the plot and table are immediately much more legible.
Less characters are needed to communicate the data in both
visualizations.
The relative scaling of parameters between datasets and the relative
scaling between the value and uncertainty for each entry are
immediately clear.
