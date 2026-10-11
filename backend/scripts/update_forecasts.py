import argparse
import asyncio
import json
import shutil
from pathlib import Path
from urllib.parse import urlencode

from kite_forecast.config.beaches import BEACHES
from kite_forecast.models.cached_forecast import CachedForecast
from kite_forecast.providers.client import get_json
from kite_forecast.providers.open_meteo_marine import (
    OpenMeteoMarineHourly,
    OpenMeteoMarineProvider,
    OpenMeteoMarineResponse,
    to_marine_forecast,
)
from kite_forecast.providers.open_meteo_weather import (
    OpenMeteoWeatherHourly,
    OpenMeteoWeatherProvider,
    OpenMeteoWeatherResponse,
    to_weather_forecast,
)

WEATHER_HOURLY_FIELDS = (
    "wind_speed_10m,wind_direction_10m,wind_gusts_10m,temperature_2m"
)

MARINE_HOURLY_FIELDS = (
    "wave_height,wave_direction,wave_period,"
    "sea_level_height_msl,ocean_current_velocity,"
    "ocean_current_direction"
)

MINIMUM_HOURLY_OBSERVATIONS = 24 * 6


def validate_hourly_data(
    hourly: OpenMeteoWeatherHourly | OpenMeteoMarineHourly,
    beach_id: str,
    forecast_type: str,
) -> None:
    lengths = [
        len(value)
        for value in (
            hourly.time,
            *(
                getattr(hourly, field_name)
                for field_name in type(hourly).model_fields
                if field_name != "time"
            ),
        )
    ]

    if len(set(lengths)) != 1:
        raise ValueError(
            f"Inconsistent hourly arrays in {forecast_type} forecast "
            f"for {beach_id}: {lengths}"
        )

    if lengths[0] < MINIMUM_HOURLY_OBSERVATIONS:
        raise ValueError(
            f"Insufficient hourly data in {forecast_type} forecast "
            f"for {beach_id}: {lengths[0]} observations"
        )


async def fetch_beach_forecast(beach_id: str) -> CachedForecast:
    beach = next((item for item in BEACHES if item.id == beach_id), None)

    if beach is None:
        raise ValueError(f"Unknown beach: {beach_id}")

    weather_url = (
        OpenMeteoWeatherProvider.BASE_URL
        + "?"
        + urlencode(
            {
                "latitude": beach.location.latitude,
                "longitude": beach.location.longitude,
                "hourly": WEATHER_HOURLY_FIELDS,
                "forecast_days": 7,
                "timezone": "Europe/Madrid",
            }
        )
    )

    marine_url = (
        OpenMeteoMarineProvider.BASE_URL
        + "?"
        + urlencode(
            {
                "latitude": beach.location.latitude,
                "longitude": beach.location.longitude,
                "hourly": MARINE_HOURLY_FIELDS,
                "forecast_days": 7,
                "timezone": "Europe/Madrid",
            }
        )
    )

    print(f"[{beach_id}] Consultando previsión meteorológica...")
    weather_data = await get_json(weather_url)
    weather_response = OpenMeteoWeatherResponse.model_validate(weather_data)

    print(f"[{beach_id}] Consultando previsión marina...")
    marine_data = await get_json(marine_url)
    marine_response = OpenMeteoMarineResponse.model_validate(marine_data)

    validate_hourly_data(weather_response.hourly, beach_id, "weather")
    validate_hourly_data(marine_response.hourly, beach_id, "marine")

    weather_forecast = to_weather_forecast(beach, weather_response)
    marine_forecast = to_marine_forecast(beach, marine_response)

    if len(marine_forecast.observations) < 24:
        raise ValueError(f"Insufficient valid marine observations for {beach_id}")

    return CachedForecast(
        weather=weather_forecast,
        marine=marine_forecast,
    )


def serialize_forecast(forecast: CachedForecast) -> str:
    return (
        json.dumps(
            forecast.model_dump(mode="json"),
            indent=2,
            ensure_ascii=False,
        )
        + "\n"
    )


async def update_single_beach(beach_id: str) -> None:
    forecast = await fetch_beach_forecast(beach_id)

    backend_dir = Path(__file__).resolve().parents[1]
    target_dir = backend_dir / "data" / "forecasts"
    target_dir.mkdir(parents=True, exist_ok=True)

    output_path = target_dir / f"{beach_id}.json"
    temporary_path = target_dir / f".{beach_id}.json.tmp"

    try:
        temporary_path.write_text(
            serialize_forecast(forecast),
            encoding="utf-8",
        )
        temporary_path.replace(output_path)
    finally:
        temporary_path.unlink(missing_ok=True)

    print(f"[{beach_id}] Previsión validada y guardada: {output_path.name}")


def recover_directories(
    target_dir: Path,
    staging_dir: Path,
    backup_dir: Path,
) -> None:
    if backup_dir.exists():
        if not target_dir.exists():
            backup_dir.rename(target_dir)
        else:
            shutil.rmtree(backup_dir)

    if staging_dir.exists():
        shutil.rmtree(staging_dir)


def publish_forecasts(
    staging_dir: Path,
    target_dir: Path,
    backup_dir: Path,
) -> None:
    had_previous_cache = target_dir.exists()

    if had_previous_cache:
        target_dir.rename(backup_dir)

    try:
        staging_dir.rename(target_dir)
    except OSError:
        if had_previous_cache and backup_dir.exists():
            backup_dir.rename(target_dir)
        raise

    if backup_dir.exists():
        shutil.rmtree(backup_dir)


async def update_forecasts() -> None:
    backend_dir = Path(__file__).resolve().parents[1]
    data_dir = backend_dir / "data"
    target_dir = data_dir / "forecasts"
    staging_dir = data_dir / ".forecasts-staging"
    backup_dir = data_dir / ".forecasts-backup"

    data_dir.mkdir(parents=True, exist_ok=True)
    recover_directories(target_dir, staging_dir, backup_dir)
    staging_dir.mkdir()

    try:
        for beach in BEACHES:
            print(f"[{beach.id}] Actualizando {beach.name}...")
            forecast = await fetch_beach_forecast(beach.id)

            output_path = staging_dir / f"{beach.id}.json"
            output_path.write_text(
                serialize_forecast(forecast),
                encoding="utf-8",
            )

            print(f"[{beach.id}] Previsión validada.")

        expected_files = {f"{beach.id}.json" for beach in BEACHES}
        actual_files = {path.name for path in staging_dir.glob("*.json")}

        if actual_files != expected_files:
            raise ValueError(f"Unexpected cache files: {actual_files}")

        publish_forecasts(staging_dir, target_dir, backup_dir)
        print("Caché de previsiones actualizada correctamente.")

    except Exception:
        if staging_dir.exists():
            shutil.rmtree(staging_dir)
        raise


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Actualiza la caché de previsiones de kite-forecast."
    )
    parser.add_argument(
        "--beach-id",
        choices=[beach.id for beach in BEACHES],
        help="Actualiza únicamente la playa indicada.",
    )
    return parser.parse_args()


async def main() -> None:
    args = parse_args()

    if args.beach_id:
        await update_single_beach(args.beach_id)
    else:
        await update_forecasts()


if __name__ == "__main__":
    asyncio.run(main())
