from datetime import datetime
import json
import os

import requests

SUN_TIME_FILE = "suntime.json"
WEATHER_FILE = "weather.json"
FORECAST_FILE = "forecast.json"
WEATHER_REFRESH_MIN = 15

with open("env.json", "r") as openfile:
    data = json.load(openfile)
    API_KEY = data["weather_api_key"]
    LAT = data["lat"]
    LON = data["lon"]
    TIME_TABLE_URL = data["timetable"]

LANG = "pl"
WEATHER_API_URL = f"https://api.openweathermap.org/data/2.5/weather?lat={LAT}&lon={LON}&appid={API_KEY}&units=metric&lang={LANG}"
FORECAST_API_URL = f"https://api.openweathermap.org/data/2.5/forecast?lat={LAT}&lon={LON}&appid={API_KEY}&units=metric&lang={LANG}"


def get_suntimes() -> str:

    get_data = True

    def read_cache_date():
        with open(SUN_TIME_FILE, "r") as openfile:
            cache = json.load(openfile)
        now = datetime.now()
        date_now = f"{now.year}-{now.month}-{now.day}"
        if date_now == cache["results"]["date"]:
            return cache
        return None

    if os.path.exists(SUN_TIME_FILE):
        try:
            data = read_cache_date()
            get_data = data is None
        except:
            pass

    if get_data:
        api_url = f"https://api.sunrisesunset.io/json?lat={LAT}&lng={LON}"
        response = requests.get(api_url)
        data = response.json()
        # cache this day
        json_object = json.dumps(data, indent=4)
        with open(SUN_TIME_FILE, "w") as outfile:
            outfile.write(json_object)

    today_sr: str = data["results"]["sunrise"]
    today_ss: str = data["results"]["sunset"]

    if "AM" in today_sr:
        today_sr = today_sr.split()[0]

    if "PM" in today_ss:
        today_ss = today_ss.split()[0]
        split = today_ss.split(":")
        hour = int(split[0]) + 12
        today_ss = f"{hour}:{split[1]}:{split[2]}"

    text = f"Wsch: {today_sr}\n Zach: {today_ss}"
    return text


def get_weather() -> dict:

    get_data = True

    def read_cache_date():
        with open(WEATHER_FILE, "r") as openfile:
            cache = json.load(openfile)
        dt_now = datetime.now()
        dt = datetime.fromtimestamp(cache["dt"])
        if dt > dt_now:
            td = dt - dt_now
        else:
            td = dt_now - dt
        minutes = td.total_seconds() / 60
        if minutes > WEATHER_REFRESH_MIN:
            return None
        return cache

    if os.path.exists(WEATHER_FILE):
        try:
            data = read_cache_date()
            get_data = data is None
        except:
            pass

    if get_data:
        response = requests.get(WEATHER_API_URL)
        data: dict = response.json()
        json_object = json.dumps(data, indent=4)
        with open(WEATHER_FILE, "w") as outfile:
            outfile.write(json_object)

    temp: float = round(data["main"]["temp"], 1)
    dscr: str = data["weather"][0]["description"]

    return {"temp": temp, "dscr": dscr}


def get_weather_forecast():
    get_data = True

    def read_cache_date():
        with open(FORECAST_FILE, "r") as openfile:
            cache = json.load(openfile)
        dt_now = datetime.now()
        dt = datetime.fromtimestamp(cache["cache_dt"])
        if dt > dt_now:
            td = dt - dt_now
        else:
            td = dt_now - dt
        minutes = td.total_seconds() / 60
        if minutes > WEATHER_REFRESH_MIN:
            return None
        return cache

    if os.path.exists(FORECAST_FILE):
        try:
            data = read_cache_date()
            get_data = data is None
        except:
            pass

    if get_data:
        response = requests.get(FORECAST_API_URL)
        data: dict = response.json()
        data["cache_dt"] = datetime.now().timestamp()
        json_object = json.dumps(data, indent=4)
        with open(FORECAST_FILE, "w") as f:
            f.write(json_object)

    days = {}
    data_list = data["list"]
    for d in data_list:
        dt = datetime.fromtimestamp(d["dt"])
        wday = dt.weekday()  # Weekday in key!!!
        temp_min = d["main"]["temp_min"]
        temp_max = d["main"]["temp_max"]
        if wday in days:
            temp_min = min(temp_min, days[wday]["temp_min"])
            temp_max = max(temp_max, days[wday]["temp_max"])
        day_data = {"temp_min": round(temp_min, 1), "temp_max": round(temp_max, 1)}
        days[wday] = day_data
        pass

    return days


def get_buses():
    url = TIME_TABLE_URL
    filename = "buses.zip"
    response = requests.get(url)
    with open(filename, mode="wb") as file:
        file.write(response.content)

    from zipfile import ZipFile

    with ZipFile(filename, "r") as zObject:
        zObject.extractall("temp")
