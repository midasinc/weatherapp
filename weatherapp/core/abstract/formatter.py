import abc


class Formatter(abc.ABC):

    """ Base abstract class for formatters.
    """

    @abc.abstractmethod
    def emit(self, column_names, data, stdout):
        """Format and print data from the iterable source."""


