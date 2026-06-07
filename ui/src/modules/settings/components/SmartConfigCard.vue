<script setup lang="ts">
import { ref, watch, computed } from 'vue'
import { RecommendService, type Recommendation } from '../services/recommend.service'
import { Sparkles, ChevronDown, Zap, Check, Loader2, Cpu, HardDrive, MonitorCog, Info } from '@lucide/vue'
import { useI18n } from 'vue-i18n'

const { t } = useI18n()
const props = defineProps<{
  modelPath: string
  modelSizeMb: number
  modelFilename: string
}>()

const emit = defineEmits<{
  apply: [config: Record<string, any>]
}>()

const recommendation = ref<Recommendation | null>(null)
const isLoading = ref(false)
const hasError = ref(false)
const showDetails = ref(false)
const isApplied = ref(false)

const tierConfig = computed(() => {
  if (!recommendation.value) return null
  const map: Record<string, { color: string; bg: string; border: string; glow: string; label: string }> = {
    OPTIMAL: {
      color: 'text-green-400',
      bg: 'bg-green-500/10',
      border: 'border-green-500/30',
      glow: 'shadow-green-500/20',
      label: t('settings.smart.optimal')
    },
    GOOD: {
      color: 'text-blue-400',
      bg: 'bg-blue-500/10',
      border: 'border-blue-500/30',
      glow: 'shadow-blue-500/20',
      label: t('settings.smart.good')
    },
    CONSTRAINED: {
      color: 'text-amber-400',
      bg: 'bg-amber-500/10',
      border: 'border-amber-500/30',
      glow: 'shadow-amber-500/20',
      label: t('settings.smart.constrained')
    }
  }
  return map[recommendation.value.tier] || map.GOOD
})

const confidenceBadge = computed(() => {
  if (!recommendation.value) return null
  const map: Record<string, { color: string; bg: string; label: string }> = {
    high: { color: 'text-green-300', bg: 'bg-green-500/15', label: t('settings.smart.high') },
    medium: { color: 'text-yellow-300', bg: 'bg-yellow-500/15', label: t('settings.smart.medium') },
    low: { color: 'text-red-300', bg: 'bg-red-500/15', label: t('settings.smart.low') }
  }
  return map[recommendation.value.confidence] || map.medium
})

const keyParams = computed(() => {
  if (!recommendation.value) return []
  const c = recommendation.value.config
  return [
    { label: 'GPU Layers', value: c.ngl === 999 ? 'Full Offload' : String(c.ngl), icon: 'gpu' },
    { label: 'Context', value: `${(c.ctx_size / 1024).toFixed(0)}K`, icon: 'ctx' },
    { label: 'Threads', value: `${c.threads} / ${c.threads_batch}`, icon: 'cpu' },
    { label: 'KV Cache', value: `${c.cache_type_k}`, icon: 'cache' },
  ]
})

async function fetchRecommendation() {
  if (!props.modelPath || props.modelSizeMb <= 0) {
    recommendation.value = null
    return
  }

  isLoading.value = true
  hasError.value = false
  isApplied.value = false

  try {
    recommendation.value = await RecommendService.getRecommendation(
      props.modelPath,
      props.modelSizeMb,
      props.modelFilename
    )
  } catch (err) {
    console.error('SmartConfig error:', err)
    hasError.value = true
    recommendation.value = null
  } finally {
    isLoading.value = false
  }
}

function applyConfig() {
  if (!recommendation.value) return
  emit('apply', { ...recommendation.value.config })
  isApplied.value = true
  setTimeout(() => { isApplied.value = false }, 2500)
}

watch(
  () => [props.modelPath, props.modelSizeMb],
  () => { fetchRecommendation() },
  { immediate: true }
)
</script>

<template>
  <div class="rounded-2xl border overflow-hidden transition-all duration-500"
    :class="[
      recommendation && tierConfig
        ? `${tierConfig.border} shadow-lg ${tierConfig.glow}`
        : 'border-outline shadow-sm'
    ]">

    <!-- Header -->
    <div class="p-4 flex items-center gap-3 relative"
      :class="recommendation && tierConfig ? tierConfig.bg : 'bg-surface-container-low'">
      <!-- Animated glow -->
      <div v-if="recommendation" class="absolute inset-0 opacity-20 pointer-events-none">
        <div class="absolute -top-4 -right-4 w-32 h-32 rounded-full blur-[60px]"
          :class="tierConfig?.color.replace('text-', 'bg-')"></div>
      </div>

      <div class="relative p-2 rounded-xl" :class="recommendation ? tierConfig?.bg : 'bg-primary-container/20'">
        <Sparkles v-if="!isLoading" class="w-5 h-5 ai-pulse"
          :class="recommendation ? tierConfig?.color : 'text-primary'" />
        <Loader2 v-else class="w-5 h-5 text-primary animate-spin" />
      </div>

      <div class="flex-1 relative">
        <h3 class="font-headline text-base font-semibold text-on-surface flex items-center gap-2">
          {{ t('settings.smart.smartConfig') }}
          <span v-if="recommendation && confidenceBadge"
            class="text-[10px] font-label px-2 py-0.5 rounded-full uppercase tracking-wider"
            :class="[confidenceBadge.bg, confidenceBadge.color]">
            {{ confidenceBadge.label }}
          </span>
        </h3>
        <p class="text-[11px] text-on-surface-variant mt-0.5">
          {{ recommendation ? tierConfig?.label : t('settings.smart.selectModelForRecs') }}
        </p>
      </div>
    </div>

    <!-- Loading State -->
    <div v-if="isLoading" class="p-4 space-y-3">
      <div class="h-3 rounded-full bg-surface-container-high animate-pulse w-3/4"></div>
      <div class="h-3 rounded-full bg-surface-container-high animate-pulse w-1/2"></div>
      <div class="grid grid-cols-2 gap-2 mt-3">
        <div class="h-16 rounded-xl bg-surface-container-high animate-pulse"></div>
        <div class="h-16 rounded-xl bg-surface-container-high animate-pulse"></div>
      </div>
    </div>

    <!-- Error State -->
    <div v-else-if="hasError" class="p-4">
      <p class="text-xs text-red-400/80">{{ t('settings.smart.errorFetching') }}</p>
      <button @click="fetchRecommendation"
        class="mt-2 text-xs text-primary hover:text-primary/80 font-semibold transition-colors">
        {{ t('settings.smart.retry') }}
      </button>
    </div>

    <!-- Empty State -->
    <div v-else-if="!recommendation" class="p-4">
      <p class="text-xs text-on-surface-variant/60 italic">
        {{ t('settings.smart.selectModelForm') }}
      </p>
    </div>

    <!-- Recommendation Content -->
    <div v-else class="p-4 space-y-3">

      <!-- Hardware & Model Summary Pills -->
      <div class="flex flex-wrap gap-1.5">
        <span v-if="recommendation.model_summary.parámetros"
          class="inline-flex items-center gap-1 text-[10px] font-label px-2 py-1 rounded-lg bg-surface-container-high text-on-surface-variant border border-outline/50">
          <Cpu class="w-3 h-3" />
          {{ recommendation.model_summary.parámetros }}
        </span>
        <span v-if="recommendation.model_summary.cuantización"
          class="inline-flex items-center gap-1 text-[10px] font-label px-2 py-1 rounded-lg bg-surface-container-high text-on-surface-variant border border-outline/50">
          <HardDrive class="w-3 h-3" />
          {{ recommendation.model_summary.cuantización }}
        </span>
        <span v-if="recommendation.model_summary.tamaño"
          class="inline-flex items-center gap-1 text-[10px] font-label px-2 py-1 rounded-lg bg-surface-container-high text-on-surface-variant border border-outline/50">
          <MonitorCog class="w-3 h-3" />
          {{ recommendation.model_summary.tamaño }}
        </span>
      </div>

      <!-- Key Parameters Grid -->
      <div class="grid grid-cols-2 gap-2">
        <div v-for="param in keyParams" :key="param.label"
          class="bg-surface-container-low border border-outline/50 rounded-xl p-2.5 group/param hover:border-primary/30 transition-colors">
          <p class="text-[10px] font-label text-on-surface-variant uppercase tracking-wider">{{ param.label }}</p>
          <p class="text-sm font-semibold text-on-surface mt-0.5 font-label">{{ param.value }}</p>
        </div>
      </div>

      <!-- Feature Flags -->
      <div class="flex flex-wrap gap-1.5">
        <span v-if="recommendation.config.flash_attention"
          class="text-[10px] font-label px-2 py-0.5 rounded-full bg-primary/10 text-primary border border-primary/20">
          ⚡ Flash Attention
        </span>
        <span v-if="recommendation.config.thinking_mode"
          class="text-[10px] font-label px-2 py-0.5 rounded-full bg-purple-500/10 text-purple-400 border border-purple-500/20">
          🧠 Thinking
        </span>
        <span v-if="recommendation.config.jinja"
          class="text-[10px] font-label px-2 py-0.5 rounded-full bg-cyan-500/10 text-cyan-400 border border-cyan-500/20">
          📝 Jinja
        </span>
        <span v-if="recommendation.config.mlock"
          class="text-[10px] font-label px-2 py-0.5 rounded-full bg-orange-500/10 text-orange-400 border border-orange-500/20">
          🔒 Mlock
        </span>
      </div>

      <!-- Expandable Explanation -->
      <button @click="showDetails = !showDetails" type="button"
        class="w-full flex items-center justify-between py-2 text-xs text-on-surface-variant hover:text-on-surface transition-colors">
        <span class="flex items-center gap-1">
          <Info class="w-3.5 h-3.5" />
          {{ t('settings.smart.details') }}
        </span>
        <ChevronDown class="w-3.5 h-3.5 transition-transform duration-300" :class="{ 'rotate-180': showDetails }" />
      </button>

      <div v-show="showDetails" class="space-y-2 animate-fade-in">
        <!-- Hardware info -->
        <div class="bg-surface-container-high/50 rounded-lg p-2.5 space-y-1.5">
          <p class="text-[10px] font-label text-on-surface-variant uppercase tracking-wider mb-1">{{ t('settings.smart.yourHardware') }}</p>
          <div v-for="(value, key) in recommendation.hardware_summary" :key="key"
            class="flex items-center justify-between">
            <span class="text-[11px] text-on-surface-variant uppercase font-label">{{ key }}</span>
            <span class="text-[11px] text-on-surface font-label">{{ value }}</span>
          </div>
        </div>

        <!-- Parameter explanations -->
        <div class="bg-surface-container-high/50 rounded-lg p-2.5 space-y-2">
          <p class="text-[10px] font-label text-on-surface-variant uppercase tracking-wider mb-1">{{ t('settings.smart.whyTheseValues') }}</p>
          <div v-for="(explanation, key) in recommendation.explanation" :key="key" class="space-y-0.5">
            <p class="text-[10px] font-label text-primary uppercase">{{ key }}</p>
            <p class="text-[11px] text-on-surface-variant leading-relaxed">{{ explanation }}</p>
          </div>
        </div>
      </div>

      <!-- Apply Button -->
      <button @click="applyConfig" type="button"
        class="w-full py-2.5 rounded-xl font-semibold text-sm flex items-center justify-center gap-2 transition-all duration-300 active:scale-[0.98]"
        :class="isApplied
          ? 'bg-green-600 text-white shadow-lg shadow-green-600/20'
          : `${tierConfig?.bg} ${tierConfig?.color} border ${tierConfig?.border} hover:opacity-90`
        ">
        <Check v-if="isApplied" class="w-4 h-4" />
        <Zap v-else class="w-4 h-4" />
        {{ isApplied ? t('settings.smart.applied') : t('settings.smart.apply') }}
      </button>
    </div>
  </div>
</template>
