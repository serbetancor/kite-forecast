<script setup lang="ts">
import { RouterLink } from "vue-router"

import ForecastIcon from "../assets/icons/ForecastIcon.vue"
import RankingIcon from "../assets/icons/RankingIcon.vue"
</script>

<template>
  <nav
    class="flex justify-center border-b border-(--previ-border)"
    aria-label="Navegación principal"
  >
    <div class="flex items-center gap-1">
      <RouterLink
        :to="{ name: 'forecast' }"
        class="group relative inline-flex items-center gap-2.5 rounded-t-xl px-5 py-4 text-sm font-semibold transition-colors duration-200"
        active-class="text-(--previ-navy)"
        inactive-class="text-slate-500 hover:bg-sky-50/70 hover:text-(--previ-navy)"
      >
        <ForecastIcon class="size-5 transition-colors" />
        <span>Previsión</span>

        <span
          class="absolute inset-x-4 -bottom-px h-0.75 rounded-full bg-(--previ-blue) opacity-0 transition-opacity duration-200"
          :class="{ 'opacity-100': $route.name === 'forecast' }"
        />
      </RouterLink>

      <RouterLink
        :to="{ name: 'ranking' }"
        class="group relative inline-flex items-center gap-2.5 rounded-t-xl px-5 py-4 text-sm font-semibold transition-colors duration-200"
        active-class="text-(--previ-navy)"
        inactive-class="text-slate-500 hover:bg-sky-50/70 hover:text-(--previ-navy)"
      >
        <RankingIcon class="size-5 transition-colors" />
        <span>Ranking</span>

        <span
          class="absolute inset-x-4 -bottom-px h-0.75 rounded-full bg-(--previ-blue) opacity-0 transition-opacity duration-200"
          :class="{ 'opacity-100': $route.name === 'ranking' }"
        />
      </RouterLink>
    </div>
  </nav>
</template>
