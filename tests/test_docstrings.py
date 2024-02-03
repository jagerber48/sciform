import doctest

from sciform import formatter, output_conversion, scinum


def load_tests(loader, tests, ignore):  # noqa: ARG001
    tests.addTests(doctest.DocTestSuite(formatter))
    tests.addTests(doctest.DocTestSuite(scinum))
    tests.addTests(doctest.DocTestSuite(output_conversion))
    return tests
