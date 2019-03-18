from weatherapp.core.abstract import Command


class Providers(Command):
    """ Print all available providers.
    """

    name = 'providers'

    def run(self, argv):
        """ Run command.
        """
        for provider in self.app.providermanager._commands:
            self.stdout.write(f'{provider}\n')

