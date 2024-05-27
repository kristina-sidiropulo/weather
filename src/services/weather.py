import time
import requests
import csv
import schedule
import logging
import pytest


def get_weather_data():
    try:
        resp = requests.get(
            'http://api.weatherapi.com/v1/current.json?key=d026faddcff44c73a5182744241805&q=Almaty&aqi=no')
        resp.raise_for_status()
        print(resp.status_code)
        print('OK')
        logging.info('Success response')
        return resp

    except Exception:
        logging.error("Error getting weather")


def print_weather_result(result):
    try:
        name = result["location"]["name"]
        last_updated = result["current"]["last_updated"]
        temperature = result["current"]["temp_c"]
        humidity = result["current"]["humidity"]
        cloud = result["current"]["cloud"]
        feelslike_c = result["current"]["feelslike_c"]
        uv = result["current"]["uv"]
        text = result["current"]["condition"]["text"]

        print(f'On {last_updated} in {name} the temperature is {int(temperature)}, it feels like {int(feelslike_c)}.'
              f' Humidity: {humidity}%, cloudy: {cloud}%, UV-index: {int(uv)}, probability of precipitation: {text}')

    except KeyError:
        logging.error("No weather data key")


def save_weather_data(result):
    try:
        weather_data = {
            'name': result["location"]["name"],
            'last_updated': result["current"]["last_updated"],
            'temperature': result["current"]["temp_c"],
            'humidity': result["current"]["humidity"],
            'cloud': result["current"]["cloud"],
            'feelslike_c': result["current"]["feelslike_c"],
            'uv': result["current"]["uv"],
            'text': result["current"]["condition"]["text"],
            'icon': result["current"]["condition"]["icon"]
        }

    except KeyError:
        logging.error("No weather data key found")
        return

    try:
        with open("weather_data.csv", "a") as csvfile:
            fieldnames = weather_data.keys()
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            if csvfile.tell() == 0:
                writer.writeheader()
            writer.writerow(weather_data)
            print('Data saved to weather_data.csv')

    except Exception:
        logging.error("Error saving weather data")


def main():
    response = get_weather_data()
    if response is None:
        print('No weather')
    else:
        print_weather_result(response.json())
        save_weather_data(response.json())


schedule.every(1).hours.do(main)
while True:
    schedule.run_pending()
    time.sleep(1)
