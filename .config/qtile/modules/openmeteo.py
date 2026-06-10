import json
import subprocess
import time
from datetime import datetime
from typing import Any
from urllib.request import urlopen

from libqtile.widget import GenPollText
from modules.colors import colors
from qtile_extras.popup import PopupRelativeLayout, PopupText
from qtile_extras.widget.mixins import ExtendedPopupMixin, TooltipMixin


# get location info
def get_ip_data() -> dict:
    url = "http://ipinfo.io/json"
    try:
        resp = urlopen(url)
        return json.load(resp)
    except:
        with open("/home/slats/.config/qtile/resourses/geoip.json") as file:
            return json.load(file)


def get_coordinates() -> tuple:
    """Returns current coordinates using IP address"""
    data = get_ip_data()
    latitude = data["loc"].split(",")[0]
    longitude = data["loc"].split(",")[1]
    location = data["city"]
    timezone = data["timezone"]
    return latitude, longitude, location, timezone


locations = {"Saint Petersburg": "Санкт-Петербург"}


# class for fetching weatherdata from openemeteo.com and display it as a widget
# including simple weather forecast data a widget tooltip


class OpenMeteo(GenPollText, TooltipMixin, ExtendedPopupMixin):
    """A widget for the Qtile windowmanager to display weather data and a simple forecast from openmeteo.com.
    Place the file openmeteo.py in your .config/qtile directory and add the following to you config.py:

    import openmeteo
    ...

    widgets_list = [
    ...
    ...
    ...
    # openmeteo weather widget
    openmeteo.OpenMeteo(
                    fontsize=16,
                    foreground=colors[14],
                    font="IBM Plex Sans SmBld",
                    tooltip_fontsize=14,
                    tooltip_color=colors[14],
                    tooltip_background=colors[20],
                    update_interval=600,
                    language="ru",
        ),
    ...
    ...
    ...
    ]

    See defaults below for a list of parameters.
    update_interval is in seconds, if you leave language unset it defaults to english.
    """

    """
    WMO Weather interpretation codes (WW)
    Clear & Cloudy
    0               Clear sky
    1, 2, 3         Mainly clear, partly cloudy, and overcast
    Fog
    45, 48          Fog and depositing rime fog
    Drizzle
    51, 53, 55      Light, moderate, and dense drizzle
    56, 57          Light and dense freezing drizzle
    Rain
    61, 63, 65      Slight, moderate, and heavy rain
    66, 67          Light and heavy freezing rain
    Snow
    71, 73, 75      Slight, moderate, and heavy snowfall
    77              Snow grains
    Showers
    80, 81, 82      Slight, moderate, and violent rain showers
    85, 86          Slight and heavy snow showers
    Thunderstorm
    95              Slight or moderate thunderstorm
    96, 99          Thunderstorm with slight and heavy hail
    """

    wmo_symbols_day = {
        "Default": "",
        "0": "",
        "1": "",
        "2": "",
        "3": "",
        "45": "",
        "48": "",
        "51": "",
        "53": "",
        "55": "",
        "56": "",
        "57": "",
        "61": "",
        "63": "",
        "65": "",
        "66": "",
        "67": "",
        "71": "",
        "73": "",
        "75": "",
        "77": "",
        "80": "",
        "81": "",
        "82": "",
        "85": "",
        "86": "",
        "95": "",
        "96": "",
        "99": "",
    }

    wmo_symbols_night = {
        "Default": "",
        "0": "",
        "1": "",
        "2": "",
        "3": "",
        "45": "",
        "48": "",
        "51": "",
        "53": "",
        "55": "",
        "56": "",
        "57": "",
        "61": "",
        "63": "",
        "65": "",
        "66": "",
        "67": "",
        "71": "",
        "73": "",
        "75": "",
        "77": "",
        "80": "",
        "81": "",
        "82": "",
        "85": "",
        "86": "",
        "95": "",
        "96": "",
        "99": "",
    }

    # wind directions
    wind_directions_en = [
        "N",
        "NE",
        "E",
        "SE",
        "S",
        "SW",
        "W",
        "NW",
    ]

    wind_directions_ru = {
        "N": "северный",
        "NE": "северо-восточный",
        "E": "восточный",
        "SE": "юго-восточный",
        "S": "южный",
        "SW": "юго-западный",
        "W": "западный",
        "NW": "северо-западный",
    }

    wind_direction_symbols = {
        "N": "↓",
        "NE": "↙",
        "E": "←",
        "SE": "↖",
        "S": "↑",
        "SW": "↗",
        "W": "→",
        "NW": "↘",
    }

    defaults: list[tuple[str, Any, str]] = [
        (
            "format",
            " {icon}   {temp} {wind_direction}{wind_speed}",
            "Display format",
        ),
        (
            "format_forecast",
            "{day}   {temp_max}/{temp_min}  {weather_details}   {precipitations}",
            "Display format for forecast",
        ),
        (
            "dateformat",
            "%a %d.%m",
            """Format for dates as in strftime""",
        ),
        (
            "timeformat",
            "%H:%M",
            """Format for times, as in strftime""",
        ),
        (
            "language",
            "en",
            """Language of response, e.g. 'en'""",
        ),
    ]

    # See documentation: https://open-meteo.com

    # constructor
    def __init__(self, **config):
        config["func"] = self.poll
        GenPollText.__init__(self, **config)
        self.add_defaults(OpenMeteo.defaults)
        coordinates = get_coordinates()
        self.latitude = coordinates[0]
        self.longitude = coordinates[1]
        determined_location = coordinates[2]
        self.location = locations.get(determined_location, determined_location)
        self.timezone = coordinates[3]
        self.current_icon = self.wmo_symbols_day["Default"]
        self.current_weather = "No Info"
        self.forecast = "No Info"

        TooltipMixin.__init__(self, **config)
        self.add_defaults(TooltipMixin.defaults)

        ExtendedPopupMixin.__init__(self, **config)
        self.add_defaults(ExtendedPopupMixin.defaults)
        self.add_callbacks({"Button1": self.show_popup})
        self.popup_layout = PopupRelativeLayout(
            width=430,
            height=250,
            controls=[
                PopupText(
                    name="current_icon",
                    pos_x=0.03,
                    pos_y=0.1,
                    width=0.16,
                    height=0.2,
                    h_align="left",
                    font="IBM Plex Sans SmBld, Hack Nerd Font Bold",
                    fontsize=60,
                    foreground=colors[14],
                ),
                PopupText(
                    name="current_weather",
                    pos_x=0.19,
                    pos_y=0.01,
                    width=0.8,
                    height=0.55,
                    h_align="right",
                    font="IBM Plex Sans SmBld, Hack Nerd Font Bold",
                    fontsize=14,
                    foreground=colors[14],
                ),
                PopupText(
                    pos_x=0.01,
                    pos_y=0.58,
                    width=0.99,
                    height=0.01,
                    h_align="center",
                    background=colors[14],
                ),
                PopupText(
                    name="forecast",
                    pos_x=0.01,
                    pos_y=0.59,
                    width=0.98,
                    height=0.42,
                    h_align="left",
                    font="IBM Plex Sans SmBld, Hack Nerd Font Bold",
                    fontsize=14,
                    foreground=colors[14],
                ),
            ],
            background=colors[22],
        )

        # build url
        self.query_url = f"https://api.open-meteo.com/v1/forecast?latitude={self.latitude}&longitude={self.longitude}"
        daily_params = "&daily=weather_code,temperature_2m_max,temperature_2m_min,sunrise,sunset,uv_index_max,precipitation_probability_max,wind_speed_10m_max,wind_gusts_10m_max"
        current_params = "&current=temperature_2m,relative_humidity_2m,apparent_temperature,is_day,weather_code,pressure_msl,surface_pressure,wind_speed_10m,wind_direction_10m,wind_gusts_10m"
        misc_params = f"&timezone={self.timezone}&wind_speed_unit=ms"

        url = self.query_url + daily_params + current_params + misc_params
        self.url = url

    def poll(self):
        max_retries = 3
        retry_delay = 2
        error_icon = ""
        cmd = [
            "curl",
            "-s",
            "--socks5-hostname",
            "localhost:12334",
            self.url,
        ]
        for attempt in range(max_retries):
            try:
                result = subprocess.run(cmd, capture_output=True, text=True, timeout=5)
                if result.returncode == 0:
                    response_json = json.loads(result.stdout)
                    return self.parse(response_json)

            except (json.JSONDecodeError, subprocess.TimeoutExpired):
                pass
            except Exception:
                pass

            if attempt < max_retries - 1:
                time.sleep(retry_delay)

        self.current_weather = "Прокси или сеть недоступны"
        self.forecast = "Не удалось обновить прогноз погоды"

        return f" {error_icon} Network Error"

    def parse(self, data):
        sunrise_time = datetime.fromisoformat(data["daily"]["sunrise"][0])
        sunset_time = datetime.fromisoformat(data["daily"]["sunset"][0])
        data["sunrise"] = sunrise_time.strftime(self.timeformat)
        data["sunset"] = sunset_time.strftime(self.timeformat)
        wind_direction = self.degrees_to_direction(
            data["current"]["wind_direction_10m"]
        )
        data["wind_direction"] = self.wind_direction_symbols[wind_direction]
        data["wind_speed"] = (
            f"{data['current']['wind_speed_10m']} {data['current_units']['wind_speed_10m']}"
        )
        data["wind_speed_max"] = (
            f"{data['daily']['wind_speed_10m_max'][0]} {data['daily_units']['wind_speed_10m_max']}"
        )
        data["wind_gusts"] = (
            f"{data['daily']['wind_gusts_10m_max'][0]} {data['daily_units']['wind_gusts_10m_max']}"
        )
        data["weather_details"] = self.wmocode2text(data["current"]["weather_code"])
        data["humidity"] = (
            f"{data['current']['relative_humidity_2m']}{data['current_units']['relative_humidity_2m']}"
        )
        data["temp"] = (
            f"{data['current']['temperature_2m']}{data['current_units']['temperature_2m']}"
        )
        data["apparent_temperature"] = (
            f"{data['current']['apparent_temperature']}{data['current_units']['apparent_temperature']}"
        )
        data["location"] = self.location
        data["icon"] = self.wmo_symbols_day["Default"]
        if data["current"]["is_day"] == 1:
            data["icon"] = self.wmo_symbols_day[str(data["current"]["weather_code"])]
        else:
            data["icon"] = self.wmo_symbols_night[str(data["current"]["weather_code"])]
        data["uv"] = data["daily"]["uv_index_max"][0]
        data["precipitations"] = (
            f"{data['daily']['precipitation_probability_max'][0]}{data['daily_units']['precipitation_probability_max']}"
        )

        # current and daily weather
        current = (
            f"{self.location}\n"
            f"{data['weather_details']}, по ощущениям {data['apparent_temperature']}\n"
            f"относительная влажность {data['humidity']}\n"
            f"вероятность осадков {data['precipitations']}"
        )

        current_daily = (
            f"{self.location}\n"
            f"{data['weather_details']}, по ощущениям {data['apparent_temperature']}\n"
            f"относительная влажность {data['humidity']}\n"
            f"вероятность осадков {data['precipitations']}\n"
            f"max скорость ветра {data['wind_speed_max']}, порывы до {data['wind_gusts']}\n"
            f"max UV-индекс {data['uv']}\n"
            f"восход {data['sunrise']}, закат {data['sunset']}"
        )
        # forecast
        fc = ""
        for i in range(1, 6):
            d = dict()
            day = datetime.strptime(data["daily"]["time"][i], "%Y-%m-%d")
            d["day"] = day.strftime(self.dateformat)
            d["temp_min"] = (
                f"{data['daily']['temperature_2m_min'][i]}{data['daily_units']['temperature_2m_min']}"
            )
            d["temp_max"] = (
                f"{data['daily']['temperature_2m_max'][i]}{data['daily_units']['temperature_2m_max']}"
            )
            d["icon"] = self.wmo_symbols_day[str(data["daily"]["weather_code"][i])]
            d["weather_details"] = self.wmocode2text(data["daily"]["weather_code"][i])
            d["precipitations"] = (
                f"{data['daily']['precipitation_probability_max'][i]}{data['daily_units']['precipitation_probability_max']}"
            )
            fc = fc + self.format_forecast.format(**d) + "\n"
        forecast = fc[:-1]  # cut last newline

        self.tooltip_text = current
        self.current_icon = data["icon"]
        self.current_weather = current_daily
        self.forecast = forecast

        return self.format.format(**data)

    def _update_popup(self):
        current_weather = self.current_weather
        current_icon = self.current_icon
        forecast = self.forecast
        self.extended_popup.update_controls(
            current_weather=current_weather,
            forecast=forecast,
            current_icon=current_icon,
        )

    # convert the wind direction in degrees to a direction
    def degrees_to_direction(self, degrees):
        val = int((degrees + 22.5) // 45 % 8)
        wdir = self.wind_directions_en[val]
        return wdir

    # convert a WMO weathercode to a textual description
    def wmocode2text(self, wmocode):
        wmo_text_en = {
            "Default": "missing",
            "0": "clear sky️",
            "1": "mainly clear️",
            "2": "partly cloudy",
            "3": "overcast️",
            "45": "fog",
            "48": "rime fog",
            "51": "light drizzle️",
            "53": "moderate drizzle️",
            "55": "dense drizzle️",
            "56": "light freezing drizzle️",
            "57": "dense freezing drizzle️",
            "61": "light rain️",
            "63": "moderate rain️",
            "65": "heavy rain️",
            "66": "light freezing rain️",
            "67": "heavy freezing rain️",
            "71": "slight snow fall️",
            "73": "moderate snow fall️",
            "75": "heavy snow fall️",
            "77": "snow grains️",
            "80": "slight showers️",
            "81": "moderate showers️",
            "82": "heavy showers️",
            "85": "slight snow showers️",
            "86": "heavy snow showers",
            "95": "thunderstorm",
            "96": "thunderstorm with slight hail",
            "99": "thunderstorm with heavy hail",
        }

        wmo_text_ru = {
            "Default": "missing",
            "0": "ясно",
            "1": "в основном ясно",
            "2": "переменная облачность",
            "3": "пасмурно",
            "45": "туман",
            "48": "изморозь",
            "51": "слабая морось",
            "53": "умеренная морось",
            "55": "сильная морось",
            "56": "слабая ледяная морось",
            "57": "сильная ледяная морось",
            "61": "слабый дождь",
            "63": "умеренный дождь",
            "65": "сильный (проливной) дождь",
            "66": "слабый ледяной дождь",
            "67": "сильный ледяной дождь",
            "71": "слабый снегопад",
            "73": "умеренный снегопад",
            "75": "сильный снегопад",
            "77": "снежная крупа",
            "80": "слабый ливневый дождь",
            "81": "умеренный ливневый дождь",
            "82": "сильный ливневый дождь",
            "85": "слабый ливневый снег",
            "86": "сильный ливневый снег",
            "95": "гроза",
            "96": "гроза с небольшим градом",
            "99": "гроза с сильным градом",
        }

        # select language dictionary
        wmo_text = wmo_text_en if self.language == "en" else wmo_text_ru

        # return translated weather description
        if str(wmocode) in wmo_text.keys():
            return wmo_text[str(wmocode)]
        else:
            return wmo_text["Default"]
