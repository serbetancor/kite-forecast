<script setup lang="ts">
import { computed } from "vue"

import { useScoreRanking } from "../composables/useScoreRanking"
import type { BeachOption } from "../models/config"
import type { ScoredHour } from "../models/forecast"
import DateSelector from "./DateSelector.vue"

const props = defineProps<{
  beaches: BeachOption[]
  forecastHorizonDays: number
}>()

const { selectedDate, entries, loading, error, hasScores } = useScoreRanking()

const timeFormatter = new Intl.DateTimeFormat("es-ES", {
  hour: "2-digit",
  minute: "2-digit",
  timeZone: "Atlantic/Canary",
})

interface BeachRankingEntry {
  beachId: string
  beachName: string
  bestHour: ScoredHour
}

const ranking = computed<BeachRankingEntry[]>(() => {
  const bestByBeach = new Map<string, ScoredHour>()

  for (const entry of entries.value) {
    const currentBest = bestByBeach.get(entry.beach_id)

    if (!currentBest || entry.score.total > currentBest.score.total) {
      bestByBeach.set(entry.beach_id, entry)
    }
  }

  return props.beaches
    .flatMap((beach) => {
      const bestHour = bestByBeach.get(beach.id)

      if (!bestHour) {
        return []
      }

      return [
        {
          beachId: beach.id,
          beachName: beach.name,
          bestHour,
        },
      ]
    })
    .sort((a, b) => b.bestHour.score.total - a.bestHour.score.total)
})

function formatTime(timestamp: string): string {
  return timeFormatter.format(new Date(timestamp))
}

function formatScore(score: number): string {
  return Math.round(score).toString()
}
</script>

<template>
  <section
    id="beach-ranking"
    class="mt-10 rounded-3xl border border-(--previ-border) bg-white p-5 shadow-sm sm:p-8"
    aria-labelledby="beach-ranking-title"
  >
    <div
      class="flex flex-col gap-4 sm:flex-row sm:items-end sm:justify-between"
    >
      <div>
        <p
          class="text-xs font-semibold tracking-[0.2em] text-(--previ-blue) uppercase"
        >
          Encuentra tu próxima sesión
        </p>

        <h2
          id="beach-ranking-title"
          class="mt-2 text-2xl font-bold tracking-tight text-(--previ-navy) sm:text-3xl"
        >
          Mejores playas
        </h2>

        <p class="mt-2 text-sm leading-6 text-(--previ-muted)">
          Las mejores condiciones previstas para cada playa y su hora más
          favorable.
        </p>
      </div>

      <DateSelector
        :model-value="selectedDate"
        :days="forecastHorizonDays"
        @update:model-value="selectedDate = $event"
      />
    </div>

    <div
      v-if="loading"
      class="py-12 text-center text-sm text-(--previ-muted)"
      role="status"
    >
      Cargando puntuaciones...
    </div>

    <div
      v-else-if="error"
      class="mt-6 rounded-xl border border-red-200 bg-red-50 p-4 text-sm text-red-800"
      role="alert"
    >
      {{ error }}
    </div>

    <div
      v-else-if="!hasScores || ranking.length === 0"
      class="mt-6 rounded-xl bg-slate-50 p-6 text-center text-sm leading-6 text-(--previ-muted)"
    >
      No hay puntuaciones disponibles para esta fecha.
    </div>

    <ol v-else class="mt-6 space-y-3">
      <li
        v-for="(item, index) in ranking"
        :key="item.beachId"
        class="flex flex-col gap-4 rounded-2xl border border-(--previ-border) p-4 sm:flex-row sm:items-center sm:justify-between"
      >
        <div class="flex min-w-0 items-center gap-4">
          <span
            class="flex size-10 shrink-0 items-center justify-center rounded-xl bg-slate-100 text-sm font-bold text-(--previ-navy)"
            :aria-label="`Posición ${index + 1}`"
          >
            {{ index + 1 }}
          </span>

          <div class="min-w-0">
            <h3 class="font-semibold text-(--previ-navy)">
              {{ item.beachName }}
            </h3>

            <p class="mt-1 text-sm text-(--previ-muted)">
              Mejor hora: {{ formatTime(item.bestHour.datetime) }}
            </p>

            <p class="mt-1 text-xs text-(--previ-muted)">
              Viento {{ formatScore(item.bestHour.score.wind.total) }}/100
              <span class="px-1">·</span>
              Olas {{ formatScore(item.bestHour.score.waves.total) }}/100
            </p>
          </div>
        </div>

        <div class="mx-auto flex items-baseline gap-1 sm:mr-0 sm:justify-end">
          <span class="text-3xl font-bold text-(--previ-blue) tabular-nums">
            {{ formatScore(item.bestHour.score.total) }}
          </span>
          <span class="text-sm text-(--previ-muted)">/100</span>
        </div>
      </li>
    </ol>

    <p class="mt-5 text-xs leading-5 text-(--previ-muted)">
      Ranking orientativo basado en la puntuación de las condiciones
      meteorológicas y marinas. La mejor puntuación no garantiza que las
      condiciones sean seguras para navegar.
    </p>
  </section>
</template>
