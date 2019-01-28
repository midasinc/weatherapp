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
from urllib.parse import quote

import config


class WeatherProvider():
    """ Base weather provider
    """

    def __init__(self, app):
        self.app = app

        self.name = config.ACCU_PROVIDER_NAME  #FIXME:

        location, url = self.get_configuration()
        self.location = location
        self.url = url

    def get_configuration_file(self):
        """ Getting the path to the configuration file
        """

        return Path.cwd() / config.CONFIG_FILE

    def _get_configuration(self):
        """ Get configuration from file
        
        :return: Return the name of the selected place (city) and url
        :rtype: tuple
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

    def run(self, refresh=False):
        """ Run provider
        """

        content = self.get_page_source(self.url, refresh=refresh)
        return self.get_weather_info(content, refresh=refresh)


class AccuWeatherProvider:
    """ Weather provider for AccuWeather site.
    """


    name = config.ACCU_PROVIDER_NAME
    title = config.ACCU_PROVIDER_TITLE

    default_location = config.DEFAULT_ACCU_LOCATION_NAME
    default_url = config.DEFAULT_ACCU_LOCATION_URL


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


class Rp5WeatherProvider:
    """ Weather provider for RP5 site.
    """


    name = config.RP5_PROVIDER_NAME
    title = config.RP5_PROVIDER_TITLE

    default_location = config.DEFAULT_RP5_LOCATION_NAME
    default_url = config.DEFAULT_RP5_LOCATION_URL

    def configurate(self, refresh=False):
        """Creating a configuration
        """

        provider = self.name

        browse_locations = config.RP5_BROWSE_LOCATIONS
        provider = 'rp5'
        countries = self.get_rp5_countries(browse_locations, refresh=refresh)
        for index, country in enumerate(countries):
            print(f'{index + 1}, {country[0]}')
        selected_index = int(input('Please select location: '))
        country = countries[selected_index - 1]

        cities = self.get_rp5_cities(country[1], refresh=refresh)
        for index, city in enumerate(cities):
            print(f'{index + 1}. {city[0]}')
        selected_index = int(input('Please select city: '))
        location = cities[selected_index - 1]

        self.save_configuration(provider, *location)


    def get_rp5_countries(self, locations_url, refresh=False):
        """Getting a list of countries for RP5 provider 
        """
        locations_page = self.get_page_source(locations_url, refresh=refresh)
        soup = BeautifulSoup(locations_page, 'lxml')

        countries = []
        for location in soup.find_all('div', class_='country_map_links'):
            url = config.ADD_URL + quote(location.find('a').attrs['href'])
            location = location.find('a').text
            countries.append((location, url))
        return countries

    def get_rp5_cities(self, cities_url, refresh=False):
        """Getting a list of cities for RP5 provider 
        """
        locations_page = self.get_page_source(cities_url, refresh=refresh)
        soup = BeautifulSoup(locations_page, 'lxml')

        cities = []
        cities_map = soup.find('div', class_='countryMap')
        if cities_map:
            for city in cities_map.find_all('h3'):
                url = config.ADD_URL + quote(city.find('a').attrs['href'])
                city = city.find('a').text
                cities.append((city, url))

        return cities

    def get_weather_info(self, page_content, refresh=False):
        """ Receiving the current weather data
        """
        city_page = BeautifulSoup(page_content, "lxml")
        current_day_section = \
            city_page.find('div', attrs={'id': 'archiveString'})
        weather_info_rp5 = {}
        condition = str(
            current_day_section.find('span', class_='wv_0').previous)
        if condition:
            condition = condition.split(', ')
            weather_info_rp5['cond'] = condition[1]
        temp = current_day_section.find('span', class_='t_0')
        if temp:
            weather_info_rp5['temp'] = temp.text
        feal_temp = current_day_section.find('div', class_='TempStr')
        if feal_temp:
            weather_info_rp5['feal_temp'] = feal_temp.text
        #TODO: Improve the selection of information in the section "Wind"
        wind_info_section = str(
            current_day_section.find('div',
                                     class_='ArchiveInfo').text).split(', ')
        wind_velocity = \
            str(current_day_section.find('span', class_='wv_1'
                                        ).text).replace('(','').replace(')','')
        wind_direction = wind_info_section[5]
        if wind_velocity and wind_direction:
            weather_info_rp5['wind'] = \
                'Вітер' + wind_velocity + ', ' + wind_direction
        return weather_info_rp5
