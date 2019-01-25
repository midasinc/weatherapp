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

import argparse
import html
import sys
from pathlib import Path

import config
from providers import AccuWeatherProvider, Rp5WeatherProvider


def configuration(refresh=False):
    """Creating a configuration
    """

    print('1. AccuWeather \n2. RP5 ')
    num_provider = int(input('Please select provider: '))

    if num_provider == 1:
        accu_conf = AccuWeatherProvider()
        accu_conf.configurate(refresh=refresh)
    elif num_provider == 2:
        rp5_conf = Rp5WeatherProvider()
        rp5_conf.configurate(refresh=refresh)

    else:
        print('Unknown weather provider')
        sys.exit(1)


def save_to_file(provider, city_name, info):
    """ Save to file rercived data
    """

    path_to_file = Path.cwd()
    with open(path_to_file / 'weather.txt', 'w') as f:
        f.write(f'\nProvider: {config.PROVIDER_NAME[provider]}\n')
        f.write(f'City: {city_name}\n')
        f.write('-' * 20)
        for key, value in info.items():
            f.write(f'\n{key}: {html.unescape(value)}')
        print('\nFile weather.txt has been saved to:')
        print(path_to_file)


def save_provider_weather_info(provider, refresh=False):
    """ Save weather info to file
    """

    if provider == 'accu':
        accu = AccuWeatherProvider()
        save_to_file(provider, accu.location, accu.run(refresh=refresh))
    elif provider == 'rp5':
        rp5 = Rp5WeatherProvider()
        save_to_file(provider, rp5.location, rp5.run(refresh=refresh))
    else:
        print("Unknown weather provider!")
        sys.exit(1)


def produce_output(provider, city_name, info):
    """ Output of the received data
    """

    print(f'\nProvider: {config.PROVIDER_NAME[provider]}\n')
    print(f'City: {city_name}')
    print('-' * 20)
    for key, value in info.items():
        print(f'{key}: {html.unescape(value)}')


def get_provider_weather_info(provider, refresh=False):
    """ Getting the name of the city and URL from the configuration file.     
        Getting information about the weather for the city.
        Output weather conditions for a specified city.
    """

    if provider == 'accu':
        accu = AccuWeatherProvider()
        produce_output(provider, accu.location, accu.run(refresh=refresh))
    elif provider == 'rp5':
        rp5 = Rp5WeatherProvider()
        produce_output(provider, rp5.location, rp5.run(refresh=refresh))
    else:
        print("Unknown weather provider!")
        sys.exit(1)


def main(argv):
    """ Main entry point.
    """

    # Adding and parsing arguments
    KNOWN_COMMANDS = {
        'accu': get_provider_weather_info,
        'rp5': get_provider_weather_info,
        'config': configuration,
        'savef': save_provider_weather_info
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
