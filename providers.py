""" Weather providers
"""
import hashlib
import configparser
import time
from pathlib import Path

import requests

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

    def get_url_hash(self, url):
        """ Generate url hash.
        """

        return hashlib.md5(url.encode('utf-8')).hexdigest()


    def get_cache_directory(self):
        """ Path to cache directory
        """
        return Path.cwd() / config.CACHE_DIR
 

    def is_valid(self, path):
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


    def get_page_source(self, url, refresh=False):
        """ Returns the contents of the page at the specified URL
        """

        cache = self.get_cache(url)
        if cache and not refresh:
            page_source = cache
        else:
            page = requests.get(url, headers=self.get_request_headers())
            page_source = page.content
            self.save_cache(url, page_source)

        return page_source.decode('utf-8')




