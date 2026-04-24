from abc import ABC, abstractmethod
from enum import Enum
from http import HTTPStatus
import requests
from fastapi import FastAPI, status,Query
from fastapi.exceptions import HTTPException
from fastapi.responses import JSONResponse
from fastapi_swagger import patch_fastapi
from pydantic import BaseModel

app = FastAPI(docs_url=None, swagger_ui_oauth2_redirect_url=None)
patch_fastapi(app, docs_url="/swagger")


class WeatherProvider(str, Enum):
    OPENWEATHER = "openweather"
    OPENMETEO = "openmeteo"


class WeatherAbstract(ABC):
    @abstractmethod
    def get_current_weather(self, lat, lon):
        pass


class OpenWeatherProvider(WeatherAbstract):
    base_url = "https://api.openweathermap.org/data/2.5/weather"

    def __init__(self, api_key):
        self.api_key = api_key
    # because the service is not available now (International internet has disconnected)
    # I have to use mock data
    def get_current_weather(self, lat, lon):
            # params = {
        #     "lat": lat,
        #     "lon": lon,
        #     "appid": self.api_key,
        # }
        #     response = requests.get(self.base_url, params)
        #     normalized_data = {"temp": float(response.json()["main"]["temp"]) - 273.15 ,
        #                        "humidity": response.json()["main"]["humidity"],
        #                        "wind_speed": response.json()["main"]["wind_speed"]}
        normalized_data = {
        "temp": 25.0,
        "humidity": 60,
        "wind_speed": 5.5  # این فیلد در پاسخ OpenWeather اصلی نیست، آن را به ساختار خود اضافه کرده‌اید
    }
        return normalized_data


class OpenMeteoProvider(WeatherAbstract):
    base_url = "https://api.open-meteo.com/v1/forecast"

    def get_current_weather(self, lat, lon):
        # params = {
        #     "exclude": "hourly",
        #     "latitude": lat,
        #     "longitude": lon,
        #     "current": "temperature_2m,relative_humidity_2m"
        # }
        # response = requests.get(self.base_url, params)
        # normalized_data = {"temp": response.json()["current"]["temperature_2m"],
        #                    "humidity": response.json()["current"]["relative_humidity_2m"],
        #                    "wind_speed": response.json()["current"]["wind_speed"]}
        normalized_data = {
            "temp": 28.0,
            "humidity": 55,
            "wind_speed": 3.2
        }
        return normalized_data


# ge : Greater than or equal
# le : Less than or equal
@app.get("/weather")
async def get_weather(lat:float = Query(ge=-90.0,le=90.0,description="Latitude"),
                      lon:float = Query(ge=-180.0,le=180.0,description="Longitude"),
                      provider : WeatherProvider = Query(description="Weather Provider")):
    if provider == WeatherProvider.OPENWEATHER:
        return OpenWeatherProvider("91ef236cc9290c783d3e6572ecc7fd35").get_current_weather(lat, lon)
    elif provider == WeatherProvider.OPENMETEO:
        return OpenMeteoProvider().get_current_weather(lat, lon)
    else:
        raise HTTPException(detail="Weather Provider is not supported", status_code=HTTPStatus.BAD_REQUEST)
