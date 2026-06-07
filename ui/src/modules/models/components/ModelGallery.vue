<script setup lang="ts">
import type { LocalModel } from '../services/models.service'
import { Cpu, Database, Settings } from '@lucide/vue'

defineProps<{
  models: LocalModel[]
  isListView: boolean
}>()
</script>

<template>
  <div v-if="models.length === 0"
    class="text-on-surface-variant py-8 text-center text-sm border border-dashed border-outline rounded-xl">
    No models found in local directory. Download one above.
  </div>

  <!-- Grid View -->
  <div v-else-if="!isListView" class="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-3 gap-5">
    <!-- Model Card -->
    <div v-for="model in models" :key="model.path"
      class="glass group cursor-pointer hover:border-primary/50 border border-outline transition-all duration-300 rounded-2xl overflow-hidden flex flex-col">
      <div class="h-28 bg-surface-container-high relative overflow-hidden flex items-center justify-center">
        <Cpu class="w-12 h-12 text-outline opacity-30 group-hover:opacity-50 transition-opacity group-hover:scale-110 duration-500" />
        <div class="absolute top-3 right-3 z-10">
          <span class="bg-green-500/10 text-green-500 text-[10px] font-bold px-2 py-0.5 rounded border border-green-500/20 flex items-center gap-1">
            <span class="w-1 h-1 rounded-full bg-green-500"></span> Ready
          </span>
        </div>
      </div>
      <div class="p-4 flex-1 flex flex-col">
        <div class="flex justify-between items-start mb-3 gap-3">
          <div class="flex-1 min-w-0">
            <h4 class="font-headline text-base text-on-surface font-semibold truncate" :title="model.filename">{{ model.filename }}</h4>
            <span class="text-xs text-on-surface-variant truncate block" :title="model.author">by {{ model.author || 'Local' }}</span>
          </div>
          <span class="font-label text-[10px] text-primary bg-primary-container/20 px-1.5 py-0.5 rounded shrink-0">{{ model.filename.split('.').pop()?.toUpperCase() || 'GGUF' }}</span>
        </div>
        <div class="flex items-center justify-between mt-auto pt-3 border-t border-outline/50">
          <div class="flex items-center gap-1.5 text-on-surface-variant">
            <Database class="w-4 h-4" />
            <span class="text-xs">{{ model.size_mb }} MB</span>
          </div>
          <div class="flex gap-2">
            <button class="p-1.5 rounded-full hover:bg-surface-container-high text-on-surface-variant hover:text-primary transition-colors">
              <Settings class="w-[18px] h-[18px]" />
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>

  <!-- List View -->
  <div v-else class="flex flex-col gap-3">
    <div v-for="model in models" :key="model.path"
      class="glass group cursor-pointer hover:border-primary/50 border border-outline transition-all duration-300 rounded-xl overflow-hidden flex items-center p-3 gap-4">
      
      <div class="w-12 h-12 rounded-lg bg-surface-container-high flex items-center justify-center shrink-0">
        <Cpu class="w-6 h-6 text-outline opacity-60 group-hover:opacity-100 transition-opacity" />
      </div>

      <div class="flex-1 min-w-0 grid grid-cols-12 gap-4 items-center">
        <div class="col-span-12 md:col-span-5 flex flex-col">
          <h4 class="font-headline text-sm text-on-surface font-semibold truncate" :title="model.filename">{{ model.filename }}</h4>
          <span class="text-xs text-on-surface-variant truncate block" :title="model.author">by {{ model.author || 'Local' }}</span>
        </div>
        
        <div class="hidden md:flex col-span-3 items-center gap-1.5 text-on-surface-variant">
          <Database class="w-4 h-4" />
          <span class="text-xs">{{ model.size_mb }} MB</span>
        </div>

        <div class="hidden md:flex col-span-2 items-center">
          <span class="font-label text-[10px] text-primary bg-primary-container/20 px-2 py-1 rounded shrink-0">{{ model.filename.split('.').pop()?.toUpperCase() || 'GGUF' }}</span>
        </div>

        <div class="hidden md:flex col-span-2 items-center justify-end gap-2">
          <span class="bg-green-500/10 text-green-500 text-[10px] font-bold px-2 py-1 rounded border border-green-500/20 flex items-center gap-1">
            <span class="w-1 h-1 rounded-full bg-green-500"></span> Ready
          </span>
          <button class="p-1.5 rounded-full hover:bg-surface-container-high text-on-surface-variant hover:text-primary transition-colors">
            <Settings class="w-[18px] h-[18px]" />
          </button>
        </div>
      </div>
    </div>
  </div>
</template>
