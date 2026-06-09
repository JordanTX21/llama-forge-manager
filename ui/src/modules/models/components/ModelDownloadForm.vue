<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useModelsStore } from '../store/models.store'
import { storeToRefs } from 'pinia'
import { CloudDownload, Download, Loader2, Zap, CheckCircle2, Cpu, AlertTriangle } from '@lucide/vue'
import { ModelsService, type HFFile } from '../services/models.service'
import { HardwareService, type HardwareInfo } from '@/services/hardware.service'
import HuggingFaceSearch from '@/components/HuggingFaceSearch.vue'
import QuantizationSelector from '@/components/QuantizationSelector.vue'
import { useI18n } from 'vue-i18n'
import { useToast } from '@/composables/useToast'

const { t } = useI18n()
const store = useModelsStore()
const { isDownloading, downloadProgress, downloadSpeed, downloadEta, downloadStatusText, downloadedSize, totalSize } = storeToRefs(store)
const toast = useToast()

const selectedRepo = ref<string>('')
const ggufFiles = ref<HFFile[]>([])
const isLoadingFiles = ref(false)
const selectedFile = ref<HFFile | null>(null)

const hardwareInfo = ref<HardwareInfo | null>(null)

const searchRef = ref<InstanceType<typeof HuggingFaceSearch> | null>(null)
const quantSelectorRef = ref<InstanceType<typeof QuantizationSelector> | null>(null)

onMounted(async () => {
  try {
    hardwareInfo.value = await HardwareService.getHardwareInfo()
  } catch (e) {
    console.error(e)
  }
})

const onRepoSelected = async (repoId: string) => {
  selectedRepo.value = repoId
  isLoadingFiles.value = true
  ggufFiles.value = []
  selectedFile.value = null

  try {
    ggufFiles.value = await ModelsService.getHFModelFiles(repoId)
    if (ggufFiles.value.length > 0) {
      const defaultQ4 = ggufFiles.value.find(f => f.path.toLowerCase().includes('q4_k_m'))
      const fileToSelect = defaultQ4 || ggufFiles.value[0]
      selectedFile.value = fileToSelect
      if (quantSelectorRef.value) {
        quantSelectorRef.value.selectFile(fileToSelect)
      }
    }
  } catch (e) {
    console.error(e)
  } finally {
    isLoadingFiles.value = false
  }
}

const onSearchCleared = () => {
  selectedRepo.value = ''
  ggufFiles.value = []
  selectedFile.value = null
  if (quantSelectorRef.value) {
    quantSelectorRef.value.clearSelection()
  }
}

const onFileSelected = (file: HFFile) => {
  selectedFile.value = file
}

const handleDownload = async () => {
  if (!selectedRepo.value || !selectedFile.value) return

  try {
    const filename = selectedFile.value.path.split('/').pop() || selectedFile.value.path
    await store.downloadModel(selectedRepo.value, filename)
    toast.success(t('models.downloadStarted'))
    if (searchRef.value) searchRef.value.clearSearch()
    onSearchCleared()
  } catch (err) {
    console.error('Error starting download', err)
    toast.error(t('models.downloadError'))
  }
}

const getIconForStatus = (tier: string) => {
  switch (tier) {
    case 'RUNS WELL': return Zap
    case 'DECENT': return CheckCircle2
    case 'TIGHT FIT': return Cpu
    case 'BARELY RUNS': return AlertTriangle
    case 'TOO HEAVY': return AlertTriangle
    default: return Zap
  }
}
</script>

<template>
  <div class="glass p-6 rounded-3xl relative group border border-outline shadow-sm flex flex-col gap-5">
    <div class="relative z-10">
      <div class="flex items-center gap-2 mb-2">
        <CloudDownload class="text-primary w-6 h-6" />
        <h3 class="font-headline text-2xl text-on-surface font-semibold tracking-tight">{{ t('models.downloadTitle') }}
        </h3>
      </div>
      <p class="text-on-surface-variant text-sm font-body mb-6">{{ t('models.downloadDescription') }}</p>

      <div class="flex flex-col lg:flex-row gap-6">

        <!-- Left Side: Search and Select -->
        <div class="flex-1 space-y-5">
          <HuggingFaceSearch ref="searchRef" :disabled="isDownloading" @select="onRepoSelected"
            @clear="onSearchCleared" />

          <QuantizationSelector v-if="selectedRepo" ref="quantSelectorRef" :files="ggufFiles"
            :hardware-info="hardwareInfo" :is-loading="isLoadingFiles" :disabled="isDownloading"
            @select="onFileSelected" />
        </div>

        <!-- Right Side: Hardware Compatibility & Action -->
        <div class="flex-1 flex flex-col justify-end gap-5 lg:min-w-[300px]">

          <!-- Compatibility Card -->
          <div v-if="quantSelectorRef?.hardwareStatus"
            class="rounded-2xl p-4 border transition-all animate-fade-in flex flex-col gap-2"
            :class="[quantSelectorRef.hardwareStatus.bg, quantSelectorRef.hardwareStatus.color.replace('text-', 'border-') + '/30']">
            <div class="flex items-center gap-2">
              <component :is="getIconForStatus(quantSelectorRef.hardwareStatus.tier)" class="w-5 h-5"
                :class="quantSelectorRef.hardwareStatus.color" />
              <h4 class="font-headline font-semibold text-sm" :class="quantSelectorRef.hardwareStatus.color">{{
                t('models.compatibilityTitle', { tier: '' }) }} {{ quantSelectorRef.hardwareStatus.tier }}</h4>
            </div>
            <div
              class="flex items-center justify-between mt-1 bg-surface-container-low/50 p-2.5 rounded-xl border border-outline/30">
              <span class="text-xs text-on-surface-variant font-medium">{{ t('models.estSpeed') }}</span>
              <span class="text-sm font-bold" :class="quantSelectorRef.hardwareStatus.color">{{
                quantSelectorRef.hardwareStatus.speed }}</span>
            </div>
            <p class="text-xs text-on-surface opacity-90 mt-1 leading-relaxed">{{ quantSelectorRef.hardwareStatus.desc
            }}</p>
          </div>

          <div v-else
            class="rounded-2xl p-4 border border-outline/50 bg-surface-container-low/50 flex items-center justify-center min-h-[110px] text-center">
            <p class="text-xs text-on-surface-variant opacity-70">{{ t('models.selectModelToView') }}</p>
          </div>

          <!-- Progress UI -->
          <div v-if="isDownloading"
            class="w-full bg-surface-container-low border border-outline rounded-xl p-4 flex flex-col gap-3 shadow-inner animate-fade-in relative overflow-hidden">
            <!-- Subtle animated background gradient -->
            <div
              class="absolute inset-0 bg-linear-to-r from-transparent via-primary/5 to-transparent -translate-x-full animate-[shimmer_2s_infinite]">
            </div>

            <div class="flex justify-between items-center mb-1 relative z-10">
              <span class="text-xs font-bold text-primary flex items-center gap-2">
                <Loader2 class="w-3.5 h-3.5 animate-spin" />
                {{ downloadStatusText }}
              </span>
              <span
                class="text-xs font-mono text-on-surface-variant bg-surface-container px-2 py-0.5 rounded-md border border-outline/50 shadow-sm">{{
                  downloadProgress }}%</span>
            </div>

            <div
              class="w-full bg-surface-container-high rounded-full h-2.5 overflow-hidden border border-outline/30 relative z-10">
              <div
                class="bg-linear-to-r from-primary to-primary/70 h-2.5 rounded-full transition-all duration-300 ease-out shadow-[0_0_10px_rgba(var(--color-primary),0.4)]"
                :style="{ width: `${downloadProgress}%` }"></div>
            </div>

            <div
              class="flex justify-between items-center text-[10px] text-on-surface-variant font-medium mt-1 relative z-10">
              <div class="flex items-center gap-2">
                <span v-if="downloadedSize"
                  class="bg-surface-container-high px-1.5 py-0.5 rounded border border-outline/30">{{ downloadedSize }}
                  / {{ totalSize || '?' }}</span>
                <span v-if="downloadSpeed" class="text-primary/80 flex items-center gap-1 font-mono tracking-tight">
                  <Zap class="w-2.5 h-2.5" />{{ downloadSpeed }}
                </span>
              </div>
              <span v-if="downloadEta"
                class="font-mono bg-surface-container-high px-1.5 py-0.5 rounded border border-outline/30 opacity-90">ETA
                {{ downloadEta }}</span>
            </div>
          </div>

          <!-- Download Button -->
          <button v-else @click="handleDownload" :disabled="!selectedFile"
            class="w-full bg-primary hover:bg-primary/90 text-on-primary py-3.5 rounded-xl font-bold flex items-center justify-center gap-2 transition-all active:scale-[0.98] shadow-lg shadow-primary/20 disabled:opacity-50 disabled:active:scale-100 disabled:shadow-none text-sm tracking-wide">
            <Download class="w-[18px] h-[18px]" />
            <span>{{ t('models.downloadModel') }}</span>
          </button>
        </div>
      </div>
    </div>
  </div>
</template>
