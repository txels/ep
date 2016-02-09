import os

from .shell import error, output, warning


class EnvVar(object):
    "An environment variable"

    def __init__(self, name, definition):
        self.name = name
        self.default = definition.get('default')
        self.help = definition.get('help')

    def __str__(self):
        value = self.name
        if self.default:
            value += ' [{0}]'.format(self.default)
        return value

    def __repr__(self):
        return '<EnvVar: {0}>'.format(str(self))

    def check(self):
        value = os.environ.get(self.name)
        if value is None:
            if self.default:
                warning('Variable {0} not set, defaulting to {1}'.format(
                    self.name, self.default
                ))
                os.environ[self.name] = str(self.default)
            else:
                error('Variable {0} not set\n - {1}'.format(
                    self.name, self.help
                ))
                return False
        else:
            output('{0}={1}'.format(self.name, value))

        return True


class Env(list):
    "A list of environment variables"

    def __init__(self, spec):
        super(Env, self).__init__()
        for name, definition in spec.items():
            self.append(EnvVar(name, definition))

    def check(self):
        return (all(map(lambda x: x.check(), self)))
