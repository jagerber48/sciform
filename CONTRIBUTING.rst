How to Contribute
=================

Contributions to ``sciform`` are welcome.
Here are some ways you can contribute:

* Fill out `the user experience survey <https://forms.gle/TkkKgywYyEMKu9U37>`_.
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
ease-of-use for the user interface and suggested changes to code
behaviors and naming choices.
New feature requests are always welcome!

Development Details
-------------------

* Begin development work on ``sciform`` by forking and cloning the
  `git repository <https://github.com/jagerber48/sciform>`_ and
  installing the development dependencies in editable mode with::

     python -m pip install -e ".[dev]"
* Tests can be run using::

     python -m unittest
* ``sciform`` is formatted using the
  `ruff linter and formatter <https://docs.astral.sh/ruff/>`_.
  Code should pass the following checks with no errors::

     ruff check .
     ruff format . --check

* ``sciform`` is configured so that you can perform the linting and
  formatting checks using ``git`` pre-commit hooks using
  `pre-commit <https://pre-commit.com/>`_.
  One way to set this up is to run the following commands in the package
  base directory with no virtual environment activated::

     python -m pip install --user pipx
     pipx ensurepath
     pipx install pre-commit
     pre-commit install

  This will install ``pre-commit`` into a globally available virtual
  environment on your system using ``pipx`` so that it is globally
  available anywhere you may run ``git`` commands.
  The last command configures the ``sciform`` repo to utilize the
  pre-configured pre-commit hooks.
  An alternative is to install ``pre-commit`` directly into your base
  python installation using ``pip``.
  Another alternative is to install ``pre-commit`` into the local
  virtual environment.
  In this last case you will always need to activate the virtual
  environment before running ``git`` commands.
* After making code changes please document your changes in the
  ``CHANGELOG.rst`` file and, if there are any changed or new behaviors,
  include appropriate unit test and documentation updates.
