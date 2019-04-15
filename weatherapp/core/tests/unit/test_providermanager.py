""" Unit tests for ProviderManager class """

import unittest

from weatherapp.core.providermanager import ProviderManager


class AnyCommand:
    """Class for tests"""
    pass


class ProviderManagerTestCase(unittest.TestCase):
    """Unit test case for provider manager"""

    def setUp(self):
        """Contain set up info for every single test."""
        self.provider_manager = ProviderManager()

    def test_load_commands(self):
        """Test _load_commands method for provider manager."""

        self.provider_manager.add('any', AnyCommand)

        message = 'An error occurs during the _load_commands method.'
        self.assertTrue(
            'accu' in self.provider_manager._commands, msg=message)
        self.assertTrue(
            'rp5' in self.provider_manager._commands, msg=message)
        self.assertFalse(
            'sinoptik' in self.provider_manager._commands, msg=message)


if __name__ == '__main__':
    unittest.main()
