import requests
import json
import sqlite3
import pandas as pd
import streamlit as st
from st_aggrid import AgGrid, GridOptionsBuilder, GridUpdateMode
import arrow
from datetime import datetime
from datetime import date, timedelta

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
    data_frame = pd.DataFrame(results, columns=["city", "lat", "lng", "country", "country_code"])
    return data_frame
def print_weather_info(lat, lng):
    url = "https://api.open-meteo.com/v1/forecast"
    params = {
        "latitude": lat,
        "longitude": lng,
        "hourly": "temperature_2m,relative_humidity_2m,precipitation_probability,surface_pressure,visibility,wind_speed_10m,uv_index,cloudcover",
        "timezone": "auto"


    }
    response = requests.get(url, params=params)
    another_dict = json.loads(response.text)
    second_element = another_dict["hourly"]["time"]
    third_element = another_dict["hourly"]["temperature_2m"]
    humidity = another_dict["hourly"]["relative_humidity_2m"]
    precip = another_dict["hourly"]["precipitation_probability"]
    pressure = another_dict["hourly"]["surface_pressure"]
    vis = [v / 1000 for v in another_dict["hourly"]["visibility"]]
    wind = another_dict["hourly"]["wind_speed_10m"]
    uv = another_dict["hourly"]["uv_index"]
    cloud = another_dict["hourly"]["cloudcover"]

    return second_element, third_element, humidity, precip, pressure, vis, wind, uv, cloud
#if __name__ == "__main__":
  #  get_city('Warsaw')
 #     time, temp, humidity = print_weather_info(lat, lng)

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
        key=f"city_grid{city}",
        theme="alpine-dark"


    )

    selected_rows = response.get("selected_rows", [])
    if selected_rows is not None and len(selected_rows) > 0:

        city_data = selected_rows.iloc[0]
        lat = city_data["lat"]
        long = city_data["lng"]
        time, temp, humidity, precip, pressure, vis, wind, uv, cloud = print_weather_info(lat, long)
        df_weather = pd.DataFrame({
            "time": time,
            "temperature": temp,
            "humidity": humidity,
            "precipitation": precip,
            "pressure": pressure,
            "visibility": vis,
            "wind_speed": wind,
            "UV_Index": uv,
            "CloudCover": cloud
        })
        st.subheader(f"Weather Forecast for {city_data['city']} (next 5 hours)")
        now_hour = datetime.now().replace(minute=0, second=0, microsecond=0)

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
                        value=f"{temp[idx]} °C",
                        delta=f"💧 {humidity[idx]}% | 🌧️ {precip[idx]}%"
                    )
                    st.caption(
                        f"🌬️ {pressure[idx]} hPa  \n👁️ {vis[idx]:.1f} km  \n💨 {wind[idx]} km/h  \n☀️ {uv[idx]}  \n☁️ {cloud[idx]}%"
                    )

        min_date = date.today()
        max_date = date.today() + timedelta(days=6)
        selected_date = st.date_input(
            "Choose date",
            min_value = min_date,
            max_value = max_date
        )
        selected_hour = st.selectbox("Choose hour", list(range(24)))
        dt = arrow.get(selected_date).replace(hour=selected_hour, minute=0)
        dt_str = dt.format("YYYY-MM-DDTHH:00")
        index = None
        for i, t in enumerate(time):
            if t == dt_str:
                index = i
                break

        if index is not None:
            st.subheader(f"Weather Forecast for next 5 hours\n(that day and hours you choose)")
            colss = st.columns(5)
            for j in range(5):
                next_index = index + j
                if next_index < len(time):
                    with colss[j]:
                        api_time = datetime.strptime(
                            time[next_index],
                            "%Y-%m-%dT%H:%M"
                        )
                        st.metric(
                            label=api_time.strftime("%H:%M"),
                            value=f"{temp[next_index]} °C",
                            delta=f"💧 {humidity[next_index]}% | 🌧️ {precip[next_index]}% "
                            )
                        st.caption(
                            f"🌬️ {pressure[next_index]} hPa  \n👁️ {vis[next_index]:.1f} km  \n💨 {wind[next_index]} km/h  \n☀️ {uv[next_index]}  \n☁️ {cloud[next_index]}%"
                        )
        st.download_button(
            label="Download Weather Forecast",
            data=df_weather.to_csv(index=False),
            file_name=f"Weather Forecast for {city_data['city']}.csv",
            mime="text/csv",
        )






#if __name__ == "__main__":
   # get_city('Warsaw')
  #  time, temp = print_weather_info(51.0, 13.40)

