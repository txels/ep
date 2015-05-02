from unittest import TestCase

from ..cli import Commands
from .mocks import MockEP


ARGS_EP_SHELL = {
    '--file': None,
    '--help': False,
    '--version': False,
    '<command>': 'coverage run --help',
    'check': False,
    'clear': False,
    'publish': False,
    'run': False,
    'setup': False,
    'shell': True
}


ARGS_EP_RUN = {
    '--file': None,
    '--help': False,
    '--version': False,
    '<command>': None,
    'check': False,
    'clear': False,
    'publish': False,
    'run': True,
    'setup': False,
    'shell': False
}


class TestCli(TestCase):

    def test_process_invokes_with_passthrough(self):
        ep = MockEP()

        Commands.process(ep, ARGS_EP_SHELL)

        self.assertEquals(
            ep.calls,
            [('shell', {'command': 'coverage run --help'})]
        )

    def test_process_filters_none_values(self):
        ep = MockEP()

        Commands.process(ep, ARGS_EP_RUN)

        self.assertEquals(
            ep.calls,
            [('run', {})]
        )
