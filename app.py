""" Main application module
"""

from argparse  import ArgumentParser

class App:

    """ Weather aggregator application
    """

    def ___init___(self):
        self.arg_parser = self._arg_parse()
        

    def _arg_parse(self):
        """ Initialize argument parser
        """    

        arg_parser = ArgumentParser(add_help=False)
        arg_parser.add_argument('command', help="Command", nargs='?')
        arg_parser.add_argument('--refresh', help="Bypass caches", 
                                action='store_true')
        return arg_parser                               

