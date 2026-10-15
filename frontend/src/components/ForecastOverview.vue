<script setup lang="ts">
import { computed } from "vue"

import CurrentIcon from "../assets/icons/CurrentIcon.vue"
import TemperatureIcon from "../assets/icons/TemperatureIcon.vue"
import TideIcon from "../assets/icons/TideIcon.vue"
import WavesIcon from "../assets/icons/WavesIcon.vue"
import WindIcon from "../assets/icons/WindIcon.vue"
import Skeleton from "../components/Skeleton.vue"
import WeatherMetricCard from "../components/WeatherMetricCard.vue"
import type { ObjectiveReport } from "../models/forecast"
import { formatTideTrend } from "../utils/formatters"
import {
  formatDirection,
  formatTime,
  formatTimestamp,
} from "../utils/formatters"

const props = defineProps<{
  forecast: ObjectiveReport
  selectedDate: string
  selectedTime: string
  loading: boolean
}>()

const metricCards = computed(() => [
  {
    title: "Viento",
    icon: WindIcon,
    iconBackground: "bg-white/50",
    value: props.forecast.wind.speed_kn,
    unit: "kn",
    detail: `Rachas: ${props.forecast.wind.gusts_kn} kn`,
    direction: formatDirection(
      props.forecast.wind.direction_deg,
      props.forecast.wind.direction_cardinal,
    ),
    score: props.forecast.score.wind.total,
  },
  {
    title: "Oleaje",
    icon: WavesIcon,
    iconBackground: "bg-white/50",
    value: props.forecast.waves.height_m,
    unit: "m",
    detail: `Periodo: ${props.forecast.waves.period_s} s`,
    direction: formatDirection(
      props.forecast.waves.direction_deg,
      props.forecast.waves.direction_cardinal,
    ),
    score: props.forecast.score.waves.total,
  },
  {
    title: "Mar de fondo",
    icon: WavesIcon,
    iconBackground: "bg-white/50",
    value: props.forecast.swell.height_m,
    unit: "m",
    detail: `Periodo: ${props.forecast.swell.period_s} s`,
    direction: formatDirection(
      props.forecast.swell.direction_deg,
      props.forecast.swell.direction_cardinal,
    ),
    score: props.forecast.score.swell.total,
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
    title: "Corriente",
    icon: CurrentIcon,
    iconBackground: "bg-sky-50",
    value: props.forecast.sea.current_velocity_kmh,
    unit: "km/h",
    direction: formatDirection(
      props.forecast.sea.current_direction_deg,
      props.forecast.sea.current_direction_cardinal,
    ),
  },
  {
    title: "Marea",
    icon: TideIcon,
    iconBackground: "bg-sky-50",
    text: formatTideTrend(props.forecast.tide.trend),
    detail: [
      `Nivel del mar: ${props.forecast.sea.level_m} m`,
      `Próxima pleamar: ${formatTime(props.forecast.tide.next_high_tide.timestamp)}`,
      `Próxima bajamar: ${formatTime(props.forecast.tide.next_low_tide.timestamp)}`,
    ].join("\n"),
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
                class="text-5xl font-bold tracking-tight text-(--previ-blue) tabular-nums"
              >
                {{ Math.round(forecast.score.total) }}
              </span>

              <span class="text-md text-(--previ-muted)">/ 100</span>
            </div>
          </div>
        </div>
      </div>
    </div>

    <div
      class="grid grid-cols-2 gap-3 sm:gap-4 xl:grid-cols-3"
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
          :text="metric.text"
          :unit="metric.unit"
          :detail="metric.detail"
          :direction="metric.direction"
          :score="metric.score"
        />
      </template>
    </div>
  </section>
</template>
