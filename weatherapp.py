#!/usr/bin/python3
"""
Weather app project.
"""

from urllib.request import urlopen, Request

accu_url = "https://www.accuweather.com/uk/ua/dnipro/322722/daily-weather-forecast/322722?day=1"

# getting page from server
headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux Mint; Linux x86_64;)'}
accu_request = Request(accu_url, headers=headers)
accu_page = urlopen(accu_request).read()

print(accu_page)