#!/usr/bin/python3
"""
Weather app project.
"""
import html
from urllib.request import urlopen, Request

# URL for current weather in the city of Dnipro on Accuweather site
ACCU_URL = "https://www.accuweather.com/uk/ua/dnipro/322722/weather-forecast/322722"
ACCU_TAGS = ('<span class="large-temp">', '<span class="cond">')


def get_request_headers():
    return {'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64)'}


def get_page_source(url):
    """ Returns the contents of the page at the specified URL
    """

    request = Request(url, headers=get_request_headers())
    page_source = urlopen(request).read()
    return page_source.decode('utf-8')


def get_tag_content(page_content, tag):
    """ Search for relevant information in the content page
    """

    tag_index = page_content.find(tag)
    tag_size = len(tag)
    value_start = tag_index + tag_size

    content = ''
    for c in page_content[value_start:]:
        if c != '<':
            content += c
        else:
            break
    return content


def get_weather_info(page_content, tags):
    """ Obtaining the required data from the received content and 
        specify the tags
    """

    return tuple([get_tag_content(page_content, tag) for tag in tags])


def produce_output(provider_name, temp, condition):
    """ Output of the received data
    """

    print(f'\n{provider_name}:\n')
    print(f'Temperature: {html.unescape(temp)}')
    print(f'Weather conditions: {condition}\n')


def main():
    """ Main entry point.
    """
    weather_sites = {"AccuWeather": (ACCU_URL, ACCU_TAGS)}
    for name in weather_sites:
        url, tags = weather_sites[name]
        content = get_page_source(url)
        temp, condition = get_weather_info(content, tags)
        produce_output(name, temp, condition)


if __name__ == '__main__':
    main()