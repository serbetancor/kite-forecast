import asyncio

from kite_forecast.config.beaches import BEACHES
from kite_forecast.config.spot_conditions import SPOT_CONDITIONS
from kite_forecast.providers.forecast_builder import build_hourly_forecasts
from kite_forecast.providers.open_meteo import OpenMeteoMarineProvider
from kite_forecast.providers.open_meteo_weather import OpenMeteoWeatherProvider
from kite_forecast.scoring.hourly import score_hourly_forecast


async def main() -> None:
    beach = BEACHES[0]
    conditions = SPOT_CONDITIONS[0]

    weather_provider = OpenMeteoWeatherProvider()
    marine_provider = OpenMeteoMarineProvider()

    weather_forecast = (await weather_provider.get_forecasts((beach,)))[0]

    marine_forecast = (await marine_provider.get_forecasts((beach,)))[0]

    hourly_forecasts = build_hourly_forecasts(
        weather_forecast,
        marine_forecast,
    )

    for forecast in hourly_forecasts:
        result = score_hourly_forecast(
            forecast,
            conditions,
        )

        print(f"\n{forecast.timestamp}")
        print("─" * 50)

        print(f"TOTAL: {result.score.total:.1f}")

        print(f"Wind: {result.score.wind.score:.1f} ({result.score.wind.reason})")

        print(f"  Speed score:     {result.wind.speed:.1f}")
        print(f"  Direction score: {result.wind.direction:.1f}")
        print(f"  Gusts score:     {result.wind.gusts:.1f}")

        print(f"Waves: {result.score.waves.score:.1f} ({result.score.waves.reason})")

        print(f"  Height score:    {result.waves.height:.1f}")
        print(f"  Period score:    {result.waves.period:.1f}")
        print(f"  Direction score: {result.waves.direction:.1f}")


if __name__ == "__main__":
    asyncio.run(main())
