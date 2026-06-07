<script setup lang="ts">
import { Field } from 'vee-validate'
import type { LocalModel } from '../../models/services/models.service'
import { Info, ChevronDown, Zap, Brain } from '@lucide/vue'
import { LLAMA_DOCS } from '../constants/llama-docs'
import Tooltip from '@/components/Tooltip.vue'

defineProps<{
  models: LocalModel[]
}>()
</script>

<template>
  <div class="grid grid-cols-1 md:grid-cols-2 gap-4 animate-fade-in">
    <div class="space-y-1">
      <label class="flex items-center gap-1 font-label text-xs text-on-surface-variant uppercase tracking-wider ml-1">
        Alias (YAML ID)
        <Tooltip :text="LLAMA_DOCS.alias">
          <Info class="w-3.5 h-3.5" />
        </Tooltip>
      </label>
      <Field name="alias" type="text"
        class="w-full bg-surface-container-low border border-outline rounded-lg p-3 text-sm focus:outline-none focus:border-primary transition-colors text-on-surface"
        placeholder="primary-router" />
    </div>

    <div class="space-y-1">
      <label class="flex items-center gap-1 font-label text-xs text-on-surface-variant uppercase tracking-wider ml-1">
        Port
        <Tooltip :text="LLAMA_DOCS.port">
          <Info class="w-3.5 h-3.5" />
        </Tooltip>
      </label>
      <Field name="port" type="number"
        class="w-full bg-surface-container-low border border-outline rounded-lg p-3 text-sm focus:outline-none focus:border-primary transition-colors text-on-surface" />
    </div>

    <div class="md:col-span-2 space-y-1">
      <label class="flex items-center gap-1 font-label text-xs text-on-surface-variant uppercase tracking-wider ml-1">
        Model Path (-m)
        <Tooltip :text="LLAMA_DOCS.model_path">
          <Info class="w-3.5 h-3.5" />
        </Tooltip>
      </label>
      <div class="flex gap-2 relative">
        <Field name="model_path" as="select"
          class="flex-1 bg-surface-container-low border border-outline rounded-lg p-3 text-sm appearance-none focus:outline-none focus:border-primary transition-colors text-on-surface">
          <option value="">-- Custom Path --</option>
          <option v-for="model in models" :key="model.path" :value="model.path.replace(/\\/g, '/')">
            {{ model.author }}/{{ model.repo }} - {{ model.filename }}
          </option>
        </Field>
        <ChevronDown class="absolute right-3 top-3 pointer-events-none text-on-surface-variant w-[18px] h-[18px]" />
      </div>
      <!-- For custom path we can just let them type it if they select Custom Path, but wait. If model_path is not in options, we should show input. We can use useField to check its value -->
    </div>

    <div class="space-y-1">
      <label class="flex items-center gap-1 font-label text-xs text-on-surface-variant uppercase tracking-wider ml-1">
        Context Size (-c)
        <Tooltip :text="LLAMA_DOCS.ctx_size">
          <Info class="w-3.5 h-3.5" />
        </Tooltip>
      </label>
      <Field name="ctx_size" type="number"
        class="w-full bg-surface-container-low border border-outline rounded-lg p-3 text-sm focus:outline-none focus:border-primary transition-colors text-on-surface" />
    </div>

    <div class="space-y-1">
      <label class="flex items-center gap-1 font-label text-xs text-on-surface-variant uppercase tracking-wider ml-1">
        NGL (GPU Layers)
        <Tooltip :text="LLAMA_DOCS.ngl">
          <Info class="w-3.5 h-3.5" />
        </Tooltip>
      </label>
      <Field name="ngl" type="number"
        class="w-full bg-surface-container-low border border-outline rounded-lg p-3 text-sm focus:outline-none focus:border-primary transition-colors text-on-surface" />
    </div>

    <div class="md:col-span-2 space-y-1">
      <label class="flex items-center gap-1 font-label text-xs text-on-surface-variant uppercase tracking-wider ml-1">
        MMProj Path (Optional)
        <Tooltip :text="LLAMA_DOCS.mmproj_path">
          <Info class="w-3.5 h-3.5" />
        </Tooltip>
      </label>
      <Field name="mmproj_path" type="text"
        class="w-full bg-surface-container-low border border-outline rounded-lg p-3 text-sm focus:outline-none focus:border-primary transition-colors text-on-surface"
        placeholder="Visual adapter path..." />
    </div>

    <!-- Toggles require v-model or checked binding, Vee-Validate handles checkbox with type="checkbox" and value -->
    <div
      class="md:col-span-2 bg-surface-container-low border border-outline rounded-xl p-3 flex items-center justify-between">
      <div class="flex items-center gap-3">
        <div class="p-1.5 bg-primary-container/20 rounded-md text-primary">
          <Zap class="w-[18px] h-[18px]" />
        </div>
        <div>
          <p class="font-body text-sm font-semibold flex items-center gap-1">Flash Attention
            <Tooltip :text="LLAMA_DOCS.flash_attention">
              <Info class="w-3.5 h-3.5 text-on-surface-variant" />
            </Tooltip>
          </p>
          <p class="font-label text-[10px] text-on-surface-variant">Enable v2 acceleration kernels</p>
        </div>
      </div>
      <label class="relative inline-flex items-center cursor-pointer">
        <Field name="flash_attention" type="checkbox" :value="true" :unchecked-value="false" class="sr-only peer" />
        <div
          class="w-9 h-5 bg-surface-variant peer-focus:outline-none rounded-full peer peer-checked:after:translate-x-full peer-checked:after:border-white after:content-[''] after:absolute after:top-[2px] after:left-[2px] after:bg-white after:border-gray-300 after:border after:rounded-full after:h-4 after:w-4 after:transition-all peer-checked:bg-primary transition-colors">
        </div>
      </label>
    </div>

    <div
      class="md:col-span-2 bg-surface-container-low border border-outline rounded-xl p-3 flex items-center justify-between">
      <div class="flex items-center gap-3">
        <div class="p-1.5 bg-primary-container/20 rounded-md text-primary">
          <Brain class="w-[18px] h-[18px]" />
        </div>
        <div>
          <p class="font-body text-sm font-semibold flex items-center gap-1">Thinking Mode
            <Tooltip :text="LLAMA_DOCS.thinking_mode">
              <Info class="w-3.5 h-3.5 text-on-surface-variant" />
            </Tooltip>
          </p>
          <p class="font-label text-[10px] text-on-surface-variant">Enable reasoning models output</p>
        </div>
      </div>
      <label class="relative inline-flex items-center cursor-pointer">
        <Field name="thinking_mode" type="checkbox" :value="true" :unchecked-value="false" class="sr-only peer" />
        <div
          class="w-9 h-5 bg-surface-variant peer-focus:outline-none rounded-full peer peer-checked:after:translate-x-full peer-checked:after:border-white after:content-[''] after:absolute after:top-[2px] after:left-[2px] after:bg-white after:border-gray-300 after:border after:rounded-full after:h-4 after:w-4 after:transition-all peer-checked:bg-primary transition-colors">
        </div>
      </label>
    </div>
  </div>
</template>
