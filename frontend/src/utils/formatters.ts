import type { TideTrend } from "../models/forecast"

export function formatDate(date: Date): string {
  const year = date.getFullYear()
  const month = String(date.getMonth() + 1).padStart(2, "0")
  const day = String(date.getDate()).padStart(2, "0")

  return `${year}-${month}-${day}`
}

export function formatTimestamp(timestamp: string): string {
  return new Intl.DateTimeFormat("es-ES", {
    dateStyle: "medium",
    timeStyle: "short",
  }).format(new Date(timestamp))
}

export function formatTime(timestamp: string): string {
  return new Intl.DateTimeFormat("es-ES", {
    hour: "2-digit",
    minute: "2-digit",
    hour12: false,
  }).format(new Date(timestamp))
}

export function formatDirection(degrees: number, cardinal: string): string {
  return `${cardinal} · ${Math.round(degrees)}°`
}

export function formatTideTrend(trend: TideTrend): string {
  const labels: Record<TideTrend, string> = {
    rising: "Marea subiendo",
    falling: "Marea bajando",
    stable: "Marea estable",
    high_tide: "Pleamar",
    low_tide: "Bajamar",
  }

  return labels[trend]
}
