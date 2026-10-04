from kite_forecast.models.forecast import HourlyForecast
from kite_forecast.models.marine import MarineForecast
from kite_forecast.models.weather import WeatherForecast


def build_hourly_forecasts(
    weather_forecast: WeatherForecast,
    marine_forecast: MarineForecast,
) -> list[HourlyForecast]:
    marine_by_timestamp = {
        observation.timestamp: observation
        for observation in marine_forecast.observations
    }

    return [
        HourlyForecast(
            beach=weather_forecast.beach,
            timestamp=weather_observation.timestamp,
            weather=weather_observation,
            marine=marine_by_timestamp[weather_observation.timestamp],
        )
        for weather_observation in weather_forecast.observations
        if weather_observation.timestamp in marine_by_timestamp
    ]
