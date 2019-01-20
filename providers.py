""" Weather providers
"""
import configparser
import config


class AccuWeatherProvider:
    """ Weather provider for AccuWeather site.
    """
    
    def __init__(self):
        self.name = config.ACCU_PROVIDER_NAME
        
        #TODO: check url, location <=> name, url
        url, location = self.get_configuration()
        self.location = location
        self.url = url

    def get_configuration(self):
        """ Get configuration from file
        """

        name = config.DEFAULT_NAME
        url = config.ACCU_DEFAULT_URL
        parser = configparser.ConfigParser(strict=False, interpolation=None)

        parser.read(self.get_configuration_file())

        if self.name in parser.sections():
            config = parser[self.name]
            name, url = config['name'], config['url']
        return name, url
