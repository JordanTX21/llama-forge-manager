<script setup lang="ts">
import { ref, watch, onMounted, onUnmounted } from 'vue'
import { Search, Loader2, X } from '@lucide/vue'
import { ModelsService, type HFModel } from '@/modules/models/services/models.service'

defineProps<{
  disabled?: boolean
}>()

const emit = defineEmits<{
  (e: 'select', repoId: string): void
  (e: 'clear'): void
}>()

const searchQuery = ref('')
const searchResults = ref<HFModel[]>([])
const isSearching = ref(false)
const showDropdown = ref(false)

const searchContainerRef = ref<HTMLElement | null>(null)

const handleClickOutside = (event: MouseEvent) => {
  if (searchContainerRef.value && !searchContainerRef.value.contains(event.target as Node)) {
    showDropdown.value = false
  }
}

onMounted(() => document.addEventListener('click', handleClickOutside))
onUnmounted(() => document.removeEventListener('click', handleClickOutside))

let debounceTimer: any = null
watch(searchQuery, (newVal) => {
  clearTimeout(debounceTimer)

  if (!newVal || newVal.length < 3) {
    searchResults.value = []
    showDropdown.value = false
    return
  }

  isSearching.value = true
  showDropdown.value = true
  debounceTimer = setTimeout(async () => {
    try {
      searchResults.value = await ModelsService.searchHFModels(newVal)
    } catch (e) {
      console.error(e)
    } finally {
      isSearching.value = false
    }
  }, 500)
})

const selectRepo = (repoId: string) => {
  searchQuery.value = repoId
  showDropdown.value = false
  searchResults.value = []
  emit('select', repoId)
}

const clearSearch = () => {
  searchQuery.value = ''
  searchResults.value = []
  showDropdown.value = false
  emit('clear')
}

defineExpose({ clearSearch })
</script>

<template>
  <div class="relative" ref="searchContainerRef">
    <label class="font-label text-xs text-on-surface-variant uppercase tracking-wider ml-1 mb-1 block">Search Hugging
      Face</label>
    <div class="relative flex items-center">
      <Search class="absolute left-3 w-4 h-4 text-on-surface-variant pointer-events-none" />
      <input v-model="searchQuery" @focus="showDropdown = true" :disabled="disabled"
        class="w-full bg-surface-container-low border border-outline pl-10 pr-16 py-3 rounded-xl text-sm text-on-surface transition-all placeholder:text-outline/70 focus:outline-none focus:border-primary shadow-inner disabled:opacity-50"
        placeholder="e.g. Llama-3-8B-Instruct" type="text" autocomplete="off" />

      <div class="absolute right-3 flex items-center gap-1">
        <Loader2 v-if="isSearching" class="w-4 h-4 text-primary animate-spin" />
        <button v-if="searchQuery" @click.stop="clearSearch"
          class="p-1.5 rounded-full hover:bg-surface-variant transition-colors text-on-surface-variant hover:text-on-surface group/clear">
          <X class="w-4 h-4 group-hover/clear:scale-110 transition-transform" />
        </button>
      </div>
    </div>

    <div v-if="showDropdown && searchResults.length > 0"
      class="absolute z-50 w-full mt-2 bg-surface-container-high border border-outline rounded-xl shadow-2xl overflow-hidden max-h-60 overflow-y-auto animate-fade-in">
      <button v-for="res in searchResults" :key="res.id" @click="selectRepo(res.id)"
        class="w-full text-left px-4 py-3 hover:bg-surface-container-highest transition-colors border-b border-outline/30 last:border-0 flex items-center justify-between group">
        <span class="text-sm font-medium text-on-surface truncate pr-4">{{ res.id }}</span>
        <span
          class="text-xs text-on-surface-variant bg-surface-container-low px-2 py-0.5 rounded-md group-hover:bg-primary/10 group-hover:text-primary transition-colors">{{
            (res.downloads / 1000).toFixed(1) }}k dl</span>
      </button>
    </div>
    <div v-else-if="showDropdown && searchQuery.length >= 3 && !isSearching"
      class="absolute z-50 w-full mt-2 bg-surface-container-high border border-outline rounded-xl shadow-2xl p-4 text-center text-sm text-on-surface-variant">
      No GGUF models found.
    </div>
  </div>
</template>
