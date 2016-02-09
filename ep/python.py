import hashlib
import os
import sys

from .shell import error, run


py_version = sys.version.split()[0]
ENV_DIR = '.ep/python'
REQS_HASH = '{0}/reqs.md5'.format(ENV_DIR)


class Python(object):

    def __init__(self, spec):
        if spec is None:
            spec = {}
        # By default, we match current python version
        self._version = spec.get('version', '==' + py_version)
        self._file = spec.get('file', 'requirements.txt')

    def check(self):
        from .version import match
        ver_check = match(py_version, self._version)
        if not ver_check:
            error('Expected python {0}, found {1}'.format(
                self._version, py_version
            ))

        file_check = os.path.exists(self._file)
        if not file_check:
            error('File not found in path: {0}'.format(self._file))

        try:
            with open(REQS_HASH) as f:
                reqs_hash = f.read()
            reqs_real_hash = self.hash_requirements(self._file)
            reqs_check = reqs_hash == reqs_real_hash
        except Exception:
            reqs_check = False
        if not reqs_check:
            error('Outdated Python requirements, need to run setup')

        return ver_check and file_check and reqs_check

    def setup(self):
        reqs_hash = Python.hash_requirements(self._file)
        commands = [
            'mkdir -p {0}'.format(ENV_DIR),
            'virtualenv --python `which python` {0}'.format(ENV_DIR),
            '{0}/bin/pip install -r {1}'.format(ENV_DIR, self._file),
            '.ep/python/bin/pip install honcho',
        ]
        success = all(map(lambda c: run(c).succeeded, commands))
        if success:
            with open(REQS_HASH, 'w') as f:
                f.write(reqs_hash)
        return success

    @staticmethod
    def read_requirements(filename):
        """
        Recursively read all requirements from a pip requirements file.

        Return a sorted list with only the libraries and versions, so that the
        output (and MD5 checksum) won't change if we just shuffle requirements
        around or edit comments.

        """
        dependencies = []
        dirname = os.path.dirname(filename)

        with open(filename, 'r') as f:
            for dependency in f.readlines():
                # Remove comments and whitespace
                dependency = dependency.split('#')[0].strip()

                if dependency.startswith('-r '):
                    include = os.path.join(dirname, dependency.split()[1])
                    dependencies += Python.read_requirements(include)
                elif dependency and not dependency.startswith('--'):
                    dependencies.append(dependency)
        return sorted(dependencies)

    @staticmethod
    def hash_requirements(filename):
        dependencies = Python.read_requirements(filename)
        as_text = "\n".join(dependencies).encode('utf-8')
        return hashlib.md5(as_text).hexdigest()
