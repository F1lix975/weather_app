import requests
import json
import sqlite3
import pandas as pd



def print_weather_info(lat, long):
    url = "https://api.open-meteo.com/v1/forecast"
    params = {
        "latitude": lat,
        "longitude": long,
        "hourly": [ "temperature_2m",
                    "relative_humidity_2m",
                    "visibility",
                    "surface_pressure",
                    "dew_point_2m",
                    "uv_index",
                    "snowfall",
                    "rain",
                    "precipitation_probability"

        ],
        "timezone": "auto"







    }
    response = requests.get(url, params=params)
    another_dict = json.loads(response.text)
    second_element = another_dict["hourly"]["time"]
    third_element = another_dict["hourly"]["temperature_2m"]
    fourth_element = another_dict["hourly"]["relative_humidity_2m"]
    fifth_element = another_dict["hourly"]["visibility"]
    sixth_element = another_dict["hourly"]["surface_pressure"]
    seventh_element = another_dict["hourly"]["dew_point_2m"]
    eighth_element = another_dict["hourly"]["uv_index"]
    nineth_element = another_dict["hourly"]["snowfall"]
    tenth_element = another_dict["hourly"]["rain"]
    eleventh_element = another_dict["hourly"]["precipitation_probability"]

    #print(another_dict["hourly"].keys())
    print(second_element, third_element, fourth_element, fifth_element, sixth_element, seventh_element, eighth_element, nineth_element, tenth_element, eleventh_element)


def get_city(city):
    """
    Fuction can return every example of a city, which user would write.
    :param city:
    :return:
    """
    conn = sqlite3.connect("base.db")
    cursor = conn.cursor()
    query = """SELECT city, lat, lng, country, iso3 FROM simplemaps_worldcities_basic WHERE upper(city) LIKE upper('%' ||?||'%')"""
    cursor.execute(query, (city,))
    results = cursor.fetchall()
    conn.close()
    data_frame = pd.DataFrame(results, columns=["city", "lat", "lng", "country", "iso3"])
    return data_frame
    





if __name__ == "__main__":
    get_city('Warsaw')
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




