#!/usr/bin/python3
"""
Weather app project.
"""
import html
from urllib.request import urlopen, Request

ACCU_URL = "https://www.accuweather.com/uk/ua/dnipro/322722/daily-weather-forecast/322722?day=1"

# getting page from server
headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64)'}
accu_request = Request(ACCU_URL, headers=headers)
accu_page = str(urlopen(accu_request).read())

ACCU_TEMP_TAG = '<span class="large-temp">'
accu_temp_tag_size = len(ACCU_TEMP_TAG)
accu_temp_tag_index = accu_page.find(ACCU_TEMP_TAG)
accu_temp_value_start = accu_temp_tag_index + accu_temp_tag_size

accu_temp = ''
for char in accu_page[accu_temp_value_start:]:
    if char != "<":
        accu_temp += char
    else:
        break

print('Temperature in Dnipro from AccuWeather: \n')
print(f'Temperature: {html.unescape(accu_temp)}\n')
