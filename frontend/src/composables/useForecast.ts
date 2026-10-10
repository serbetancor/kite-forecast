import { ref } from "vue"

import type { BeachOption } from "../models/config"
import type { KiteSizingMatrix, ObjectiveReport } from "../models/forecast"
import { getAppConfig, getForecastData } from "../services/forecastService"

function formatDate(date: Date): string {
  const year = date.getFullYear()
  const month = String(date.getMonth() + 1).padStart(2, "0")
  const day = String(date.getDate()).padStart(2, "0")

  return `${year}-${month}-${day}`
}

export function useForecast() {
  const beaches = ref<BeachOption[]>([])
  const forecastHorizonDays = ref(7)

  const selectedBeach = ref("")
  const selectedDate = ref(formatDate(new Date()))
  const selectedTime = ref("12:00")

  const forecast = ref<ObjectiveReport | null>(null)
  const kiteSizing = ref<KiteSizingMatrix | null>(null)

  const loading = ref(false)
  const error = ref("")

  async function searchForecast() {
    loading.value = true
    error.value = ""

    try {
      const data = await getForecastData({
        beach: selectedBeach.value,
        date: selectedDate.value,
        time: selectedTime.value,
      })

      forecast.value = data.forecast
      kiteSizing.value = data.kiteSizing
    } catch (err) {
      error.value =
        err instanceof Error
          ? err.message
          : "Ha ocurrido un error al consultar la previsión."

      forecast.value = null
      kiteSizing.value = null
    } finally {
      loading.value = false
    }
  }

  async function loadConfig() {
    try {
      const config = await getAppConfig()

      if (config.beaches.length === 0) {
        throw new Error("No hay playas disponibles.")
      }

      beaches.value = config.beaches
      forecastHorizonDays.value = config.forecast_horizon_days
      selectedBeach.value = config.beaches[0].id

      await searchForecast()
    } catch (err) {
      error.value =
        err instanceof Error
          ? err.message
          : "Ha ocurrido un error al cargar la configuración."
    }
  }

  void loadConfig()

  return {
    beaches,
    forecastHorizonDays,
    selectedBeach,
    selectedDate,
    selectedTime,
    forecast,
    kiteSizing,
    loading,
    error,
    searchForecast,
  }
}
