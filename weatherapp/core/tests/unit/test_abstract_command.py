""" Unit tests for abstract command class """

import argparse
import unittest

from weatherapp.core.abstract import Command


class AbstractCommandTestCase(unittest.TestCase):
    """Unit test case for abstract command class"""

    def test_get_parser(self):
        """Test get parser method"""

        self.parser = Command.get_parser()
        self.assertIsInstance(self.parser, argparse.ArgumentParser)




if __name__ == '__main__':
    unittest.main()
