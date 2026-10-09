import asyncio
from datetime import datetime

from kite_forecast.config.beaches import BEACHES
from kite_forecast.providers.forecast_builder import build_hourly_forecasts
from kite_forecast.providers.open_meteo_marine import OpenMeteoMarineProvider
from kite_forecast.providers.open_meteo_weather import OpenMeteoWeatherProvider
from kite_forecast.services.kite_sizing import build_kite_sizing_matrix
from kite_forecast.services.spot_scoring import score_forecast


async def main() -> None:
    beach = next(item for item in BEACHES if item.id == "salinas")
    timestamp = datetime.fromisoformat("2026-10-10T12:00")

    weather_provider = OpenMeteoWeatherProvider()
    marine_provider = OpenMeteoMarineProvider()

    weather = await weather_provider.get_forecast(beach, timestamp)
    marine = await marine_provider.get_forecast(beach, timestamp)

    forecasts = build_hourly_forecasts(weather, marine)
    if not forecasts:
        raise ValueError(f"No forecast found for {beach.name} at {timestamp}")

    forecast = forecasts[0]
    result = score_forecast(forecast)

    matrix = build_kite_sizing_matrix(forecast)

    print(f"Viento medio: {matrix.wind_speed_knots:.1f} kn")
    print(f"Rachas: {matrix.wind_gusts_knots:.1f} kn")

    print(f"\nCombinaciones generadas: {len(matrix.cells)}")
    print(f"Pesos: {matrix.weights_kg[0]}–{matrix.weights_kg[-1]} kg")
    print(f"Tallas: {matrix.kite_sizes_m2[0]}–{matrix.kite_sizes_m2[-1]} m²")

    print("\nIdoneidad para un rider de 75 kg:")
    for size in range(4, 22):
        cell = next(
            item
            for item in matrix.cells
            if item.weight_kg == 75 and item.kite_size_m2 == size
        )
        print(f"{size} m²: {cell.score:.1f}/100")

    print(f"Score velocidad: {result.wind.speed:.1f}/100")
    print(f"Score dirección: {result.wind.direction:.1f}/100")
    print(f"Score rachas: {result.wind.gusts:.1f}/100")
    print(f"Score viento: {result.wind.total:.1f}/100")

    print(f"Score olas: {result.score.waves.score:.1f}/100")
    print(f"Score total: {result.score.total:.1f}/100")


if __name__ == "__main__":
    asyncio.run(main())
