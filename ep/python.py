import os
import sys

from .shell import run


py_version = sys.version.split()[0]


class PythonDependencies(object):

    def __init__(self, spec):
        self.version = spec.get('version', py_version)
        self._file = spec.get('file', 'requirements.txt')

    def check(self):
        ver_check = self.version == py_version
        if not ver_check:
            print('Expected python {0}, found {1}'.format(
                self.version, py_version
            ))
        file_check = os.path.exists(self._file)
        if not file_check:
            print('File not found in path: {}'.format(self._file))
        return ver_check and file_check

    def install(self):
        run('mkdir -p .ep/python')
        run('virtualenv .ep/python')
        run('.ep/python/bin/pip install -r {}'.format(self._file))
        run('.ep/python/bin/pip install honcho')
