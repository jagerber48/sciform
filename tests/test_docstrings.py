import doctest

from sciform import formatter, output_conversion, scinum
from sciform.options import input_options, populated_options


def load_tests(loader, tests, ignore):  # noqa: ARG001
    tests.addTests(doctest.DocTestSuite(formatter))
    tests.addTests(doctest.DocTestSuite(scinum))
    tests.addTests(doctest.DocTestSuite(output_conversion))
    tests.addTests(doctest.DocTestSuite(input_options))
    tests.addTests(doctest.DocTestSuite(populated_options))
    return tests
