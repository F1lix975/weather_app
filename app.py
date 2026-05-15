import requests
import json
import sqlite3

with open ("worldcities.sql", "r", encoding="utf-8") as file:
    skrypt_sql = file.read()
print(skrypt_sql)



def print_weather_info(lat, long):
    url = "https://api.open-meteo.com/v1/forecast"
    params = {
        "latitude": lat,
        "longitude": long,
        "hourly": "temperature_2m",
        "hourly_units": "temperature_2m"

    }
    response = requests.get(url, params=params)
    another_dict = json.loads(response.text)
    second_element = another_dict["hourly"]
    third_element = another_dict["hourly_units"]
    return(second_element, third_element)


if __name__ == "__main__":
    weather = print_weather_info(51.0 , 13.40)

def get_geo_cords(name, countryCode):

    link = "https://geocoding-api.open-meteo.com/v1/search?name=Berlin&count=10&language=en&format=json"
    data = {
        "name": name,
        "countryCode": countryCode

    }
    answer = requests.get(link, params=data)
    data_dict = json.loads(answer.text)
    #print(data_dict['results'])
    first_element = data_dict['results'][0]
    return(first_element['latitude'], first_element['longitude'])
if __name__ == "__main__":
    cordinates = get_geo_cords('Warsaw', 'PL')
#def get_city():
 #   address = "https://wikipedia.org"
  #  another_data = {
   # "name": "San Francisco",
    #"latitude": 37.75,
    #"longitude" :-122.44,
    #"country": "US",
    #"population": 3592294,
    #"is_capital": False
    #}
    #reply = requests.get(address, params=another_data)
    #dict_of_countries = json.loads(reply.text)
    #print(dict_of_countries)
#if __name__ == "__main__":
#    get_city()




