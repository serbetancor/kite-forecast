from datetime import date, datetime
from typing import TypedDict

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from kite_forecast.config.beaches import BEACHES
from kite_forecast.services.forecast import ForecastService

app = FastAPI(title="Kite Forecast API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

forecast_service = ForecastService()


class BeachConfig(TypedDict):
    id: str
    name: str


class AppConfig(TypedDict):
    forecast_horizon_days: int
    beaches: list[BeachConfig]


@app.get("/config")
async def get_config() -> AppConfig:
    return {
        "forecast_horizon_days": 7,
        "beaches": [
            {
                "id": beach.id,
                "name": beach.name,
            }
            for beach in BEACHES
        ],
    }


@app.get("/forecast")
async def get_forecast(
    beach: str,
    date: date,
    time: str,
):
    selected_beach = next(
        (item for item in BEACHES if item.id == beach),
        None,
    )

    if selected_beach is None:
        raise HTTPException(
            status_code=404,
            detail=f"Unknown beach: {beach}",
        )

    try:
        timestamp = datetime.fromisoformat(f"{date}T{time}")
    except ValueError as error:
        raise HTTPException(
            status_code=400,
            detail="Invalid time format",
        ) from error

    return await forecast_service.get_forecast(
        selected_beach,
        timestamp,
    )


@app.get("/kite-sizing")
async def get_kite_sizing(
    beach: str,
    date: date,
    time: str,
):
    selected_beach = next(
        (item for item in BEACHES if item.id == beach),
        None,
    )

    if selected_beach is None:
        raise HTTPException(
            status_code=404,
            detail=f"Unknown beach: {beach}",
        )

    try:
        timestamp = datetime.fromisoformat(f"{date}T{time}")
    except ValueError as error:
        raise HTTPException(
            status_code=400,
            detail="Invalid time format",
        ) from error

    try:
        return await forecast_service.get_kite_sizing(
            selected_beach,
            timestamp,
        )
    except ValueError as error:
        raise HTTPException(
            status_code=404,
            detail=str(error),
        ) from error
