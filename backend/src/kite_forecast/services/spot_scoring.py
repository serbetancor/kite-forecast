from kite_forecast.config.spot_conditions import SPOT_CONDITIONS
from kite_forecast.models.forecast import HourlyForecast
from kite_forecast.models.score import (
    HourlyScore,
    WaveScore,
    WindScore,
)
from kite_forecast.models.spot_conditions import SpotConditions


def _direction_score(
    direction_deg: float,
    preferred_directions_deg: tuple[float, ...],
    tolerance_deg: float,
) -> float:
    differences = [
        abs((direction_deg - preferred + 180) % 360 - 180)
        for preferred in preferred_directions_deg
    ]
    difference = min(differences)
    return max(0.0, 100.0 * (1.0 - difference / tolerance_deg))


def _wind_speed_score(
    speed_kn: float,
    min_speed_kn: float,
    ideal_speed_kn: float,
    max_speed_kn: float,
) -> float:
    if speed_kn < min_speed_kn or speed_kn > max_speed_kn:
        return 0.0

    if speed_kn <= ideal_speed_kn:
        denominator = ideal_speed_kn - min_speed_kn
        if denominator == 0:
            return 100.0
        return 100.0 * (speed_kn - min_speed_kn) / denominator

    denominator = max_speed_kn - ideal_speed_kn
    if denominator == 0:
        return 100.0
    return 100.0 * (max_speed_kn - speed_kn) / denominator


def _wind_gusts_score(gusts_kn: float, max_gust_kn: float) -> float:
    if gusts_kn <= max_gust_kn:
        return 100.0
    return max(0.0, 100.0 * max_gust_kn / gusts_kn)


def _wave_height_score(
    height_m: float,
    min_height_m: float,
    ideal_height_m: float,
    max_height_m: float,
) -> float:
    if height_m < min_height_m or height_m > max_height_m:
        return 0.0

    if height_m <= ideal_height_m:
        denominator = ideal_height_m - min_height_m
        if denominator == 0:
            return 100.0
        return 100.0 * (height_m - min_height_m) / denominator

    denominator = max_height_m - ideal_height_m
    if denominator == 0:
        return 100.0
    return 100.0 * (max_height_m - height_m) / denominator


def _wave_period_score(period_s: float, min_period_s: float) -> float:
    if period_s < min_period_s:
        return 0.0

    return min(100.0, 100.0 * period_s / (2 * min_period_s))


def score_wind(
    forecast: HourlyForecast,
    conditions: SpotConditions,
) -> WindScore:
    wind_conditions = conditions.wind
    observation = forecast.weather

    speed_score = _wind_speed_score(
        observation.wind_speed_kn,
        wind_conditions.min_speed_kn,
        wind_conditions.ideal_speed_kn,
        wind_conditions.max_speed_kn,
    )
    direction_score = _direction_score(
        observation.wind_direction_deg,
        wind_conditions.preferred_directions_deg,
        wind_conditions.direction_tolerance_deg,
    )
    gusts_score = _wind_gusts_score(
        observation.wind_gusts_kn,
        wind_conditions.max_gust_kn,
    )

    if speed_score == 0.0:
        gusts_score = 0.0

    weights = wind_conditions.score_weights
    total = (
        speed_score * weights.speed
        + direction_score * weights.direction
        + gusts_score * weights.gusts
    )

    return WindScore(
        total=total,
        speed=speed_score,
        direction=direction_score,
        gusts=gusts_score,
    )


def score_waves(
    forecast: HourlyForecast,
    conditions: SpotConditions,
) -> WaveScore:
    wave_conditions = conditions.waves
    observation = forecast.marine

    height_score = _wave_height_score(
        observation.wave_height_m,
        wave_conditions.min_height_m,
        wave_conditions.ideal_height_m,
        wave_conditions.max_height_m,
    )
    period_score = _wave_period_score(
        observation.wave_period_s,
        wave_conditions.min_period_s,
    )
    direction_score = _direction_score(
        observation.wave_direction_deg,
        wave_conditions.preferred_directions_deg,
        wave_conditions.direction_tolerance_deg,
    )

    weights = wave_conditions.score_weights
    total = (
        height_score * weights.height
        + period_score * weights.period
        + direction_score * weights.direction
    )

    return WaveScore(
        total=total,
        height=height_score,
        period=period_score,
        direction=direction_score,
    )


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

    return HourlyScore(
        total=wind.total * 0.7 + waves.total * 0.3,
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
