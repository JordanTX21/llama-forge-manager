<script setup lang="ts">
import { ref, onMounted, onUnmounted, computed } from 'vue'
import { Database, ChevronDown, Loader2 } from '@lucide/vue'
import { ModelsService, type HFFile } from '@/modules/models/services/models.service'
import type { HardwareInfo } from '@/services/hardware.service'

const props = defineProps<{
  files: HFFile[]
  hardwareInfo: HardwareInfo | null
  isLoading: boolean
  disabled?: boolean
}>()

const emit = defineEmits<{
  (e: 'select', file: HFFile): void
}>()

const showFileDropdown = ref(false)
const selectedFile = ref<HFFile | null>(null)
const fileContainerRef = ref<HTMLElement | null>(null)

const handleClickOutside = (event: MouseEvent) => {
  if (fileContainerRef.value && !fileContainerRef.value.contains(event.target as Node)) {
    showFileDropdown.value = false
  }
}

onMounted(() => document.addEventListener('click', handleClickOutside))
onUnmounted(() => document.removeEventListener('click', handleClickOutside))

const selectFile = (file: HFFile) => {
  selectedFile.value = file
  showFileDropdown.value = false
  emit('select', file)
}

const clearSelection = () => {
  selectedFile.value = null
  showFileDropdown.value = false
}

const isVisionEncoder = (filename: string) => {
  return filename.toLowerCase().includes('mmproj') || filename.toLowerCase().includes('vision')
}

const extractQuant = (filename: string) => {
  if (isVisionEncoder(filename)) return 'VISION'
  const match = filename.match(/Q[0-9]_[K0-9]_[A-Z]/i) || filename.match(/Q[0-9]_[0-9]/i)
  return match ? match[0] : 'GGUF'
}

const hardwareStatus = computed(() => ModelsService.getFileStats(selectedFile.value, props.hardwareInfo))

const getStats = (file: HFFile) => ModelsService.getFileStats(file, props.hardwareInfo)

defineExpose({ clearSelection, selectFile, hardwareStatus })
</script>

<template>
  <div class="animate-fade-in" ref="fileContainerRef">
    <label
      class="font-label text-xs text-on-surface-variant uppercase tracking-wider ml-1 mb-1 flex items-center gap-2">
      <Database class="w-3 h-3" /> Select Quantization (GGUF)
    </label>
    <div class="relative">
      <button @click="showFileDropdown = !showFileDropdown" :disabled="isLoading || files.length === 0 || disabled"
        class="w-full bg-surface-container-low border border-outline px-4 py-3 rounded-xl text-sm text-on-surface transition-all hover:border-primary/50 focus:outline-none focus:border-primary shadow-inner disabled:opacity-50 flex items-center justify-between text-left">

        <span v-if="isLoading">Loading files...</span>
        <span v-else-if="files.length === 0">No GGUF files found in this repo.</span>
        <span v-else-if="selectedFile" class="truncate pr-4 font-medium">{{ selectedFile.path.split('/').pop() }}</span>
        <span v-else>Select a file...</span>

        <Loader2 v-if="isLoading" class="w-4 h-4 text-primary animate-spin" />
        <ChevronDown v-else class="w-4 h-4 text-on-surface-variant" />
      </button>

      <!-- Rich Dropdown -->
      <div v-if="showFileDropdown && files.length > 0"
        class="absolute z-50 w-full left-0 mt-2 bg-[#101010] border border-outline/50 rounded-xl shadow-2xl overflow-hidden max-h-80 overflow-y-auto animate-fade-in">
        <button v-for="file in files" :key="file.path" @click="selectFile(file)"
          class="w-full text-left px-3 py-3 hover:bg-[#1a1a1a] transition-colors border-b border-outline/20 last:border-0 flex flex-col gap-1.5 group">

          <div class="flex items-center justify-between w-full">
            <div class="flex items-center gap-2 overflow-hidden w-full">
              <span
                class="text-xs font-semibold text-gray-200 truncate group-hover:text-primary transition-colors flex-1">{{
                  file.path.split('/').pop() }}</span>
              <span class="text-[9px] uppercase font-bold px-1 py-0.5 rounded border whitespace-nowrap"
                :class="isVisionEncoder(file.path) ? 'border-purple-500/30 text-purple-400 bg-purple-500/10' : 'border-primary/30 text-primary bg-primary/5'">
                {{ extractQuant(file.path) }}
              </span>
            </div>
          </div>

          <div class="flex items-center gap-2 text-[10px] font-mono justify-between">
            <span class="text-gray-400 whitespace-nowrap">{{ (file.size / (1024 ** 3)).toFixed(1) }} GB <span
                class="text-green-500/80 font-bold ml-0.5">{{ getStats(file)?.ramPercentage }}%</span></span>

            <span class="text-yellow-500/80 whitespace-nowrap text-center">{{ getStats(file)?.speed }}</span>

            <span class="font-bold tracking-wider whitespace-nowrap text-right" :class="getStats(file)?.color">
              {{ getStats(file)?.tier }} <span class="opacity-70 font-sans font-normal">{{ getStats(file)?.score
                }}</span>
            </span>
          </div>
        </button>
      </div>
    </div>
  </div>
</template>
