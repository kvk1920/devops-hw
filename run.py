import os
import logging
import time
import graphyte
import json
import requests
import sys


logging.getLogger().setLevel(logging.DEBUG)


API_KEY = os.getenv('WEATHERBIT_API_KEY')
GRAPHITE_HOST = 'graphite'


def send_metrics(weather):
    sender = graphyte.Sender(GRAPHITE_HOST, prefix='weather')
    print(weather, file=sys.stderr)
    for weather_param in weather:
        sender.send(weather_param[0], float(weather_param[1]))


def main():
    result = json.loads(requests.get(
        f'https://api.weatherbit.io/v2.0/current?city=Moscow&key={API_KEY}').text
    )
    assert result['count'] == 1
    result = result['data'][0]
    time.sleep(5)
    metric = [
        ('temperature', float(result['temp'])),
        ('wind_speed', float(result['wind_spd'])),
        ('clouds', float(result['clouds'])),
    ]
    send_metrics(metric)


if __name__ == '__main__':
    main()
