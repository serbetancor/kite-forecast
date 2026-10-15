from kite_forecast.config.spot_conditions import SPOT_CONDITIONS
from kite_forecast.models.forecast import HourlyForecast
from kite_forecast.models.score import HourlyScore, SwellScore, WaveScore, WindScore
from kite_forecast.scoring.swell import score_swell
from kite_forecast.scoring.wave import score_waves
from kite_forecast.scoring.wind import score_wind


def score_forecast(forecast: HourlyForecast) -> HourlyScore:
    conditions = next(
        (item for item in SPOT_CONDITIONS if item.beach_id == forecast.beach.id),
        None,
    )
    if conditions is None:
        raise ValueError(
            f"No scoring configuration found for beach: {forecast.beach.id}"
        )

    wind = score_wind(forecast, conditions)
    waves = score_waves(forecast, conditions)
    swell = score_swell(forecast, conditions)

    return HourlyScore(
        total=wind.total * 0.8 + waves.total * 0.1 + swell.total * 0.1,
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
        swell=SwellScore(
            total=swell.total,
            height=swell.height,
            period=swell.period,
            direction=swell.direction,
        ),
    )
