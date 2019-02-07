""" Abstract classes for project
"""

import abc
import argparse
import configparser
import hashlib
import time
from pathlib import Path

import requests

import config


class Command(abc.ABC):
    """ Base class for commands.

    :param app: Main application instance
    :type app: `app.App`
    """

    def __init__(self, app):
        self.app = app

    @staticmethod
    def get_parser():
        """ Initialize argument parser for command.
        """
        parser = argparse.ArgumentParser()
        return parser

    @abc.abstractmethod
    def run(self, argv):
        """ Invoked by application when the command is run.
            Should be overridden in subclass.
        """


class WeatherProvider(Command):
    """ Weather provider abstract class.

        Defines behavior for all weather providers.
    """

    def __init__(self, app):
        super().__init__(app)

        location, url = self._get_configuration()
        self.location = location
        self.url = url

    @abc.abstractmethod
    def get_name(self):
        """ Provider name
        """

    @abc.abstractmethod
    def get_default_location(self):
        """ Default location name
        """

    @abc.abstractmethod
    def get_default_url(self):
        """ Defalt location url
        """

    @abc.abstractmethod
    def configurate(self):
        """ Performs provider configuration.
        """

    @abc.abstractmethod
    def get_weather_info(self, content):
        """ Collects weather information.

        Gets weather information from source and produce it in
        the following format.

        weather_info = {
            'cond':        ''  # weather condition
            'temp':        ''  # temperature
            'feels_like':  ''  # feels like temperature
            'wind':        ''  # information about wind
        }
        """

    @staticmethod
    def get_configuration_file():
        """ Getting the path to the configuration file
        """

        return Path.cwd() / config.CONFIG_FILE

    def _get_configuration(self):
        """ Get configuration from file
        
        :return: Return the name of the selected place (city) and url
        :rtype: tuple
        """
        provider = self.get_name()
        name = self.get_default_location()
        url = self.get_default_url()
        
        parser = configparser.ConfigParser(strict=False, interpolation=None)

        parser.read(self.get_configuration_file())

        if provider in parser.sections():
            location_config = parser[provider]
            name, url = location_config['name'], location_config['url']

        return name, url

    def save_configuration(self, provider, name, url):
        """ Save configuration to file

        :param provider: provider id
        :param type: str

        :param name: city name
        :param type: str

        :param url: Preferred location URL
        :param type: str
        """

        parser = configparser.ConfigParser(strict=False, interpolation=None)
        parser.add_section(provider)

        config_file = self.get_configuration_file()

        if config_file.exists():
            parser.read(config_file)

        parser[provider] = {'name': name, 'url': url}

        with open(self.get_configuration_file(), 'w') as configfile:
            parser.write(configfile)

    @staticmethod
    def get_request_headers():
        """ Return custom headers for url requests.
        """

        return {'User-Agent': config.FAKE_MOZILLA_AGENT}

    @staticmethod
    def get_url_hash(url):
        """ Generate url hash.
        """

        return hashlib.md5(url.encode('utf-8')).hexdigest()

    @staticmethod
    def get_cache_directory():
        """ Path to cache directory
        """
        return Path.cwd() / config.CACHE_DIR

    @staticmethod
    def is_valid(path):
        """ Check if current cache file is valid
        """

        return (time.time() - path.stat().st_mtime) < config.CACHE_TIME

    def get_cache(self, url):
        """ Return cache by given url address if any.
        """

        cache = b''
        url_hash = self.get_url_hash(url)
        cache_dir = self.get_cache_directory()
        if cache_dir.exists():
            cache_path = cache_dir / url_hash
            if cache_path.exists() and self.is_valid(cache_path):
                with cache_path.open('rb') as cache_file:
                    cache = cache_file.read()
        return cache

    def save_cache(self, url, page_source):
        """ Save page source data to file
        """
        url_hash = self.get_url_hash(url)
        cache_dir = self.get_cache_directory()
        if not cache_dir.exists():
            cache_dir.mkdir(parents=True)

        with (cache_dir / url_hash).open('wb') as cache_file:
            cache_file.write(page_source)

    def get_page_source(self, url):
        """ Returns the contents of the page at the specified URL
        """

        cache = self.get_cache(url)
        if cache and not self.app.options.refresh:
            page_source = cache
        else:
            page = requests.get(url, headers=self.get_request_headers())
            page_source = page.content
            self.save_cache(url, page_source)

        return page_source.decode('utf-8')

    def run(self, argv):
        """ Run provider
        """

        content = self.get_page_source(self.url)
        return self.get_weather_info(content)
