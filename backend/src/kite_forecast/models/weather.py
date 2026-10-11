from datetime import datetime

from pydantic import BaseModel

from kite_forecast.models.beach import Beach


class WeatherObservation(BaseModel):
    timestamp: datetime
    wind_speed_kmh: float
    wind_direction_deg: float
    wind_gusts_kmh: float
    temperature_c: float


class WeatherForecast(BaseModel):
    beach: Beach
    model_latitude: float
    model_longitude: float
    observations: list[WeatherObservation]
