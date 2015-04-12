import os
from unittest import TestCase

from ..env import Env


class TestEnv(TestCase):

    def tearDown(self):
        try:
            del os.environ['A_HOST']
        except:
            pass

    def test_found(self):
        os.environ['A_HOST'] = 'localhost'
        spec = {
            'A_HOST': {'help': 'A hostname'}
        }
        env = Env(spec)
        self.assertTrue(env.check())

    def test_not_found(self):
        spec = {
            'A_HOST': {'help': 'A hostname'}
        }
        env = Env(spec)
        self.assertFalse(env.check())

    def test_not_found_with_default(self):
        spec = {
            'A_HOST': {'default': 'default_localhost'}
        }
        env = Env(spec)
        self.assertTrue(env.check())
        self.assertEqual(os.environ['A_HOST'], 'default_localhost')
