```vue
<script setup lang="ts">
import Skeleton from "./Skeleton.vue"
</script>

<template>
  <section class="mt-6" aria-hidden="true">
    <!-- Skeleton móvil -->
    <div class="lg:hidden">
      <Skeleton class="mb-5 h-4 w-64 max-w-full rounded-full" />

      <div class="mb-6">
        <Skeleton class="mb-2 h-4 w-16 rounded-full" />
        <Skeleton class="h-12 w-full rounded-xl" />
      </div>

      <div class="space-y-3">
        <article
          v-for="index in 4"
          :key="`mobile-${index}`"
          class="rounded-2xl border border-(--previ-border) bg-white p-4 shadow-sm"
        >
          <div class="flex items-center gap-3">
            <Skeleton class="size-14 shrink-0 rounded-xl" />

            <div class="min-w-0 flex-1">
              <div class="mb-2 flex items-center justify-between gap-2">
                <Skeleton class="h-4 w-28 rounded-full" />
                <Skeleton class="h-5 w-16 rounded-full" />
              </div>

              <Skeleton class="h-2 w-full rounded-full" />
            </div>
          </div>
        </article>
      </div>

      <Skeleton class="mt-4 h-3 w-full rounded-full" />
      <Skeleton class="mt-2 h-3 w-4/5 rounded-full" />
    </div>

    <!-- Skeleton desktop -->
    <div class="hidden rounded-2xl bg-slate-900 p-6 lg:block">
      <div
        class="flex flex-col gap-2 sm:flex-row sm:items-start sm:justify-between"
      >
        <div class="space-y-3">
          <Skeleton class="h-6 w-56 rounded-lg" />
          <Skeleton class="h-3 w-64 max-w-full rounded-full" />
        </div>

        <Skeleton class="h-4 w-40 rounded-full" />
      </div>

      <div class="mt-8 overflow-hidden">
        <div class="grid grid-cols-9 gap-2">
          <div></div>

          <Skeleton
            v-for="index in 8"
            :key="`weight-${index}`"
            class="h-3 w-full rounded-sm"
          />

          <template v-for="row in 5" :key="`row-${row}`">
            <Skeleton class="h-4 w-10 rounded-sm" />

            <Skeleton
              v-for="column in 8"
              :key="`${row}-${column}`"
              class="aspect-square w-full rounded-sm"
            />
          </template>
        </div>
      </div>

      <Skeleton class="mt-6 h-3 w-48 rounded-full" />
    </div>
  </section>
</template>
```
