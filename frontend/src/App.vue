<script setup lang="ts">
import { ref } from "vue"

import KiteSizingHeatmap from "./components/KiteSizingHeatMap.vue"
import type { KiteSizingMatrix, ObjectiveReport } from "./models/forecast"

const API_BASE_URL = "http://localhost:8000"

const beaches = [
  { id: "salinas", name: "Salinas" },
  { id: "vargas", name: "Vargas" },
  { id: "bocabarranco", name: "Bocabarranco" },
  { id: "las-burras", name: "Las Burras" },
  { id: "castillo-del-romeral", name: "Castillo del Romeral" },
  { id: "el-burrero", name: "El Burrero" },
  { id: "punta-de-maspalomas", name: "Punta de Maspalomas" },
]

const times = [
  { value: "08:00", label: "08:00" },
  { value: "10:00", label: "10:00" },
  { value: "12:00", label: "12:00" },
  { value: "14:00", label: "14:00" },
  { value: "16:00", label: "16:00" },
  { value: "18:00", label: "18:00" },
]

function formatDate(date: Date): string {
  const year = date.getFullYear()
  const month = String(date.getMonth() + 1).padStart(2, "0")
  const day = String(date.getDate()).padStart(2, "0")

  return `${year}-${month}-${day}`
}

const selectedBeach = ref("salinas")
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
    const params = new URLSearchParams({
      beach: selectedBeach.value,
      date: selectedDate.value,
      time: selectedTime.value,
    })

    const [forecastResponse, sizingResponse] = await Promise.all([
      fetch(`${API_BASE_URL}/forecast?${params.toString()}`),
      fetch(`${API_BASE_URL}/kite-sizing?${params.toString()}`),
    ])

    if (!forecastResponse.ok || !sizingResponse.ok) {
      throw new Error(
        "No se ha podido obtener la previsión. Inténtalo de nuevo.",
      )
    }

    const [forecastData, sizingData] = await Promise.all([
      forecastResponse.json(),
      sizingResponse.json(),
    ])

    forecast.value = forecastData as ObjectiveReport
    kiteSizing.value = sizingData as KiteSizingMatrix
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

function formatTimestamp(timestamp: string): string {
  return new Intl.DateTimeFormat("es-ES", {
    dateStyle: "medium",
    timeStyle: "short",
  }).format(new Date(timestamp))
}

function formatDirection(degrees: number, cardinal: string): string {
  return `${cardinal} · ${Math.round(degrees)}°`
}

searchForecast()
</script>

<template>
  <div class="min-h-screen bg-(--previ-bg) text-(--previ-text)">
    <!-- Cabecera -->
    <header class="border-b border-(--previ-border) bg-white">
      <div
        class="mx-auto flex max-w-7xl items-center justify-between px-5 py-5 sm:px-8"
      >
        <a href="#" class="flex items-center gap-3" aria-label="Preví, inicio">
          <span
            class="flex h-11 w-11 items-center justify-center rounded-xl bg-(--previ-navy) text-xl font-bold text-white"
          >
            P
          </span>

          <span>
            <span
              class="block text-2xl font-bold tracking-tight text-(--previ-navy)"
            >
              preví<span class="text-(--previ-gold)">.</span>
            </span>
            <span
              class="block text-[10px] font-semibold tracking-[0.22em] text-(--previ-muted) uppercase"
            >
              Wind & sea forecast
            </span>
          </span>
        </a>

        <span
          class="hidden items-center gap-2 rounded-full border border-(--previ-border) px-4 py-2 text-xs font-medium text-(--previ-muted) sm:flex"
        >
          <span class="h-2 w-2 rounded-full bg-(--previ-blue)"></span>
          Gran Canaria
        </span>
      </div>
    </header>

    <main class="mx-auto max-w-7xl px-5 py-8 sm:px-8 sm:py-12">
      <!-- Presentación -->
      <section
        class="relative overflow-hidden rounded-3xl bg-(--previ-navy) px-6 py-10 text-white sm:px-10 sm:py-14"
      >
        <div
          class="pointer-events-none absolute -top-20 -right-12 h-64 w-64 rounded-full border border-white/10"
        ></div>
        <div
          class="pointer-events-none absolute -top-10 -right-2 h-44 w-44 rounded-full border border-white/10"
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

          <p
            class="mt-5 max-w-xl text-base leading-7 text-slate-300 sm:text-lg"
          >
            Consulta las condiciones del viento, el estado del mar y la talla de
            cometa orientativa para tu próxima sesión de kitesurf.
          </p>
        </div>

        <div
          class="relative mt-8 flex items-center gap-3 text-sm text-slate-300"
        >
          <span class="h-px w-10 bg-(--previ-gold)"></span>
          Previsión para tu próxima sesión
        </div>
      </section>

      <!-- Formulario -->
      <section
        class="relative z-10 -mt-5 rounded-2xl border border-(--previ-border) bg-white p-5 shadow-lg shadow-slate-900/5 sm:mx-5 sm:p-7"
      >
        <form
          class="grid grid-cols-1 gap-5 sm:grid-cols-2 lg:grid-cols-4 lg:items-end"
          @submit.prevent="searchForecast"
        >
          <div>
            <label
              for="beach"
              class="mb-2 block text-sm font-semibold text-(--previ-navy)"
            >
              Spot
            </label>
            <select
              id="beach"
              v-model="selectedBeach"
              class="w-full rounded-xl border border-(--previ-border) bg-white px-4 py-3 text-(--previ-text) transition outline-none focus:border-(--previ-blue) focus:ring-2 focus:ring-sky-100"
            >
              <option
                v-for="beach in beaches"
                :key="beach.id"
                :value="beach.id"
              >
                {{ beach.name }}
              </option>
            </select>
          </div>

          <div>
            <label
              for="date"
              class="mb-2 block text-sm font-semibold text-(--previ-navy)"
            >
              Fecha
            </label>
            <input
              id="date"
              v-model="selectedDate"
              type="date"
              required
              class="w-full rounded-xl border border-(--previ-border) bg-white px-4 py-3 text-(--previ-text) transition outline-none focus:border-(--previ-blue) focus:ring-2 focus:ring-sky-100"
            />
          </div>

          <div>
            <label
              for="time"
              class="mb-2 block text-sm font-semibold text-(--previ-navy)"
            >
              Hora
            </label>
            <select
              id="time"
              v-model="selectedTime"
              class="w-full rounded-xl border border-(--previ-border) bg-white px-4 py-3 text-(--previ-text) transition outline-none focus:border-(--previ-blue) focus:ring-2 focus:ring-sky-100"
            >
              <option
                v-for="time in times"
                :key="time.value"
                :value="time.value"
              >
                {{ time.label }}
              </option>
            </select>
          </div>

          <button
            type="submit"
            :disabled="loading"
            class="flex min-h-12 items-center justify-center gap-2 rounded-xl bg-(--previ-blue) px-5 py-3 font-semibold text-white transition hover:bg-(--previ-navy) disabled:cursor-wait disabled:opacity-60"
          >
            <span v-if="loading">Consultando...</span>
            <span v-else>Consultar condiciones</span>
            <span v-if="!loading" aria-hidden="true">→</span>
          </button>
        </form>
      </section>

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
          class="mx-auto mb-4 h-8 w-8 animate-spin rounded-full border-2 border-(--previ-border) border-t-(--previ-blue)"
        ></div>
        Consultando las condiciones del mar...
      </div>

      <!-- Resultados -->
      <template v-if="forecast">
        <section class="mt-12">
          <div
            class="mb-6 flex flex-col gap-2 sm:flex-row sm:items-end sm:justify-between"
          >
            <div>
              <p
                class="text-xs font-semibold tracking-[0.2em] text-(--previ-blue) uppercase"
              >
                Tu previsión
              </p>
              <h2
                class="mt-2 text-3xl font-bold tracking-tight text-(--previ-navy)"
              >
                {{ forecast.beach.name }}
              </h2>
              <p class="mt-1 text-sm text-(--previ-muted)">
                {{ selectedDate }} · {{ selectedTime }}
              </p>
            </div>

            <p class="text-xs text-(--previ-muted)" v-if="forecast.timestamp">
              Actualizado: {{ formatTimestamp(forecast.timestamp) }}
            </p>
          </div>

          <div class="grid grid-cols-1 gap-4 sm:grid-cols-2 xl:grid-cols-4">
            <!-- Viento -->
            <article
              class="rounded-2xl border border-(--previ-border) bg-white p-6"
            >
              <div class="flex items-center justify-between">
                <span class="text-sm font-medium text-(--previ-muted)">
                  Viento
                </span>
                <span
                  class="flex h-10 w-10 items-center justify-center rounded-xl bg-sky-50 text-xl"
                  aria-hidden="true"
                >
                  ↗
                </span>
              </div>
              <p class="mt-5 text-4xl font-bold text-(--previ-navy)">
                {{ forecast.wind.speed_knots }}
                <span class="text-base font-medium text-(--previ-muted)">
                  kn
                </span>
              </p>
              <p class="mt-2 text-sm text-(--previ-muted)">
                Rachas: {{ forecast.wind.gusts_knots }} kn
              </p>
              <p class="mt-1 text-sm text-(--previ-blue)">
                {{
                  formatDirection(
                    forecast.wind.direction_deg,
                    forecast.wind.direction_cardinal,
                  )
                }}
              </p>
            </article>

            <!-- Temperatura -->
            <article
              class="rounded-2xl border border-(--previ-border) bg-white p-6"
            >
              <div class="flex items-center justify-between">
                <span class="text-sm font-medium text-(--previ-muted)">
                  Temperatura
                </span>
                <span
                  class="flex h-10 w-10 items-center justify-center rounded-xl bg-amber-50 text-xl"
                  aria-hidden="true"
                >
                  ☀
                </span>
              </div>
              <p class="mt-5 text-4xl font-bold text-(--previ-navy)">
                {{ forecast.weather.temperature_c }}
                <span class="text-base font-medium text-(--previ-muted)">
                  °C
                </span>
              </p>
              <p class="mt-2 text-sm text-(--previ-muted)">
                Temperatura del aire
              </p>
            </article>

            <!-- Oleaje -->
            <article
              class="rounded-2xl border border-(--previ-border) bg-white p-6"
            >
              <div class="flex items-center justify-between">
                <span class="text-sm font-medium text-(--previ-muted)">
                  Oleaje
                </span>
                <span
                  class="flex h-10 w-10 items-center justify-center rounded-xl bg-sky-50 text-xl"
                  aria-hidden="true"
                >
                  ≋
                </span>
              </div>
              <p class="mt-5 text-4xl font-bold text-(--previ-navy)">
                {{ forecast.waves.height_m }}
                <span class="text-base font-medium text-(--previ-muted)">
                  m
                </span>
              </p>
              <p class="mt-2 text-sm text-(--previ-muted)">
                Periodo: {{ forecast.waves.period_s }} s
              </p>
              <p class="mt-1 text-sm text-(--previ-blue)">
                {{
                  formatDirection(
                    forecast.waves.direction_deg,
                    forecast.waves.direction_cardinal,
                  )
                }}
              </p>
            </article>

            <!-- Corriente -->
            <article
              class="rounded-2xl border border-(--previ-border) bg-white p-6"
            >
              <div class="flex items-center justify-between">
                <span class="text-sm font-medium text-(--previ-muted)">
                  Corriente
                </span>
                <span
                  class="flex h-10 w-10 items-center justify-center rounded-xl bg-sky-50 text-xl"
                  aria-hidden="true"
                >
                  ⇢
                </span>
              </div>
              <p class="mt-5 text-4xl font-bold text-(--previ-navy)">
                {{ forecast.sea.current_velocity_kmh }}
                <span class="text-base font-medium text-(--previ-muted)">
                  km/h
                </span>
              </p>
              <p class="mt-2 text-sm text-(--previ-muted)">
                Nivel del mar: {{ forecast.sea.level_m }} m
              </p>
              <p class="mt-1 text-sm text-(--previ-blue)">
                {{
                  formatDirection(
                    forecast.sea.current_direction_deg,
                    forecast.sea.current_direction_cardinal,
                  )
                }}
              </p>
            </article>
          </div>
        </section>
      </template>

      <!-- Matriz de tallas -->
      <section v-if="kiteSizing" class="mt-12">
        <div class="mb-6">
          <p
            class="text-xs font-semibold tracking-[0.2em] text-(--previ-blue) uppercase"
          >
            Encuentra tu talla
          </p>
          <h2
            class="mt-2 text-3xl font-bold tracking-tight text-(--previ-navy)"
          >
            Tu cometa, según el viento
          </h2>
          <p class="mt-3 max-w-2xl text-sm leading-6 text-(--previ-muted)">
            Explora la matriz según tu peso y la talla de cometa. Las
            puntuaciones son orientativas y no sustituyen una evaluación de las
            condiciones ni las recomendaciones de seguridad.
          </p>
        </div>

        <KiteSizingHeatmap :matrix="kiteSizing" />
      </section>
    </main>

    <!-- Pie -->
    <footer class="mt-16 border-t border-(--previ-border) bg-white">
      <div
        class="mx-auto flex max-w-7xl flex-col gap-3 px-5 py-7 text-sm text-(--previ-muted) sm:flex-row sm:items-center sm:justify-between sm:px-8"
      >
        <p>
          <span class="font-bold text-(--previ-navy)">preví.</span>
          Hecho para seguir el viento.
        </p>
        <p>Consulta siempre las condiciones reales antes de navegar.</p>
      </div>
    </footer>
  </div>
</template>
