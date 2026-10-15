from kite_forecast.models.forecast import HourlyForecast
from kite_forecast.models.score import WindScore
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


def _wind_speed_score(
    speed_kn: float,
    min_speed_kn: float,
    ideal_speed_kn: float,
    max_speed_kn: float,
) -> float:
    if speed_kn < min_speed_kn:
        return 0.0

    if speed_kn <= ideal_speed_kn:
        return linear_score(
            speed_kn,
            min_speed_kn,
            ideal_speed_kn,
            0.0,
            100.0,
        )

    if speed_kn <= max_speed_kn:
        return linear_score(
            speed_kn,
            ideal_speed_kn,
            max_speed_kn,
            100.0,
            0.0,
        )

    return 0.0


def _wind_gusts_score(gusts_kn: float, max_gust_kn: float) -> float:
    if gusts_kn <= max_gust_kn:
        return 100.0
    return max(0.0, 100.0 * max_gust_kn / gusts_kn)


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
