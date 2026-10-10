<script setup lang="ts">
defineProps<{
  class?: string
}>()
</script>

<template>
  <div
    aria-hidden="true"
    class="animate-pulse rounded-md bg-slate-200/80"
    :class="$props.class"
  ></div>
</template>
