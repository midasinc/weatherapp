import abc
import argparse
import sys


class Command(abc.ABC):
    """ Base class for commands.

    :param app: Main application instance
    :type app: 'app.App'
    """

    def __init__(self, app, stdout=None):
        self.app = app
        self.stdout = stdout or sys.stdout

    @staticmethod
    def get_parser():
        """ Initialize argument parser for command.
        """
        parser = argparse.ArgumentParser()
        return parser

    @abc.abstractmethod
    def run(self, argv):
        """ Invoked by application when the command is run.
            Should be overridden in subclass.
        """
