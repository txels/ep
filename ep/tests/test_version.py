from unittest import TestCase

from ..version import match


class TestVersion(TestCase):

    def test_equal(self):
        self.assertTrue(match('2.7.4', '==2.7.4'))

    def test_not_equal(self):
        self.assertFalse(match('2.6.4', '==2.7.4'))

    def test_family_equal(self):
        self.assertTrue(match('2.7.5', '>=2.7.0, <2.8.0'))

    def test_family_not_equal(self):
        self.assertFalse(match('1.2.3', '>=2.7.0, <2.8.0, ==1.2.2'))
