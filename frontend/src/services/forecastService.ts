import type { AppConfig, BeachOption } from "../models/config"
import type {
  KiteSizingMatrix,
  ObjectiveReport,
  ScoredHour,
} from "../models/forecast"
import type {
  ForecastData,
  ForecastQuery,
  OpenMeteoResponse,
  WeeklyBeachForecast,
} from "../models/response"

export const API_BASE_URL = import.meta.env.VITE_API_BASE_URL
export const WEATHER_API_URL = "https://api.open-meteo.com/v1/forecast"
export const MARINE_API_URL = "https://marine-api.open-meteo.com/v1/marine"

async function fetchJson<T>(
  url: string,
  errorMessage: string,
  init?: RequestInit,
): Promise<T> {
  const response = await fetch(url, init)

  if (!response.ok) {
    throw new Error(`${errorMessage} (HTTP ${response.status})`)
  }

  return (await response.json()) as T
}

export async function fetchOpenMeteo<T>(
  baseUrl: string,
  beach: BeachOption,
  end_date: string,
  start_date?: string,
): Promise<T> {
  const params = new URLSearchParams({
    latitude: String(beach.latitude),
    longitude: String(beach.longitude),
    start_date: start_date ?? end_date,
    end_date: end_date,
    timezone: "Atlantic/Canary",
  })

  if (baseUrl === WEATHER_API_URL) {
    params.set(
      "hourly",
      "wind_speed_10m,wind_direction_10m,wind_gusts_10m,temperature_2m",
    )
    params.set("wind_speed_unit", "kn")
  } else {
    params.set(
      "hourly",
      [
        "wave_height",
        "wave_direction",
        "wave_period",
        "swell_wave_height",
        "swell_wave_direction",
        "swell_wave_period",
        "sea_level_height_msl",
        "ocean_current_velocity",
        "ocean_current_direction",
      ].join(","),
    )
  }

  return fetchJson<T>(
    `${baseUrl}?${params.toString()}`,
    "No se han podido descargar los datos de Open-Meteo.",
  )
}

async function postJson<T>(
  path: string,
  body: unknown,
  errorMessage: string,
): Promise<T> {
  return fetchJson<T>(`${API_BASE_URL}${path}`, errorMessage, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(body),
  })
}

let configPromise: Promise<AppConfig> | null = null

export function getAppConfig(): Promise<AppConfig> {
  if (!configPromise) {
    configPromise = fetch(`${API_BASE_URL}/config`)
      .then(async (response) => {
        if (!response.ok) {
          throw new Error("Failed to load app config")
        }

        return response.json() as Promise<AppConfig>
      })
      .catch((error) => {
        // Permitir reintentar si falla la primera petición
        configPromise = null
        throw error
      })
  }

  return configPromise
}

function getBeach(config: AppConfig, beachId: string): BeachOption {
  const beach = config.beaches.find((item) => item.id === beachId)

  if (!beach) {
    throw new Error(`No se ha encontrado la playa ${beachId}.`)
  }

  return beach
}

export async function getForecastData(
  query: ForecastQuery,
): Promise<ForecastData> {
  const config = await getAppConfig()
  const beach = getBeach(config, query.beach)

  const [weather, marine] = await Promise.all([
    fetchOpenMeteo<OpenMeteoResponse>(WEATHER_API_URL, beach, query.date),
    fetchOpenMeteo<OpenMeteoResponse>(MARINE_API_URL, beach, query.date),
  ])

  const payload = {
    beach: query.beach,
    target_date: query.date,
    time: query.time,
    weather,
  }

  const [forecast, kiteSizing] = await Promise.all([
    postJson<ObjectiveReport>(
      "/forecast",
      { ...payload, marine },
      "No se ha podido calcular el informe de la playa.",
    ),
    postJson<KiteSizingMatrix>(
      "/kite-sizing",
      payload,
      "No se ha podido calcular la tabla de tallas.",
    ),
  ])

  return { forecast, kiteSizing }
}

export async function getScores(
  targetDate: string,
  forecasts: WeeklyBeachForecast[],
): Promise<ScoredHour[]> {
  return postJson<ScoredHour[]>(
    "/scores",
    {
      target_date: targetDate,
      forecasts,
    },
    "No se han podido calcular las puntuaciones de las playas.",
  )
}
