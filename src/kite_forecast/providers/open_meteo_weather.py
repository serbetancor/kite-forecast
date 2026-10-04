from datetime import datetime

from pydantic import BaseModel

from kite_forecast.models.beach import Beach
from kite_forecast.models.weather import WeatherForecast, WeatherObservation
from kite_forecast.providers.client import get_json


class OpenMeteoWeatherHourly(BaseModel):
    time: list[str]
    wind_speed_10m: list[float]
    wind_direction_10m: list[float]
    wind_gusts_10m: list[float]
    temperature_2m: list[float]


class OpenMeteoWeatherResponse(BaseModel):
    latitude: float
    longitude: float
    timezone: str
    hourly: OpenMeteoWeatherHourly


class OpenMeteoWeatherProvider:
    BASE_URL = "https://api.open-meteo.com/v1/forecast"

    async def get_forecasts(
        self,
        beaches: tuple[Beach, ...],
    ) -> list[WeatherForecast]:
        latitudes = ",".join(str(beach.location.latitude) for beach in beaches)
        longitudes = ",".join(str(beach.location.longitude) for beach in beaches)

        url = (
            f"{self.BASE_URL}"
            f"?latitude={latitudes}"
            f"&longitude={longitudes}"
            "&hourly=wind_speed_10m,wind_direction_10m,"
            "wind_gusts_10m,temperature_2m"
            "&forecast_days=2"
            "&timezone=Europe%2FMadrid"
        )

        data = await get_json(url)

        if isinstance(data, list):
            locations = [
                OpenMeteoWeatherResponse.model_validate(location) for location in data
            ]
        else:
            locations = [OpenMeteoWeatherResponse.model_validate(data)]

        return [
            to_weather_forecast(beach, response)
            for beach, response in zip(beaches, locations)
        ]


def to_weather_observations(
    response: OpenMeteoWeatherResponse,
) -> list[WeatherObservation]:
    hourly = response.hourly

    return [
        WeatherObservation(
            timestamp=datetime.fromisoformat(timestamp),
            wind_speed_knots=wind_speed,
            wind_direction_deg=wind_direction,
            wind_gusts_knots=wind_gusts,
            temperature_c=temperature,
        )
        for (
            timestamp,
            wind_speed,
            wind_direction,
            wind_gusts,
            temperature,
        ) in zip(
            hourly.time,
            hourly.wind_speed_10m,
            hourly.wind_direction_10m,
            hourly.wind_gusts_10m,
            hourly.temperature_2m,
        )
    ]


def to_weather_forecast(
    beach: Beach,
    response: OpenMeteoWeatherResponse,
) -> WeatherForecast:
    return WeatherForecast(
        beach=beach,
        model_latitude=response.latitude,
        model_longitude=response.longitude,
        observations=to_weather_observations(response),
    )
