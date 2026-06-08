<script setup lang="ts">
import { ref, computed, onMounted, watch } from 'vue'
import { useRoute } from 'vue-router'
import { SettingsService, type CommandConfig } from '../services/settings.service'
import { useModelsStore } from '../../models/store/models.store'
import { storeToRefs } from 'pinia'
import { useCommandForm } from '../composables/useCommandForm'
import { useToast } from '@/composables/useToast'

import SettingsHero from '../components/SettingsHero.vue'
import SettingsBasicForm from '../components/SettingsBasicForm.vue'
import SettingsAdvancedForm from '../components/SettingsAdvancedForm.vue'
import SettingsCodeEditor from '../components/SettingsCodeEditor.vue'
import SmartConfigCard from '../components/SmartConfigCard.vue'
import AgentConfigModal from '@/components/AgentConfigModal.vue'
import { ChevronsUpDown, Terminal, Code, Asterisk, Save, Play } from '@lucide/vue'
import { useI18n } from 'vue-i18n'

const { t } = useI18n()
const modelsStore = useModelsStore()
const { models } = storeToRefs(modelsStore)

const commands = ref<CommandConfig[]>([])
const selectedCommandFilename = ref('')
const isCodeMode = ref(false)

const { setValues, resetForm, values, setFieldValue, handleSubmit } = useCommandForm()
const route = useRoute()
const { success, error: toastError } = useToast()
const isRunning = ref(false)
const showAgentModal = ref(false)
const agentModelName = ref('')
const pendingFormToRun = ref<Record<string, any> | null>(null)

// SmartConfig: derive model metadata from the currently selected model_path
const selectedModelMeta = computed(() => {
  const path = (values.model_path || '') as string
  if (!path) return { path: '', sizeMb: 0, filename: '' }
  const normalizedPath = path.replace(/\\/g, '/')
  const filename = normalizedPath.split('/').pop() || ''
  const model = models.value.find(m => m.path.replace(/\\/g, '/') === normalizedPath)
  return {
    path: normalizedPath,
    sizeMb: model ? model.size_mb : 0,
    filename
  }
})

const applySmartConfig = (config: Record<string, any>) => {
  for (const [key, val] of Object.entries(config)) {
    setFieldValue(key as any, val)
  }
  success(t('settings.recommendationApplied'))
}

const fetchCommands = async () => {
  try {
    const res = await SettingsService.getCommands()
    commands.value = res
  } catch (err) {
    console.error(err)
  }
}

const loadCommand = (config: CommandConfig) => {
  setValues(config)
}

watch(selectedCommandFilename, (newFilename) => {
  if (!newFilename) {
    resetForm()
    return
  }
  const cmd = commands.value.find(c => c.filename === newFilename)
  if (cmd) {
    loadCommand(cmd)
  }
})

/** Save configuration and return the filename on success, or null on failure. */
const saveConfig = async (formValues: Record<string, any>): Promise<string | null> => {
  try {
    const payload = (isCodeMode.value ? { raw_content: formValues.raw_content } : formValues) as CommandConfig
    await SettingsService.saveCommand(payload)
    await fetchCommands()
    return payload.filename.endsWith('.ps1') ? payload.filename : payload.filename + '.ps1'
  } catch (err: any) {
    console.error(err)
    if (err.response?.status === 400 && err.response.data?.detail) {
      toastError(t('settings.syntaxError', { detail: err.response.data.detail }))
    } else {
      toastError(t('settings.errorSaving'))
    }
    return null
  }
}

// handleSubmit will automatically validate using Yup schema before executing this function
const onSubmit = handleSubmit(async (formValues: Record<string, any>) => {
  const filename = await saveConfig(formValues)
  if (filename) {
    success(t('settings.configSaved'))
  }
})

/** Save + Run: auto-saves the form, then executes the .ps1 script */
const onRun = handleSubmit(async (formValues: Record<string, any>) => {
  const dontAsk = localStorage.getItem('agents_dont_ask')
  if (dontAsk !== 'true') {
    pendingFormToRun.value = formValues
    const actualModelPath = (formValues.model_path as string || '').replace(/\\/g, '/')
    const fallbackName = actualModelPath.split('/').pop() || formValues.filename || 'model'
    agentModelName.value = formValues.alias || fallbackName.replace('.gguf', '')
    showAgentModal.value = true
  } else {
    executeRunCommand(formValues)
  }
})

const executeRunCommand = async (formValues: Record<string, any>) => {
  isRunning.value = true
  const filename = await saveConfig(formValues)
  if (!filename) {
    isRunning.value = false
    return
  }

  try {
    const res = await SettingsService.runCommand(filename)
    if (res.status === 'started') {
      success(t('settings.modelStarted', { alias: formValues.alias || filename }))
    } else {
      toastError(res.message || t('settings.failedToStart'))
    }
  } catch (err: any) {
    toastError(err?.response?.data?.detail || t('settings.errorStarting'))
  } finally {
    isRunning.value = false
  }
}

const onModalComplete = () => {
  if (pendingFormToRun.value) {
    executeRunCommand(pendingFormToRun.value)
    pendingFormToRun.value = null
  }
}

onMounted(async () => {
  await fetchCommands()
  if (models.value.length === 0) {
    await modelsStore.fetchModels()
  }

  const modelQuery = route.query.model as string
  if (modelQuery) {
    const cmd = commands.value.find(c => c.model_path && c.model_path.replace(/\\/g, '/').endsWith(modelQuery))
    if (cmd) {
      selectedCommandFilename.value = cmd.filename
    } else {
      resetForm()
      const modelObj = models.value.find(m => m.filename === modelQuery)
      if (modelObj) {
        setFieldValue('model_path', modelObj.path.replace(/\\/g, '/'))
        setFieldValue('filename', modelObj.filename.replace('.gguf', '') + '.ps1')
        setFieldValue('alias', modelObj.filename.replace('.gguf', ''))
      }
    }
  }
})
</script>

<template>
  <div class="space-y-8 w-full max-w-[1200px] mx-auto pb-12">
    <!-- Header Section -->
    <header class="hidden md:block">
      <h2 class="font-headline text-3xl text-on-surface mb-1 font-semibold tracking-tight">{{ t('settings.title') }}</h2>
      <p class="text-on-surface-variant font-body text-sm">{{ t('settings.description') }}</p>
    </header>

    <div class="grid grid-cols-1 xl:grid-cols-12 gap-8">

      <!-- Left Column -->
      <div class="xl:col-span-4 space-y-6">

        <SettingsHero />

        <div class="glass p-5 rounded-2xl border border-outline shadow-sm">
          <h3 class="font-headline text-lg font-semibold mb-4 text-on-surface">{{ t('settings.loadCommand') }}</h3>
          <div class="relative">
            <select v-model="selectedCommandFilename"
              class="w-full bg-surface-container-low border border-outline rounded-xl p-3.5 text-sm appearance-none focus:outline-none focus:border-primary transition-colors text-on-surface shadow-inner">
              <option value="">{{ t('settings.newCommand') }}</option>
              <option v-for="cmd in commands" :key="cmd.filename" :value="cmd.filename">
                {{ cmd.filename }}
              </option>
            </select>
            <ChevronsUpDown class="absolute right-3 top-3.5 pointer-events-none text-on-surface-variant w-4 h-4" />
          </div>
          <p class="text-xs text-on-surface-variant mt-2 px-1">{{ t('settings.selectPreset') }}</p>
        </div>

        <SmartConfigCard
          :model-path="selectedModelMeta.path"
          :model-size-mb="selectedModelMeta.sizeMb"
          :model-filename="selectedModelMeta.filename"
          @apply="applySmartConfig"
        />
      </div>

      <!-- Right Column: Form -->
      <div class="xl:col-span-8">
        <!-- We use form with handleSubmit from useCommandForm instead of Form component -->
        <form @submit="onSubmit" class="glass p-6 rounded-3xl border border-outline shadow-sm relative overflow-hidden">
          <div class="flex items-center justify-between mb-6 pb-4 border-b border-outline/50">
            <div>
              <h3 class="font-headline text-xl font-semibold text-on-surface flex items-center gap-2">
                <Terminal class="text-primary w-5 h-5" />
                {{ t('settings.commandParameters') }}
              </h3>
              <p class="text-xs text-on-surface-variant mt-1">{{ t('settings.configArgs') }}</p>
            </div>

            <!-- Code Mode Toggle -->
            <div class="flex items-center gap-3 bg-surface-container-low px-3 py-1.5 rounded-lg border border-outline">
              <span class="text-xs font-label text-on-surface-variant"
                :class="{ 'text-primary': !isCodeMode }">{{ t('settings.form') }}</span>
              <label class="relative inline-flex items-center cursor-pointer">
                <input type="checkbox" v-model="isCodeMode" class="sr-only peer" />
                <div
                  class="w-8 h-4 bg-surface-variant peer-focus:outline-none rounded-full peer peer-checked:after:translate-x-full peer-checked:after:border-white after:content-[''] after:absolute after:top-[2px] after:left-[2px] after:bg-white after:border-gray-300 after:border after:rounded-full after:h-3 after:w-3 after:transition-all peer-checked:bg-primary transition-colors">
                </div>
              </label>
              <span class="text-xs font-label text-on-surface-variant flex items-center gap-1"
                :class="{ 'text-primary font-bold': isCodeMode }">
                <Code class="w-[14px] h-[14px]" />
                {{ t('settings.code') }}
              </span>
            </div>
          </div>

          <div class="space-y-6">
            <!-- Form Mode -->
            <div v-show="!isCodeMode" class="space-y-6 animate-fade-in">
              <div class="space-y-1">
                <label
                  class="flex items-center gap-1 font-label text-xs text-on-surface-variant uppercase tracking-wider ml-1">
                  {{ t('settings.configFilename') }}
                  <Asterisk class="text-red-400 w-[14px] h-[14px]"
                    title="Nombre del archivo final que se guardará (ej. my-model.ps1). Requerido." />
                </label>
                <!-- Using Field explicitly imported from vee-validate is done in child components, but here we can just use regular inputs with v-model or import Field here too -->
                <input :value="values.filename"
                  @input="e => setFieldValue('filename', (e.target as HTMLInputElement).value)" type="text"
                  class="w-full bg-surface-container-low border border-outline rounded-xl p-3.5 text-sm focus:outline-none focus:border-primary transition-colors text-on-surface"
                  placeholder="my-model.ps1" required />
              </div>

              <SettingsBasicForm :models="models" />
              <SettingsAdvancedForm />
            </div>

            <!-- Code Mode -->
            <div v-if="isCodeMode">
              <div class="space-y-1 mb-4">
                <label
                  class="flex items-center gap-1 font-label text-xs text-on-surface-variant uppercase tracking-wider ml-1">
                  {{ t('settings.configFilename') }}
                </label>
                <input :value="values.filename"
                  @input="e => setFieldValue('filename', (e.target as HTMLInputElement).value)" type="text"
                  class="w-full bg-surface-container-low border border-outline rounded-xl p-3.5 text-sm focus:outline-none focus:border-primary transition-colors text-on-surface"
                  placeholder="my-model.ps1" required />
              </div>
              <SettingsCodeEditor />
            </div>

          </div>

          <div class="mt-8 pt-5 border-t border-outline flex items-center justify-end gap-3 relative z-10">
            <button type="button" @click="resetForm()"
              class="px-5 py-2.5 rounded-xl font-semibold text-sm text-on-surface-variant hover:bg-surface-container-high transition-colors">
              {{ t('settings.reset') }}
            </button>
            <button v-if="selectedCommandFilename" type="button" @click="onRun" :disabled="isRunning"
              class="bg-green-600 hover:bg-green-500 text-white px-5 py-2.5 rounded-xl font-semibold flex items-center gap-2 transition-all shadow-lg shadow-green-600/20 active:scale-95 text-sm disabled:opacity-50 disabled:cursor-not-allowed">
              <Play class="w-[18px] h-[18px]" />
              {{ isRunning ? t('settings.starting') : t('settings.saveRun') }}
            </button>
            <button type="submit"
              class="bg-primary hover:bg-primary/90 text-on-primary px-6 py-2.5 rounded-xl font-semibold flex items-center gap-2 transition-all shadow-lg shadow-primary/20 active:scale-95 text-sm">
              <Save class="w-[18px] h-[18px]" />
              {{ t('settings.saveConfig') }}
            </button>
          </div>
        </form>
      </div>

    </div>

    <AgentConfigModal v-model="showAgentModal" :modelName="agentModelName" @configured="onModalComplete" @skipped="onModalComplete" />
  </div>
</template>
