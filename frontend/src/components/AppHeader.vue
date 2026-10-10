<template>
  <header class="border-b border-(--previ-border) bg-white">
    <div
      class="mx-auto flex max-w-7xl items-center justify-between px-5 py-5 sm:px-8"
    >
      <a href="#" class="flex items-center gap-3" aria-label="Preví, inicio">
        <span
          class="flex size-11 items-center justify-center rounded-xl bg-(--previ-navy) text-xl font-bold text-white"
        >
          P
        </span>

        <span>
          <span
            class="block text-2xl font-bold tracking-tight text-(--previ-navy)"
          >
            preví<span class="text-(--previ-gold)">.</span>
          </span>
          <span
            class="block text-[10px] font-semibold tracking-[0.22em] text-(--previ-muted) uppercase"
          >
            Wind & sea forecast
          </span>
        </span>
      </a>

      <span
        class="hidden items-center gap-2 rounded-full border border-(--previ-border) px-4 py-2 text-xs font-medium text-(--previ-muted) sm:flex"
      >
        <span class="size-2 rounded-full bg-(--previ-blue)"></span>
        Gran Canaria
      </span>
    </div>
  </header>
</template>
