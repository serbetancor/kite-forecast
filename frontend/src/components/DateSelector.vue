<script setup lang="ts">
import { computed } from "vue"

import { formatDate } from "../utils/formatters"

const props = defineProps<{
  modelValue: string
  days: number
}>()

const emit = defineEmits<{
  "update:modelValue": [value: string]
}>()

const dateOptions = computed(() => {
  const today = new Date()
  today.setHours(12, 0, 0, 0)

  return Array.from({ length: Math.max(1, props.days) }, (_, index) => {
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
  })
})
</script>

<template>
  <fieldset>
    <legend class="mb-2 text-sm font-medium text-(--previ-navy)">
      Día de previsión
    </legend>

    <div class="grid grid-cols-4 gap-2 sm:grid-cols-7">
      <button
        v-for="date in dateOptions"
        :key="date.value"
        type="button"
        :aria-pressed="modelValue === date.value"
        class="flex w-full min-w-0 flex-col items-center rounded-xl border px-2 py-2 transition"
        :class="
          modelValue === date.value
            ? 'border-(--previ-blue) bg-sky-50 text-(--previ-blue)'
            : 'border-(--previ-border) text-(--previ-text) hover:border-(--previ-blue)'
        "
        @click="emit('update:modelValue', date.value)"
      >
        <span class="text-xs font-medium">{{ date.day }}</span>
        <span class="text-lg leading-6 font-semibold">
          {{ date.number }}
        </span>
        <span class="text-xs">{{ date.month }}</span>
      </button>
    </div>
  </fieldset>
</template>
