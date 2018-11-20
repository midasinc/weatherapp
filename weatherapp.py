#!/usr/bin/python3
"""
Weather app project.
"""
import html
from urllib.request import urlopen, Request

headers = {'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64)'}

# URL for current weather in the city of Dnipro on Accuweather site
ACCU_URL = "https://www.accuweather.com/uk/ua/dnipro/322722/weather-forecast/322722"

# getting page from Accuweather
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

print('\nWeather in Dnipro from AccuWeather:')
print(f'Temperature: {html.unescape(accu_temp)}')
print(f'Weather conditions: {html.unescape(accu_cond)}\n')

# URL for current weather in the city of Dnipro on RP5 site
RP5_URL = (
    'http://rp5.ua/%D0%9F%D0%BE%D0%B3%D0%BE%D0%B4%D0%B0_%D0%B2_%D0%94%D0'
    '%BD%D1%96%D0%BF%D1%80%D1%96_(%D0%94%D0%BD%D1%96%D0%BF%D1%80%D0%BE'
    '%D0%BF%D0%B5%D1%82%D1%80%D0%BE%D0%B2%D1%81%D1%8C%D0%BA%D1%83)')

# getting page from rp5.ua
rp5_request = Request(RP5_URL, headers=headers)
rp5_page = urlopen(rp5_request).read()
rp5_content = rp5_page.decode('utf-8')

# Getting temperature from rp5.ua
RP5_TEMP_CONTAINER_TAG = '<div id="ArchTemp">'
RP5_TEMP_TAG = '<span class="t_0" style="display: block;">'
rp5_temp_tag = rp5_content.find(RP5_TEMP_TAG,
                                rp5_content.find(RP5_TEMP_CONTAINER_TAG))

rp5_temp_tag_size = len(RP5_TEMP_TAG)
rp5_temp_tag_start = rp5_temp_tag + rp5_temp_tag_size
rp5_temp = ""
for char in rp5_content[rp5_temp_tag_start:]:
    if char != '<':
        rp5_temp += char
    else:
        break

# Getting weather conditions from the rp5.ua
RP5_COND_CONTAINER_TAG = '<div class="ArchiveInfo">'
RP5_COND_TAG = '°F</span>, '
rp5_cond_tag = rp5_content.find(RP5_COND_TAG,
                                rp5_content.find(RP5_COND_CONTAINER_TAG))

rp5_cond_tag_size = len(RP5_COND_TAG)
rp5_cond_tag_start = rp5_cond_tag + rp5_cond_tag_size
rp5_cond = ""
for char in rp5_content[rp5_cond_tag_start:]:
    if char != ',':
        rp5_cond += char
    else:
        break

print('Weather in Dnipro from RP5:')
print(f'Temperature: {html.unescape(rp5_temp)}')
print(f'Weather conditions: {html.unescape(rp5_cond)}\n')