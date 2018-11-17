#!/usr/bin/python3
"""
Weather app project.
"""
import html
from urllib.request import urlopen, Request

# URL for current weather in the city of Dnipro on Accuweather site
ACCU_URL = "https://www.accuweather.com/uk/ua/dnipro/322722/weather-forecast/322722"

# getting page from Accuweather
headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64)'}
accu_request = Request(ACCU_URL, headers=headers)
accu_page = urlopen(accu_request).read()
accu_page = accu_page.decode('utf-8')

# Getting temperature from Accuweather
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

# Getting weather conditions from the Accuweather
ACCU_COND_TAG = '<span class="cond">'
accu_cond_tag_size = len(ACCU_COND_TAG)
accu_cond_tag_index = accu_page.find(ACCU_COND_TAG)
accu_cond_value_start = accu_cond_tag_index + accu_cond_tag_size

accu_cond = ''
for char in accu_page[accu_cond_value_start:]:
    if char != "<":
        accu_cond += char
    else:
        break

print('Weather in Dnipro from AccuWeather: \n')
print(f'Temperature: {html.unescape(accu_temp)}\n')
print(f'Weather conditions: {html.unescape(accu_cond)}\n')
