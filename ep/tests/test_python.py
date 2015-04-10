from unittest import TestCase

from ..python import PythonDependencies


class TestPython(TestCase):

    def test_version(self):
        spec = {
            'version': '>=2.3.4'
        }
        py = PythonDependencies(spec)
        self.assertTrue(py.check())

    def test_requirements(self):
        spec = {
            'file': 'ep/samples/some_requirements.txt'
        }
        py = PythonDependencies(spec)
        self.assertTrue(py.check())

    def test_requirements_missing(self):
        spec = {
            'file': 'non_existing_requirements.txt'
        }
        py = PythonDependencies(spec)
        self.assertFalse(py.check())
