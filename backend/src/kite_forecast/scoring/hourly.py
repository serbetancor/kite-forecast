from kite_forecast.models.forecast import HourlyForecast
from kite_forecast.models.score import (
    HourlyScore,
    WaveScore,
    WindScore,
)
from kite_forecast.models.spot_conditions import SpotConditions
from kite_forecast.scoring.wave import score_waves
from kite_forecast.scoring.wind import score_wind


def score_hourly_forecast(
    forecast: HourlyForecast,
    conditions: SpotConditions,
) -> HourlyScore:
    wind = score_wind(
        speed_kn=forecast.weather.wind_speed_kn,
        direction_deg=forecast.weather.wind_direction_deg,
        gust_speed_kn=forecast.weather.wind_gusts_kn,
        conditions=conditions.wind,
    )

    waves = score_waves(
        height_m=forecast.marine.wave_height_m,
        direction_deg=forecast.marine.wave_direction_deg,
        period_s=forecast.marine.wave_period_s,
        conditions=conditions.waves,
    )

    total = wind.total * 0.6 + waves.total * 0.4

    return HourlyScore(
        total=total,
        wind=WindScore(
            total=wind.total,
            speed=wind.speed,
            direction=wind.direction,
            gusts=wind.gusts,
        ),
        waves=WaveScore(
            total=waves.total,
            height=waves.height,
            period=waves.period,
            direction=waves.direction,
        ),
    )
