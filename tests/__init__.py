import unittest
from math import isnan


class NanTestCase(unittest.TestCase):
    def assertNanEqual(self, first, second, msg=None):  # noqa: N802
        if isnan(first):
            self.assertTrue(isnan(second), msg=msg)
        else:
            self.assertEqual(first, second, msg=msg)
