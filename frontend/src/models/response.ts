import type { KiteSizingMatrix, ObjectiveReport } from "../models/forecast"

export interface ForecastQuery {
  beach: string
  date: string
  time: string
}

export interface ForecastData {
  forecast: ObjectiveReport
  kiteSizing: KiteSizingMatrix
}

export interface OpenMeteoResponse {
  latitude: number
  longitude: number
  timezone: string
  hourly: Record<string, unknown[]>
}

export interface BeachForecastPayload {
  beach_id: string
  weather: OpenMeteoResponse
  marine: OpenMeteoResponse
}

export interface WeeklyBeachForecast {
  beach_id: string
  weather: OpenMeteoResponse
  marine: OpenMeteoResponse
}
