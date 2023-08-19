Examples
########

Test Cases
==========

The :mod:`sciform`
`test suite <https://github.com/jagerber48/sciform/tree/main/tests>`_
contains hundreds of example formatting test cases which showcase the
many available formatting options.

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
scalings between the value and uncertainty for each entry are
immediately clear.
