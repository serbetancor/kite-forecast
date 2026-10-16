<script setup lang="ts">
import { onMounted, ref } from "vue"

import BeachRanking from "../components/BeachRanking.vue"
import type { BeachOption } from "../models/config"
import type { WeeklyBeachForecast } from "../models/response"
import { getAppConfig } from "../services/forecastService"
import { loadWeeklyForecasts } from "../services/scoresService"

const beaches = ref<BeachOption[]>([])
const weeklyForecasts = ref<WeeklyBeachForecast[]>([])
const forecastHorizonDays = ref(7)
const loading = ref(true)
const error = ref("")

onMounted(async () => {
  try {
    const config = await getAppConfig()

    if (config.beaches.length === 0) {
      throw new Error("No hay playas disponibles.")
    }

    beaches.value = config.beaches
    forecastHorizonDays.value = config.forecast_horizon_days
    weeklyForecasts.value = await loadWeeklyForecasts(config.beaches)
  } catch (err) {
    error.value =
      err instanceof Error
        ? err.message
        : "No se han podido cargar las previsiones."
  } finally {
    loading.value = false
  }
})
</script>

<template>
  <section class="space-y-6">
    <header class="space-y-2">
      <p
        class="text-sm font-semibold tracking-wide text-(--previ-blue) uppercase"
      >
        Kite Forecast
      </p>

      <h1
        class="text-3xl font-bold tracking-tight text-(--previ-navy) sm:text-4xl"
      >
        Ranking de playas
      </h1>

      <p class="max-w-2xl text-sm leading-6 text-(--previ-text)">
        Descubre qué playas de Gran Canaria ofrecen las mejores condiciones para
        practicar kitesurf y a qué hora conviene navegar.
      </p>
    </header>

    <div
      v-if="loading"
      class="rounded-xl border border-(--previ-border) bg-white p-6 text-sm"
      role="status"
    >
      Cargando previsiones meteorológicas y marinas...
    </div>

    <div
      v-else-if="error"
      class="rounded-xl border border-red-200 bg-red-50 p-4 text-sm text-red-700"
      role="alert"
    >
      {{ error }}
    </div>

    <BeachRanking
      v-else
      :beaches="beaches"
      :forecast-horizon-days="forecastHorizonDays"
      :weekly-forecasts="weeklyForecasts"
    />
  </section>
</template>
