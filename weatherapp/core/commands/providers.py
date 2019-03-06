from weatherapp.core.abstract import Command


class Providers(Command):
    """ Print all available providers.
    """

    name = 'providers'

    def run(self, argv):
        """ Run command.
        """

        for name in self.app.provider_manager._commands:
            print(name)
