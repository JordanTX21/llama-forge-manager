<script setup lang="ts">
defineProps<{
  text: string
}>()
</script>

<template>
  <div class="relative flex items-center group cursor-help">
    <slot />
    <div class="absolute bottom-full left-1/2 -translate-x-1/2 mb-2 w-max max-w-xs p-2 text-xs font-medium text-on-surface bg-surface-container-high border border-outline rounded-lg shadow-xl opacity-0 invisible group-hover:opacity-100 group-hover:visible transition-all duration-200 z-50 pointer-events-none">
      {{ text }}
    </div>
  </div>
</template>
