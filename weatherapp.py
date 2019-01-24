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

import config
from providers import AccuWeatherProvider


def configuration(refresh=False):
    """Creating a configuration
    """

    print('1. AccuWeather \n2. RP5 ')
    num_provider = int(input('Please select provider: '))

    if num_provider == 1:
        accu_conf = AccuWeatherProvider()
        accu_conf.configurate(refresh=refresh)

    else:
        print('Unknown weather provider')
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
        # 'savef': save_weather_info
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
