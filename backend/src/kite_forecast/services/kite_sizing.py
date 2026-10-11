from kite_forecast.models.forecast import HourlyForecast
from kite_forecast.models.kite_sizing import (
    KiteSizingCell,
    KiteSizingMatrix,
)

WEIGHT_MIN_KG = 40
WEIGHT_MAX_KG = 120
WEIGHT_STEP_KG = 5

KITE_SIZE_MIN_M2 = 4
KITE_SIZE_MAX_M2 = 21

SIZE_TOLERANCE_RATIO = 0.25


def _suitability_score(
    kite_size_m2: int,
    ideal_size_m2: float,
) -> float:
    tolerance = ideal_size_m2 * SIZE_TOLERANCE_RATIO

    if tolerance <= 0:
        return 0.0

    difference = abs(kite_size_m2 - ideal_size_m2)
    score = 100.0 * (1.0 - difference / tolerance)

    return max(0.0, min(100.0, score))


def build_kite_sizing_matrix(
    forecast: HourlyForecast,
) -> KiteSizingMatrix:
    wind_speed = forecast.weather.wind_speed_kn
    wind_gusts = forecast.weather.wind_gusts_kn

    weights = list(
        range(
            WEIGHT_MIN_KG,
            WEIGHT_MAX_KG + 1,
            WEIGHT_STEP_KG,
        )
    )
    kite_sizes = list(range(KITE_SIZE_MIN_M2, KITE_SIZE_MAX_M2 + 1))

    cells: list[KiteSizingCell] = []

    for weight in weights:
        if wind_speed <= 0:
            ideal_size = 0.0
        else:
            ideal_size = weight * 2.2 / wind_speed

        for kite_size in kite_sizes:
            score = _suitability_score(
                kite_size,
                ideal_size,
            )

            cells.append(
                KiteSizingCell(
                    weight_kg=weight,
                    kite_size_m2=kite_size,
                    score=score,
                )
            )

    return KiteSizingMatrix(
        timestamp=forecast.timestamp,
        wind_speed_kn=wind_speed,
        wind_gusts_kn=wind_gusts,
        weights_kg=weights,
        kite_sizes_m2=kite_sizes,
        cells=cells,
    )
