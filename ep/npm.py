import os

from .shell import error, run


class Npm(object):

    def __init__(self, spec):
        self._file = 'package.json'
        self._spec = spec

    def check(self):
        file_check = os.path.exists(self._file)
        if not file_check:
            error('File not found in path: {0}'.format(self._file))
        return file_check

    def setup(self):
        result = run('npm install')
        return result.succeeded
