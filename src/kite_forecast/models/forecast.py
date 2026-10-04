from datetime import datetime

from pydantic import BaseModel

from kite_forecast.models.beach import Beach
from kite_forecast.models.marine import MarineObservation
from kite_forecast.models.weather import WeatherObservation


class HourlyForecast(BaseModel):
    beach: Beach
    timestamp: datetime
    weather: WeatherObservation
    marine: MarineObservation
