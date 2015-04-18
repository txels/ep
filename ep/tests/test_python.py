from unittest import TestCase

from ..python import Python


class TestPython(TestCase):

    def test_version_and_requirements(self):
        spec = {
            'version': '>=2.3.4',
            'file': 'requirements/test.txt'
        }
        py = Python(spec)
        self.assertTrue(py.check())

    def test_version_not_matched(self):
        spec = {
            'version': '==2.9.4',
        }
        py = Python(spec)
        self.assertFalse(py.check())

    def test_requirements_missing(self):
        spec = {
            'file': 'non_existing_requirements.txt'
        }
        py = Python(spec)
        self.assertFalse(py.check())

    def test_requirements_changed(self):
        spec = {
            'file': 'ep/samples/changed_requirements.txt'
        }
        py = Python(spec)
        self.assertFalse(py.check())
