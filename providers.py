""" Weather providers
"""
import config

class AccuWeatherProvider:
    """ Weather provider for AccuWeather site.
    """
    
    def __init__(self):
        #TODO: Determine the use of the provider name
        self.name = config.ACCU_PROVIDER_NAME

    def get_configuration(self):
        """ Get configuration from file
        """

        name = DEFAULT_NAME
        
        if provider == 'accu':
            url = ACCU_DEFAULT_URL
        elif provider == 'rp5':
            url = RP5_DEFAULT_URL

        parser = configparser.ConfigParser(strict=False, interpolation=None)
        parser.read(get_configuration_file())

        if provider in parser.sections():
            config = parser[provider]
            name, url = config['name'], config['url']
        return name, url
