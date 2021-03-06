"""Integration tests for the application"""

from weatherapp.core.abstract import Command


class Providers(Command):
    """ Print all available providers.
    """

    name = 'providers'

    def run(self, argv):
        """ Run command.
        """
        for name, provider in self.app.providermanager:
            self.app.stdout.write(f'{provider.title}: {name}\n')
