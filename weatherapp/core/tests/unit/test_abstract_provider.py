""" Unit tests for abstract provider class """

import unittest

from weatherapp.core.abstract import WeatherProvider


class AbstractProviderTestCase(unittest.TestCase):
    """Unit test case for abstract WeatherProvider class"""

    def test_get_request_headers(self):
        """ Test get_request_headers method """

        self.headers = WeatherProvider.get_request_headers()
        
        self.assertEqual(self.headers, 
            {'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64)'})
        self.assertNotEqual(self.headers, {'User-Agent': 'Any'})
    def test_get_configuration_file(self):
        """ Test getting the path to the configuration file """

        self.config_path = WeatherProvider.get_configuration_file()
        self.assertIsNotNone(self.config_path)



if __name__ == '__main__':
    unittest.main()
