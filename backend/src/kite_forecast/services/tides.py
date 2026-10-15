from datetime import datetime

from kite_forecast.models.beach import Beach
from kite_forecast.models.forecast import MarineObservation
from kite_forecast.models.report import (
    TideEventReport,
    TideReport,
    TideTrend,
)
from kite_forecast.services.forecast_cache import ForecastCache

STABLE_THRESHOLD_M = 0.02


class TideService:
    def __init__(self, cache: ForecastCache) -> None:
        self.cache = cache

    def _get_observations(self, beach: Beach) -> list[MarineObservation]:
        cached_forecast = self.cache.get_forecast(beach)

        return sorted(
            cached_forecast.marine.observations,
            key=lambda observation: observation.timestamp,
        )

    @staticmethod
    def _get_trend(
        observations: list[MarineObservation],
        index: int,
    ) -> TideTrend:
        current = observations[index]
        current_level = current.sea_level_height_m

        if 0 < index < len(observations) - 1:
            previous_level = observations[index - 1].sea_level_height_m
            next_level = observations[index + 1].sea_level_height_m

            if current_level > previous_level and current_level >= next_level:
                return "high_tide"

            if current_level < previous_level and current_level <= next_level:
                return "low_tide"

        if index + 1 < len(observations):
            delta = observations[index + 1].sea_level_height_m - current_level
        elif index > 0:
            delta = current_level - observations[index - 1].sea_level_height_m
        else:
            return "stable"

        if delta > STABLE_THRESHOLD_M:
            return "rising"
        if delta < -STABLE_THRESHOLD_M:
            return "falling"

        return "stable"

    @staticmethod
    def _get_extrema(
        observations: list[MarineObservation],
    ) -> tuple[list[MarineObservation], list[MarineObservation]]:
        high_tides: list[MarineObservation] = []
        low_tides: list[MarineObservation] = []

        for index in range(1, len(observations) - 1):
            previous_level = observations[index - 1].sea_level_height_m
            current_level = observations[index].sea_level_height_m
            next_level = observations[index + 1].sea_level_height_m

            if current_level > previous_level and current_level >= next_level:
                high_tides.append(observations[index])
            elif current_level < previous_level and current_level <= next_level:
                low_tides.append(observations[index])

        return high_tides, low_tides

    @staticmethod
    def _to_event(
        observation: MarineObservation,
    ) -> TideEventReport:

        return TideEventReport(
            timestamp=observation.timestamp,
            level_m=observation.sea_level_height_m,
        )

    def get_tide_report(
        self,
        beach: Beach,
        timestamp: datetime,
    ) -> TideReport:
        observations = self._get_observations(beach)

        index_by_timestamp = {
            observation.timestamp: index
            for index, observation in enumerate(observations)
        }
        index = index_by_timestamp.get(timestamp)

        if index is None:
            raise ValueError(
                f"No marine observation found for {beach.id} at {timestamp}"
            )

        high_tides, low_tides = self._get_extrema(observations)

        next_high = next(
            (
                observation
                for observation in high_tides
                if observation.timestamp > timestamp
            ),
        )
        next_low = next(
            (
                observation
                for observation in low_tides
                if observation.timestamp > timestamp
            ),
        )

        return TideReport(
            trend=self._get_trend(observations, index),
            next_high_tide=self._to_event(next_high),
            next_low_tide=self._to_event(next_low),
        )
