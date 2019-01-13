#!/usr/bin/env python
"""
Weather app project.

The module receives the following arguments: 

Arguments:
----------
accu - сalling weather from the provider AccuWeather
rp5 - сalling weather from the provider RP5
config - configuring the module for displaying weather for a given city

Optional arguments:
------------------
savef - save weather to file. The command is used together with `accu`, 'rp5'
--refresh - updates data not from the cache. The command is used together with
            `accu`, 'rp5' and 'config'.
"""

import sys
import html
import hashlib
import time
import argparse
import configparser
from pathlib import Path
from bs4 import BeautifulSoup
from urllib.parse import quote

import requests


PROVIDER_NAME = {'accu': 'AccuWeather', 'rp5': 'RP5'}
CONFIG_FILE = 'weatherapp.ini'
DEFAULT_NAME = 'Дніпро'

# AccuWeather section
ACCU_URL = (
    "https://www.accuweather.com/uk/ua/dnipro/322722/weather-forecast/322722")
ACCU_DEFAULT_URL = (
    'https://www.accuweather.com/uk/ua/dnipro/322722/weather-forecast/322722')
ACCU_BROWSE_LOCATIONS = 'https://www.accuweather.com/uk/browse-locations'

# RP5 section
RP5_URL = (
    'http://rp5.ua/%D0%9F%D0%BE%D0%B3%D0%BE%D0%B4%D0%B0_%D0%B2_%D0%94%D0%BD%D1'
    '%96%D0%BF%D1%80%D1%96_%28%D0%94%D0%BD%D1%96%D0%BF%D1%80%D0%BE%D0%BF%D0%B5'
    '%D1%82%D1%80%D0%BE%D0%B2%D1%81%D1%8C%D0%BA%D1%83%29')
RP5_DEFAULT_URL = ('http://rp5.ua/%D0%9F%D0%BE%D0%B3%D0%BE%D0%B4%D0%B0_%D0%B2_'
                   '%D0%9A%D0%B8%D1%94%D0%B2%D1%96')
RP5_BROWSE_LOCATIONS = ('http://rp5.ua/%D0%9F%D0%BE%D0%B3%D0%BE%D0%B4%D0%B0_'
                        '%D0%B2_%D1%81%D0%B2%D1%96%D1%82%D1%96')

# Cache constants
CACHE_DIR = '.wappcache'
CACHE_TIME = 10


def get_request_headers():
    return {'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64)'}


def get_cache_directory():
    """ Path to cache directory
    """
    return Path.cwd() / CACHE_DIR


def get_url_hash(url):
    """ Generate url hash.
    """

    return hashlib.md5(url.encode('utf-8')).hexdigest()


def is_valid(path):
    """ Check if current cache file is valid
    """

    return (time.time() - path.stat().st_mtime) < CACHE_TIME


def get_cache(url):
    """ Return cache by given url address if any.
    """

    cache = b''
    url_hash = get_url_hash(url)
    cache_dir = get_cache_directory()
    if cache_dir.exists():
        cache_path = cache_dir / url_hash
        if cache_path.exists() and is_valid(cache_path):
            with cache_path.open('rb') as cache_file:
                cache = cache_file.read()
    return cache


def save_cache(url, page_source):
    """ Save page source data to file
    """
    url_hash = get_url_hash(url)
    cache_dir = get_cache_directory()
    if not cache_dir.exists():
        cache_dir.mkdir(parents=True)

    with (cache_dir / url_hash).open('wb') as cache_file:
        cache_file.write(page_source)


def get_page_source(url, refresh=False):
    """ Returns the contents of the page at the specified URL
    """

    cache = get_cache(url)
    if cache and not refresh:
        page_source = cache
    else:
        page = requests.get(url, headers=get_request_headers())
        page_source = page.content
        save_cache(url, page_source)

    return page_source.decode('utf-8')


def get_accu_locations(locations_url, refresh=False):
    """Getting a list of cities for ACCU provider 
    """
    locations_page = get_page_source(locations_url, refresh=refresh)
    soup = BeautifulSoup(locations_page, 'lxml')

    locations = []
    for location in soup.find_all('li', {'class': 'drilldown cl'}):
        url = location.find('a').attrs['href']
        location = location.find('em').text
        locations.append((location, url))
    return locations


def get_rp5_countries(locations_url, refresh=False):
    """Getting a list of countries for RP5 provider 
    """
    locations_page = get_page_source(locations_url, refresh=refresh)
    soup = BeautifulSoup(locations_page, 'lxml')

    countries = []
    add_url = 'http://rp5.ua/'
    for location in soup.find_all('div', class_='country_map_links'):
        url = add_url + quote(location.find('a').attrs['href'])
        location = location.find('a').text
        countries.append((location, url))
    return countries


def get_rp5_cities(cities_url, refresh=False):
    """Getting a list of cities for RP5 provider 
    """
    locations_page = get_page_source(cities_url, refresh=refresh)
    soup = BeautifulSoup(locations_page, 'lxml')

    cities = []
    add_url = 'http://rp5.ua/'

    cities_map = soup.find('div', class_='countryMap')
    if cities_map:
        for city in cities_map.find_all('h3'):
            url = add_url + quote(city.find('a').attrs['href'])
            city = city.find('a').text
            cities.append((city, url))

    return cities


def get_configuration_file():
    """ Getting the path to the configuration file
    """
    return Path.cwd() / CONFIG_FILE


def get_configuration(provider):
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


def save_configuration(provider, name, url):
    """ Save configuration to file
    """
    parser = configparser.ConfigParser(strict=False, interpolation=None)
    parser.add_section(provider)

    config_file = get_configuration_file()

    if config_file.exists():
        parser.read(config_file)

    parser[provider] = {'name': name, 'url': url}

    with open(get_configuration_file(), 'w') as configfile:
        parser.write(configfile)


def configurate(refresh=False):
    """Creating a configuration
    """
    print('1. AccuWeather \n2. RP5 ')
    num_provider = int(input('Please select provider: '))

    if num_provider == 1:
        browse_locations = ACCU_BROWSE_LOCATIONS
        provider = 'accu'
        locations = get_accu_locations(browse_locations, refresh=refresh)
        while locations:
            for index, location in enumerate(locations):
                print(f'{index + 1}, {location[0]}')
            selected_index = int(input('Please select location: '))
            location = locations[selected_index - 1]
            locations = get_accu_locations(location[1], refresh=refresh)
    elif num_provider == 2:
        browse_locations = RP5_BROWSE_LOCATIONS
        provider = 'rp5'
        countries = get_rp5_countries(browse_locations, refresh=refresh)
        for index, country in enumerate(countries):
            print(f'{index + 1}, {country[0]}')
        selected_index = int(input('Please select location: '))
        country = countries[selected_index - 1]

        cities = get_rp5_cities(country[1], refresh=refresh)
        for index, city in enumerate(cities):
            print(f'{index + 1}. {city[0]}')
        selected_index = int(input('Please select city: '))
        location = cities[selected_index - 1]
    else:
        print('Unknown weather provider')
        sys.exit(1)

    save_configuration(provider, *location)


def save_weather_info(provider):
    """ Saving weather forecast to file
    """

    city_name, city_url = get_configuration(provider)
    content = get_page_source(city_url)
    save_weather_to_file(provider, city_name,
                         get_weather_info(provider, content))


def save_weather_to_file(provider, city_name, info):
    """ Save the weather forecast from Accuweather to a file
    """
    path_to_wapp = Path.cwd()
    with open(path_to_wapp / 'weather.txt', 'w') as f:
        f.write(f'\nProvider: {PROVIDER_NAME[provider]}\n')
        f.write(f'City: {city_name}\n')
        f.write('-' * 20)
        for key, value in info.items():
            f.write(f'\n{key}: {html.unescape(value)}')
        print('\nFile weather.txt has been saved to:')
        print(path_to_wapp)


def get_weather_info(command, page_content, refresh=False):
    """ Receiving the current weather data
    """

    def get_weather_info_accu(city_page, refresh=False):
        """ Getting data about the current weather for AccuWeather    
        """
        current_day_section = \
            city_page.find('li', class_='day current first cl')
        if current_day_section == None:
            current_day_section = \
                city_page.find('li', class_='night current first cl')

        weather_info_accu = {}
        current_day_url = current_day_section.find('a').attrs['href']
        if current_day_url:
            current_day_page = get_page_source(
                current_day_url, refresh=refresh)
            if current_day_page:
                current_day = \
                    BeautifulSoup(current_day_page, "lxml")
                weather_details = \
                    current_day.find('div', attrs={'id': 'detail-now'})
                condition = weather_details.find('span', class_='cond')
                if condition:
                    weather_info_accu['cond'] = condition.text
                temp = weather_details.find('span', class_='large-temp')
                if temp:
                    weather_info_accu['temp'] = temp.text
                feal_temp = weather_details.find('span', class_='small-temp')
                if feal_temp:
                    weather_info_accu['feal_temp'] = feal_temp.text.replace(
                        'RealFeel® ', '')
                wind_info = weather_details.find_all('li', class_='wind')
                if wind_info:
                    weather_info_accu['wind'] = \
                        ' '.join(map(lambda t: t.text.strip(), wind_info))
        return weather_info_accu

    def get_weather_info_rp5(city_page):
        """ Getting data about the current weather for RP5    
        """

        current_day_section = \
            city_page.find('div', attrs={'id': 'archiveString'})
        weather_info_rp5 = {}
        condition = \
            str(current_day_section.find('span', class_='wv_0').previous)
        if condition:
            condition = condition.split(', ')
            weather_info_rp5['cond'] = condition[1]
        temp = current_day_section.find('span', class_='t_0')
        if temp:
            weather_info_rp5['temp'] = temp.text
        feal_temp = current_day_section.find('div', class_='TempStr')
        if feal_temp:
            weather_info_rp5['feal_temp'] = feal_temp.text
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

    city_page = BeautifulSoup(page_content, "lxml")
    weather_info = {}
    if command == 'accu':
        weather_info = get_weather_info_accu(city_page, refresh=False)
    if command == 'rp5':
        weather_info = get_weather_info_rp5(city_page)

    return weather_info


def produce_output(provider, city_name, info):
    """ Output of the received data
    """

    print(f'\nProvider: {PROVIDER_NAME[provider]}\n')
    print(f'City: {city_name}')
    print('-' * 20)
    for key, value in info.items():
        print(f'{key}: {html.unescape(value)}')


def get_provider_weather_info(provider, refresh=False):
    """ Getting the name of the city and URL from the configuration file.
        Getting information about the weather for the city.
        Output weather conditions for a specified city.
    """
    city_name, city_url = get_configuration(provider)
    content = get_page_source(city_url, refresh=refresh)
    produce_output(provider, city_name,
                   get_weather_info(provider, content, refresh=refresh))


def main(argv):
    """ Main entry point.
    """

    # Adding and parsing arguments
    KNOWN_COMMANDS = {
        'accu': get_provider_weather_info,
        'rp5': get_provider_weather_info,
        'config': configurate,
        'savef': save_weather_info
    }

    parser = argparse.ArgumentParser()
    parser.add_argument('command', help='Short name of provider', nargs=1)
    parser.add_argument('--refresh', help='Update caches', action='store_true')
    parser.add_argument(
        'command2', help='Save weather info to file', nargs='?')
    params = parser.parse_args(argv)

    if params.command:
        command = params.command[0]
        if command in KNOWN_COMMANDS:
            if command == 'config':
                KNOWN_COMMANDS[command](refresh=params.refresh)
            else:
                KNOWN_COMMANDS[command](command, refresh=params.refresh)

        else:
            print("Unknown command provided!")
            sys.exit(1)
    if params.command2:
        command2 = params.command2
        if command2 in KNOWN_COMMANDS:
            KNOWN_COMMANDS[command2](command)
        else:
            print("Unknown command provided!")
            sys.exit(1)


if __name__ == '__main__':
    main(sys.argv[1:])