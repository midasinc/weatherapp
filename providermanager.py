class ProviderManager:

    """ Discovers registered providers and loads them.
    """

    def __init__(self):
        self._providers = {}
        self._load_providers()