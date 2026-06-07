<script setup lang="ts">
import { ref, onMounted, watch } from 'vue'
import { SettingsService, type CommandConfig } from '../services/settings.service'
import { useModelsStore } from '../../models/store/models.store'
import { storeToRefs } from 'pinia'
import { useCommandForm } from '../composables/useCommandForm'

import SettingsHero from '../components/SettingsHero.vue'
import SettingsBasicForm from '../components/SettingsBasicForm.vue'
import SettingsAdvancedForm from '../components/SettingsAdvancedForm.vue'
import SettingsCodeEditor from '../components/SettingsCodeEditor.vue'
import { ChevronsUpDown, Terminal, Code, Asterisk, Save } from '@lucide/vue'

// Import Form from vee-validate to wrap our fields
import { Form } from 'vee-validate'

const modelsStore = useModelsStore()
const { models } = storeToRefs(modelsStore)

const commands = ref<CommandConfig[]>([])
const selectedCommandFilename = ref('')
const isCodeMode = ref(false)

const { setValues, resetForm, values, setFieldValue } = useCommandForm()

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

// handleSubmit will automatically validate using Yup schema before executing this function
const onSubmit = async (formValues: Record<string, any>) => {
  try {
    // Determine whether we are saving raw code or form data
    const payload = (isCodeMode.value ? { raw_content: formValues.raw_content } : formValues) as CommandConfig

    await SettingsService.saveCommand(payload)
    alert('Configuración guardada exitosamente.')
    await fetchCommands()
  } catch (err: any) {
    console.error(err)
    if (err.response?.status === 400 && err.response.data?.detail) {
      alert(`Error de sintaxis: ${err.response.data.detail}`)
    } else {
      alert('Error al guardar configuración.')
    }
  }
}

onMounted(() => {
  fetchCommands()
  if (models.value.length === 0) {
    modelsStore.fetchModels()
  }
})
</script>

<template>
  <div class="space-y-8 w-full max-w-[1200px] mx-auto pb-12">
    <!-- Header Section -->
    <header class="hidden md:block">
      <h2 class="font-headline text-3xl text-on-surface mb-1 font-semibold tracking-tight">Inference Settings</h2>
      <p class="text-on-surface-variant font-body text-sm">Configure parameters for local model execution and llama-swap
        routing.</p>
    </header>

    <div class="grid grid-cols-1 xl:grid-cols-12 gap-8">

      <!-- Left Column -->
      <div class="xl:col-span-4 space-y-6">

        <SettingsHero />

        <div class="glass p-5 rounded-2xl border border-outline shadow-sm">
          <h3 class="font-headline text-lg font-semibold mb-4 text-on-surface">Load Command</h3>
          <div class="relative">
            <select v-model="selectedCommandFilename"
              class="w-full bg-surface-container-low border border-outline rounded-xl p-3.5 text-sm appearance-none focus:outline-none focus:border-primary transition-colors text-on-surface shadow-inner">
              <option value="">-- New Command --</option>
              <option v-for="cmd in commands" :key="cmd.filename" :value="cmd.filename">
                {{ cmd.filename }}
              </option>
            </select>
            <ChevronsUpDown class="absolute right-3 top-3.5 pointer-events-none text-on-surface-variant w-4 h-4" />
          </div>
          <p class="text-xs text-on-surface-variant mt-2 px-1">Select an existing preset or create a new one.</p>
        </div>
      </div>

      <!-- Right Column: Form -->
      <div class="xl:col-span-8">
        <!-- We use Form from vee-validate which provides form context to Fields -->
        <Form @submit="onSubmit" class="glass p-6 rounded-3xl border border-outline shadow-sm relative overflow-hidden"
          :initial-values="values">
          <div class="flex items-center justify-between mb-6 pb-4 border-b border-outline/50">
            <div>
              <h3 class="font-headline text-xl font-semibold text-on-surface flex items-center gap-2">
                <Terminal class="text-primary w-5 h-5" />
                Command Parameters
              </h3>
              <p class="text-xs text-on-surface-variant mt-1">Configure arguments for llama-server.exe</p>
            </div>

            <!-- Code Mode Toggle -->
            <div class="flex items-center gap-3 bg-surface-container-low px-3 py-1.5 rounded-lg border border-outline">
              <span class="text-xs font-label text-on-surface-variant"
                :class="{ 'text-primary': !isCodeMode }">Form</span>
              <label class="relative inline-flex items-center cursor-pointer">
                <input type="checkbox" v-model="isCodeMode" class="sr-only peer" />
                <div
                  class="w-8 h-4 bg-surface-variant peer-focus:outline-none rounded-full peer peer-checked:after:translate-x-full peer-checked:after:border-white after:content-[''] after:absolute after:top-[2px] after:left-[2px] after:bg-white after:border-gray-300 after:border after:rounded-full after:h-3 after:w-3 after:transition-all peer-checked:bg-primary transition-colors">
                </div>
              </label>
              <span class="text-xs font-label text-on-surface-variant flex items-center gap-1"
                :class="{ 'text-primary font-bold': isCodeMode }">
                <Code class="w-[14px] h-[14px]" />
                Code
              </span>
            </div>
          </div>

          <div class="space-y-6">
            <!-- Form Mode -->
            <div v-show="!isCodeMode" class="space-y-6 animate-fade-in">
              <div class="space-y-1">
                <label
                  class="flex items-center gap-1 font-label text-xs text-on-surface-variant uppercase tracking-wider ml-1">
                  Config Filename (.ps1)
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
                  Config Filename (.ps1)
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
              Reset
            </button>
            <button type="submit"
              class="bg-primary hover:bg-primary/90 text-on-primary px-6 py-2.5 rounded-xl font-semibold flex items-center gap-2 transition-all shadow-lg shadow-primary/20 active:scale-95 text-sm">
              <Save class="w-[18px] h-[18px]" />
              Save Configuration
            </button>
          </div>
        </Form>
      </div>

    </div>
  </div>
</template>
