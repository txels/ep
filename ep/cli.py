from docopt import docopt

from . import __version__
from .main import EP

USAGE = """
Welcome to ep {0}

Usage:
  ep clear
  ep check [--file=<FILE>]
  ep setup [--file=<FILE>]
  ep run [--file=<FILE>]
  ep --version
  ep -h | --help

Options:
  -h, --help               show this help message and exit
  --version                Show version
  -f FILE, --file=FILE     Load spec from file

""".format(__version__)


class Commands(object):
    """
    The commands that are installed as entry points in setup.py

    """
    @staticmethod
    def main():
        args = docopt(USAGE, version=__version__)

        filename = args['--file'] or 'ep.yml'
        ep = EP(filename)

        for command in ['clear', 'check', 'setup', 'run']:
            if args[command]:
                getattr(ep, command)()
