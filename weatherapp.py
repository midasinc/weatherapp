#!/usr/bin/env python
"""
Weather app project.

This module takes three arguments: `accu`, 'config' and `s`.

Arguments:
----------
accu - сalling weather from the provider AccuWeather
config - configuring the module for displaying weather for a given city

Optional arguments:
------------------
savef - save weather to file 
"""
import sys
import html
import argparse
import configparser
from pathlib import Path
from bs4 import BeautifulSoup
from urllib.request import urlopen, Request

PROVIDER_NAME = {'accu': 'AccuWeather', 'rp5': 'RP5'}

CONFIG_LOCATION = 'Location'
CONFIG_FILE = 'weatherapp.ini'

# AccuWeather section
ACCU_URL = (
    "https://www.accuweather.com/uk/ua/dnipro/322722/weather-forecast/322722")

ACCU_BROWSE_LOCATIONS = 'https://www.accuweather.com/uk/browse-locations'

ACCU_DEFAULT_NAME = 'Kyiv'
ACCU_DEFAULT_URL = 'https://www.accuweather.com/uk/ua/kyiv/324505/weather-forecast/324505'

# RP5 section
RP5_URL = (
    'http://rp5.ua/%D0%9F%D0%BE%D0%B3%D0%BE%D0%B4%D0%B0_%D0%B2_%D0%94%D0'
    '%BD%D1%96%D0%BF%D1%80%D1%96_(%D0%94%D0%BD%D1%96%D0%BF%D1%80%D0%BE'
    '%D0%BF%D0%B5%D1%82%D1%80%D0%BE%D0%B2%D1%81%D1%8C%D0%BA%D1%83)')


def get_request_headers():
    return {'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64)'}


def get_page_source(url):
    """ Returns the contents of the page at the specified URL
    """
    request = Request(url, headers=get_request_headers())
    page_source = urlopen(request).read()
    return page_source.decode('utf-8')


def get_locations(locations_url):
    """Getting a list of cities 
    """
    locations_page = get_page_source(locations_url)
    soup = BeautifulSoup(locations_page, 'lxml')

    locations = []
    for location in soup.find_all('li', {'class': 'drilldown cl'}):
        url = location.find('a').attrs['href']
        location = location.find('em').text
        locations.append((location, url))
    return locations


def get_configuration_file():
    """ Getting the path to the configuration file
    """
    return Path.home() / CONFIG_FILE


def get_configuration(provider):
    """ Get configuration from file
    """
    if provider == 'accu':
        name = ACCU_DEFAULT_NAME
        url = ACCU_DEFAULT_URL

        parser = configparser.ConfigParser()
        parser.read(get_configuration_file())
        if CONFIG_LOCATION in parser.sections():
            config = parser[CONFIG_LOCATION]
            name, url = config['name'], config['url']

    elif provider == 'rp5':
        pass

    return name, url


def save_configuration(name, url):
    """ Save configuration to file
    """
    parser = configparser.ConfigParser()
    parser[CONFIG_LOCATION] = {'name': name, 'url': url}
    with open(get_configuration_file(), 'w') as configfile:
        parser.write(configfile)


def configurate():
    """Creating a configuration
    """
    locations = get_locations(ACCU_BROWSE_LOCATIONS)
    while locations:
        for index, location in enumerate(locations):
            print(f'{index + 1}, {location[0]}')
        selected_index = int(input('Please select location: '))
        location = locations[selected_index - 1]
        locations = get_locations(location[1])

    save_configuration(*location)


def save_weather_info():
    """ Saving weather forecast to file
    """

    city_name, city_url = get_configuration()
    content = get_page_source(city_url)
    save_accu_weather(city_name, get_weather_info("accu", content))


def save_accu_weather(city_name, info):
    """ Save the weather forecast from Accuweather to a file
    """
    path_to_wapp = Path.cwd()
    with open(path_to_wapp / 'weather.txt', 'w') as f:
        f.write('Provider: Accu Weather\n')
        f.write(f'City: {city_name}')
        f.write('-' * 20)
        for key, value in info.items():
            f.write(f'\n{key}: {html.unescape(value)}')
        print('\nFile weather.txt has been saved to:')
        print(path_to_wapp)


def get_weather_info(command, page_content):
    """ Receiving the current weather data
    """

    def get_weather_info_accu(city_page):
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
            current_day_page = get_page_source(current_day_url)
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
                    weather_info_accu['feal_temp'] = feal_temp.text
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
        weather_info = get_weather_info_accu(city_page)
    if command == 'rp5':
        weather_info = get_weather_info_rp5(city_page)

    return weather_info


def produce_output(provider, city_name, info):
    """ Output of the received data
    """

    print(f'\nProvider: {PROVIDER_NAME[provider]}: \n')
    print(f'City: {city_name}')
    print('-' * 20)
    for key, value in info.items():
        print(f'{key}: {html.unescape(value)}')


def get_provider_weather_info(provider):
    """ Getting the name of the city and URL from the configuration file.
        Getting information about the weather for the city.
        Output weather conditions for a specified city.
    """
    city_name, city_url = get_configuration(provider)
    content = get_page_source(city_url)
    produce_output(provider, city_name, get_weather_info(provider, content))


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
    parser.add_argument(
        'command2', help='Save weather info to file', nargs='?')
    params = parser.parse_args(argv)

    if params.command:
        command = params.command[0]
        if command in KNOWN_COMMANDS:
            KNOWN_COMMANDS[command](command)
        else:
            print("Unknown command provided!")
            sys.exit(1)
    if params.command2:
        command2 = params.command2[0]
        if command2 in KNOWN_COMMANDS:
            KNOWN_COMMANDS[command2]()
        else:
            print("Unknown command provided!")
            sys.exit(1)


if __name__ == '__main__':
    main(sys.argv[1:])