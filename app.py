import requests
import json
import sqlite3

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


def get_city(city, country):
    conn = sqlite3.connect("base.db")
    cursor = conn.cursor()
    query = """SELECT city, lat, lng, country FROM simplemaps_worldcities_basic WHERE city = ? AND country = ?"""
    cursor.execute(query, (city, country))
    result = cursor.fetchone()
    conn.close()
    if result:
        return("Latitude:", result[1],
               "Longitude:", result[2])

    else:
        print("City can't be found")

if __name__ == "__main__":
    get_city('Warsaw', 'Poland')
    weather = print_weather_info(51.0 , 13.40)


#def get_geo_cords(name, countryCode):

 #   link = "https://geocoding-api.open-meteo.com/v1/search?name=Berlin&count=10&language=en&format=json"
  #  data = {
   #     "name": name,
    #    "countryCode": countryCode

    #}
    #answer = requests.get(link, params=data)
   # data_dict = json.loads(answer.text)
   # print(data_dict['results'])
   # first_element = data_dict['results'][0]
    #return(first_element['latitude'], first_element['longitude'])
#if __name__ == "__main__":
#    cordinates = get_geo_cords('Warsaw', 'PL')




