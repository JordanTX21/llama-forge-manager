<script setup lang="ts">
import { ref, watch } from 'vue'
import { AgentsService } from '@/services/agents.service'
import type { AgentInfo } from '@/services/agents.service'
import { useToast } from '@/composables/useToast'
import OpencodeImg from '@/assets/img/agents/opencode.webp'
import QwenImg from '@/assets/img/agents/qwen.webp'

const agentImages: Record<string, string> = {
  'opencode': OpencodeImg,
  'qwencode': QwenImg
}

const props = defineProps<{
  modelValue: boolean
  modelName: string
}>()

const emit = defineEmits(['update:modelValue', 'configured', 'skipped'])

const toast = useToast()

const installedAgents = ref<AgentInfo[]>([])
const loading = ref(false)
const configuring = ref(false)
const dontAskAgain = ref(false)

const closeModal = () => {
  if (dontAskAgain.value) {
    localStorage.setItem('agents_dont_ask', 'true')
  }
  emit('update:modelValue', false)
  emit('skipped')
}

const configure = async (agent: AgentInfo) => {
  if (dontAskAgain.value) {
    localStorage.setItem('agents_dont_ask', 'true')
  }
  configuring.value = true
  try {
    const endpoint = "http://127.0.0.1:8080/v1" // Local llama.cpp endpoint usually managed by swap or direct
    await AgentsService.configureAgent(agent.id, props.modelName, endpoint)
    toast.success(`Configurado para ${agent.name}`)
    emit('update:modelValue', false)
    emit('configured')
  } catch (err: any) {
    toast.error(err.message || 'Error al configurar el agente')
  } finally {
    configuring.value = false
  }
}

watch(() => props.modelValue, async (newVal) => {
  if (newVal) {
    loading.value = true
    try {
      const res = await AgentsService.getStatus()
      installedAgents.value = res.installed
      if (installedAgents.value.length === 0) {
        // If no agents are installed, close the modal immediately and save don't ask
        closeModal()
      }
    } catch (e) {
      console.error(e)
      closeModal()
    } finally {
      loading.value = false
    }
  }
})

// Use explicit imports to ensure Vite bundles the images
const getImageUrl = (id: string) => {
  return agentImages[id] || ''
}
</script>

<template>
  <div v-if="modelValue"
    class="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/60 backdrop-blur-sm transition-opacity">
    <div class="bg-surface-container-high border border-outline rounded-2xl w-full max-w-md shadow-2xl p-6 relative">
      <button @click="closeModal"
        class="absolute top-4 right-4 text-on-surface-variant hover:text-primary transition-colors">
        <svg class="w-6 h-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
        </svg>
      </button>

      <h3 class="text-xl font-headline font-bold text-on-surface mb-2">Configurar Agente de IA</h3>
      <p class="text-sm text-on-surface-variant mb-6">
        ¿Deseas configurar el modelo <strong>{{ modelName }}</strong> en alguno de los agentes instalados para que esté
        listo para usar?
      </p>

      <div v-if="loading" class="flex justify-center py-8">
        <div class="w-8 h-8 border-4 border-primary border-t-transparent rounded-full animate-spin"></div>
      </div>
      <div v-else-if="installedAgents.length > 0" class="space-y-3 mb-6">
        <button v-for="agent in installedAgents" :key="agent.id" @click="configure(agent)" :disabled="configuring"
          class="w-full flex items-center gap-4 p-4 rounded-xl border border-outline bg-surface-container hover:border-primary hover:bg-primary/5 transition-all text-left group disabled:opacity-50">
          <img :src="getImageUrl(agent.id)" :alt="agent.name"
            class="w-10 h-10 object-contain rounded-lg bg-white p-1" />
          <div class="flex-1">
            <h4 class="font-medium text-on-surface group-hover:text-primary transition-colors">{{ agent.name }}</h4>
            <span class="text-xs text-on-surface-variant">Conectar localmente</span>
          </div>
          <svg class="w-5 h-5 text-on-surface-variant group-hover:text-primary" fill="none" viewBox="0 0 24 24"
            stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7" />
          </svg>
        </button>
      </div>

      <div class="mt-4 flex items-center gap-2">
        <input type="checkbox" id="dontAsk" v-model="dontAskAgain"
          class="rounded border-outline bg-surface-container-low text-primary focus:ring-primary focus:ring-offset-surface-container-high" />
        <label for="dontAsk" class="text-sm text-on-surface-variant cursor-pointer select-none">No volver a
          preguntar</label>
      </div>

      <div class="mt-6 flex justify-end">
        <button @click="closeModal"
          class="px-5 py-2 rounded-xl text-sm font-medium text-on-surface-variant hover:text-on-surface hover:bg-surface-container transition-colors">
          Saltar
        </button>
      </div>
    </div>
  </div>
</template>
