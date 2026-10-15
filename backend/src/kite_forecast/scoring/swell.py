from kite_forecast.models.forecast import HourlyForecast
from kite_forecast.models.score import (
    SwellScore,
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


def _swell_height_score(
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


def _swell_period_score(period_s: float, min_period_s: float) -> float:
    if period_s < min_period_s:
        return 0.0

    return min(100.0, 100.0 * period_s / (2 * min_period_s))


def score_swell(
    forecast: HourlyForecast,
    conditions: SpotConditions,
) -> SwellScore:
    swell_conditions = conditions.swell
    observation = forecast.marine

    height_score = _swell_height_score(
        observation.swell_wave_height_m,
        swell_conditions.min_height_m,
        swell_conditions.ideal_height_m,
        swell_conditions.max_height_m,
    )
    period_score = _swell_period_score(
        observation.swell_wave_period_s,
        swell_conditions.min_period_s,
    )
    direction_score = _direction_score(
        observation.swell_wave_direction_deg,
        swell_conditions.preferred_directions_deg,
        swell_conditions.direction_tolerance_deg,
    )

    weights = swell_conditions.score_weights
    total = (
        height_score * weights.height
        + period_score * weights.period
        + direction_score * weights.direction
    )

    return SwellScore(
        total=total,
        height=height_score,
        period=period_score,
        direction=direction_score,
    )
