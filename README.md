# Kite Forecast

Personal project to explore weather and marine forecast data for kitesurfing spots in Gran Canaria.

The project retrieves objective forecast conditions for a specific beach and date/time, normalizes data from external providers, and exposes it through a backend that can be consumed by a web frontend.

The long-term goal is to build a simple interface where a user can select a beach and a specific date and time and get a clear report of the expected conditions.

## Project structure

```text
kite-forecast/
├── backend/
│   ├── src/
│   │   └── kite_forecast/
│   ├── tests/
│   ├── pyproject.toml
│   └── README.md
│
├── frontend/
│   ├── src/
│   ├── public/
│   ├── package.json
│   └── ...
│
├── .gitignore
├── .vscode/
└── README.md
```

## Backend

The backend is written in Python and is responsible for retrieving, normalizing and combining weather and marine forecast data.

The current architecture is:

```text
External APIs
     ↓
Providers
     ↓
Normalized domain models
     ↓
HourlyForecast
     ↓
ForecastService
     ↓
ObjectiveReport
```

The forecast API works with a **single beach and a specific date/time**, rather than retrieving a complete forecast range.

### Main components

- **Models** — Domain models for beaches, locations, weather, marine conditions and forecasts.
- **Providers** — Integrations with external forecast providers.
- **ForecastService** — Coordinates the different providers and builds the final forecast.
- **ObjectiveReport** — Output model containing the objective conditions shown to the user.
- **Utils** — Shared utilities such as wind and wave direction conversion.

The current objective report contains:

- Wind speed
- Wind direction
- Wind gusts
- Temperature
- Wave height
- Wave direction
- Wave period
- Sea level
- Ocean current velocity
- Ocean current direction

Scoring and recommendations are intentionally not part of the current report.

### Technologies

- Python 3.13
- Pydantic
- httpx
- pytest
- Pyright
- uv

### Backend commands

Run these commands from the `backend/` directory.

Install/synchronize dependencies:

```bash
uv sync
```

Run tests:

```bash
uv run pytest
```

Run type checking:

```bash
uv run pyright
```

Inspect a forecast manually:

```bash
uv run python -m kite_forecast.inspect_forecast
```

## Frontend

The frontend is a Vue 3 application written in TypeScript and built with Vite.

It is currently being developed as the web interface for the objective forecast reports.

### Technologies

- Vue 3
- TypeScript
- Vite
- Tailwind CSS
- Prettier
- prettier-plugin-tailwindcss

### Frontend commands

Run these commands from the `frontend/` directory.

Install dependencies:

```bash
npm install
```

Start the development server:

```bash
npm run dev
```

Format the frontend:

```bash
npm run format
```

Check formatting without modifying files:

```bash
npm run format:check
```

Build the frontend:

```bash
npm run build
```

## Beaches

The project currently supports seven kitesurfing spots in Gran Canaria:

1. Salinas
2. Vargas
3. Bocabarranco
4. Las Burras
5. Castillo del Romeral
6. El Burrero
7. Punta de Maspalomas

## Current status

The backend is already capable of retrieving and combining weather and marine data for a specific beach and date/time and returning an objective report.

The next stage is to connect the frontend to the backend and build the user interface for selecting:

- Beach
- Date
- Time

and displaying the resulting objective forecast report.

Scoring, recommendations and other interpretation of the conditions will be added later.
