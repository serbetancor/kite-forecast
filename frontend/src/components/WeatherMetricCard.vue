<script setup lang="ts">
import type { Component } from "vue"

defineProps<{
  title: string
  icon: Component
  iconBackground: string
  value?: number
  text?: string
  unit?: string
  detail?: string
  direction?: string
  score?: number
}>()
</script>

<template>
  <article
    class="flex flex-col justify-center rounded-2xl border border-(--previ-border) p-4 sm:p-6"
    :class="score ? 'bg-(--previ-blue)/5' : 'bg-white'"
  >
    <div class="flex items-center justify-between">
      <span class="text-sm font-medium text-(--previ-muted)">
        {{ title }}
      </span>
      <div
        class="ml-auto flex shrink-0 items-baseline gap-1 sm:mr-2"
        v-if="score"
      >
        <span
          class="text-md font-bold tracking-tight text-(--previ-blue) tabular-nums"
        >
          {{ Math.round(score) }}
        </span>
        <span class="text-xs text-(--previ-muted)">/ 100</span>
      </div>
      <div
        class="hidden size-8 shrink-0 items-center justify-center rounded-xl text-xl sm:flex sm:size-10"
        :class="iconBackground"
        aria-hidden="true"
      >
        <component
          :is="icon"
          class="size-4 text-(--previ-blue) sm:size-5"
          aria-hidden="true"
        />
      </div>
    </div>

    <p
      class="mt-5 flex items-baseline gap-1 text-4xl font-bold text-(--previ-navy)"
      v-if="value || unit"
    >
      <span v-if="value">{{ value }}</span>
      <span v-if="unit" class="text-base font-medium text-(--previ-muted)">
        {{ unit }}
      </span>
    </p>

    <p
      class="mt-5 text-2xl font-bold text-(--previ-navy) sm:text-4xl"
      v-if="text"
    >
      {{ text }}
    </p>

    <p
      v-if="detail"
      class="mt-2 text-xs whitespace-pre-line text-(--previ-muted) sm:text-sm"
    >
      {{ detail }}
    </p>

    <p v-if="direction" class="mt-1 text-sm text-(--previ-blue)">
      {{ direction }}
    </p>
  </article>
</template>
