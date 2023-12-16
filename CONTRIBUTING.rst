How to Contribute
=================

Contributions to ``sciform`` are welcome.
Here are some ways you can contribute:

* Create a
  `discussion topic <https://github.com/jagerber48/sciform/discussions>`_
  if you have an idea for a new feature or a general topic for
  discussion.
* Create an `issue <https://github.com/jagerber48/sciform/issues>`_ if
  you find a bug with ``sciform`` or another challenge with the package.
* If you would like to make improvements to the source code or
  documentation then you may do so directly by opening a
  `pull request <https://github.com/jagerber48/sciform/pulls>`_.

The current main goal for the development of ``sciform`` is
stabilization of the public user interface.
To this end, ``sciform`` is seeking feedback/suggestions about
ease-of-use for the user interface as well as naming suggestions for the
various objects and options that users interact with.
While stabilizing the interface will take precedence for the time being,
new feature requests are always welcome!

Development Details
-------------------

* Begin development work on ``sciform`` by forking and installing the
  `git repository <https://github.com/jagerber48/sciform>`_ and
  installing the development dependencies in editable mode with::

     python -m pip install -e .[dev]
* Tests can be run using::

     python -m unittest
* ``sciform`` is formatted using the
  `ruff linter and formatter <https://docs.astral.sh/ruff/>`_.
  Code should pass the following checks with no errors::

     ruff check .
     ruff format . --check
