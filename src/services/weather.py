import time
import requests
import csv
import schedule

def get_weather_data():
    resp = requests.get('http://api.weatherapi.com/v1/current.json?key=d026faddcff44c73a5182744241805&q=Almaty&aqi=no')
    print(resp.status_code)
    print('OK')
    return resp.json()


def print_weather_result(result):
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


def save_weather_data(result):
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

    with open("weather_data.csv", "a") as csvfile:
        fieldnames = weather_data.keys()
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        if csvfile.tell() == 0:
            writer.writeheader()
        writer.writerow(weather_data)
        print('Data saved to weather_data.csv')


def main():
    result = get_weather_data()
    print_weather_result(result)
    save_weather_data(result)


schedule.every(1).hours.do(main)
while True:
    schedule.run_pending()
    time.sleep(1)


