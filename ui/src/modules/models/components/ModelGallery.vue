<script setup lang="ts">
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import type { LocalModel } from '../services/models.service'
import type { CommandConfig } from '../../settings/services/settings.service'
import { SettingsService } from '../../settings/services/settings.service'
import { useI18n } from 'vue-i18n'
import { useToast } from '@/composables/useToast'
import { Cpu, Database, Settings, Play } from '@lucide/vue'
import Model1 from '@/assets/img/model-1.png'
import Model2 from '@/assets/img/model-2.png'
import Model3 from '@/assets/img/model-3.png'

const { t } = useI18n()
const props = defineProps<{
  models: LocalModel[]
  isListView: boolean
  commands: CommandConfig[]
}>()

const router = useRouter()
const { success, error: toastError } = useToast()

/** Set of model filenames currently running (for badge state) */
const runningModels = ref<Set<string>>(new Set())

const isVisionEncoder = (model: LocalModel): boolean => {
  return model.filename.toLowerCase().includes('mmproj')
}

const modelImages = [Model1, Model2, Model3]

const getModelImage = (filename: string) => {
  let hash = 0
  for (let i = 0; i < filename.length; i++) {
    hash = filename.charCodeAt(i) + ((hash << 5) - hash)
  }
  return modelImages[Math.abs(hash) % modelImages.length]
}

const getCommandForModel = (model: LocalModel): CommandConfig | undefined => {
  return props.commands.find(cmd =>
    cmd.model_path && cmd.model_path.replace(/\\/g, '/').endsWith(model.filename)
  )
}

const goToSettings = (model: LocalModel) => {
  router.push({ name: 'settings', query: { model: model.filename } })
}

const runModel = async (model: LocalModel) => {
  const cmd = getCommandForModel(model)
  if (!cmd) return

  runningModels.value.add(model.filename)
  try {
    const res = await SettingsService.runCommand(cmd.filename)
    if (res.status === 'started') {
      success(`Model "${cmd.alias || model.filename}" started successfully.`)
    } else {
      toastError(res.message || 'Failed to start model.')
      runningModels.value.delete(model.filename)
    }
  } catch (err: any) {
    toastError(err?.response?.data?.detail || 'Error starting model.')
    runningModels.value.delete(model.filename)
  }

  // Auto-clear "running" badge after 8 seconds
  setTimeout(() => {
    runningModels.value.delete(model.filename)
  }, 8000)
}
</script>

<template>
  <div v-if="models.length === 0"
    class="text-on-surface-variant py-8 text-center text-sm border border-dashed border-outline rounded-xl">
    {{ t('models.noModelsFound') }}
  </div>

  <!-- Grid View -->
  <div v-else-if="!isListView" class="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-3 gap-5">
    <!-- Model Card -->
    <div v-for="model in models" :key="model.path"
      class="glass group cursor-pointer hover:border-primary/50 border border-outline transition-all duration-300 rounded-2xl overflow-hidden flex flex-col">
      <div class="h-28 bg-surface-container-high relative overflow-hidden flex items-center justify-center">
        <component v-if="isVisionEncoder(model)" :is="Cpu"
          class="w-12 h-12 text-outline opacity-30 group-hover:opacity-50 transition-opacity group-hover:scale-110 duration-500" />
        <img v-else :src="getModelImage(model.filename)"
          class="w-full h-full object-cover opacity-60 group-hover:opacity-80 transition-opacity group-hover:scale-110 duration-500" />
        <div class="absolute top-3 right-3 z-10">
          <span v-if="runningModels.has(model.filename)"
            class="bg-blue-500/10 text-blue-400 text-[10px] font-bold px-2 py-0.5 rounded border border-blue-500/20 flex items-center gap-1 animate-pulse">
            <span class="w-1 h-1 rounded-full bg-blue-400"></span> {{ t('models.running') }}
          </span>
          <span v-else
            class="bg-green-500/10 text-green-500 text-[10px] font-bold px-2 py-0.5 rounded border border-green-500/20 flex items-center gap-1">
            <span class="w-1 h-1 rounded-full bg-green-500"></span> {{ t('models.ready') }}
          </span>
        </div>
      </div>
      <div class="p-4 flex-1 flex flex-col">
        <div class="flex justify-between items-start mb-3 gap-3">
          <div class="flex-1 min-w-0">
            <h4 class="font-headline text-base text-on-surface font-semibold truncate" :title="model.filename">{{
              model.filename }}</h4>
            <span class="text-xs text-on-surface-variant truncate block" :title="model.author">{{ t('models.by', {
              author: model.author || t('models.local') }) }}</span>
          </div>
          <span v-if="isVisionEncoder(model)"
            class="font-label text-[10px] text-purple-400 bg-purple-500/10 border border-purple-500/20 px-1.5 py-0.5 rounded shrink-0">MMPROJ</span>
          <span v-else
            class="font-label text-[10px] text-primary bg-primary-container/20 px-1.5 py-0.5 rounded shrink-0">{{
              model.filename.split('.').pop()?.toUpperCase() || 'GGUF' }}</span>
        </div>
        <div class="flex items-center justify-between mt-auto pt-3 border-t border-outline/50">
          <div class="flex items-center gap-1.5 text-on-surface-variant">
            <Database class="w-4 h-4" />
            <span class="text-xs">{{ model.size_mb }} MB</span>
          </div>
          <div class="flex gap-2">
            <button v-if="!isVisionEncoder(model) && getCommandForModel(model)" @click.stop="runModel(model)"
              class="p-1.5 rounded-full hover:bg-green-500/10 text-on-surface-variant hover:text-green-400 transition-colors"
              :title="t('models.runModelTitle')">
              <Play class="w-[18px] h-[18px]" />
            </button>
            <button v-if="!isVisionEncoder(model)" @click.stop="goToSettings(model)"
              class="p-1.5 rounded-full hover:bg-surface-container-high text-on-surface-variant hover:text-primary transition-colors">
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

      <div
        class="w-12 h-12 rounded-lg bg-surface-container-high flex items-center justify-center shrink-0 overflow-hidden">
        <component v-if="isVisionEncoder(model)" :is="Cpu"
          class="w-6 h-6 text-outline opacity-60 group-hover:opacity-100 transition-opacity" />
        <img v-else :src="getModelImage(model.filename)"
          class="w-full h-full object-cover opacity-60 group-hover:opacity-100 transition-opacity" />
      </div>

      <div class="flex-1 min-w-0 grid grid-cols-12 gap-4 items-center">
        <div class="col-span-12 md:col-span-5 flex flex-col">
          <h4 class="font-headline text-sm text-on-surface font-semibold truncate" :title="model.filename">{{
            model.filename }}</h4>
          <span class="text-xs text-on-surface-variant truncate block" :title="model.author">{{ t('models.by', {
            author:
              model.author || t('models.local') }) }}</span>
        </div>

        <div class="hidden md:flex col-span-3 items-center gap-1.5 text-on-surface-variant">
          <Database class="w-4 h-4" />
          <span class="text-xs">{{ model.size_mb }} MB</span>
        </div>

        <div class="hidden md:flex col-span-2 items-center">
          <span v-if="isVisionEncoder(model)"
            class="font-label text-[10px] text-purple-400 bg-purple-500/10 border border-purple-500/20 px-2 py-1 rounded shrink-0">MMPROJ</span>
          <span v-else class="font-label text-[10px] text-primary bg-primary-container/20 px-2 py-1 rounded shrink-0">{{
            model.filename.split('.').pop()?.toUpperCase() || 'GGUF' }}</span>
        </div>

        <div class="hidden md:flex col-span-2 items-center justify-end gap-2">
          <span v-if="runningModels.has(model.filename)"
            class="bg-blue-500/10 text-blue-400 text-[10px] font-bold px-2 py-1 rounded border border-blue-500/20 flex items-center gap-1 animate-pulse">
            <span class="w-1 h-1 rounded-full bg-blue-400"></span> {{ t('models.running') }}
          </span>
          <span v-else
            class="bg-green-500/10 text-green-500 text-[10px] font-bold px-2 py-1 rounded border border-green-500/20 flex items-center gap-1">
            <span class="w-1 h-1 rounded-full bg-green-500"></span> {{ t('models.ready') }}
          </span>
          <button v-if="!isVisionEncoder(model) && getCommandForModel(model)" @click.stop="runModel(model)"
            class="p-1.5 rounded-full hover:bg-green-500/10 text-on-surface-variant hover:text-green-400 transition-colors"
            :title="t('models.runModelTitle')">
            <Play class="w-[18px] h-[18px]" />
          </button>
          <button v-if="!isVisionEncoder(model)" @click.stop="goToSettings(model)"
            class="p-1.5 rounded-full hover:bg-surface-container-high text-on-surface-variant hover:text-primary transition-colors">
            <Settings class="w-[18px] h-[18px]" />
          </button>
        </div>
      </div>
    </div>
  </div>
</template>
