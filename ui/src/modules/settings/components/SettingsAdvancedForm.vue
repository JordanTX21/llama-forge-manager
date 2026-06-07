<script setup lang="ts">
import { ref } from 'vue'
import { Field } from 'vee-validate'
import { Settings2, ChevronDown, Info } from '@lucide/vue'
import { LLAMA_DOCS } from '../constants/llama-docs'
import Tooltip from '@/components/Tooltip.vue'

const showAdvanced = ref(false)
</script>

<template>
  <div class="mt-2">
    <button @click="showAdvanced = !showAdvanced" type="button"
      class="w-full flex items-center justify-between p-3 bg-surface-container-high border border-outline rounded-xl hover:bg-surface-variant transition-colors">
      <span class="font-semibold text-on-surface text-sm flex items-center gap-2">
        <Settings2 class="text-primary w-5 h-5" />
        Advanced Settings
      </span>
      <ChevronDown class="transition-transform duration-300 w-5 h-5" :class="{ 'rotate-180': showAdvanced }" />
    </button>

    <div v-show="showAdvanced" class="mt-3 p-5 glass rounded-xl border border-outline space-y-6">

      <!-- Sampling -->
      <div>
        <h4 class="font-headline text-base mb-3 text-primary border-b border-outline pb-1">Sampling</h4>
        <div class="grid grid-cols-2 md:grid-cols-3 gap-3">
          <div>
            <label class="flex items-center gap-1 font-label text-[10px] text-on-surface-variant uppercase">Temperature
              <Tooltip :text="LLAMA_DOCS.temp">
                <Info class="w-3 h-3" />
              </Tooltip>
            </label>
            <Field name="temp" type="number" step="0.1"
              class="w-full bg-surface-container-low border border-outline rounded-lg p-2 text-sm text-on-surface" />
          </div>
          <div>
            <label class="flex items-center gap-1 font-label text-[10px] text-on-surface-variant uppercase">Top P
              <Tooltip :text="LLAMA_DOCS.top_p">
                <Info class="w-3 h-3" />
              </Tooltip>
            </label>
            <Field name="top_p" type="number" step="0.05"
              class="w-full bg-surface-container-low border border-outline rounded-lg p-2 text-sm text-on-surface" />
          </div>
          <div>
            <label class="flex items-center gap-1 font-label text-[10px] text-on-surface-variant uppercase">Top K
              <Tooltip :text="LLAMA_DOCS.top_k">
                <Info class="w-3 h-3" />
              </Tooltip>
            </label>
            <Field name="top_k" type="number"
              class="w-full bg-surface-container-low border border-outline rounded-lg p-2 text-sm text-on-surface" />
          </div>
          <div>
            <label class="flex items-center gap-1 font-label text-[10px] text-on-surface-variant uppercase">Min P
              <Tooltip :text="LLAMA_DOCS.min_p">
                <Info class="w-3 h-3" />
              </Tooltip>
            </label>
            <Field name="min_p" type="number" step="0.05"
              class="w-full bg-surface-container-low border border-outline rounded-lg p-2 text-sm text-on-surface" />
          </div>
          <div>
            <label class="flex items-center gap-1 font-label text-[10px] text-on-surface-variant uppercase">Presence
              Penalty
              <Tooltip :text="LLAMA_DOCS.presence_penalty">
                <Info class="w-3 h-3" />
              </Tooltip>
            </label>
            <Field name="presence_penalty" type="number" step="0.1"
              class="w-full bg-surface-container-low border border-outline rounded-lg p-2 text-sm text-on-surface" />
          </div>
          <div>
            <label class="flex items-center gap-1 font-label text-[10px] text-on-surface-variant uppercase">Repeat
              Penalty
              <Tooltip :text="LLAMA_DOCS.repeat_penalty">
                <Info class="w-3 h-3" />
              </Tooltip>
            </label>
            <Field name="repeat_penalty" type="number" step="0.1"
              class="w-full bg-surface-container-low border border-outline rounded-lg p-2 text-sm text-on-surface" />
          </div>
        </div>
      </div>

      <!-- Memory & Cache -->
      <div>
        <h4 class="font-headline text-base mb-3 text-primary border-b border-outline pb-1">Memory & Cache</h4>
        <div class="grid grid-cols-1 md:grid-cols-2 gap-3">
          <div>
            <label class="flex items-center gap-1 font-label text-[10px] text-on-surface-variant uppercase">Cache Type K
              <Tooltip :text="LLAMA_DOCS.cache_type_k">
                <Info class="w-3 h-3" />
              </Tooltip>
            </label>
            <Field name="cache_type_k" type="text"
              class="w-full bg-surface-container-low border border-outline rounded-lg p-2 text-sm text-on-surface"
              placeholder="q8_0" />
          </div>
          <div>
            <label class="flex items-center gap-1 font-label text-[10px] text-on-surface-variant uppercase">Cache Type V
              <Tooltip :text="LLAMA_DOCS.cache_type_v">
                <Info class="w-3 h-3" />
              </Tooltip>
            </label>
            <Field name="cache_type_v" type="text"
              class="w-full bg-surface-container-low border border-outline rounded-lg p-2 text-sm text-on-surface"
              placeholder="q8_0" />
          </div>
          <div class="flex flex-col gap-2 mt-1">
            <label class="flex items-center gap-2 cursor-pointer">
              <Field name="kv_unified" type="checkbox" :value="true" :unchecked-value="false"
                class="w-4 h-4 rounded bg-surface-container-low border-outline text-primary focus:ring-primary focus:ring-offset-surface" />
              <span class="text-[13px] font-medium text-on-surface flex items-center gap-1">KV Unified
                <Tooltip :text="LLAMA_DOCS.kv_unified">
                  <Info class="w-3 h-3 text-on-surface-variant" />
                </Tooltip>
              </span>
            </label>
            <label class="flex items-center gap-2 cursor-pointer">
              <Field name="no_mmap" type="checkbox" :value="true" :unchecked-value="false"
                class="w-4 h-4 rounded bg-surface-container-low border-outline text-primary focus:ring-primary focus:ring-offset-surface" />
              <span class="text-[13px] font-medium text-on-surface flex items-center gap-1">No Mmap
                <Tooltip :text="LLAMA_DOCS.no_mmap">
                  <Info class="w-3 h-3 text-on-surface-variant" />
                </Tooltip>
              </span>
            </label>
            <label class="flex items-center gap-2 cursor-pointer">
              <Field name="mlock" type="checkbox" :value="true" :unchecked-value="false"
                class="w-4 h-4 rounded bg-surface-container-low border-outline text-primary focus:ring-primary focus:ring-offset-surface" />
              <span class="text-[13px] font-medium text-on-surface flex items-center gap-1">Mlock
                <Tooltip :text="LLAMA_DOCS.mlock">
                  <Info class="w-3 h-3 text-on-surface-variant" />
                </Tooltip>
              </span>
            </label>
          </div>
        </div>
      </div>

      <!-- Compute & Threads -->
      <div>
        <h4 class="font-headline text-base mb-3 text-primary border-b border-outline pb-1">Compute & Threads (-1 =
          Default)</h4>
        <div class="grid grid-cols-2 md:grid-cols-3 gap-3">
          <div>
            <label class="flex items-center gap-1 font-label text-[10px] text-on-surface-variant uppercase">Threads (-t)
              <Tooltip :text="LLAMA_DOCS.threads">
                <Info class="w-3 h-3" />
              </Tooltip>
            </label>
            <Field name="threads" type="number"
              class="w-full bg-surface-container-low border border-outline rounded-lg p-2 text-sm text-on-surface" />
          </div>
          <div>
            <label class="flex items-center gap-1 font-label text-[10px] text-on-surface-variant uppercase">Threads
              Batch (-tb)
              <Tooltip :text="LLAMA_DOCS.threads_batch">
                <Info class="w-3 h-3" />
              </Tooltip>
            </label>
            <Field name="threads_batch" type="number"
              class="w-full bg-surface-container-low border border-outline rounded-lg p-2 text-sm text-on-surface" />
          </div>
          <div>
            <label class="flex items-center gap-1 font-label text-[10px] text-on-surface-variant uppercase">Num
              Processes (-np)
              <Tooltip :text="LLAMA_DOCS.np">
                <Info class="w-3 h-3" />
              </Tooltip>
            </label>
            <Field name="np" type="number"
              class="w-full bg-surface-container-low border border-outline rounded-lg p-2 text-sm text-on-surface" />
          </div>
          <div>
            <label class="flex items-center gap-1 font-label text-[10px] text-on-surface-variant uppercase">Core Ratio
              (-Cr)
              <Tooltip :text="LLAMA_DOCS.cr">
                <Info class="w-3 h-3" />
              </Tooltip>
            </label>
            <Field name="cr" type="text"
              class="w-full bg-surface-container-low border border-outline rounded-lg p-2 text-sm text-on-surface"
              placeholder="e.g. 0-11" />
          </div>
          <div>
            <label class="flex items-center gap-1 font-label text-[10px] text-on-surface-variant uppercase">Core Ratio
              Batch
              <Tooltip :text="LLAMA_DOCS.crb">
                <Info class="w-3 h-3" />
              </Tooltip>
            </label>
            <Field name="crb" type="text"
              class="w-full bg-surface-container-low border border-outline rounded-lg p-2 text-sm text-on-surface"
              placeholder="e.g. 0-11" />
          </div>
          <div class="flex flex-col gap-2 justify-end pb-1">
            <label class="flex items-center gap-2 cursor-pointer">
              <Field name="cpu_strict" type="checkbox" :value="true" :unchecked-value="false"
                class="w-4 h-4 rounded bg-surface-container-low border-outline text-primary focus:ring-primary focus:ring-offset-surface" />
              <span class="text-[13px] font-medium text-on-surface flex items-center gap-1">CPU Strict
                <Tooltip :text="LLAMA_DOCS.cpu_strict">
                  <Info class="w-3 h-3 text-on-surface-variant" />
                </Tooltip>
              </span>
            </label>
            <label class="flex items-center gap-2 cursor-pointer">
              <Field name="cpu_strict_batch" type="checkbox" :value="true" :unchecked-value="false"
                class="w-4 h-4 rounded bg-surface-container-low border-outline text-primary focus:ring-primary focus:ring-offset-surface" />
              <span class="text-[13px] font-medium text-on-surface flex items-center gap-1">CPU Strict Batch
                <Tooltip :text="LLAMA_DOCS.cpu_strict_batch">
                  <Info class="w-3 h-3 text-on-surface-variant" />
                </Tooltip>
              </span>
            </label>
          </div>
        </div>
      </div>

      <!-- Batching & Processing -->
      <div>
        <h4 class="font-headline text-base mb-3 text-primary border-b border-outline pb-1">Batching (-1 = Default)</h4>
        <div class="grid grid-cols-2 md:grid-cols-3 gap-3">
          <div>
            <label class="flex items-center gap-1 font-label text-[10px] text-on-surface-variant uppercase">Batch Size
              (-b)
              <Tooltip :text="LLAMA_DOCS.batch_size">
                <Info class="w-3 h-3" />
              </Tooltip>
            </label>
            <Field name="batch_size" type="number"
              class="w-full bg-surface-container-low border border-outline rounded-lg p-2 text-sm text-on-surface" />
          </div>
          <div>
            <label class="flex items-center gap-1 font-label text-[10px] text-on-surface-variant uppercase">UBatch Size
              (-ub)
              <Tooltip :text="LLAMA_DOCS.ubatch_size">
                <Info class="w-3 h-3" />
              </Tooltip>
            </label>
            <Field name="ubatch_size" type="number"
              class="w-full bg-surface-container-low border border-outline rounded-lg p-2 text-sm text-on-surface" />
          </div>
          <div>
            <label class="flex items-center gap-1 font-label text-[10px] text-on-surface-variant uppercase">Prio
              <Tooltip :text="LLAMA_DOCS.prio">
                <Info class="w-3 h-3" />
              </Tooltip>
            </label>
            <Field name="prio" type="number"
              class="w-full bg-surface-container-low border border-outline rounded-lg p-2 text-sm text-on-surface" />
          </div>
          <div>
            <label class="flex items-center gap-1 font-label text-[10px] text-on-surface-variant uppercase">Prio Batch
              <Tooltip :text="LLAMA_DOCS.prio_batch">
                <Info class="w-3 h-3" />
              </Tooltip>
            </label>
            <Field name="prio_batch" type="number"
              class="w-full bg-surface-container-low border border-outline rounded-lg p-2 text-sm text-on-surface" />
          </div>
          <div>
            <label class="flex items-center gap-1 font-label text-[10px] text-on-surface-variant uppercase">Poll (%)
              <Tooltip :text="LLAMA_DOCS.poll">
                <Info class="w-3 h-3" />
              </Tooltip>
            </label>
            <Field name="poll" type="number"
              class="w-full bg-surface-container-low border border-outline rounded-lg p-2 text-sm text-on-surface" />
          </div>
          <div>
            <label class="flex items-center gap-1 font-label text-[10px] text-on-surface-variant uppercase">Poll Batch
              (%)
              <Tooltip :text="LLAMA_DOCS.poll_batch">
                <Info class="w-3 h-3" />
              </Tooltip>
            </label>
            <Field name="poll_batch" type="number"
              class="w-full bg-surface-container-low border border-outline rounded-lg p-2 text-sm text-on-surface" />
          </div>
        </div>
      </div>

      <!-- MoE & Speculative -->
      <div>
        <h4 class="font-headline text-base mb-3 text-primary border-b border-outline pb-1">MoE & Speculative Decoding
        </h4>
        <div class="grid grid-cols-1 md:grid-cols-3 gap-3">
          <div>
            <label class="flex items-center gap-1 font-label text-[10px] text-on-surface-variant uppercase">MoE Cores
              (-ncmoe)
              <Tooltip :text="LLAMA_DOCS.ncmoe">
                <Info class="w-3 h-3" />
              </Tooltip>
            </label>
            <Field name="ncmoe" type="number"
              class="w-full bg-surface-container-low border border-outline rounded-lg p-2 text-sm text-on-surface" />
          </div>
          <div>
            <label class="flex items-center gap-1 font-label text-[10px] text-on-surface-variant uppercase">Spec Type
              <Tooltip :text="LLAMA_DOCS.spec_type">
                <Info class="w-3 h-3" />
              </Tooltip>
            </label>
            <Field name="spec_type" type="text"
              class="w-full bg-surface-container-low border border-outline rounded-lg p-2 text-sm text-on-surface"
              placeholder="draft-mtp" />
          </div>
          <div>
            <label class="flex items-center gap-1 font-label text-[10px] text-on-surface-variant uppercase">Spec Draft
              Max N
              <Tooltip :text="LLAMA_DOCS.spec_draft_n_max">
                <Info class="w-3 h-3" />
              </Tooltip>
            </label>
            <Field name="spec_draft_n_max" type="number"
              class="w-full bg-surface-container-low border border-outline rounded-lg p-2 text-sm text-on-surface" />
          </div>
        </div>
      </div>

      <!-- Misc -->
      <div>
        <h4 class="font-headline text-base mb-3 text-primary border-b border-outline pb-1">Misc</h4>
        <label class="flex items-center gap-2 cursor-pointer">
          <Field name="jinja" type="checkbox" :value="true" :unchecked-value="false"
            class="w-4 h-4 rounded bg-surface-container-low border-outline text-primary focus:ring-primary focus:ring-offset-surface" />
          <span class="text-[13px] font-medium text-on-surface flex items-center gap-1">Jinja Template Engine
            <Tooltip :text="LLAMA_DOCS.jinja">
              <Info class="w-3 h-3 text-on-surface-variant" />
            </Tooltip>
          </span>
        </label>
      </div>

    </div>
  </div>
</template>
