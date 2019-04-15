import unittest
import io

from weatherapp.core.app import App


class CommandsTestCase(unittest.TestCase):

    """ Test case for commands tests.
    """

    def test_providers(self):
        """ Test providers command.
        """

        stdout = io.StringIO()
        App(stdout=stdout).run(['providers'])
        stdout.seek(0)
        self.assertEqual(stdout.read(), 'AccuWeather: accu\nRP5: rp5\n')


if __name__ == '__main__':
    unittest.main()
