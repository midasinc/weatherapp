
# Project "weatherapp.core"

## About 
The **weatherapp.core** application is an aggregator of weather sites and is designed to view weather conditions from various sources in a convenient form in one place.

The following weather sites are currently supported:

* [AccuWeather](www.accuweather.com)
* [RP5](rp5.ua)

**weatherapp.core** is a console application and has the possibility of further development - expanding the functionality and increasing the number of sources of weather conditions.




## Installation

1. Install Python from <https://www.python.org/>. You'll need Python 3.6 or later, primarily because of the use of f-strings.
2. The sample can be run on any operating system that supports Python 3.x, including recent versions of Windows, Linux, and Mac OS.
3. Follow these steps to install the sample code on your computer:
	- Download or clone the repository [weatherapp.core](https://github.com/midasinc/weatherapp.core) to your machine.
	- Use the following command to locally install the package:
	     `$ pip install .`
 
 
 
## Usage


#### Basic commands:

* get weather conditions from all providers
`$ wfapp`

* get weather conditions from a specific provider
`$ wfapp [provider id]`

* run with update cache:
`$ wfapp --refresh`
or
`$ wfapp [provider id] --refresh`

* get a list of all providers:
` $ wfapp providers`

* select a location to get weather data from a specific provider:
`$ wfapp configurate [provider id]`

***List [provider id]:***
- `accu` - [AccuWeather](www.accuweather.com)
- `rp5` - [RP5](rp5.ua)


#### Optional commands:

* for show traceback on errors:
`--debug`

* for setting the login level of the program(default WARNING) INFO:
`-v`

* for setting the login level of the program(default WARNING) DEBUG:
`-vv `



## License
The **weatherapp.core** is open-source software licensed under the [MIT license](https://opensource.org/licenses/MIT)

