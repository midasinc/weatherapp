""" Weather providers
"""
import configparser
import hashlib
import re
import time
from pathlib import Path
from urllib.parse import quote

import requests
from bs4 import BeautifulSoup

import config


class AccuWeatherProvider(WeatherProvider):
    """ Weather provider for AccuWeather site.
    """

    name = config.ACCU_PROVIDER_NAME
    title = config.ACCU_PROVIDER_TITLE

    default_location = config.DEFAULT_ACCU_LOCATION_NAME
    default_url = config.DEFAULT_ACCU_LOCATION_URL

    def configurate(self):
        """Creating a configuration
        """
        provider = self.name
        locations = self.get_accu_locations(config.ACCU_BROWSE_LOCATIONS)
        while locations:
            for index, location in enumerate(locations):
                print(f'{index + 1}, {location[0]}')
            selected_index = int(input('Please select location: '))
            location = locations[selected_index - 1]
            locations = self.get_accu_locations(location[1])

        self.save_configuration(provider, *location)

    def get_accu_locations(self, locations_url):
        """Getting a list of cities for ACCU provider 
        """
        locations_page = self.get_page_source(locations_url)
        soup = BeautifulSoup(locations_page, 'lxml')

        locations = []
        for location in soup.find_all('li', {'class': 'drilldown cl'}):
            url = location.find('a').attrs['href']
            location = location.find('em').text
            locations.append((location, url))
        return locations

    def get_weather_info(self, page_content):
        """ Receiving the current weather data
        """
        city_page = BeautifulSoup(page_content, "lxml")
        current_day_section = city_page.find(
            'li', class_=re.compile('(day|night) current first cl'))

        weather_info = {}
        current_day_url = current_day_section.find('a').attrs['href']
        if current_day_url:
            current_day_page = self.get_page_source(current_day_url)
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


class RP5Provider(WeatherProvider):
    """ Weather provider for RP5 site.
    """

    name = config.RP5_PROVIDER_NAME
    title = config.RP5_PROVIDER_TITLE

    default_location = config.DEFAULT_RP5_LOCATION_NAME
    default_url = config.DEFAULT_RP5_LOCATION_URL

    def configurate(self):
        """Creating a configuration
        """

        provider = self.name

        browse_locations = config.RP5_BROWSE_LOCATIONS
        countries = self.get_rp5_countries(browse_locations)
        for index, country in enumerate(countries):
            print(f'{index + 1}, {country[0]}')
        selected_index = int(input('Please select location: '))
        country = countries[selected_index - 1]

        cities = self.get_rp5_cities(country[1])
        for index, city in enumerate(cities):
            print(f'{index + 1}. {city[0]}')
        selected_index = int(input('Please select city: '))
        location = cities[selected_index - 1]

        self.save_configuration(provider, *location)

    def get_rp5_countries(self, locations_url):
        """Getting a list of countries for RP5 provider 
        """
        locations_page = self.get_page_source(locations_url)
        soup = BeautifulSoup(locations_page, 'lxml')

        countries = []
        for location in soup.find_all('div', class_='country_map_links'):
            url = config.ADD_URL + quote(location.find('a').attrs['href'])
            location = location.find('a').text
            countries.append((location, url))
        return countries

    def get_rp5_cities(self, cities_url):
        """Getting a list of cities for RP5 provider 
        """
        locations_page = self.get_page_source(cities_url)
        soup = BeautifulSoup(locations_page, 'lxml')

        cities = []
        cities_map = soup.find('div', class_='countryMap')
        if cities_map:
            for city in cities_map.find_all('h3'):
                url = config.ADD_URL + quote(city.find('a').attrs['href'])
                city = city.find('a').text
                cities.append((city, url))

        return cities

    def get_weather_info(self, page_content):
        """ Receiving the current weather data
        """
        city_page = BeautifulSoup(page_content, "lxml")
        current_day_section = city_page.find(
            'div', attrs={'id': 'archiveString'})
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
        # TODO: Improve the selection of information in the section "Wind"
        wind_info_section = str(
            current_day_section.find('div',
                                     class_='ArchiveInfo').text).split(', ')
        wind_velocity = str(
            current_day_section.find('span', class_='wv_1').text).replace(
                '(', '').replace(')', '')
        wind_direction = wind_info_section[5]
        if wind_velocity and wind_direction:
            weather_info_rp5['wind'] = \
                'Вітер' + wind_velocity + ', ' + wind_direction
        return weather_info_rp5
