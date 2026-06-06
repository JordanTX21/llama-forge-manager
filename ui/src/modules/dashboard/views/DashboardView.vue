<script setup lang="ts">
import { ref, onMounted, onUnmounted } from 'vue'
import { DashboardService, type HardwareStats } from '../services/dashboard.service'

const stats = ref<HardwareStats | null>(null)
let pollInterval: ReturnType<typeof setInterval> | null = null

const fetchStats = async () => {
  try {
    stats.value = await DashboardService.getHardwareStats()
  } catch (err) {
    console.error('Failed to fetch stats', err)
  }
}

onMounted(() => {
  fetchStats()
  pollInterval = setInterval(fetchStats, 3000)
})

onUnmounted(() => {
  if (pollInterval) clearInterval(pollInterval)
})
</script>

<template>
  <div class="space-y-6 w-full max-w-4xl mx-auto">
    <!-- Status Banner -->
    <section class="flex items-center justify-between p-4 bg-surface-container-low rounded-2xl border border-outline">
      <div class="flex items-center gap-3">
        <div class="w-2 h-2 rounded-full bg-primary ai-pulse"></div>
        <p class="font-label text-sm text-on-surface">Engine Connected</p>
      </div>
      <span v-if="stats && stats.gpu.available"
        class="font-label text-xs text-primary bg-primary-container px-2 py-1 rounded-md">
        {{ stats.gpu.used_mb }} MB VRAM
      </span>
      <span v-else class="font-label text-xs text-on-surface-variant bg-surface-container-high px-2 py-1 rounded-md">
        CPU Only
      </span>
    </section>

    <!-- Bento Widgets Grid -->
    <div v-if="stats" class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">

      <!-- VRAM Usage Widget -->
      <div
        class="bg-surface-container-low border border-outline p-6 rounded-3xl flex flex-col items-center justify-center space-y-4 relative overflow-hidden">
        <div class="w-full flex justify-between items-start z-10">
          <div class="flex flex-col">
            <span class="font-label text-xs text-on-surface-variant uppercase tracking-wider">VRAM Usage</span>
            <span v-if="stats.gpu.available" class="font-headline text-2xl text-on-surface mt-1 font-semibold">{{
              (stats.gpu.used_mb / 1024).toFixed(1) }} <span class="text-on-surface-variant text-base">/ {{
                (stats.gpu.total_mb / 1024).toFixed(1) }} GB</span></span>
            <span v-else class="font-headline text-xl text-on-surface mt-1 font-semibold">N/A</span>
          </div>
        </div>

        <div v-if="stats.gpu.available"
          class="relative w-32 h-32 circular-progress flex items-center justify-center transition-all duration-1000 z-10"
          :style="`--progress: ${(stats.gpu.used_mb / stats.gpu.total_mb) * 100};`">
          <span class="font-headline text-2xl font-bold text-on-surface">{{ Math.round((stats.gpu.used_mb /
            stats.gpu.total_mb) * 100) }}%</span>
        </div>
        <div v-else class="relative w-32 h-32 flex items-center justify-center z-10">
          <span class="text-on-surface-variant">No GPU</span>
        </div>

        <p class="font-body text-sm text-on-surface-variant text-center z-10">{{ stats.gpu.available ? 'NVIDIA GPU' :
          'System GPU' }}</p>
      </div>

      <!-- System RAM Widget -->
      <div
        class="bg-surface-container-low border border-outline p-6 rounded-3xl flex flex-col justify-between space-y-6">
        <div class="w-full flex justify-between items-start">
          <div class="flex flex-col">
            <span class="font-label text-xs text-on-surface-variant uppercase tracking-wider">System RAM</span>
            <span class="font-headline text-2xl text-on-surface mt-1 font-semibold">{{ (stats.ram.total_gb -
              stats.ram.free_gb).toFixed(1) }} <span class="text-on-surface-variant text-base">/ {{ stats.ram.total_gb
              }} GB</span></span>
          </div>
        </div>

        <div class="space-y-3">
          <div class="w-full h-2 bg-outline rounded-full overflow-hidden">
            <div class="h-full bg-primary rounded-full transition-all duration-500"
              :style="`width: ${stats.ram.usage_percent}%;`"></div>
          </div>
          <div class="flex justify-between font-label text-xs text-on-surface-variant">
            <span>Physical: {{ stats.ram.usage_percent }}%</span>
            <span>Free: {{ stats.ram.free_gb }} GB</span>
          </div>
        </div>
      </div>

      <!-- CPU Load Widget -->
      <div
        class="bg-surface-container-low border border-outline p-6 rounded-3xl flex flex-col justify-between space-y-6">
        <div class="w-full flex justify-between items-start">
          <div class="flex flex-col">
            <span class="font-label text-xs text-on-surface-variant uppercase tracking-wider">CPU Load</span>
            <span class="font-headline text-2xl text-on-surface mt-1 font-semibold">{{ stats.cpu.usage_percent
            }}%</span>
          </div>
        </div>

        <div class="space-y-4">
          <div class="space-y-2">
            <div class="flex justify-between font-label text-xs">
              <span class="text-on-surface">Total Cores: {{ stats.cpu.cores }}</span>
              <span class="text-primary">{{ stats.cpu.usage_percent }}%</span>
            </div>
            <div class="w-full h-1 bg-outline rounded-full overflow-hidden">
              <div class="h-full bg-primary rounded-full transition-all duration-500"
                :style="`width: ${stats.cpu.usage_percent}%;`"></div>
            </div>
          </div>
          <p class="font-label text-xs text-on-surface-variant">{{ stats.cpu.threads }} Threads Active</p>
        </div>
      </div>

    </div>

    <div v-else class="flex items-center justify-center h-64 text-on-surface-variant">
      <div class="w-4 h-4 rounded-full bg-primary ai-pulse mr-3"></div>
      Loading telemetry...
    </div>

  </div>
</template>
