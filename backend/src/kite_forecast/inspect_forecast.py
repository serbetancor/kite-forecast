import asyncio
from datetime import datetime

from kite_forecast.config.beaches import BEACHES
from kite_forecast.reports.objective import ObjectiveReport
from kite_forecast.services.forecast import ForecastService


def print_report(report: ObjectiveReport) -> None:
    print()
    print("=" * 50)
    print(f"{report.beach.name} — {report.timestamp}")
    print("=" * 50)

    print("\nWIND")
    print(f"  Speed:     {report.wind.speed_knots:.1f} kn")
    print(
        f"  Direction: {report.wind.direction_cardinal} "
        f"({report.wind.direction_deg:.0f}°)"
    )
    print(f"  Gusts:     {report.wind.gusts_knots:.1f} kn")

    print("\nWEATHER")
    print(f"  Temperature: {report.weather.temperature_c:.1f} °C")

    print("\nWAVES")
    print(f"  Height:    {report.waves.height_m:.2f} m")
    print(
        f"  Direction: {report.waves.direction_cardinal} "
        f"({report.waves.direction_deg:.0f}°)"
    )
    print(f"  Period:    {report.waves.period_s:.1f} s")

    print("\nSEA")
    print(f"  Level:     {report.sea.level_m:.2f} m")
    print(f"  Current:   {report.sea.current_velocity_kmh:.1f} km/h")
    print(
        f"  Direction: {report.sea.current_direction_cardinal} "
        f"({report.sea.current_direction_deg:.0f}°)"
    )

    print()


async def main() -> None:
    service = ForecastService()

    report = await service.get_forecast(
        beach=BEACHES[0],
        timestamp=datetime(2026, 10, 5, 12),
    )

    print_report(report)


if __name__ == "__main__":
    asyncio.run(main())
