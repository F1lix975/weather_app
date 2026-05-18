import requests
import json
import sqlite3
import pandas as pd
import streamlit as st
from st_aggrid import AgGrid, GridOptionsBuilder, GridUpdateMode
import arrow
from datetime import datetime

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


    }
    response = requests.get(url, params=params)
    another_dict = json.loads(response.text)
    second_element = another_dict["hourly"]["time"]
    third_element = another_dict["hourly"]["temperature_2m"]
    return second_element, third_element
#if __name__ == "__main__":
  #  get_city('Warsaw')
 #     time, temp = print_weather_info(lat, lng)

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

        city_data = selected_rows.iloc[0]
        lat = city_data["lat"]
        long = city_data["lng"]
        time, temp = print_weather_info(lat, long)
        df_weather = pd.DataFrame({
            "time": time,
            "temperature": temp
        })
        st.subheader(f"Weather Forecast for {city_data['city']}")
        now_hour = datetime.utcnow().replace(minute=0, second=0, microsecond=0)

        start_index = 0

        for i, t in enumerate(time):
            api_time = datetime.strptime(t, "%Y-%m-%dT%H:%M")

            if api_time >= now_hour:
                start_index = i
                break

        cols = st.columns(5)

        for i, col in enumerate(cols):
            idx = start_index + i

            if idx < len(time):
                with col:
                    st.metric(
                        label=time[idx][11:16],
                        value=f"{temp[idx]} °C"
                    )
        selected_date = st.date_input("Choose date")
        selected_hour = st.selectbox("Choose hour", list(range(24)))
        dt = arrow.get(selected_date).replace(hour=selected_hour, minute=0)
        dt_str = dt.format("YYYY-MM-DDTHH:00")
        index = None
        for i, t in enumerate(time):
            if t == dt_str:
                index = i
                break

        if index is not None:
            st.metric(
                label=time[index][11:16],
                value=f"{temp[index]} °C"
            )
        else:
            st.warning("No data for selected time")
        st.download_button(
            label="Download Weather Forecast",
            data=df_weather.to_csv(index=False),
            file_name=f"Weather Forecast for {city_data['city']}.csv",
            mime="text/csv",
        )






#if __name__ == "__main__":
   # get_city('Warsaw')
  #  time, temp = print_weather_info(51.0, 13.40)

