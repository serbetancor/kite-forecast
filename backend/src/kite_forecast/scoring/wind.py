from kite_forecast.models.score import WindScore
from kite_forecast.models.spot_conditions import WindConditions
from kite_forecast.scoring.utils import (
    angular_distance_deg,
    linear_score,
)


def score_wind_speed(
    speed_knots: float,
    conditions: WindConditions,
) -> float:
    if speed_knots < conditions.min_speed_knots:
        return 0.0

    if speed_knots <= conditions.ideal_speed_knots:
        return linear_score(
            speed_knots,
            conditions.min_speed_knots,
            conditions.ideal_speed_knots,
            0.0,
            100.0,
        )

    if speed_knots <= conditions.max_speed_knots:
        return linear_score(
            speed_knots,
            conditions.ideal_speed_knots,
            conditions.max_speed_knots,
            100.0,
            0.0,
        )

    return 0.0


def score_wind_direction(
    direction_deg: float,
    conditions: WindConditions,
) -> float:
    closest_distance = min(
        angular_distance_deg(direction_deg, preferred_direction)
        for preferred_direction in conditions.preferred_directions_deg
    )

    tolerance = conditions.direction_tolerance_deg

    if closest_distance >= tolerance:
        return 0.0

    return 100.0 * (1 - closest_distance / tolerance)


def score_wind_gusts(
    gust_speed_knots: float,
    conditions: WindConditions,
) -> float:
    if gust_speed_knots <= conditions.max_gust_knots:
        return 100.0

    return 0.0


def score_wind(
    speed_knots: float,
    direction_deg: float,
    gust_speed_knots: float,
    conditions: WindConditions,
) -> WindScore:
    speed_score = score_wind_speed(
        speed_knots,
        conditions,
    )

    direction_score = score_wind_direction(
        direction_deg,
        conditions,
    )

    gust_score = score_wind_gusts(
        gust_speed_knots,
        conditions,
    )

    weights = conditions.score_weights

    total = (
        speed_score * weights.speed
        + direction_score * weights.direction
        + gust_score * weights.gusts
    )

    return WindScore(
        total=total,
        speed=speed_score,
        direction=direction_score,
        gusts=gust_score,
    )
