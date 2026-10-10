<script setup lang="ts">
import type { Component } from "vue"

defineProps<{
  title: string
  icon: Component
  iconBackground: string
  value: string | number
  unit: string
  detail: string
  direction?: string
}>()
</script>

<template>
  <article
    class="rounded-2xl border border-(--previ-border) bg-white p-4 sm:p-6"
  >
    <div class="flex items-center justify-between">
      <span class="text-sm font-medium text-(--previ-muted)">
        {{ title }}
      </span>

      <span
        class="flex size-8 shrink-0 items-center justify-center rounded-xl text-xl sm:size-10"
        :class="iconBackground"
        aria-hidden="true"
      >
        <component
          :is="icon"
          class="size-4 text-(--previ-blue) sm:size-5"
          aria-hidden="true"
        />
      </span>
    </div>

    <p class="mt-5 text-4xl font-bold text-(--previ-navy)">
      {{ value }}
      <span class="text-base font-medium text-(--previ-muted)">
        {{ unit }}
      </span>
    </p>

    <p class="mt-2 text-xs text-(--previ-muted) sm:text-sm">
      {{ detail }}
    </p>

    <p v-if="direction" class="mt-1 text-sm text-(--previ-blue)">
      {{ direction }}
    </p>
  </article>
</template>
