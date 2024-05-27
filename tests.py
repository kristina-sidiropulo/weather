import csv
from unittest.mock import patch

import requests_mock
from pytest import mark

from src.services.weather import get_weather_data, save_weather_data, print_weather_result


@mark.parametrize('status_code, resp_is_none', [
    (200, False),
    (500, True),
])
def test_get_weather_data(status_code, resp_is_none):
    with requests_mock.Mocker() as m:
        url = 'http://api.weatherapi.com/v1/current.json?key=d026faddcff44c73a5182744241805&q=Almaty&aqi=no'
        m.get(url, status_code=status_code)

        resp = get_weather_data()

        if not resp_is_none:
            assert resp.status_code == status_code


@mark.parametrize('payload, called', [
    ({
         'location': {
             'name': 'Almaty',
         },
         'current': {
             'last_updated': '2024-05-27 21:30',
             'temp_c': 14.0,
             'condition': {
                 'text': 'Clear',
                 'icon': '//cdn.weatherapi.com/weather/64x64/night/113.png',
             },
             'humidity': 63,
             'cloud': 0,
             'feelslike_c': 14.0,
             'uv': 2,
         }
     }, True),
    ({}, False)
])
def test_print_weather_result(payload, called):
    with patch('builtins.print') as mock_print:
        print_weather_result(payload)
        assert mock_print.called == called


@mark.parametrize('payload, called', [
    ({
         'location': {
             'name': 'Almaty',
         },
         'current': {
             'last_updated': '2024-05-27 21:30',
             'temp_c': 14.0,
             'condition': {
                 'text': 'Clear',
                 'icon': '//cdn.weatherapi.com/weather/64x64/night/113.png',
             },
             'humidity': 63,
             'cloud': 0,
             'feelslike_c': 14.0,
             'uv': 2,
         }
     }, True),
    ({}, False)
])
def test_save_weather_data(payload, called):
    with patch.object(csv.DictWriter, 'writerow', return_value=None) as mock_method:
        mock_method.side_effect = Exception()
        save_weather_data(payload)

        assert mock_method.called == called


