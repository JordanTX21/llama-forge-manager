<script setup lang="ts">
import { SettingsService } from '../services/settings.service'
import { Play } from '@lucide/vue'

const startSwap = async () => {
  try {
    await SettingsService.startSwap()
    alert('Llama-Swap iniciado. Puedes conectarte en el puerto 8080.')
  } catch (err) {
    console.error(err)
    alert('Error al iniciar Llama-Swap.')
  }
}
</script>

<template>
  <div class="glass rounded-2xl overflow-hidden relative group border border-outline shadow-xl">
    <div class="absolute inset-0 opacity-10 pointer-events-none">
      <div class="absolute top-0 right-0 w-48 h-48 bg-primary blur-[80px]"></div>
    </div>
    <div class="p-5 md:flex items-center justify-between relative z-10">
      <div>
        <div class="flex items-center gap-2 mb-1">
          <span class="w-1.5 h-1.5 rounded-full bg-primary animate-pulse"></span>
          <span class="font-label text-[10px] text-primary tracking-widest uppercase">Accelerator Ready</span>
        </div>
        <h2 class="font-headline text-xl font-bold">Llama-Swap Router</h2>
        <p class="text-on-surface-variant text-sm max-w-sm mt-1">Optimize local inference by dynamically switching between active models.</p>
      </div>
      <div class="mt-4 md:mt-0">
        <button @click="startSwap"
          class="bg-primary-container text-primary font-semibold px-6 py-2.5 rounded-lg shadow hover:bg-primary-container/80 transition-all active:scale-95 flex items-center gap-2 text-sm">
          <span>Run Swap</span>
          <Play class="text-primary w-5 h-5" />
        </button>
      </div>
    </div>
  </div>
</template>
