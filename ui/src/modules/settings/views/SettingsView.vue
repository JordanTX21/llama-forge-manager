<script setup lang="ts">
import { ref, onMounted, watch } from 'vue'
import { SettingsService, type CommandConfig } from '../services/settings.service'
import { ModelsService, type LocalModel } from '../../models/services/models.service'

const models = ref<LocalModel[]>([])
const commands = ref<CommandConfig[]>([])

// UI State
const showAdvanced = ref(false)

// Form state - Basic
const filename = ref('')
const selectedModelPath = ref('')
const mmproj = ref('')
const alias = ref('mi-modelo')
const ctxSize = ref(4096)
const ngl = ref(35)
const port = ref(8080)
const flashAttention = ref(true)
const thinkingMode = ref(false)

// Form state - Advanced
const threads = ref(-1)
const threadsBatch = ref(-1)
const np = ref(-1)
const cr = ref('')
const crb = ref('')
const cpuStrict = ref(false)
const cpuStrictBatch = ref(false)

const batchSize = ref(-1)
const ubatchSize = ref(-1)
const prio = ref(-1)
const prioBatch = ref(-1)
const poll = ref(-1)
const pollBatch = ref(-1)

const cacheTypeK = ref('q8_0')
const cacheTypeV = ref('q8_0')
const kvUnified = ref(false)
const noMmap = ref(false)
const mlock = ref(false)

const ncmoe = ref(-1)
const specType = ref('')
const specDraftNMax = ref(-1)

const temp = ref(0.6)
const topP = ref(0.95)
const topK = ref(20)
const minP = ref(0.0)
const presencePenalty = ref(0.0)
const repeatPenalty = ref(1.0)

const jinja = ref(false)

const selectedCommandIndex = ref<number | ''>('')

const fetchModelsAndCommands = async () => {
  try {
    const resModels = await ModelsService.getLocalModels()
    models.value = resModels.models
    commands.value = await SettingsService.getCommands()
  } catch (err) {
    console.error('Error fetching data', err)
  }
}

watch(selectedCommandIndex, (idx) => {
  if (idx !== '' && commands.value[idx as number]) {
    const cmd = commands.value[idx as number]
    // Basic
    filename.value = cmd.filename.replace('.ps1', '')
    selectedModelPath.value = cmd.model_path.replace(/\\/g, '/')
    mmproj.value = cmd.mmproj_path ? cmd.mmproj_path.replace(/\\/g, '/') : ''
    alias.value = cmd.alias
    ctxSize.value = cmd.ctx_size
    ngl.value = cmd.ngl
    port.value = cmd.port
    flashAttention.value = cmd.flash_attention
    thinkingMode.value = cmd.thinking_mode

    // Advanced
    threads.value = cmd.threads
    threadsBatch.value = cmd.threads_batch
    np.value = cmd.np
    cr.value = cmd.cr
    crb.value = cmd.crb
    cpuStrict.value = cmd.cpu_strict
    cpuStrictBatch.value = cmd.cpu_strict_batch

    batchSize.value = cmd.batch_size
    ubatchSize.value = cmd.ubatch_size
    prio.value = cmd.prio
    prioBatch.value = cmd.prio_batch
    poll.value = cmd.poll
    pollBatch.value = cmd.poll_batch

    cacheTypeK.value = cmd.cache_type_k || 'q8_0'
    cacheTypeV.value = cmd.cache_type_v || 'q8_0'
    kvUnified.value = cmd.kv_unified
    noMmap.value = cmd.no_mmap
    mlock.value = cmd.mlock

    ncmoe.value = cmd.ncmoe
    specType.value = cmd.spec_type
    specDraftNMax.value = cmd.spec_draft_n_max

    temp.value = cmd.temp
    topP.value = cmd.top_p
    topK.value = cmd.top_k
    minP.value = cmd.min_p
    presencePenalty.value = cmd.presence_penalty
    repeatPenalty.value = cmd.repeat_penalty

    jinja.value = cmd.jinja

  } else {
    // Reset form
    filename.value = ''
    alias.value = ''
    ctxSize.value = 4096
    ngl.value = 35
    port.value = 8080
    flashAttention.value = false
    thinkingMode.value = false
    mmproj.value = ''

    threads.value = -1
    threadsBatch.value = -1
    np.value = -1
    cr.value = ''
    crb.value = ''
    cpuStrict.value = false
    cpuStrictBatch.value = false

    batchSize.value = -1
    ubatchSize.value = -1
    prio.value = -1
    prioBatch.value = -1
    poll.value = -1
    pollBatch.value = -1

    cacheTypeK.value = 'q8_0'
    cacheTypeV.value = 'q8_0'
    kvUnified.value = false
    noMmap.value = false
    mlock.value = false

    ncmoe.value = -1
    specType.value = ''
    specDraftNMax.value = -1

    temp.value = 0.6
    topP.value = 0.95
    topK.value = 20
    minP.value = 0.0
    presencePenalty.value = 0.0
    repeatPenalty.value = 1.0

    jinja.value = false
  }
})

const startSwap = async () => {
  try {
    await SettingsService.startSwap()
    alert('Llama-Swap iniciado. Puedes conectarte en el puerto 8080.')
  } catch (err) {
    console.error(err)
    alert('Error al iniciar Llama-Swap.')
  }
}

const saveCommand = async () => {
  if (!filename.value || !alias.value || !selectedModelPath.value) {
    alert('Faltan campos requeridos (Filename, Alias, Model Path)')
    return
  }

  const config: CommandConfig = {
    filename: filename.value.endsWith('.ps1') ? filename.value : `${filename.value}.ps1`,
    model_path: selectedModelPath.value,
    mmproj_path: mmproj.value,
    alias: alias.value,
    ctx_size: ctxSize.value,
    ngl: ngl.value,
    port: port.value,
    flash_attention: flashAttention.value,
    thinking_mode: thinkingMode.value,

    threads: threads.value,
    threads_batch: threadsBatch.value,
    np: np.value,
    cr: cr.value,
    crb: crb.value,
    cpu_strict: cpuStrict.value,
    cpu_strict_batch: cpuStrictBatch.value,

    batch_size: batchSize.value,
    ubatch_size: ubatchSize.value,
    prio: prio.value,
    prio_batch: prioBatch.value,
    poll: poll.value,
    poll_batch: pollBatch.value,

    cache_type_k: cacheTypeK.value,
    cache_type_v: cacheTypeV.value,
    kv_unified: kvUnified.value,
    no_mmap: noMmap.value,
    mlock: mlock.value,

    ncmoe: ncmoe.value,
    spec_type: specType.value,
    spec_draft_n_max: specDraftNMax.value,

    temp: temp.value,
    top_p: topP.value,
    top_k: topK.value,
    min_p: minP.value,
    presence_penalty: presencePenalty.value,
    repeat_penalty: repeatPenalty.value,

    jinja: jinja.value
  }

  try {
    await SettingsService.saveCommand(config)
    alert(`Comando guardado e inyectado en config.yaml correctamente.`)
    await fetchModelsAndCommands()
  } catch (err) {
    console.error(err)
    alert('Error al guardar el comando.')
  }
}

onMounted(fetchModelsAndCommands)
</script>

<template>
  <div class="w-full max-w-4xl mx-auto space-y-12">

    <!-- Header Section -->
    <header class="hidden md:block">
      <h2 class="font-headline text-4xl text-on-surface mb-2 font-semibold tracking-tight">Execution Settings</h2>
      <p class="text-on-surface-variant font-body">Configure system-wide settings and optimize your local inference.</p>
    </header>

    <!-- Hero Card Section -->
    <section>
      <div class="glass rounded-3xl overflow-hidden relative group border border-outline shadow-2xl">
        <div class="absolute inset-0 opacity-20 pointer-events-none">
          <div class="absolute top-0 right-0 w-64 h-64 bg-primary blur-[100px]"></div>
        </div>
        <div class="p-8 md:flex items-center justify-between relative z-10">
          <div>
            <div class="flex items-center gap-2 mb-2">
              <span class="w-2 h-2 rounded-full bg-primary animate-pulse"></span>
              <span class="font-label text-xs text-primary tracking-widest uppercase">Accelerator Ready</span>
            </div>
            <h2 class="font-headline text-2xl font-bold mb-2">Llama-Swap Router</h2>
            <p class="text-on-surface-variant max-w-md">Optimize your local inference by dynamically switching between
              active models for peak performance.</p>
          </div>
          <div class="mt-6 md:mt-0">
            <button @click="startSwap"
              class="bg-primary-container text-primary font-semibold px-8 py-4 rounded-xl shadow-lg hover:bg-primary-container/80 transition-all active:scale-95 flex items-center gap-2">
              <span>Run Llama-Swap</span>
              <span class="material-symbols-outlined text-primary">play_arrow</span>
            </button>
          </div>
        </div>
      </div>
    </section>

    <!-- Configuration Form Section -->
    <section class="space-y-6">
      <div class="flex items-center justify-between mb-4">
        <h3 class="font-headline text-2xl font-semibold">Command Parameters</h3>
        <span
          class="text-on-surface-variant font-label text-xs border border-outline px-2 py-1 rounded-full">v2.4.1-stable</span>
      </div>

      <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
        <!-- Dropdown -->
        <div class="md:col-span-2 space-y-2">
          <label class="font-label text-xs text-on-surface-variant uppercase tracking-wider ml-1">Load Command</label>
          <div class="relative">
            <select v-model="selectedCommandIndex"
              class="w-full bg-surface-container-low border border-outline rounded-xl p-4 appearance-none focus:outline-none focus:border-primary transition-colors text-on-surface">
              <option value="">-- Create New Command --</option>
              <option v-for="(cmd, index) in commands" :key="cmd.filename" :value="index">
                {{ cmd.filename }} (Alias: {{ cmd.alias }})
              </option>
            </select>
            <span
              class="material-symbols-outlined absolute right-4 top-4 pointer-events-none text-on-surface-variant">expand_more</span>
          </div>
        </div>

        <!-- BASIC INPUTS -->
        <div class="space-y-2">
          <label class="font-label text-xs text-on-surface-variant uppercase tracking-wider ml-1">Filename (.ps1)</label>
          <input v-model="filename"
            class="w-full bg-surface-container-low border border-outline rounded-xl p-4 focus:outline-none focus:border-primary transition-colors text-on-surface"
            placeholder="llama-3-8b-q4_k_m" type="text" />
        </div>
        <div class="space-y-2">
          <label class="font-label text-xs text-on-surface-variant uppercase tracking-wider ml-1">Alias (YAML ID)</label>
          <input v-model="alias"
            class="w-full bg-surface-container-low border border-outline rounded-xl p-4 focus:outline-none focus:border-primary transition-colors text-on-surface"
            placeholder="primary-router" type="text" />
        </div>

        <div class="md:col-span-2 space-y-2">
          <label class="font-label text-xs text-on-surface-variant uppercase tracking-wider ml-1">Model Path</label>
          <div class="flex gap-2 relative">
            <select v-model="selectedModelPath"
              class="flex-1 bg-surface-container-low border border-outline rounded-xl p-4 appearance-none focus:outline-none focus:border-primary transition-colors text-on-surface">
              <option value="">-- Custom Path --</option>
              <option v-for="model in models" :key="model.path" :value="model.path.replace(/\\/g, '/')">
                {{ model.author }}/{{ model.repo }} - {{ model.filename }}
              </option>
            </select>
            <span
              class="material-symbols-outlined absolute right-4 top-4 pointer-events-none text-on-surface-variant">expand_more</span>
          </div>
          <input v-if="!selectedModelPath && models.length > 0" v-model="selectedModelPath" placeholder="Manual path..."
            class="w-full bg-surface-container-low border border-outline rounded-xl p-4 focus:outline-none focus:border-primary transition-colors text-on-surface mt-2" />
        </div>

        <div class="space-y-2">
          <label class="font-label text-xs text-on-surface-variant uppercase tracking-wider ml-1">Context Size (-c)</label>
          <input v-model="ctxSize"
            class="w-full bg-surface-container-low border border-outline rounded-xl p-4 focus:outline-none focus:border-primary transition-colors text-on-surface"
            type="number" />
        </div>
        <div class="space-y-2">
          <label class="font-label text-xs text-on-surface-variant uppercase tracking-wider ml-1">NGL (GPU Layers)</label>
          <input v-model="ngl"
            class="w-full bg-surface-container-low border border-outline rounded-xl p-4 focus:outline-none focus:border-primary transition-colors text-on-surface"
            type="number" />
        </div>
        <div class="space-y-2">
          <label class="font-label text-xs text-on-surface-variant uppercase tracking-wider ml-1">Port</label>
          <input v-model="port"
            class="w-full bg-surface-container-low border border-outline rounded-xl p-4 focus:outline-none focus:border-primary transition-colors text-on-surface"
            type="number" />
        </div>
        <div class="space-y-2">
          <label class="font-label text-xs text-on-surface-variant uppercase tracking-wider ml-1">MMProj Path (Optional)</label>
          <input v-model="mmproj"
            class="w-full bg-surface-container-low border border-outline rounded-xl p-4 focus:outline-none focus:border-primary transition-colors text-on-surface"
            type="text" placeholder="Visual adapter path..." />
        </div>

        <!-- BASIC TOGGLES -->
        <div
          class="md:col-span-2 bg-surface-container-low border border-outline rounded-xl p-4 flex items-center justify-between mt-2">
          <div class="flex items-center gap-3">
            <div class="p-2 bg-primary-container/20 rounded-lg text-primary">
              <span class="material-symbols-outlined">bolt</span>
            </div>
            <div>
              <p class="font-body font-semibold">Flash Attention</p>
              <p class="font-label text-xs text-on-surface-variant">Enable v2 acceleration kernels</p>
            </div>
          </div>
          <label class="relative inline-flex items-center cursor-pointer">
            <input type="checkbox" v-model="flashAttention" class="sr-only peer">
            <div
              class="w-11 h-6 bg-surface-container-high peer-focus:outline-none rounded-full peer peer-checked:after:translate-x-full peer-checked:after:border-white after:content-[''] after:absolute after:top-[2px] after:left-[2px] after:bg-white after:border-gray-300 after:border after:rounded-full after:h-5 after:w-5 after:transition-all peer-checked:bg-primary transition-colors">
            </div>
          </label>
        </div>

        <div
          class="md:col-span-2 bg-surface-container-low border border-outline rounded-xl p-4 flex items-center justify-between mt-2">
          <div class="flex items-center gap-3">
            <div class="p-2 bg-primary-container/20 rounded-lg text-primary">
              <span class="material-symbols-outlined">psychology</span>
            </div>
            <div>
              <p class="font-body font-semibold">Thinking Mode</p>
              <p class="font-label text-xs text-on-surface-variant">Enable reasoning models output</p>
            </div>
          </div>
          <label class="relative inline-flex items-center cursor-pointer">
            <input type="checkbox" v-model="thinkingMode" class="sr-only peer">
            <div
              class="w-11 h-6 bg-surface-container-high peer-focus:outline-none rounded-full peer peer-checked:after:translate-x-full peer-checked:after:border-white after:content-[''] after:absolute after:top-[2px] after:left-[2px] after:bg-white after:border-gray-300 after:border after:rounded-full after:h-5 after:w-5 after:transition-all peer-checked:bg-primary transition-colors">
            </div>
          </label>
        </div>

        <!-- ADVANCED SETTINGS ACCORDION -->
        <div class="md:col-span-2 mt-4">
          <button @click="showAdvanced = !showAdvanced" type="button" class="w-full flex items-center justify-between p-4 bg-surface-container-high border border-outline rounded-xl hover:bg-surface-variant transition-colors">
            <span class="font-semibold text-on-surface flex items-center gap-2">
              <span class="material-symbols-outlined text-primary">tune</span>
              Advanced Settings
            </span>
            <span class="material-symbols-outlined transition-transform duration-300" :class="{ 'rotate-180': showAdvanced }">expand_more</span>
          </button>
          
          <div v-show="showAdvanced" class="mt-4 p-6 glass rounded-2xl border border-outline space-y-8">
            
            <!-- Sampling -->
            <div>
              <h4 class="font-headline text-lg mb-4 text-primary border-b border-outline pb-2">Sampling</h4>
              <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
                <div>
                  <label class="font-label text-xs text-on-surface-variant uppercase">Temperature</label>
                  <input v-model="temp" type="number" step="0.1" class="w-full bg-surface-container-low border border-outline rounded-lg p-3 text-on-surface" />
                </div>
                <div>
                  <label class="font-label text-xs text-on-surface-variant uppercase">Top P</label>
                  <input v-model="topP" type="number" step="0.05" class="w-full bg-surface-container-low border border-outline rounded-lg p-3 text-on-surface" />
                </div>
                <div>
                  <label class="font-label text-xs text-on-surface-variant uppercase">Top K</label>
                  <input v-model="topK" type="number" class="w-full bg-surface-container-low border border-outline rounded-lg p-3 text-on-surface" />
                </div>
                <div>
                  <label class="font-label text-xs text-on-surface-variant uppercase">Min P</label>
                  <input v-model="minP" type="number" step="0.05" class="w-full bg-surface-container-low border border-outline rounded-lg p-3 text-on-surface" />
                </div>
                <div>
                  <label class="font-label text-xs text-on-surface-variant uppercase">Presence Penalty</label>
                  <input v-model="presencePenalty" type="number" step="0.1" class="w-full bg-surface-container-low border border-outline rounded-lg p-3 text-on-surface" />
                </div>
                <div>
                  <label class="font-label text-xs text-on-surface-variant uppercase">Repeat Penalty</label>
                  <input v-model="repeatPenalty" type="number" step="0.1" class="w-full bg-surface-container-low border border-outline rounded-lg p-3 text-on-surface" />
                </div>
              </div>
            </div>

            <!-- Memory & Cache -->
            <div>
              <h4 class="font-headline text-lg mb-4 text-primary border-b border-outline pb-2">Memory & Cache</h4>
              <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
                <div>
                  <label class="font-label text-xs text-on-surface-variant uppercase">Cache Type K</label>
                  <input v-model="cacheTypeK" type="text" class="w-full bg-surface-container-low border border-outline rounded-lg p-3 text-on-surface" placeholder="q8_0" />
                </div>
                <div>
                  <label class="font-label text-xs text-on-surface-variant uppercase">Cache Type V</label>
                  <input v-model="cacheTypeV" type="text" class="w-full bg-surface-container-low border border-outline rounded-lg p-3 text-on-surface" placeholder="q8_0" />
                </div>
                <div class="flex flex-col gap-3 mt-2">
                  <label class="flex items-center gap-3 cursor-pointer">
                    <input type="checkbox" v-model="kvUnified" class="w-5 h-5 rounded bg-surface-container-low border-outline text-primary focus:ring-primary focus:ring-offset-surface">
                    <span class="text-sm font-medium text-on-surface">KV Unified</span>
                  </label>
                  <label class="flex items-center gap-3 cursor-pointer">
                    <input type="checkbox" v-model="noMmap" class="w-5 h-5 rounded bg-surface-container-low border-outline text-primary focus:ring-primary focus:ring-offset-surface">
                    <span class="text-sm font-medium text-on-surface">No Mmap (Load completely to RAM)</span>
                  </label>
                  <label class="flex items-center gap-3 cursor-pointer">
                    <input type="checkbox" v-model="mlock" class="w-5 h-5 rounded bg-surface-container-low border-outline text-primary focus:ring-primary focus:ring-offset-surface">
                    <span class="text-sm font-medium text-on-surface">Mlock (Prevent swapping)</span>
                  </label>
                </div>
              </div>
            </div>

            <!-- Compute & Threads -->
            <div>
              <h4 class="font-headline text-lg mb-4 text-primary border-b border-outline pb-2">Compute & Threads (-1 = Default)</h4>
              <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
                <div>
                  <label class="font-label text-xs text-on-surface-variant uppercase">Threads (-t)</label>
                  <input v-model="threads" type="number" class="w-full bg-surface-container-low border border-outline rounded-lg p-3 text-on-surface" />
                </div>
                <div>
                  <label class="font-label text-xs text-on-surface-variant uppercase">Threads Batch (-tb)</label>
                  <input v-model="threadsBatch" type="number" class="w-full bg-surface-container-low border border-outline rounded-lg p-3 text-on-surface" />
                </div>
                <div>
                  <label class="font-label text-xs text-on-surface-variant uppercase">Num Processes (-np)</label>
                  <input v-model="np" type="number" class="w-full bg-surface-container-low border border-outline rounded-lg p-3 text-on-surface" />
                </div>
                <div>
                  <label class="font-label text-xs text-on-surface-variant uppercase">Core Ratio (-Cr)</label>
                  <input v-model="cr" type="text" class="w-full bg-surface-container-low border border-outline rounded-lg p-3 text-on-surface" placeholder="e.g. 0-11" />
                </div>
                <div>
                  <label class="font-label text-xs text-on-surface-variant uppercase">Core Ratio Batch (-Crb)</label>
                  <input v-model="crb" type="text" class="w-full bg-surface-container-low border border-outline rounded-lg p-3 text-on-surface" placeholder="e.g. 0-11" />
                </div>
                <div class="flex flex-col gap-3 justify-end pb-2">
                  <label class="flex items-center gap-3 cursor-pointer">
                    <input type="checkbox" v-model="cpuStrict" class="w-5 h-5 rounded bg-surface-container-low border-outline text-primary focus:ring-primary focus:ring-offset-surface">
                    <span class="text-sm font-medium text-on-surface">CPU Strict</span>
                  </label>
                  <label class="flex items-center gap-3 cursor-pointer">
                    <input type="checkbox" v-model="cpuStrictBatch" class="w-5 h-5 rounded bg-surface-container-low border-outline text-primary focus:ring-primary focus:ring-offset-surface">
                    <span class="text-sm font-medium text-on-surface">CPU Strict Batch</span>
                  </label>
                </div>
              </div>
            </div>

            <!-- Batching & Processing -->
            <div>
              <h4 class="font-headline text-lg mb-4 text-primary border-b border-outline pb-2">Batching (-1 = Default)</h4>
              <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
                <div>
                  <label class="font-label text-xs text-on-surface-variant uppercase">Batch Size (-b)</label>
                  <input v-model="batchSize" type="number" class="w-full bg-surface-container-low border border-outline rounded-lg p-3 text-on-surface" />
                </div>
                <div>
                  <label class="font-label text-xs text-on-surface-variant uppercase">UBatch Size (-ub)</label>
                  <input v-model="ubatchSize" type="number" class="w-full bg-surface-container-low border border-outline rounded-lg p-3 text-on-surface" />
                </div>
                <div>
                  <label class="font-label text-xs text-on-surface-variant uppercase">Prio</label>
                  <input v-model="prio" type="number" class="w-full bg-surface-container-low border border-outline rounded-lg p-3 text-on-surface" />
                </div>
                <div>
                  <label class="font-label text-xs text-on-surface-variant uppercase">Prio Batch</label>
                  <input v-model="prioBatch" type="number" class="w-full bg-surface-container-low border border-outline rounded-lg p-3 text-on-surface" />
                </div>
                <div>
                  <label class="font-label text-xs text-on-surface-variant uppercase">Poll (%)</label>
                  <input v-model="poll" type="number" class="w-full bg-surface-container-low border border-outline rounded-lg p-3 text-on-surface" />
                </div>
                <div>
                  <label class="font-label text-xs text-on-surface-variant uppercase">Poll Batch (%)</label>
                  <input v-model="pollBatch" type="number" class="w-full bg-surface-container-low border border-outline rounded-lg p-3 text-on-surface" />
                </div>
              </div>
            </div>

            <!-- MoE & Speculative -->
            <div>
              <h4 class="font-headline text-lg mb-4 text-primary border-b border-outline pb-2">MoE & Speculative Decoding</h4>
              <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
                <div>
                  <label class="font-label text-xs text-on-surface-variant uppercase">MoE Cores (-ncmoe)</label>
                  <input v-model="ncmoe" type="number" class="w-full bg-surface-container-low border border-outline rounded-lg p-3 text-on-surface" />
                </div>
                <div>
                  <label class="font-label text-xs text-on-surface-variant uppercase">Spec Type</label>
                  <input v-model="specType" type="text" class="w-full bg-surface-container-low border border-outline rounded-lg p-3 text-on-surface" placeholder="draft-mtp" />
                </div>
                <div>
                  <label class="font-label text-xs text-on-surface-variant uppercase">Spec Draft Max N</label>
                  <input v-model="specDraftNMax" type="number" class="w-full bg-surface-container-low border border-outline rounded-lg p-3 text-on-surface" />
                </div>
              </div>
            </div>

            <!-- Misc -->
            <div>
               <h4 class="font-headline text-lg mb-4 text-primary border-b border-outline pb-2">Misc</h4>
               <label class="flex items-center gap-3 cursor-pointer">
                  <input type="checkbox" v-model="jinja" class="w-5 h-5 rounded bg-surface-container-low border-outline text-primary focus:ring-primary focus:ring-offset-surface">
                  <span class="text-sm font-medium text-on-surface">Jinja Template Engine</span>
                </label>
            </div>

          </div>
        </div>

        <!-- Save Button -->
        <div class="md:col-span-2 pt-8">
          <button @click="saveCommand"
            class="w-full bg-primary-container text-primary hover:bg-primary-container/80 border border-primary/20 font-bold py-4 rounded-xl shadow-2xl transition-all text-lg flex justify-center items-center gap-2">
            <span class="material-symbols-outlined">save</span>
            Save Configuration
          </button>
        </div>
      </div>
    </section>

  </div>
</template>
