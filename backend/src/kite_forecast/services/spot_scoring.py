from kite_forecast.config.spot_conditions import SPOT_CONDITIONS
from kite_forecast.models.forecast import HourlyForecast
from kite_forecast.models.score import (
    ComponentScore,
    HourlyScore,
    HourlyScoreResult,
    WaveScoreBreakdown,
    WindScoreBreakdown,
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
    speed_knots: float,
    min_speed_knots: float,
    ideal_speed_knots: float,
    max_speed_knots: float,
) -> float:
    if speed_knots < min_speed_knots or speed_knots > max_speed_knots:
        return 0.0

    if speed_knots <= ideal_speed_knots:
        denominator = ideal_speed_knots - min_speed_knots
        if denominator == 0:
            return 100.0
        return 100.0 * (speed_knots - min_speed_knots) / denominator

    denominator = max_speed_knots - ideal_speed_knots
    if denominator == 0:
        return 100.0
    return 100.0 * (max_speed_knots - speed_knots) / denominator


def _wind_gusts_score(gusts_knots: float, max_gust_knots: float) -> float:
    if gusts_knots <= max_gust_knots:
        return 100.0
    return max(0.0, 100.0 * max_gust_knots / gusts_knots)


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
) -> WindScoreBreakdown:
    wind_conditions = conditions.wind
    observation = forecast.weather

    speed_score = _wind_speed_score(
        observation.wind_speed_knots,
        wind_conditions.min_speed_knots,
        wind_conditions.ideal_speed_knots,
        wind_conditions.max_speed_knots,
    )
    direction_score = _direction_score(
        observation.wind_direction_deg,
        wind_conditions.preferred_directions_deg,
        wind_conditions.direction_tolerance_deg,
    )
    gusts_score = _wind_gusts_score(
        observation.wind_gusts_knots,
        wind_conditions.max_gust_knots,
    )

    if speed_score == 0.0:
        gusts_score = 0.0

    weights = wind_conditions.score_weights
    total = (
        speed_score * weights.speed
        + direction_score * weights.direction
        + gusts_score * weights.gusts
    )

    return WindScoreBreakdown(
        speed=speed_score,
        direction=direction_score,
        gusts=gusts_score,
        total=total,
    )


def score_waves(
    forecast: HourlyForecast,
    conditions: SpotConditions,
) -> WaveScoreBreakdown:
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

    return WaveScoreBreakdown(
        height=height_score,
        period=period_score,
        direction=direction_score,
        total=total,
    )


def score_forecast(forecast: HourlyForecast) -> HourlyScoreResult:
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

    return HourlyScoreResult(
        score=HourlyScore(
            wind=ComponentScore(
                score=wind.total,
                reason="Provisional wind score.",
            ),
            waves=ComponentScore(
                score=waves.total,
                reason="Wave scoring is not calibrated yet.",
            ),
            total=wind.total * 0.7 + waves.total * 0.3,
        ),
        wind=wind,
        waves=waves,
    )
