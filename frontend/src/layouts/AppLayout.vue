<script setup lang="ts">
import AppFooter from "../components/AppFooter.vue"
import AppHeader from "../components/AppHeader.vue"
import AppNavigation from "../components/AppNavigation.vue"
</script>

<template>
  <div class="min-h-screen bg-(--previ-bg) text-(--previ-text)">
    <AppHeader />

    <div class="mx-auto max-w-7xl px-5 sm:px-8">
      <AppNavigation />
    </div>

    <main class="mx-auto max-w-7xl px-5 py-8 sm:px-8 sm:py-12">
      <slot />
    </main>

    <AppFooter />
  </div>
</template>
