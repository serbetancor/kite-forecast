<script setup lang="ts">
import { ref } from "vue"

import ForecastFilters from "../components/ForecastFilters.vue"
import ForecastOverview from "../components/ForecastOverview.vue"
import KiteSizingSection from "../components/KiteSizingSection.vue"
import { useForecast } from "../composables/useForecast"

const {
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
} = useForecast()

const filtersExpanded = ref(true)

function handleSearch() {
  filtersExpanded.value = false
  searchForecast()
}
</script>

<template>
  <!-- Presentación -->
  <section
    class="relative overflow-hidden rounded-3xl bg-(--previ-navy) px-6 py-10 text-white sm:px-10 sm:py-14"
  >
    <div
      class="pointer-events-none absolute -top-20 -right-12 size-64 rounded-full border border-white/10"
    ></div>
    <div
      class="pointer-events-none absolute -top-10 -right-2 size-44 rounded-full border border-white/10"
    ></div>

    <div class="relative max-w-2xl">
      <p
        class="mb-4 text-xs font-semibold tracking-[0.24em] text-(--previ-gold) uppercase"
      >
        Tu próxima sesión empieza aquí
      </p>

      <h1
        class="max-w-xl text-4xl leading-tight font-bold tracking-tight sm:text-6xl"
      >
        El mar marca el ritmo.
        <span class="text-sky-300">Tú eliges el momento.</span>
      </h1>

      <p class="mt-5 max-w-xl text-base leading-7 text-slate-300 sm:text-lg">
        Consulta las condiciones del viento, el estado del mar y la talla de
        cometa orientativa para tu próxima sesión de kitesurf.
      </p>
    </div>

    <div class="relative mt-8 flex items-center gap-3 text-sm text-slate-300">
      <span class="h-px w-10 bg-(--previ-gold)"></span>
      Previsión para tu próxima sesión
    </div>
  </section>

  <!-- Resumen de búsqueda en móvil -->
  <button
    v-if="!filtersExpanded"
    type="button"
    class="relative z-10 -mt-5 w-full rounded-2xl border border-(--previ-border) bg-white p-4 shadow-lg shadow-slate-900/5 sm:mx-5 sm:hidden sm:p-5"
    aria-label="Modificar búsqueda"
    @click="filtersExpanded = true"
  >
    <span>
      <span class="block text-sm font-semibold text-(--previ-navy)">
        Modificar búsqueda
      </span>
      <span class="mt-1 block text-xs text-(--previ-muted)">
        {{ selectedDate }} · {{ selectedTime }}
      </span>
    </span>

    <span class="text-sm font-semibold text-(--previ-blue)"> Editar </span>
  </button>

  <div class="sm:block" :class="filtersExpanded ? 'block' : 'hidden'">
    <ForecastFilters
      v-model:selected-beach="selectedBeach"
      v-model:selected-date="selectedDate"
      v-model:selected-time="selectedTime"
      :beaches="beaches"
      :forecast-horizon-days="forecastHorizonDays"
      :loading="loading"
      @search="handleSearch"
    />
  </div>

  <!-- Error -->
  <div
    v-if="error"
    role="alert"
    class="mt-8 rounded-xl border border-red-200 bg-red-50 p-4 text-sm text-red-800"
  >
    {{ error }}
  </div>

  <!-- Estado de carga -->
  <div
    v-if="loading && !forecast"
    class="py-16 text-center text-(--previ-muted)"
    role="status"
  >
    <div
      class="mx-auto mb-4 size-8 animate-spin rounded-full border-2 border-(--previ-border) border-t-(--previ-blue)"
    ></div>
    Consultando las condiciones del mar...
  </div>

  <ForecastOverview
    v-if="forecast"
    :forecast="forecast"
    :selected-date="selectedDate"
    :selected-time="selectedTime"
    :loading="loading"
  />

  <KiteSizingSection
    v-if="kiteSizing"
    :matrix="kiteSizing"
    :loading="loading"
  />
</template>
