from datetime import datetime

from kite_forecast.models.forecast import MarineForecast, MarineObservation
from kite_forecast.models.report import (
    TideEventReport,
    TideReport,
    TideTrend,
)

STABLE_THRESHOLD_M = 0.02


class TideService:
    @staticmethod
    def _get_trend(
        observations: list[MarineObservation],
        index: int,
    ) -> TideTrend:
        current_level = observations[index].sea_level_height_m

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
        observation: MarineObservation | None,
    ) -> TideEventReport | None:
        if observation is None:
            return None

        return TideEventReport(
            timestamp=observation.timestamp,
            level_m=observation.sea_level_height_m,
        )

    def get_tide_report(
        self,
        marine_forecast: MarineForecast,
        timestamp: datetime,
    ) -> TideReport:
        observations = sorted(
            marine_forecast.observations,
            key=lambda observation: observation.timestamp,
        )

        index_by_timestamp = {
            observation.timestamp: index
            for index, observation in enumerate(observations)
        }
        index = index_by_timestamp.get(timestamp)

        if index is None:
            raise ValueError(
                f"No marine observation found for {marine_forecast.beach.id} at {timestamp}"
            )

        high_tides, low_tides = self._get_extrema(observations)

        next_high = next(
            (
                observation
                for observation in high_tides
                if observation.timestamp > timestamp
            ),
            None,
        )
        next_low = next(
            (
                observation
                for observation in low_tides
                if observation.timestamp > timestamp
            ),
            None,
        )

        return TideReport(
            trend=self._get_trend(observations, index),
            next_high_tide=self._to_event(next_high),
            next_low_tide=self._to_event(next_low),
        )
