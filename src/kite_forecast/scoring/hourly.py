from kite_forecast.models.forecast import HourlyForecast
from kite_forecast.models.score import ComponentScore, HourlyScore, HourlyScoreResult
from kite_forecast.models.spot_conditions import SpotConditions
from kite_forecast.scoring.wave import describe_waves, score_waves
from kite_forecast.scoring.wind import describe_wind, score_wind


def score_hourly_forecast(
    forecast: HourlyForecast,
    conditions: SpotConditions,
) -> HourlyScoreResult:
    wind = score_wind(
        speed_knots=forecast.weather.wind_speed_knots,
        direction_deg=forecast.weather.wind_direction_deg,
        gust_speed_knots=forecast.weather.wind_gusts_knots,
        conditions=conditions.wind,
    )

    waves = score_waves(
        height_m=forecast.marine.wave_height_m,
        direction_deg=forecast.marine.wave_direction_deg,
        period_s=forecast.marine.wave_period_s,
        conditions=conditions.waves,
    )

    total = wind.total * 0.6 + waves.total * 0.4

    score = HourlyScore(
        wind=ComponentScore(
            score=wind.total,
            reason=describe_wind(
                speed_knots=forecast.weather.wind_speed_knots,
                direction_deg=forecast.weather.wind_direction_deg,
                gust_speed_knots=forecast.weather.wind_gusts_knots,
            ),
        ),
        waves=ComponentScore(
            score=waves.total,
            reason=describe_waves(
                height_m=forecast.marine.wave_height_m,
                direction_deg=forecast.marine.wave_direction_deg,
                period_s=forecast.marine.wave_period_s,
            ),
        ),
        total=total,
    )

    return HourlyScoreResult(
        score=score,
        wind=wind,
        waves=waves,
    )
