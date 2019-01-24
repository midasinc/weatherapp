#!/usr/bin/env python
""" Weather providers
"""
import configparser
import hashlib
import re
import time
from pathlib import Path

import requests
from bs4 import BeautifulSoup

import config


class AccuWeatherProvider:
    """ Weather provider for AccuWeather site.
    """

    def __init__(self):
        self.name = config.ACCU_PROVIDER_NAME
        location, url = self.get_configuration()
        self.location = location
        self.url = url

    def get_configuration_file(self):
        """ Getting the path to the configuration file
        """
        return Path.cwd() / config.CONFIG_FILE

    def get_configuration(self):
        """ Get configuration from file
        """

        provider = self.name
        place_name = config.DEFAULT_NAME
        url = config.ACCU_DEFAULT_URL

        parser = configparser.ConfigParser(strict=False, interpolation=None)

        parser.read(self.get_configuration_file())

        if provider in parser.sections():
            location_config = parser[provider]
            place_name, url = location_config['name'], location_config['url']
        return place_name, url

    def save_configuration(self, provider, name, url):
        """ Save configuration to file
        """
        # FIXME: Check provider use

        parser = configparser.ConfigParser(strict=False, interpolation=None)
        parser.add_section(provider)

        config_file = self.get_configuration_file()

        if config_file.exists():
            parser.read(config_file)

        parser[provider] = {'name': name, 'url': url}

        with open(self.get_configuration_file(), 'w') as configfile:
            parser.write(configfile)

    def configurate(self, refresh=False):
        """Creating a configuration
        """
        provider = self.name
        locations = self.get_accu_locations(
            config.ACCU_BROWSE_LOCATIONS, refresh=refresh)
        while locations:
            for index, location in enumerate(locations):
                print(f'{index + 1}, {location[0]}')
            selected_index = int(input('Please select location: '))
            location = locations[selected_index - 1]
            locations = self.get_accu_locations(location[1], refresh=refresh)

        self.save_configuration(provider, *location)

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

    def get_accu_locations(self, locations_url, refresh=False):
        """Getting a list of cities for ACCU provider 
        """
        locations_page = self.get_page_source(locations_url, refresh=refresh)
        soup = BeautifulSoup(locations_page, 'lxml')

        locations = []
        for location in soup.find_all('li', {'class': 'drilldown cl'}):
            url = location.find('a').attrs['href']
            location = location.find('em').text
            locations.append((location, url))
        return locations

    def get_weather_info(self, page_content, refresh=False):
        """ Receiving the current weather data
        """
        city_page = BeautifulSoup(page_content, "lxml")
        current_day_section = city_page.find(
            'li', class_=re.compile('(day|night) current first cl'))

        weather_info = {}
        current_day_url = current_day_section.find('a').attrs['href']
        if current_day_url:
            current_day_page = self.get_page_source(
                current_day_url, refresh=refresh)
            if current_day_page:
                current_day = \
                    BeautifulSoup(current_day_page, "lxml")
                weather_details = \
                    current_day.find('div', attrs={'id': 'detail-now'})
                condition = weather_details.find('span', class_='cond')
                if condition:
                    weather_info['cond'] = condition.text
                temp = weather_details.find('span', class_='large-temp')
                if temp:
                    weather_info['temp'] = temp.text
                feal_temp = weather_details.find('span', class_='small-temp')
                if feal_temp:
                    weather_info['feal_temp'] = feal_temp.text.replace(
                        'RealFeel® ', '')
                wind_info = weather_details.find_all('li', class_='wind')
                if wind_info:
                    weather_info['wind'] = \
                        ' '.join(map(lambda t: t.text.strip(), wind_info))
        return weather_info

    def save_weather_info(self, provider):
        """ Saving weather forecast to file
        """

        city_name, city_url = self.get_configuration(provider)
        content = self.get_page_source(city_url)
        self.save_weather_to_file(provider, city_name,
                                  self.get_weather_info(provider, content))

    def save_weather_to_file(self, provider, city_name, info):
        """ Save the weather forecast from Accuweather to a file
        """
        path_to_wapp = Path.cwd()
        with open(path_to_wapp / 'weather.txt', 'w') as f:
            f.write(f'\nProvider: {config.PROVIDER_NAME[provider]}\n')
            f.write(f'City: {city_name}\n')
            f.write('-' * 20)
            for key, value in info.items():
                f.write(f'\n{key}: {html.unescape(value)}')
            print('\nFile weather.txt has been saved to:')
            print(path_to_wapp)

    def run(self, refresh=False):
        content = self.get_page_source(self.url, refresh=refresh)
        return self.get_weather_info(content, refresh=refresh)
