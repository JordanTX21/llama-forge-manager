<script setup lang="ts">
import { Field, ErrorMessage } from 'vee-validate'
import { Terminal, Info } from '@lucide/vue'
</script>

<template>
  <div class="space-y-2 animate-fade-in">
    <div class="flex items-center justify-between mb-2">
      <label class="flex items-center gap-2 font-label text-xs text-on-surface-variant uppercase tracking-wider">
        <Terminal class="w-4 h-4 text-primary" />
        Raw PowerShell Script
      </label>
      <span class="text-[10px] text-on-surface-variant bg-surface-container-high px-2 py-0.5 rounded font-mono border border-outline">.ps1</span>
    </div>
    
    <div class="relative group">
      <Field name="raw_content" as="textarea" rows="12" class="w-full bg-[#1e1e1e] border border-outline rounded-xl p-4 text-[13px] font-mono text-[#d4d4d4] focus:outline-none focus:border-primary transition-colors resize-y leading-relaxed shadow-inner" placeholder="# Llama Server Execution Script
$env:LLAMA_BIN_DIR = 'C:\llama.cpp\bin'
...
" />
      <ErrorMessage name="raw_content" class="text-red-400 text-xs mt-1 absolute -bottom-5 left-1" />
    </div>
    
    <div class="mt-3 p-3 bg-primary-container/10 border border-primary/20 rounded-lg flex items-start gap-2">
      <Info class="text-primary w-5 h-5 mt-0.5" />
      <p class="text-xs text-on-surface-variant leading-relaxed">
        You are editing the raw script. 
        <strong class="text-on-surface">The server will automatically parse your changes.</strong>
        If you introduce a syntax error or omit required flags (like <code class="bg-surface-variant px-1 py-0.5 rounded">-a</code> or <code class="bg-surface-variant px-1 py-0.5 rounded">-m</code>), the server will reject the save to prevent corruption.
      </p>
    </div>
  </div>
</template>
