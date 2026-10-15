from datetime import datetime

from pydantic import BaseModel

from kite_forecast.models.beach import Beach
from kite_forecast.models.score import HourlyScore
from datetime import datetime
from typing import Literal

from pydantic import BaseModel

TideTrend = Literal[
    "rising",
    "falling",
    "stable",
    "high_tide",
    "low_tide",
]


class TideEventReport(BaseModel):
    timestamp: datetime
    level_m: float


class TideReport(BaseModel):
    trend: TideTrend
    next_high_tide: TideEventReport
    next_low_tide: TideEventReport


class WindReport(BaseModel):
    speed_kn: float
    direction_deg: float
    direction_cardinal: str
    gusts_kn: float


class WavesReport(BaseModel):
    height_m: float
    direction_deg: float
    direction_cardinal: str
    period_s: float


class SwellReport(BaseModel):
    height_m: float
    direction_deg: float
    direction_cardinal: str
    period_s: float


class SeaReport(BaseModel):
    level_m: float
    current_velocity_kmh: float
    current_direction_deg: float
    current_direction_cardinal: str


class WeatherReport(BaseModel):
    temperature_c: float


class ObjectiveReport(BaseModel):
    beach: Beach
    timestamp: datetime
    wind: WindReport
    waves: WavesReport
    swell: SwellReport
    sea: SeaReport
    tide: TideReport
    weather: WeatherReport
    score: HourlyScore
