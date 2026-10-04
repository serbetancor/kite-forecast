from kite_forecast.models.score import WaveScoreBreakdown
from kite_forecast.models.spot_conditions import WaveConditions
from kite_forecast.scoring.utils import angular_distance_deg, linear_score


def score_wave_height(
    height_m: float,
    conditions: WaveConditions,
) -> float:
    if height_m < conditions.min_height_m:
        return 0.0

    if height_m <= conditions.ideal_height_m:
        return linear_score(
            height_m,
            conditions.min_height_m,
            conditions.ideal_height_m,
            0.0,
            100.0,
        )

    if height_m <= conditions.max_height_m:
        return linear_score(
            height_m,
            conditions.ideal_height_m,
            conditions.max_height_m,
            100.0,
            0.0,
        )

    return 0.0


def score_wave_period(
    period_s: float,
    conditions: WaveConditions,
) -> float:
    if period_s < conditions.min_period_s:
        return 0.0

    return 100.0


def score_waves(
    height_m: float,
    direction_deg: float,
    period_s: float,
    conditions: WaveConditions,
) -> WaveScoreBreakdown:
    height_score = score_wave_height(
        height_m,
        conditions,
    )

    direction_score = score_wave_direction(
        direction_deg,
        conditions,
    )

    period_score = score_wave_period(
        period_s,
        conditions,
    )

    weights = conditions.score_weights

    total = (
        height_score * weights.height
        + direction_score * weights.direction
        + period_score * weights.period
    )

    return WaveScoreBreakdown(
        height=height_score,
        direction=direction_score,
        period=period_score,
        total=total,
    )


def score_wave_direction(
    direction_deg: float,
    conditions: WaveConditions,
) -> float:
    closest_distance = min(
        angular_distance_deg(direction_deg, preferred_direction)
        for preferred_direction in conditions.preferred_directions_deg
    )

    tolerance = conditions.direction_tolerance_deg

    if closest_distance >= tolerance:
        return 0.0

    return 100.0 * (1 - closest_distance / tolerance)


def describe_waves(
    height_m: float,
    direction_deg: float,
    period_s: float,
) -> str:
    return f"{height_m:.1f} m, {direction_deg:.0f}°, período {period_s:.1f} s"
