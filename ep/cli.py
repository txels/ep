from docopt import docopt

from . import __version__  # NOQA
from .main import EP
from .shell import graceful_ctrlc


COMMANDS = ['clear', 'setup', 'check', 'run', 'shell', 'publish']

USAGE = """
Welcome to ep {version}

Usage:
  ep clear
  ep check [--file=<FILE>]
  ep setup [--file=<FILE>]
  ep run [--file=<FILE>]
  ep publish [--file=<FILE>]
  ep shell <command> [--file=<FILE>]
  ep --version
  ep -h | --help

Options:
  -h, --help               show this help message and exit
  --version                Show version
  -f FILE, --file=FILE     Load spec from file

""".format(version=__version__)


class Commands(object):
    """
    The commands that are installed as entry points in setup.py

    This CLI parser parses command-line options, deals with -f|--file,
    --version and --help, and passes all the rest through to `ep.main.EP`.
    It does so by calling methods in EP that match the first argument.
    Additional arguments are passed as keyword arguments to the EP methods.

    E.g.:
        ep shell <command> [--file=<FILE>]

        ep shell "pip list"

    Will result in a call to ``ep.shell(command="pip list")`` where ``ep`` is
    an instance of ``EP``.

    """
    @staticmethod
    @graceful_ctrlc
    def main():
        args = docopt(USAGE, version=__version__)
        ep = Commands.parse_yml(args)
        Commands.process(ep, args)

    @staticmethod
    def parse_yml(args):
        filename = args['--file'] or 'ep.yml'
        return EP(filename)

    @staticmethod
    def process(ep, args):
        for command in COMMANDS:
            if args[command]:
                method = getattr(ep, command)

                # Create kwargs by stripping out angle brackets and filtering
                # out empty arguments (docopt includes None values for those)
                kwargs = dict([
                    (arg[1:-1], args[arg])
                    for arg in filter(lambda x: x.startswith('<'), args)
                    if args[arg] is not None
                ])

                method(**kwargs)
