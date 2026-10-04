<script setup lang="ts">
import { ref } from "vue";
import type { ObjectiveReport } from "./models/forecast";

const beaches = [
  { id: "salinas", name: "Salinas" },
  { id: "vargas", name: "Vargas" },
  { id: "bocabarranco", name: "Bocabarranco" },
  { id: "las-burras", name: "Las Burras" },
  { id: "castillo-del-romeral", name: "Castillo del Romeral" },
  { id: "el-burrero", name: "El Burrero" },
  { id: "punta-de-maspalomas", name: "Punta de Maspalomas" },
];

const today = new Date();

const availableDates = Array.from({ length: 7 }, (_, index) => {
  const date = new Date(today);
  date.setDate(today.getDate() + index);

  return date.toISOString().split("T")[0];
});

const selectedBeach = ref(beaches[0].id);
const selectedDate = ref("2026-10-05");
const selectedTime = ref("12:00");

const forecast = ref<ObjectiveReport | null>(null);

async function searchForecast() {
  const params = new URLSearchParams({
    beach: selectedBeach.value,
    date: selectedDate.value,
    time: selectedTime.value,
  });

  const response = await fetch(`http://127.0.0.1:8000/forecast?${params}`);

  if (!response.ok) {
    console.error("Failed to fetch forecast");
    return;
  }

  forecast.value = await response.json();
}
</script>

<template>
  <main class="min-h-screen bg-slate-950 text-white">
    <div class="mx-auto max-w-5xl px-6 py-10">
      <header class="mb-10">
        <h1 class="text-4xl font-bold tracking-tight">Kite Forecast</h1>

        <p class="mt-2 text-slate-400">
          Condiciones de viento y mar para tu próxima sesión.
        </p>
      </header>

      <section class="rounded-2xl bg-slate-900 p-6">
        <h2 class="text-lg font-semibold">Consulta las condiciones</h2>

        <div class="mt-6 grid gap-5 md:grid-cols-3">
          <label class="flex flex-col gap-2">
            <span class="text-sm text-slate-400"> Playa </span>

            <select
              v-model="selectedBeach"
              class="rounded-lg border border-slate-700 bg-slate-800 px-4 py-3 outline-none focus:border-sky-500"
            >
              <option
                v-for="beach in beaches"
                :key="beach.id"
                :value="beach.id"
              >
                {{ beach.name }}
              </option>
            </select>
          </label>

          <label class="flex flex-col gap-2">
            <span class="text-sm text-slate-400"> Fecha </span>

            <input
              v-model="selectedDate"
              type="date"
              :min="availableDates[0]"
              :max="availableDates[availableDates.length - 1]"
              class="rounded-lg border border-slate-700 bg-slate-800 px-4 py-3 outline-none focus:border-sky-500"
            />
          </label>

          <label class="flex flex-col gap-2">
            <span class="text-sm text-slate-400"> Hora </span>

            <input
              v-model="selectedTime"
              type="time"
              class="rounded-lg border border-slate-700 bg-slate-800 px-4 py-3 outline-none focus:border-sky-500"
            />
          </label>
        </div>

        <button
          class="mt-6 rounded-lg bg-sky-500 px-6 py-3 font-semibold text-slate-950 transition hover:bg-sky-400"
          type="button"
          @click="searchForecast"
        >
          Ver condiciones
        </button>
      </section>
      <section v-if="forecast" class="mt-6 rounded-2xl bg-slate-900 p-6">
        <div class="flex items-center justify-between">
          <div>
            <h2 class="text-2xl font-bold">
              {{ forecast.beach }}
            </h2>
          </div>
        </div>

        <div class="mt-6 grid gap-4 sm:grid-cols-2 lg:grid-cols-4">
          <div class="rounded-xl bg-slate-800 p-5">
            <p class="text-sm text-slate-400">Viento</p>

            <p class="mt-2 text-2xl font-bold">
              {{ forecast.wind.speed_knots }} kn
            </p>

            <p class="mt-1 text-slate-400">
              {{ forecast.wind.direction_cardinal }}
              · rachas {{ forecast.wind.gusts_knots }} kn
            </p>
          </div>

          <div class="rounded-xl bg-slate-800 p-5">
            <p class="text-sm text-slate-400">Temperatura</p>

            <p class="mt-2 text-2xl font-bold">
              {{ forecast.weather.temperature_c }} °C
            </p>
          </div>

          <div class="rounded-xl bg-slate-800 p-5">
            <p class="text-sm text-slate-400">Oleaje</p>

            <p class="mt-2 text-2xl font-bold">
              {{ forecast.waves.height_m }} m
            </p>

            <p class="mt-1 text-slate-400">
              {{ forecast.waves.direction_cardinal }}
              · {{ forecast.waves.period_s }} s
            </p>
          </div>

          <div class="rounded-xl bg-slate-800 p-5">
            <p class="text-sm text-slate-400">Corriente</p>

            <p class="mt-2 text-2xl font-bold">
              {{ forecast.sea.current_velocity_kmh }} km/h
            </p>

            <p class="mt-1 text-slate-400">
              Dirección {{ forecast.sea.current_direction_cardinal }}
            </p>
          </div>
        </div>
      </section>
    </div>
  </main>
</template>
