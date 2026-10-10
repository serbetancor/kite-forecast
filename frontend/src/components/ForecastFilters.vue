<script setup lang="ts">
import { computed, watch } from "vue"

import type { BeachOption } from "../models/config"
import { formatDate } from "../utils/formatters"

const props = defineProps<{
  beaches: BeachOption[]
  forecastHorizonDays: number
  selectedBeach: string
  selectedDate: string
  selectedTime: string
  loading: boolean
}>()

const emit = defineEmits<{
  "update:selectedBeach": [value: string]
  "update:selectedDate": [value: string]
  "update:selectedTime": [value: string]
  search: []
}>()

const dateOptions = computed(() => {
  const today = new Date()
  today.setHours(12, 0, 0, 0)

  return Array.from(
    { length: Math.max(1, props.forecastHorizonDays) },
    (_, index) => {
      const date = new Date(today)
      date.setDate(today.getDate() + index)

      return {
        value: formatDate(date),
        day:
          index === 0
            ? "HOY"
            : new Intl.DateTimeFormat("es-ES", {
                weekday: "short",
              })
                .format(date)
                .replace(".", "")
                .toUpperCase(),
        number: date.getDate(),
        month: new Intl.DateTimeFormat("es-ES", {
          month: "short",
        })
          .format(date)
          .replace(".", ""),
      }
    },
  )
})

const availableTimes = computed(() => {
  const hours = Array.from(
    { length: 24 },
    (_, hour) => `${String(hour).padStart(2, "0")}:00`,
  )

  const today = formatDate(new Date())

  if (props.selectedDate !== today) {
    return hours
  }

  const now = new Date()
  const firstAvailableHour =
    now.getMinutes() === 0 ? now.getHours() : now.getHours() + 1

  return hours.filter((time) => Number(time.slice(0, 2)) >= firstAvailableHour)
})

watch(
  [() => props.selectedDate, availableTimes],
  () => {
    if (!availableTimes.value.includes(props.selectedTime)) {
      const firstTime = availableTimes.value[0]

      if (firstTime) {
        emit("update:selectedTime", firstTime)
      }
    }
  },
  { immediate: true },
)
</script>

<template>
  <section
    class="relative z-10 -mt-5 rounded-2xl border border-(--previ-border) bg-white p-4 shadow-lg shadow-slate-900/5 sm:mx-5 sm:p-5"
  >
    <form class="space-y-5" @submit.prevent="emit('search')">
      <div>
        <label
          for="beach"
          class="mb-1.5 block text-sm font-medium text-(--previ-navy)"
        >
          Spot
        </label>

        <select
          id="beach"
          :value="selectedBeach"
          class="w-full rounded-xl border border-(--previ-border) bg-white px-4 py-2.5 text-(--previ-text) transition outline-none focus:border-(--previ-blue) focus:ring-2 focus:ring-sky-100"
          @change="
            emit(
              'update:selectedBeach',
              ($event.target as HTMLSelectElement).value,
            )
          "
        >
          <option v-for="beach in beaches" :key="beach.id" :value="beach.id">
            {{ beach.name }}
          </option>
        </select>
      </div>

      <fieldset>
        <legend class="mb-2 text-sm font-medium text-(--previ-navy)">
          Día de previsión
        </legend>

        <div class="grid grid-cols-4 gap-2 sm:grid-cols-7 lg:grid-cols-7">
          <button
            v-for="date in dateOptions"
            :key="date.value"
            type="button"
            :aria-pressed="selectedDate === date.value"
            class="flex w-full min-w-0 flex-col items-center rounded-xl border px-2 py-2 transition"
            :class="
              selectedDate === date.value
                ? 'border-(--previ-blue) bg-sky-50 text-(--previ-blue)'
                : 'border-(--previ-border) bg-white text-(--previ-text) hover:border-(--previ-blue)'
            "
            @click="emit('update:selectedDate', date.value)"
          >
            <span class="text-xs font-medium">{{ date.day }}</span>
            <span class="text-lg leading-6 font-semibold">
              {{ date.number }}
            </span>
            <span class="text-xs">{{ date.month }}</span>
          </button>
        </div>
      </fieldset>

      <fieldset>
        <legend class="mb-2 text-sm font-medium text-(--previ-navy)">
          Hora
        </legend>

        <div
          class="grid grid-cols-4 gap-2 sm:grid-cols-4 md:grid-cols-6 lg:grid-cols-8"
        >
          <button
            v-for="time in availableTimes"
            :key="time"
            type="button"
            :aria-pressed="selectedTime === time"
            class="w-full min-w-0 rounded-lg border px-2 py-2 text-sm font-medium transition"
            :class="
              selectedTime === time
                ? 'border-(--previ-navy) bg-(--previ-navy) text-white'
                : 'border-(--previ-border) bg-white text-(--previ-text) hover:border-(--previ-blue)'
            "
            @click="emit('update:selectedTime', time)"
          >
            {{ time }}
          </button>

          <p
            v-if="availableTimes.length === 0"
            class="col-span-full text-sm text-(--previ-muted)"
          >
            Ya no quedan horas disponibles para hoy.
          </p>
        </div>
      </fieldset>

      <button
        type="submit"
        :disabled="
          loading || beaches.length === 0 || availableTimes.length === 0
        "
        class="flex min-h-10 w-full items-center justify-center gap-2 rounded-xl bg-(--previ-blue) px-5 py-2.5 font-semibold text-white transition hover:bg-(--previ-navy) disabled:cursor-wait disabled:opacity-60"
      >
        <span v-if="loading">Consultando...</span>
        <span v-else>Consultar condiciones</span>
        <span v-if="!loading" aria-hidden="true">→</span>
      </button>
    </form>
  </section>
</template>
