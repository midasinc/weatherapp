PROVIDER_NAME = {'accu': 'AccuWeather', 'rp5': 'RP5'}

# Fake user agent for weather sites requests
FAKE_MOZILLA_AGENT = 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64)'

# Configuration settings
CONFIG_FILE = '.weatherapp.ini'  # configuration file name

# Cache settings
CACHE_DIR = '.wappcache'  # cache directory name
CACHE_TIME = 300          # how long cache files are valid (in seconds)

# AccuWeather provider related configuration
ACCU_PROVIDER_NAME = 'accu'          # provider id
ACCU_PROVIDER_TITLE = 'AccuWeather'  # provider title

DEFAULT_ACCU_LOCATION_NAME = 'Дніпро'
DEFAULT_ACCU_LOCATION_URL = (
    'https://www.accuweather.com/uk/ua/dnipro/322722/weather-forecast/322722')
ACCU_BROWSE_LOCATIONS = 'https://www.accuweather.com/uk/browse-locations'

# rp5.ua provider related configuration
RP5_PROVIDER_NAME = 'rp5'          # provider id
RP5_PROVIDER_TITLE = 'rp5.ua'      # provider title

DEFAULT_RP5_LOCATION_NAME = 'Дніпро'
DEFAULT_RP5_LOCATION_URL = (
    'http://rp5.ua/%D0%9F%D0%BE%D0%B3%D0%BE%D0%B4%D0%B0_%D0%B2_'
    '%D0%9A%D0%B8%D1%94%D0%B2%D1%96')
RP5_BROWSE_LOCATIONS = ('http://rp5.ua/%D0%9F%D0%BE%D0%B3%D0%BE%D0%B4%D0%B0_'
                        '%D0%B2_%D1%81%D0%B2%D1%96%D1%82%D1%96')
ADD_URL = 'http://rp5.ua/'
