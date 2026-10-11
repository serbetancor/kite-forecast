<script setup lang="ts">
import { computed } from "vue"

import CurrentIcon from "../assets/icons/CurrentIcon.vue"
import TemperatureIcon from "../assets/icons/TemperatureIcon.vue"
import WavesIcon from "../assets/icons/WavesIcon.vue"
import WindIcon from "../assets/icons/WindIcon.vue"
import Skeleton from "../components/Skeleton.vue"
import type { ObjectiveReport } from "../models/forecast"
import { formatDirection, formatTimestamp } from "../utils/formatters"
import WeatherMetricCard from "./WeatherMetricCard.vue"

const props = defineProps<{
  forecast: ObjectiveReport
  selectedDate: string
  selectedTime: string
  loading: boolean
}>()

const isGoodConditions = computed(
  () => Math.round(props.forecast.score.total) < 70,
)
const metricCards = computed(() => [
  {
    title: "Viento",
    icon: WindIcon,
    iconBackground: "bg-sky-50",
    value: props.forecast.wind.speed_kmh,
    unit: "kmh",
    detail: `Rachas: ${props.forecast.wind.gusts_kmh} kmh`,
    direction: formatDirection(
      props.forecast.wind.direction_deg,
      props.forecast.wind.direction_cardinal,
    ),
  },
  {
    title: "Temperatura",
    icon: TemperatureIcon,
    iconBackground: "bg-amber-50",
    value: props.forecast.weather.temperature_c,
    unit: "°C",
    detail: "Temperatura del aire",
  },
  {
    title: "Oleaje",
    icon: WavesIcon,
    iconBackground: "bg-sky-50",
    value: props.forecast.waves.height_m,
    unit: "m",
    detail: `Periodo: ${props.forecast.waves.period_s} s`,
    direction: formatDirection(
      props.forecast.waves.direction_deg,
      props.forecast.waves.direction_cardinal,
    ),
  },
  {
    title: "Corriente",
    icon: CurrentIcon,
    iconBackground: "bg-sky-50",
    value: props.forecast.sea.current_velocity_kmh,
    unit: "km/h",
    detail: `Nivel del mar: ${props.forecast.sea.level_m} m`,
    direction: formatDirection(
      props.forecast.sea.current_direction_deg,
      props.forecast.sea.current_direction_cardinal,
    ),
  },
])
</script>

<template>
  <section class="mt-12">
    <div class="mb-6 flex items-end justify-between gap-2">
      <div class="flex w-full flex-col">
        <p
          class="text-xs font-semibold tracking-[0.2em] text-(--previ-blue) uppercase"
        >
          Tu previsión
        </p>

        <Skeleton v-if="loading" class="mt-2 h-15 w-full rounded-lg" />
        <div v-else class="flex w-full items-center justify-between">
          <div class="flex flex-col">
            <h2
              class="mt-2 text-3xl font-bold tracking-tight text-(--previ-navy)"
            >
              {{ forecast.beach.name }}
            </h2>
            <p v-if="forecast.timestamp" class="text-xs text-(--previ-muted)">
              Actualizado: {{ formatTimestamp(forecast.timestamp) }}
            </p>
          </div>
          <div class="mt-auto ml-auto flex shrink-0 flex-col items-end gap-1">
            <div class="flex items-baseline gap-1">
              <span
                class="text-5xl font-bold tracking-tight tabular-nums"
                :class="isGoodConditions ? 'text-red-500' : 'text-green-600'"
              >
                {{ Math.round(forecast.score.total) }}
              </span>

              <span class="text-md text-(--previ-muted)">/ 100</span>
            </div>

            <span
              class="text-xs font-medium"
              :class="isGoodConditions ? 'text-red-500' : 'text-green-600'"
            >
              {{
                isGoodConditions
                  ? "Condiciones limitadas"
                  : "Buenas condiciones"
              }}
            </span>
          </div>
        </div>
      </div>
    </div>

    <div
      class="grid grid-cols-2 gap-3 sm:gap-4 xl:grid-cols-4"
      :aria-busy="loading"
    >
      <template v-if="loading">
        <div
          v-for="metric in metricCards"
          :key="metric.title"
          class="min-h-44 rounded-2xl border border-(--previ-border) bg-white p-5 shadow-sm"
          role="status"
          :aria-label="`Cargando ${metric.title.toLowerCase()}`"
        >
          <div class="mb-6 flex items-center gap-3">
            <Skeleton class="size-10 rounded-xl" />
            <Skeleton class="h-4 w-28 rounded-full" />
          </div>

          <Skeleton class="h-9 w-2/3 rounded-lg" />

          <div class="mt-3 mb-5">
            <Skeleton class="h-3 w-1/3 rounded-full" />
          </div>

          <Skeleton class="h-3 w-5/6 rounded-full" />
        </div>
      </template>

      <template v-else>
        <WeatherMetricCard
          v-for="metric in metricCards"
          :key="metric.title"
          :title="metric.title"
          :icon="metric.icon"
          :icon-background="metric.iconBackground"
          :value="metric.value"
          :unit="metric.unit"
          :detail="metric.detail"
          :direction="metric.direction"
        />
      </template>
    </div>
  </section>
</template>
