import type { AppConfig } from "../models/config"
import type { KiteSizingMatrix, ObjectiveReport } from "../models/forecast"

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL
interface ForecastQuery {
  beach: string
  date: string
  time: string
}

interface ForecastData {
  forecast: ObjectiveReport
  kiteSizing: KiteSizingMatrix
}

async function fetchJson<T>(url: string, errorMessage: string): Promise<T> {
  const response = await fetch(url)

  if (!response.ok) {
    throw new Error(errorMessage)
  }

  return (await response.json()) as T
}

export function getAppConfig(): Promise<AppConfig> {
  return fetchJson<AppConfig>(
    `${API_BASE_URL}/config`,
    "No se ha podido cargar la configuración.",
  )
}

export async function getForecastData(
  query: ForecastQuery,
): Promise<ForecastData> {
  const params = new URLSearchParams({
    beach: query.beach,
    date: query.date,
    time: query.time,
  })
  const queryString = params.toString()

  const [forecast, kiteSizing] = await Promise.all([
    fetchJson<ObjectiveReport>(
      `${API_BASE_URL}/forecast?${queryString}`,
      "No se ha podido obtener la previsión. Inténtalo de nuevo.",
    ),
    fetchJson<KiteSizingMatrix>(
      `${API_BASE_URL}/kite-sizing?${queryString}`,
      "No se ha podido obtener la previsión. Inténtalo de nuevo.",
    ),
  ])

  return { forecast, kiteSizing }
}
