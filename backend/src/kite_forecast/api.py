from datetime import date, datetime

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
