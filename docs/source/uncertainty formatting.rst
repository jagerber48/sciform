Uncertainty Formatting
######################

One of, if not the, most important use cases for scientific formatting
is formatting a value together with its specified uncertainty, e.g.
``84.3 +/- 0.2``.
We attempt to follow
`BIPM <https://www.bipm.org/documents/20126/2071204/JCGM_100_2008_E.pdf/cb0ef43f-baa5-11cf-3f85-4dcd86f77bd6>`_
or `NIST <https://www.nist.gov/pml/nist-technical-note-1297>`_
recomendations for conventions when possible.



The ability to format pairs of floats as
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
