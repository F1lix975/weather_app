import requests


def print_weather_info():
    url = "https://api.open-meteo.com/v1/forecast"
    params = {
        "latitude": 52.52,
        "longitude": 13.41,
        "hourly": "temperature_2m",
        "start_date": "2026-05-13",
        "end_date": "2026-05-13",
    }
    response = requests.get(url, params=params)
    print(response.text)

if __name__ == "__main__":
    print_weather_info()

from requests.structures import CaseInsensitiveDict
def print_geocode_location():
    link = "https://geocoding-api.open-meteo.com/v1/search?name=Berlin&count=10&language=en&format=json"
    data = {
        "name": "Berlin",
        "latitude": 52.52437,
        "longitude": 13.41053,
    }
    answer = requests.get(link, params=data)
    print(answer.text)
    print_geocode_location()
