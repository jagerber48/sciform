Uncertainty Formatting
######################

One of, if not the, most important use cases for scientific formatting
is formatting a value together with its specified uncertainty, e.g.
``84.3 +/- 0.2``. The ability to format pairs of floats as
value/uncertainty pairs will be supported by the forthcoming ``ufloat``
class.

Value/uncertainty formatting is not yet fully implemented or tested, but
it will support

* Selection of the exponent based on the value
* Selection of the least significant digit based on a user-requested
  number of sig figs to display for the uncertainty.
* Optional padding so that the value and uncertainty have the same
  width
* Short form "parentheses" uncertainty display, e.g.
  ``84.3 +/- 2= 84.3(2)``.
