<script setup lang="ts">
import { ref } from 'vue'
import { useModelsStore } from '../store/models.store'
import { storeToRefs } from 'pinia'
import { CloudDownload, Download } from '@lucide/vue'

const store = useModelsStore()
const { isDownloading } = storeToRefs(store)

const repoId = ref('')
const filename = ref('')

const handleDownload = async () => {
  if (!repoId.value || !filename.value) return

  try {
    await store.downloadModel(repoId.value, filename.value)
    alert('Descarga iniciada en segundo plano.')
    repoId.value = ''
    filename.value = ''
  } catch (err) {
    console.error('Error starting download', err)
    alert('Error al iniciar descarga.')
  }
}
</script>

<template>
  <div class="glass p-5 rounded-2xl relative overflow-hidden group border border-outline">
    <div
      class="absolute -top-16 -right-16 w-48 h-48 bg-primary/5 rounded-full blur-[80px] group-hover:bg-primary/10 transition-colors duration-500">
    </div>
    <div class="relative z-10">
      <div class="flex items-center gap-2 mb-4">
        <CloudDownload class="text-primary w-6 h-6" />
        <h3 class="font-headline text-xl text-on-surface font-semibold">Download from Hugging Face</h3>
      </div>
      <div class="grid grid-cols-1 lg:grid-cols-3 gap-4 items-end">
        <div>
          <label class="font-label text-xs text-on-surface-variant uppercase tracking-wider ml-1">Repo ID</label>
          <input v-model="repoId"
            class="w-full bg-surface-container-low border border-outline px-3 py-2.5 rounded-lg text-sm text-on-surface transition-all placeholder:text-outline focus:outline-none focus:border-primary"
            placeholder="meta-llama/Llama-3-8B" type="text" />
        </div>
        <div>
          <label class="font-label text-xs text-on-surface-variant uppercase tracking-wider ml-1">Filename</label>
          <input v-model="filename"
            class="w-full bg-surface-container-low border border-outline px-3 py-2.5 rounded-lg text-sm text-on-surface transition-all placeholder:text-outline focus:outline-none focus:border-primary"
            placeholder="llama-3-8b.Q4_K_M.gguf" type="text" />
        </div>
        <div class="flex flex-col gap-3">
          <p class="text-[10px] font-label text-on-surface-variant text-center opacity-70">GGUF format recommended for
            CPU/GPU hybrid inference.</p>
          <button @click="handleDownload" :disabled="isDownloading"
            class="w-full bg-primary-container text-primary hover:bg-primary-container/80 px-4 py-2.5 rounded-lg font-semibold flex items-center justify-center gap-2 transition-all active:scale-[0.98] shadow-lg shadow-primary-container/20 disabled:opacity-50 text-sm">
            <Download class="w-[18px] h-[18px]" />
            <span>{{ isDownloading ? 'Downloading...' : 'Download Model' }}</span>
          </button>
        </div>
      </div>
    </div>
  </div>
</template>
