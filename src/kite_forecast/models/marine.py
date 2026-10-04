from datetime import datetime

from pydantic import BaseModel

from kite_forecast.models.beach import Beach


class MarineObservation(BaseModel):
    timestamp: datetime
    wave_height_m: float
    wave_direction_deg: float
    wave_period_s: float
    sea_level_height_m: float
    current_velocity_kmh: float
    current_direction_deg: float


class MarineForecast(BaseModel):
    beach: Beach
    model_latitude: float
    model_longitude: float
    observations: list[MarineObservation]
