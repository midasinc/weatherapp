""" Main application module
"""
import sys
from argparse import ArgumentParser

from providermanager import ProviderManager


class App:
    """ Weather aggregator application
    """

    def ___init___(self):
        self.arg_parser = self._arg_parse()
        self.providermanager = ProviderManager()

    def _arg_parse(self):
        """ Initialize argument parser
        """

        arg_parser = ArgumentParser(add_help=False)
        arg_parser.add_argument('command', help="Command", nargs='?')
        arg_parser.add_argument(
            '--refresh', help="Bypass caches", action='store_true')
        arg_parser.add_argument(
            'command2', help="Save weather to file", nargs='?')

        return arg_parser

    def produce_output(self, title, location, info):
        """Print results
        
        :param title: weather provider name
        :type title: str
        :param location: city name
        :type location: str
        :param info: weather conditions for the city 
        :type info: dict
        """

        print(f'{title}:')
        print("#" * 10, end='\n\n')

        print(f'{location}')
        print("#" * 20)
        for key, value in info.items():
            print(f'{key}: {value}')
        print("=" * 40, end='\n\n')

    def run(self, argv):
        """ Run application.
        :param argv: list of passed arguments
        """

        self.options, remaining_args = self.arg_parser.parse_known_args(argv)
        command_name = self.options.command

        if not command_name:
            # run all command providers by default
            for name, provider in self.providermanager._providers.items():
                self.produce_output(provider.title,
                                    provider(self).location,
                                    provider(self).run())
        elif command_name in self.providermanager:
            provider = self.providermanager[command_name](self)
            self.produce_output(provider.title, provider.location,
                                provider.run())


def main(argv=sys.argv[1:]):
    """Main entry point
    """

    return App().run(argv)


if __name__ == '__main__':
    main(sys.argv[1:])
