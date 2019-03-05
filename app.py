#!/usr/bin/env python
""" Main application module
"""
import logging
import sys
from argparse import ArgumentParser

import config
from commandmanager import CommandManager
from providermanager import ProviderManager


class App:
    """ Weather aggregator application
    """

    logger = logging.getLogger(__name__)
    LOG_LEVEL_MAP = {0: logging.WARNING, 
                     1: logging.INFO, 
                     2: logging.DEBUG}

    def __init__(self):
        self.arg_parser = self._arg_parse()
        self.provider_manager = ProviderManager()
        self.commandmanager = CommandManager()

    def _arg_parse(self):
        """ Initialize argument parser
        """

        arg_parser = ArgumentParser(add_help=False)
        arg_parser.add_argument('command', help="Command", nargs='?')
        arg_parser.add_argument(
            '--refresh', help="Bypass caches", action='store_true')
        arg_parser.add_argument(
            '--debug',
            action='store_true',
            default=False,
            help='Show tracebacks on errors.')

        arg_parser.add_argument(
            '-v',
            '--verbose',
            action='count',
            dest='verbose_level',
            default=config.DEFAULT_VERBOSE_LEVEL,
            help='Increase verbosity of output.')

        return arg_parser

    def configure_logging(self):
        """ Create logging handlers for any log output.
        """

        root_logger = logging.getLogger('')
        root_logger.setLevel(logging.DEBUG)

        console = logging.StreamHandler()
        console_level = self.LOG_LEVEL_MAP.get(self.options.verbose_level,
                                               logging.WARNING)
        console.setLevel(console_level)
        formatter = logging.Formatter(config.DEFAULT_MESSAGE_FORMAT)
        console.setFormatter(formatter)
        root_logger.addHandler(console)

    def produce_output(self, title, location, info):
        """Print results
        
        :param title: weather provider name
        :type title: str
        :param location: city name
        :type location: str
        :param info: weather conditions for the city 
        :type info: dict
        """

        print(f'\n{title}:')
        print("#" * 10, end='\n\n')

        print(f'{location}')
        print("#" * 25)
        for key, value in info.items():
            print(f'{key}: {value}')
        print("=" * 40, end='\n\n')

    def run(self, argv):
        """ Run application.

        :param argv: list of passed arguments
        """

        self.options, remaining_args = self.arg_parser.parse_known_args(argv)
        self.configure_logging()
        self.logger.debug("  %s", argv)

        command_name = self.options.command

        if command_name in self.commandmanager:
            command_factory = self.commandmanager.get(command_name)

            try:
                command_factory(self).run(remaining_args)

            except Exception:
                msg = "Error during command: %s run"
                if self.options.debug:
                    self.logger.exception(msg, command_name)
                else:
                    self.logger.error(msg, command_name)

        if not command_name:
            # run all command providers by default
            for name, provider in self.provider_manager._providers.items():
                self.produce_output(
                    provider(self).title,
                    provider(self).location,
                    provider(self).run(remaining_args))

        elif command_name in self.provider_manager:
            provider = self.provider_manager[command_name]
            self.produce_output(
                provider(self).title,
                provider(self).location,
                provider(self).run(remaining_args))


def main(argv=sys.argv[1:]):
    """Main entry point
    """

    if '--debug' in argv:
        return App().run(argv)
    else:
        try:
            return App().run(argv)
        except Exception:
            print('\nThe program can not continue to work '
                  'due to a runtime error!\n')
            raise SystemExit


if __name__ == '__main__':
    main(sys.argv[1:])
