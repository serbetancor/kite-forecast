<script setup lang="ts">
import type { KiteSizingMatrix } from "../models/forecast"
import KiteSizingHeatmap from "./KiteSizingHeatmap.vue"
import KiteSizingMobile from "./KiteSizingMobile.vue"
import KiteSizingSectionSkeleton from "./KiteSizingSectionSkeleton.vue"

defineProps<{
  matrix: KiteSizingMatrix
  loading: boolean
}>()
</script>

<template>
  <section class="mt-12">
    <div class="mb-6">
      <p
        class="text-xs font-semibold tracking-[0.2em] text-(--previ-blue) uppercase"
      >
        Encuentra tu talla
      </p>

      <h2 class="mt-2 text-3xl font-bold tracking-tight text-(--previ-navy)">
        Tu cometa, según el viento
      </h2>

      <p class="mt-3 max-w-2xl text-sm leading-6 text-(--previ-muted)">
        Explora la matriz según tu peso y la talla de cometa. Las puntuaciones
        son orientativas y no sustituyen una evaluación de las condiciones ni
        las recomendaciones de seguridad.
      </p>
    </div>

    <KiteSizingSectionSkeleton v-if="loading" />

    <template v-else>
      <div class="lg:hidden">
        <KiteSizingMobile :matrix="matrix" />
      </div>

      <div class="hidden lg:block">
        <KiteSizingHeatmap :matrix="matrix" />
      </div>
    </template>
  </section>
</template>
