import requests
import json
import sqlite3
import pandas as pd
import streamlit as st
from st_aggrid import AgGrid, GridOptionsBuilder, GridUpdateMode
st.title("Weather Forecast")
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
def print_weather_info(lat, lng):
    url = "https://api.open-meteo.com/v1/forecast"
    params = {
        "latitude": lat,
        "longitude": lng,
        "hourly": "temperature_2m",
        "hourly_units": "temperature_2m"

    }
    response = requests.get(url, params=params)
    another_dict = json.loads(response.text)
    second_element = another_dict["hourly"]
    third_element = another_dict["hourly_units"]
    return(second_element, third_element)


city = st.text_input("Write your city here")
if city:
    df = get_city(city)
    if df.empty:
        st.warning("No results found")
        st.stop()
    gb = GridOptionsBuilder.from_dataframe(df)
    gb.configure_selection("single", use_checkbox=True)
    grid_options = gb.build()

    response = AgGrid(
        df,
        gridOptions=grid_options,
        update_mode=GridUpdateMode.SELECTION_CHANGED,
        key="city_grid"

    )

    selected_rows = response.get("selected_rows", [])

    if selected_rows is not None and len(selected_rows) > 0:
        st.session_state["selected_city"] = selected_rows.iloc[0]
    if st.button("Get weather"):
        if "selected_city" not in st.session_state:
            st.warning("Select city")
            st.stop()
        city_data = st.session_state["selected_city"]
        lat = city_data["lat"]
        long = city_data["lng"]
        weather = print_weather_info(lat, long)
        st.subheader(f"Weather Forecast for {city_data['city']}")
        st.json(weather)



if __name__ == "__main__":
    get_city('Warsaw')
    print_weather_info(51.0, 13.40)

