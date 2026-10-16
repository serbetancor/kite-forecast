import { computed, ref, watch } from "vue"

import type { ScoredHour } from "../models/forecast"
import type { WeeklyBeachForecast } from "../models/response"
import { getScores } from "../services/forecastService"

function formatDate(date: Date): string {
  const year = date.getFullYear()
  const month = String(date.getMonth() + 1).padStart(2, "0")
  const day = String(date.getDate()).padStart(2, "0")

  return `${year}-${month}-${day}`
}

export function useScoreRanking(weeklyForecasts: WeeklyBeachForecast[]) {
  const selectedDate = ref(formatDate(new Date()))
  const entries = ref<ScoredHour[]>([])
  const loading = ref(false)
  const error = ref("")

  let requestId = 0

  async function loadScores() {
    const currentRequestId = ++requestId

    loading.value = true
    error.value = ""

    try {
      const scores = await getScores(selectedDate.value, weeklyForecasts)
      if (currentRequestId === requestId) {
        entries.value = scores
      }
    } catch (err) {
      if (currentRequestId === requestId) {
        error.value =
          err instanceof Error
            ? err.message
            : "Ha ocurrido un error al cargar las puntuaciones."

        entries.value = []
      }
    } finally {
      if (currentRequestId === requestId) {
        loading.value = false
      }
    }
  }

  watch(
    selectedDate,
    () => {
      void loadScores()
    },
    { immediate: true },
  )

  const hasScores = computed(() => entries.value.length > 0)

  return {
    selectedDate,
    entries,
    loading,
    error,
    hasScores,
  }
}
