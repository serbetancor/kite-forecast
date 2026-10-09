<script setup lang="ts">
import { computed, ref } from "vue"

import type { KiteSizingCell, KiteSizingMatrix } from "../models/forecast"

const props = defineProps<{
  matrix: KiteSizingMatrix
}>()

const selectedCell = ref<KiteSizingCell | null>(null)

const cellsByCombination = computed(() => {
  const cells = new Map<string, KiteSizingCell>()

  for (const cell of props.matrix.cells) {
    cells.set(`${cell.weight_kg}-${cell.kite_size_m2}`, cell)
  }

  return cells
})

function getCell(weight: number, size: number): KiteSizingCell | undefined {
  return cellsByCombination.value.get(`${weight}-${size}`)
}

function getCellColor(score: number): string {
  if (score < 20) return "#1e293b"
  if (score < 40) return "#164e63"
  if (score < 60) return "#0369a1"
  if (score < 80) return "#0ea5e9"
  return "#7dd3fc"
}

function selectCell(cell: KiteSizingCell | undefined) {
  if (cell) {
    selectedCell.value = cell
  }
}
</script>

<template>
  <section class="mt-6 rounded-2xl bg-slate-900 p-6">
    <div
      class="flex flex-col gap-2 sm:flex-row sm:items-start sm:justify-between"
    >
      <div>
        <h2 class="text-xl font-bold text-white">Recomendación de talla</h2>
        <p class="mt-1 text-sm text-slate-400">
          Selecciona tu peso y consulta la puntuación para cada talla.
        </p>
      </div>

      <div class="text-sm text-slate-400">
        Viento: {{ matrix.wind_speed_knots }} kn
        <span class="mx-1">·</span>
        Rachas: {{ matrix.wind_gusts_knots }} kn
      </div>
    </div>

    <div class="mt-6 overflow-x-auto pb-3">
      <div class="min-w-212.5">
        <div class="mb-2 pl-16 text-center text-sm text-slate-400">
          Peso del rider (kg)
        </div>

        <div
          class="grid gap-1"
          :style="{
            gridTemplateColumns: `60px repeat(${matrix.weights_kg.length}, minmax(0, 1fr))`,
          }"
        >
          <div></div>

          <div
            v-for="weight in matrix.weights_kg"
            :key="weight"
            class="pb-2 text-center text-xs text-slate-400"
          >
            {{ weight }}
          </div>

          <template
            v-for="size in [...matrix.kite_sizes_m2].reverse()"
            :key="size"
          >
            <div
              class="flex items-center justify-end pr-3 text-sm text-slate-300"
            >
              {{ size }} m²
            </div>

            <button
              v-for="weight in matrix.weights_kg"
              :key="`${weight}-${size}`"
              type="button"
              class="aspect-square min-w-0 rounded-sm border transition hover:z-10 hover:scale-110 hover:border-white focus:ring-2 focus:ring-white focus:outline-none"
              :style="{
                backgroundColor: getCell(weight, size)
                  ? getCellColor(getCell(weight, size)!.score)
                  : '#0f172a',
                borderColor:
                  selectedCell?.weight_kg === weight &&
                  selectedCell?.kite_size_m2 === size
                    ? '#ffffff'
                    : 'transparent',
              }"
              :title="`${weight} kg · ${size} m² · ${getCell(weight, size)?.score.toFixed(1) ?? 'Sin datos'}`"
              :aria-label="`${weight} kg, cometa de ${size} m², puntuación ${getCell(weight, size)?.score.toFixed(1) ?? 'sin datos'}`"
              @click="selectCell(getCell(weight, size))"
            ></button>
          </template>
        </div>
      </div>
    </div>

    <div
      class="mt-2 flex flex-wrap items-center justify-between gap-4 text-xs text-slate-400"
    >
      <span>Puntuación de adecuación</span>

      <div class="flex items-center gap-2">
        <span>0</span>

        <div class="flex gap-1">
          <div
            v-for="score in [0, 20, 40, 60, 80, 100]"
            :key="score"
            class="h-3 w-7 rounded-sm"
            :style="{ backgroundColor: getCellColor(score) }"
          ></div>
        </div>

        <span>100</span>
      </div>
    </div>

    <div
      v-if="selectedCell"
      class="mt-6 rounded-xl border border-sky-500/30 bg-slate-800 p-4"
    >
      <p class="text-sm text-slate-400">Combinación seleccionada</p>

      <div
        class="mt-2 flex flex-wrap items-baseline gap-x-6 gap-y-2 text-white"
      >
        <p class="text-lg font-semibold">
          {{ selectedCell.weight_kg }} kg
          <span class="text-slate-400">·</span>
          {{ selectedCell.kite_size_m2 }} m²
        </p>

        <p class="text-2xl font-bold text-sky-300">
          {{ selectedCell.score.toFixed(1) }}
          <span class="text-sm font-normal text-slate-400">/ 100</span>
        </p>
      </div>
    </div>

    <p v-else class="mt-4 text-sm text-slate-400">
      Selecciona una celda para consultar su puntuación exacta.
    </p>
  </section>
</template>
