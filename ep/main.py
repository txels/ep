from functools import wraps
import shutil

import yaml

from . import __version__
from .env import Env
from .npm import NpmDependencies
from .python import PythonDependencies
from .shell import run

try:
    basestring        # added in Python 2.3
except NameError:
    basestring = str


DEFAULTS = {
    'ep': __version__,
    'run': 'honcho start',
    'check': [],
    'dependencies': {},
    'env': {},
}


DEPENDENCY_HANDLERS = {
    'npm': NpmDependencies,
    'python': PythonDependencies,
}


class EP(object):

    def __init__(self, filename):
        """
        Parse the ep yaml file.

        Store all higher level ep.yml properties in attributes starting with _
        E.g. _run, _version...
        """
        with open(filename) as f:
            self.spec = yaml.load(f)

        for key, default in DEFAULTS.items():
            setattr(self, '_' + key, self.spec.get(key, default))

        self.dependencies = self._parse_dependencies(self._dependencies)
        self.env = self._parse_environment(self._env)

        for attr in ['_run', '_check']:
            val = getattr(self, attr)
            if isinstance(val, basestring):
                setattr(self, attr, [val])

    def _parse_dependencies(self, dependencies):
        handlers = []
        for dependency_type in dependencies:
            if isinstance(dependency_type, dict):
                dependency_type, value = list(dependency_type.items())[0]
            else:
                value = None

            handler = DEPENDENCY_HANDLERS[dependency_type]
            handlers.append(handler(value))

        return handlers

    def _parse_environment(self, environment):
        return Env(environment)

    def _shell_run(self, commands):
        if commands:
            commands = ' && '.join(commands)
            result = run(
                '. .ep/python/bin/activate && {0}'.format(commands)
            )
            return result.succeeded
        else:
            return True

    def clear(self):
        shutil.rmtree('.ep', ignore_errors=True)

    def check(self):
        env_checks = self.env.check()
        dep_checks = (all(map(lambda x: x.check(), self.dependencies)))
        check_commands = self._shell_run(self._check)
        return env_checks and dep_checks and check_commands

    def do_check(fun):
        @wraps(fun)
        def wrapper(self, *args, **kwargs):
            if self.check():
                fun(self, *args, **kwargs)
            else:
                print('[ERROR] Checks failed, mission aborted.')
                exit(1)
        return wrapper

    def setup(self):
        success = True
        for deps in self.dependencies:
            deps.check()
            success = success and deps.setup()
        if not success:
            exit(1)

    @do_check
    def run(self):
        success = self._shell_run(self._run)
        if not success:
            exit(1)
