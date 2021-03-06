from functools import wraps
import shutil

import yaml

from . import __version__  # NOQA
from .compat import basestring  # NOQA
from .env import Env
from .npm import Npm
from .python import Python
from .shell import abort, run

DEFAULTS = {
    'ep': __version__,
    'run': 'honcho start',
    'dependencies': {},
    'env': {},
    'check': [],
    'setup': [],
    'publish': ['python setup.py sdist bdist_wheel upload'],
}


DEPENDENCY_HANDLERS = {
    'npm': Npm,
    'python': Python,
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

        for key in set(list(self.spec.keys()) + list(DEFAULTS.keys())):
            setattr(self, '_' + key, self.spec.get(key, DEFAULTS.get(key, [])))

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

    def do_check(fun):
        @wraps(fun)
        def wrapper(self, *args, **kwargs):
            if self.check():
                # pylint: disable=not-callable
                fun(self, *args, **kwargs)
            else:
                abort('[ERROR] Checks failed, mission aborted.')
        return wrapper

    def fail_fast(fun):
        @wraps(fun)
        def wrapper(self, *args, **kwargs):
            # pylint: disable=not-callable
            success = fun(self, *args, **kwargs)
            if not success:
                abort()
        return wrapper

    def run_entrypoint(self, entrypoint, **kwargs):
        try:
            method = getattr(self, entrypoint, None)
            if method:
                return method(**kwargs)
            else:
                commands = getattr(self, '_' + entrypoint)
                return self.wrapped_execution(commands)
        except AttributeError:
            abort('Entry point "{}" not found in EP file'.format(entrypoint))

    def clear(self):
        shutil.rmtree('.ep', ignore_errors=True)

    def check(self):
        env_checks = self.env.check()
        dep_checks = (all(map(lambda x: x.check(), self.dependencies)))
        check_commands = self._shell_run(self._check)
        return env_checks and dep_checks and check_commands

    def setup(self):
        success = True
        for deps in self.dependencies:
            deps.check()
            success = success and deps.setup()
        if self._setup:
            self._shell_run(self._setup)
        if not success:
            abort()

    @do_check
    @fail_fast
    def wrapped_execution(self, commands):
        return self._shell_run(commands)

    @fail_fast
    def publish(self):
        return self._shell_run(self._publish)

    def shell(self, command):
        self._shell_run([command])
