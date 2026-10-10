<script setup lang="ts">
import { computed, nextTick, onMounted, ref, watch } from "vue"

import type { KiteSizingCell, KiteSizingMatrix } from "../models/forecast"

const props = defineProps<{
  matrix: KiteSizingMatrix
}>()

const weightSelector = ref<HTMLElement | null>(null)

function getCentralWeight(): number {
  const weights = props.matrix.weights_kg
  return weights[Math.floor(weights.length / 2)] ?? 0
}

const selectedWeight = ref(getCentralWeight())

async function centerSelectedWeight(): Promise<void> {
  await nextTick()

  const container = weightSelector.value
  const selectedButton = container?.querySelector<HTMLButtonElement>(
    '[aria-pressed="true"]',
  )

  if (!container || !selectedButton) return

  const buttonCenter =
    selectedButton.offsetLeft + selectedButton.offsetWidth / 2

  container.scrollTo({
    left: buttonCenter - container.clientWidth / 2,
    behavior: "auto",
  })
}

const availableSizes = computed(() =>
  [...props.matrix.kite_sizes_m2]
    .filter((size) =>
      props.matrix.cells.some(
        (cell) =>
          cell.weight_kg === selectedWeight.value &&
          cell.kite_size_m2 === size &&
          cell.score > 0,
      ),
    )
    .sort((a, b) => a - b),
)

const rankedCells = computed(() =>
  availableSizes.value
    .map((size) =>
      props.matrix.cells.find(
        (cell) =>
          cell.weight_kg === selectedWeight.value && cell.kite_size_m2 === size,
      ),
    )
    .filter((cell): cell is KiteSizingCell => cell !== undefined)
    .sort((a, b) => b.score - a.score),
)

onMounted(centerSelectedWeight)

watch(selectedWeight, centerSelectedWeight)

watch(
  () => props.matrix.weights_kg,
  (weights) => {
    if (!weights.includes(selectedWeight.value)) {
      selectedWeight.value = getCentralWeight()
    }

    void centerSelectedWeight()
  },
)
</script>

<template>
  <section class="mt-6 max-w-full min-w-0">
    <div class="mb-5">
      <p class="text-sm text-(--previ-muted)">
        Selecciona tu peso para comparar las tallas de cometa.
      </p>
    </div>

    <fieldset class="mb-6 min-w-0">
      <legend class="mb-2 text-sm font-semibold text-(--previ-navy)">
        Tu peso
      </legend>

      <div
        ref="weightSelector"
        class="w-full max-w-full min-w-0 snap-x snap-mandatory overflow-x-auto overscroll-x-contain"
      >
        <div class="flex w-max gap-2 px-1 py-2">
          <button
            v-for="weight in matrix.weights_kg"
            :key="weight"
            type="button"
            :aria-pressed="selectedWeight === weight"
            class="min-w-16 shrink-0 snap-center rounded-xl border px-4 py-3 text-sm font-semibold transition"
            :class="
              selectedWeight === weight
                ? 'border-(--previ-blue) bg-sky-50 text-(--previ-blue)'
                : 'border-(--previ-border) bg-white text-(--previ-text) hover:border-(--previ-blue)'
            "
            @click="selectedWeight = weight"
          >
            {{ weight }} kg
          </button>
        </div>
      </div>
    </fieldset>

    <div v-if="rankedCells.length" class="space-y-3">
      <article
        v-for="(cell, index) in rankedCells"
        :key="`${cell.weight_kg}-${cell.kite_size_m2}`"
        class="rounded-2xl border border-(--previ-border) bg-white p-4 shadow-sm"
      >
        <div class="flex items-center gap-3">
          <div
            class="flex size-14 shrink-0 items-center justify-center rounded-xl bg-sky-50 text-sm font-bold text-sky-800"
          >
            {{ cell.kite_size_m2 }} m²
          </div>

          <div class="min-w-0 flex-1">
            <div class="mb-2 flex items-center justify-between gap-2">
              <span class="text-sm font-semibold text-(--previ-navy)">
                {{ index === 0 ? "Mayor puntuación" : "Adecuación" }}
              </span>

              <span class="text-lg font-bold text-(--previ-navy)">
                {{ cell.score.toFixed(1) }}
                <span class="text-xs font-normal text-(--previ-muted)">
                  / 100
                </span>
              </span>
            </div>

            <div
              class="h-2 overflow-hidden rounded-full bg-slate-100"
              role="progressbar"
              :aria-valuenow="cell.score"
              aria-valuemin="0"
              aria-valuemax="100"
              :aria-label="`Puntuación para cometa de ${cell.kite_size_m2} metros cuadrados`"
            >
              <div
                class="h-full rounded-full bg-sky-500"
                :style="{
                  width: `${Math.min(100, Math.max(0, cell.score))}%`,
                }"
              ></div>
            </div>
          </div>
        </div>
      </article>
    </div>

    <p
      v-else
      class="rounded-xl border border-(--previ-border) p-5 text-sm text-(--previ-muted)"
    >
      No hay tallas con puntuación superior a cero para este peso.
    </p>

    <p class="mt-4 text-xs leading-5 text-(--previ-muted)">
      Las puntuaciones son orientativas y no sustituyen la evaluación de las
      condiciones del mar y del viento ni las recomendaciones de seguridad.
    </p>
  </section>
</template>
