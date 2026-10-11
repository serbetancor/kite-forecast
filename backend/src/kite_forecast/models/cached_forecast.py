from pydantic import BaseModel, model_validator

from kite_forecast.models.marine import MarineForecast
from kite_forecast.models.weather import WeatherForecast


class CachedForecast(BaseModel):
    weather: WeatherForecast
    marine: MarineForecast

    @model_validator(mode="after")
    def validate_matching_beaches(self) -> "CachedForecast":
        if self.weather.beach.id != self.marine.beach.id:
            raise ValueError(
                "Weather and marine forecasts must belong to the same beach"
            )

        return self
