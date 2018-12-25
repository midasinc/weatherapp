#!/usr/bin/env python
"""
Weather app project.
"""
import sys
import html
import argparse
import configparser
from pathlib import Path
from bs4 import BeautifulSoup
from urllib.request import urlopen, Request

# URL and tags for current weather in the city of Dnipro on Accuweather site
ACCU_URL = (
    "https://www.accuweather.com/uk/ua/dnipro/322722/weather-forecast/322722")
ACCU_TAGS = ('<span class="large-temp">', '<span class="cond">')

# URL and tags for current weather in the city of Dnipro on RP5 site
RP5_URL = (
    'http://rp5.ua/%D0%9F%D0%BE%D0%B3%D0%BE%D0%B4%D0%B0_%D0%B2_%D0%94%D0'
    '%BD%D1%96%D0%BF%D1%80%D1%96_(%D0%94%D0%BD%D1%96%D0%BF%D1%80%D0%BE'
    '%D0%BF%D0%B5%D1%82%D1%80%D0%BE%D0%B2%D1%81%D1%8C%D0%BA%D1%83)')
RP5_TAGS = ('<span class="t_0" style="display: block;">',
            ('<div class="ArchiveInfo">', '°F</span>, '))
DEFAULT_NAME = 'Kyiv'
DEFAULT_URL = 'https://www.accuweather.com/uk/ua/kyiv/324505/weather-forecast/324505'
ACCU_BROWSE_LOCATIONS = 'https://www.accuweather.com/uk/browse-locations'
CONFIG_LOCATION = 'Location'
CONFIG_FILE = 'weatherapp.ini'


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

def get_configuration():
    """ Get configuration from file
    """
    name = DEFAULT_NAME
    url = DEFAULT_URL

    parser = configparser.ConfigParser()
    parser.read(get_configuration_file())
    if CONFIG_LOCATION in parser.sections():
        config = parser[CONFIG_LOCATION]
        name, url = config['name'], config['url']

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
        #TODO: доработать функцию

    """ Saving weather forecast to file
    """
    
    path_to_wapp = Path(__file__).parent
    with open(path_to_wapp / 'weather.txt', 'w') as f:
        f.write('some text here')
        print('\nFile weather.txt has been saved to:\n')
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


def produce_output(city_name, info):
    """ Output of the received data
    """
    print('Accu Weather: \n')
    print(f'{city_name}')
    print('-'*20)
    for key, value in info.items():
        print(f'{key}: {html.unescape(value)}')

def get_accu_weather_info():
    """ Getting the name of the city and URL from the configuration file.
        Getting information about the weather for the city.
        Output weather conditions for a specified city.
    """
    city_name, city_url = get_configuration()
    content = get_page_source(city_url)
    produce_output(city_name, get_weather_info("accu", content)) #FIXME:  - исправить "accu" на универсальную команду

def main(argv):
    """ Main entry point.
    """

    # Adding and parsing arguments
    KNOWN_COMMANDS = {'accu': get_accu_weather_info,
                        'config': configurate,
                        's': save_weather_info }
    # KNOWN_COMMANDS = {'accu': 'AccuWeather', 'rp5': 'RP5', 'sin': "Sinoptik"}
    
    parser = argparse.ArgumentParser()
    parser.add_argument('command', help='Service name', nargs=1)
    parser.add_argument('command2', help='Save weather info to file', nargs='?')
    params = parser.parse_args(argv)

    if params.command:
        command = params.command[0]
        if command in KNOWN_COMMANDS:
            KNOWN_COMMANDS[command]()
        else:
            print("Unknown command provided!")
            sys.exit(1)


if __name__ == '__main__':
    main(sys.argv[1:])