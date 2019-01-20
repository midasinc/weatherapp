""" Weather providers
"""

from pathlib import Path
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

    def get_configuration_file(self):
        """ Getting the path to the configuration file
        """
        return Path.cwd() / config.CONFIG_FILE

    def get_configuration(self, provider):
        """ Get configuration from file
        """
        #FIXME: Check provider use

        name = config.DEFAULT_NAME
        url = config.ACCU_DEFAULT_URL
        parser = configparser.ConfigParser(strict=False, interpolation=None)

        parser.read(self.get_configuration_file())

        if provider in parser.sections():
            config = parser[provider]
            name, url = config['name'], config['url']
        return name, url

    def save_configuration(self, provider, name, url):
        """ Save configuration to file
        """
        #FIXME: Check provider use
        
        parser = configparser.ConfigParser(strict=False, interpolation=None)
        parser.add_section(provider)

        config_file = self.get_configuration_file()

        if config_file.exists():
            parser.read(config_file)

        parser[provider] = {'name': name, 'url': url}

        with open(self.get_configuration_file(), 'w') as configfile:
            parser.write(configfile)

    def get_request_headers(self):
        """ Return custom headers for url requests.
        """

        return {'User-Agent': config.FAKE_MOZILLA_AGENT}



