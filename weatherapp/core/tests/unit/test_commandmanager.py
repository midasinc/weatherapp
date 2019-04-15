""" Unit tests for CommandManager class """

import unittest

from weatherapp.core.commandmanager import CommandManager


class AnyCommand:
    """Class for tests"""
    pass


class CommandManagerTestCase(unittest.TestCase):
    """Unit test case for command manager"""

    def setUp(self):
        """Contain set up info for every single test."""
        self.command_manager = CommandManager()
        self.command_manager.add('any', AnyCommand)

    def test_add(self):
        """Test add method for command manager."""

        message = "Command 'any' is missing in command manager"

        self.assertTrue(
            'any' in self.command_manager._commands, msg=message)
        self.assertEqual(
            self.command_manager.get('any'), AnyCommand, msg=message)


    def test_load_commands(self):
        """Test _load_commands method for command manager."""

        message = 'An error occurs during the _load_commands method.'
        self.assertTrue(
            'configurate' in self.command_manager._commands, msg=message)
        self.assertTrue(
            'providers' in self.command_manager._commands, msg=message)

    def test_get(self):
        """Test get method for command manager."""

        self.assertEqual(self.command_manager.get('any'), AnyCommand)
        self.assertIsNone(self.command_manager.get('bar'), AnyCommand)

    def test_contains(self):
        """Test if '__contains__' method is working."""

        self.assertTrue('any' in self.command_manager)
        self.assertFalse('bar' in self.command_manager)


if __name__ == '__main__':
    unittest.main()
