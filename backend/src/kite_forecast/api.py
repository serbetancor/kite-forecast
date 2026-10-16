import os
from datetime import date, datetime
from typing import TypedDict
from zoneinfo import ZoneInfo

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from kite_forecast.config.beaches import BEACHES
from kite_forecast.models.forecast import (
    MarineForecast,
    WeatherForecast,
)
from kite_forecast.models.requests import (
    ForecastRequest,
    KiteSizingRequest,
    ScoresRequest,
)
from kite_forecast.models.scored_forecast import ScoredHour
from kite_forecast.providers.forecast_builder import build_hourly_forecasts
from kite_forecast.providers.open_meteo_marine import to_marine_forecast
from kite_forecast.providers.open_meteo_weather import to_weather_forecast
from kite_forecast.services.forecast import ForecastService
from kite_forecast.services.spot_scoring import score_forecast

app = FastAPI(title="Kite Forecast API")


frontend_urls = os.getenv("FRONTEND_URL", "http://localhost:5173")

app.add_middleware(
    CORSMiddleware,
    allow_origins=frontend_urls,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

forecast_service = ForecastService()
CANARY_TZ = ZoneInfo("Atlantic/Canary")


class BeachConfig(TypedDict):
    id: str
    name: str
    latitude: float
    longitude: float


class AppConfig(TypedDict):
    forecast_horizon_days: int
    beaches: list[BeachConfig]


def _get_beach(beach_id: str):
    beach = next(
        (item for item in BEACHES if item.id == beach_id),
        None,
    )
    if beach is None:
        raise HTTPException(
            status_code=404,
            detail=f"Unknown beach: {beach_id}",
        )
    return beach


def _get_timestamp(target_date: date, time: str) -> datetime:
    try:
        return datetime.fromisoformat(f"{target_date}T{time}")
    except ValueError as error:
        raise HTTPException(
            status_code=400,
            detail="Invalid time format",
        ) from error


@app.get("/config")
async def get_config() -> AppConfig:
    return {
        "forecast_horizon_days": 7,
        "beaches": [
            {
                "id": beach.id,
                "name": beach.name,
                "latitude": beach.location.latitude,
                "longitude": beach.location.longitude,
            }
            for beach in BEACHES
        ],
    }


@app.post("/forecast")
async def get_forecast(request: ForecastRequest):
    beach = _get_beach(request.beach)
    timestamp = _get_timestamp(request.target_date, request.time)

    try:
        weather_forecast = to_weather_forecast(
            beach,
            request.weather,
        )
        marine_forecast = to_marine_forecast(
            beach,
            request.marine,
        )

        return forecast_service.get_forecast(
            beach,
            timestamp,
            weather_forecast,
            marine_forecast,
        )
    except ValueError as error:
        raise HTTPException(status_code=422, detail=str(error)) from error


@app.post("/kite-sizing")
async def get_kite_sizing(request: KiteSizingRequest):
    beach = _get_beach(request.beach)
    timestamp = _get_timestamp(request.target_date, request.time)

    try:
        weather_forecast = to_weather_forecast(
            beach,
            request.weather,
        )
        return forecast_service.get_kite_sizing(
            beach,
            timestamp,
            weather_forecast,
        )
    except ValueError as error:
        raise HTTPException(status_code=422, detail=str(error)) from error


@app.post("/scores")
async def get_scores(request: ScoresRequest) -> list[ScoredHour]:
    entries: list[ScoredHour] = []
    seen: set[tuple[str, datetime]] = set()

    for item in request.forecasts:
        beach = _get_beach(item.beach_id)

        try:
            weather_forecast: WeatherForecast = to_weather_forecast(
                beach,
                item.weather,
            )
            marine_forecast: MarineForecast = to_marine_forecast(
                beach,
                item.marine,
            )

            hourly_forecasts = build_hourly_forecasts(
                weather_forecast,
                marine_forecast,
            )

            for forecast in hourly_forecasts:
                local_timestamp = (
                    forecast.timestamp.replace(tzinfo=CANARY_TZ)
                    if forecast.timestamp.tzinfo is None
                    else forecast.timestamp.astimezone(CANARY_TZ)
                )

                if local_timestamp.date() != request.target_date:
                    continue

                if not 7 <= local_timestamp.hour <= 19:
                    continue

                key = (beach.id, local_timestamp)
                if key in seen:
                    continue

                seen.add(key)

                entries.append(
                    ScoredHour(
                        beach_id=beach.id,
                        datetime=local_timestamp,
                        score=score_forecast(forecast),
                    )
                )

        except ValueError as error:
            raise HTTPException(
                status_code=422,
                detail=f"Invalid forecast for {beach.name}: {error}",
            ) from error

    return sorted(
        entries,
        key=lambda entry: (entry.datetime, entry.beach_id),
    )
