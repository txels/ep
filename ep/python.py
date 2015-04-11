import os
import sys

from .shell import run
from .version import match


py_version = sys.version.split()[0]


class PythonDependencies(object):

    def __init__(self, spec):
        if spec is None:
            spec = {}
        # By default, we match current python version
        self._version = spec.get('version', '==' + py_version)
        self._file = spec.get('file', 'requirements.txt')

    def check(self):
        ver_check = match(py_version, self._version)
        if not ver_check:
            print('Expected python {0}, found {1}'.format(
                self._version, py_version
            ))
        file_check = os.path.exists(self._file)
        if not file_check:
            print('File not found in path: {0}'.format(self._file))
        return ver_check and file_check

    def setup(self):
        run('mkdir -p .ep/python')
        run('virtualenv .ep/python')
        run('.ep/python/bin/pip install -r {0}'.format(self._file))
        run('.ep/python/bin/pip install honcho')
