from unittest import TestCase

from ..main import EP


class TestParsing(TestCase):

    def test_yaml_parsing(self):
        ep = EP('ep/samples/example.yml')
        self.assertEqual(2, len(ep.env))
        self.assertEqual(1, len(ep.dependencies))
        self.assertEqual(['echo "Hello World"'], ep._run)

    def test_yaml_parsing_defaults(self):
        ep = EP('ep/samples/defaults.yml')
        self.assertEqual(1, len(ep.env))
        self.assertEqual(5555, ep.env[0].default)
        self.assertEqual('A number between 5000 and 7000', ep.env[0].help)

    def test_yaml_parsing_multiple_run_commands(self):
        ep = EP('ep/samples/multi-run.yml')
        self.assertListEqual(
            ['echo "Hello World, I will go to sleep for 3 seconds..."',
             'sleep 3',
             'git status'
             ],
            ep._run
        )

    def test_self_ep_yml(self):
        ep = EP('ep.yml')
        self.assertTrue(ep.check())

    def test_arbitrary_entrypoints(self):
        ep = EP('ep/samples/arbitrary-entrypoint.yml')
        self.assertListEqual(
            ['sleep 10',
             'sleep 20',
             ],
            ep._procrastinate
        )
