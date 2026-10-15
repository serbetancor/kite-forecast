from kite_forecast.models.forecast import HourlyForecast
from kite_forecast.models.score import WaveScore
from kite_forecast.models.spot_conditions import SpotConditions
from kite_forecast.scoring.utils import angular_distance_deg, linear_score


def _direction_score(
    direction_deg: float,
    preferred_directions_deg: tuple[float, ...],
    tolerance_deg: float,
) -> float:
    closest_distance = min(
        angular_distance_deg(direction_deg, preferred_direction)
        for preferred_direction in preferred_directions_deg
    )

    if closest_distance >= tolerance_deg:
        return 0.0

    return 100.0 * (1 - closest_distance / tolerance_deg)


def _wave_height_score(
    height_m: float,
    min_height_m: float,
    ideal_height_m: float,
    max_height_m: float,
) -> float:
    if height_m < min_height_m:
        return 0.0

    if height_m <= ideal_height_m:
        return linear_score(
            height_m,
            min_height_m,
            ideal_height_m,
            0.0,
            100.0,
        )

    if height_m <= max_height_m:
        return linear_score(
            height_m,
            ideal_height_m,
            max_height_m,
            100.0,
            0.0,
        )

    return 0.0


def _wave_period_score(period_s: float, min_period_s: float) -> float:
    if period_s < min_period_s:
        return 0.0

    return min(100.0, 100.0 * period_s / (2 * min_period_s))


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
        + direction_score * weights.direction
        + period_score * weights.period
    )

    return WaveScore(
        total=total,
        height=height_score,
        period=period_score,
        direction=direction_score,
    )
