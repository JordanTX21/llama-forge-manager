<script setup lang="ts">
import { useRoute } from 'vue-router'
import { useI18n } from 'vue-i18n'
import AppToast from './components/AppToast.vue'
import { onMounted } from 'vue'

const route = useRoute()
const { t, locale } = useI18n()

const changeLanguage = (event: Event) => {
  const target = event.target as HTMLSelectElement
  locale.value = target.value
  localStorage.setItem('language', target.value)
  document.documentElement.lang = target.value
}

onMounted(() => {
  document.documentElement.lang = locale.value as string
})
</script>

<template>
  <div class="flex h-screen bg-black text-on-surface font-headline overflow-hidden">
    <!-- Visual Polish: Background Ambient Glow -->
    <div class="fixed top-1/4 -right-24 w-64 h-64 bg-primary opacity-5 blur-[120px] pointer-events-none z-0"></div>
    <div class="fixed bottom-1/4 -left-24 w-64 h-64 bg-primary opacity-5 blur-[120px] pointer-events-none z-0"></div>

    <!-- Top AppBar (Mobile mostly, or Desktop Header) -->
    <header
      class="fixed top-0 w-full z-40 glass border-b border-outline flex items-center justify-between px-6 h-16 md:hidden">
      <div class="flex items-center gap-3">
        <h1
          class="text-xl font-bold bg-clip-text text-transparent bg-linear-to-r from-blue-400 to-blue-600 tracking-tight">
          LlamaForgeManager</h1>
      </div>
      <!-- Mobile Language Switcher -->
      <select :value="locale" @change="changeLanguage" class="bg-surface-container-low text-sm rounded-lg px-2 py-1 border border-outline text-on-surface outline-none">
        <option value="en">EN</option>
        <option value="es">ES</option>
      </select>
    </header>

    <!-- Sidebar (Desktop) -->
    <aside class="hidden md:flex w-72 glass border-r border-outline flex-col z-30">
      <div class="p-6 h-16 flex items-center">
        <h1
          class="text-2xl font-bold bg-clip-text text-transparent bg-linear-to-r from-blue-400 to-blue-600 tracking-tight">
          LlamaForgeManager
        </h1>
      </div>
      <nav class="flex-1 px-4 space-y-2 mt-4">
        <router-link to="/"
          :class="['w-full flex items-center px-4 py-3 text-sm font-medium rounded-xl transition-all duration-200', route.name === 'dashboard' ? 'bg-primary-container text-primary' : 'text-on-surface-variant hover:bg-surface-container-low hover:text-on-surface']">
          <svg class="w-5 h-5 mr-3" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
              d="M3 12l2-2m0 0l7-7 7 7M5 10v10a1 1 0 001 1h3m10-11l2 2m-2-2v10a1 1 0 01-1 1h-3m-6 0a1 1 0 001-1v-4a1 1 0 011-1h2a1 1 0 011 1v4a1 1 0 001 1m-6 0h6" />
          </svg>
          {{ t('nav.dashboard') }}
        </router-link>
        <router-link to="/models"
          :class="['w-full flex items-center px-4 py-3 text-sm font-medium rounded-xl transition-all duration-200', route.name === 'models' ? 'bg-primary-container text-primary' : 'text-on-surface-variant hover:bg-surface-container-low hover:text-on-surface']">
          <svg class="w-5 h-5 mr-3" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
              d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-4l-4 4m0 0l-4-4m4 4V4" />
          </svg>
          {{ t('nav.models') }}
        </router-link>
        <router-link to="/settings"
          :class="['w-full flex items-center px-4 py-3 text-sm font-medium rounded-xl transition-all duration-200', route.name === 'settings' ? 'bg-primary-container text-primary' : 'text-on-surface-variant hover:bg-surface-container-low hover:text-on-surface']">
          <svg class="w-5 h-5 mr-3" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
              d="M10.325 4.317c.426-1.756 2.924-1.756 3.35 0a1.724 1.724 0 002.573 1.066c1.543-.94 3.31.826 2.37 2.37a1.724 1.724 0 001.065 2.572c1.756.426 1.756 2.924 0 3.35a1.724 1.724 0 00-1.066 2.573c.94 1.543-.826 3.31-2.37 2.37a1.724 1.724 0 00-2.572 1.065c-.426 1.756-2.924 1.756-3.35 0a1.724 1.724 0 00-2.573-1.066c-1.543.94-3.31-.826-2.37-2.37a1.724 1.724 0 00-1.065-2.572c-1.756-.426-1.756-2.924 0-3.35a1.724 1.724 0 001.066-2.573c-.94-1.543.826-3.31 2.37-2.37.996.608 2.296.07 2.572-1.065z" />
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
              d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
          </svg>
          {{ t('nav.settings') }}
        </router-link>
      </nav>
      
      <!-- Desktop Language Switcher -->
      <div class="p-4 px-6 border-t border-outline flex items-center justify-between">
         <span class="text-sm font-label text-on-surface-variant">Language</span>
         <select :value="locale" @change="changeLanguage" class="bg-surface-container-low text-sm rounded-lg px-2 py-1 border border-outline text-on-surface outline-none cursor-pointer">
           <option value="en">English</option>
           <option value="es">Español</option>
         </select>
      </div>

      <div class="p-6 border-t border-outline">
        <div class="flex items-center space-x-3 text-sm">
          <div class="w-2 h-2 rounded-full bg-primary ai-pulse"></div>
          <span class="text-on-surface font-label">{{ t('nav.engineOnline') }}</span>
        </div>
      </div>
    </aside>

    <!-- Main Content -->
    <main class="flex-1 overflow-y-auto pt-20 md:pt-8 pb-32 md:pb-8 px-4 md:px-12 z-10 relative">
      <router-view v-slot="{ Component }">
        <transition name="fade" mode="out-in">
          <component :is="Component" />
        </transition>
      </router-view>
    </main>

    <!-- Bottom Navigation Bar (Mobile) -->
    <nav
      class="fixed bottom-0 w-full z-50 glass border-t border-outline flex justify-around items-center h-20 px-4 pb-4 md:hidden">
      <router-link to="/"
        :class="['flex flex-col items-center justify-center transition-transform active:scale-95', route.name === 'dashboard' ? 'text-primary' : 'text-on-surface-variant']">
        <svg class="w-6 h-6 mb-1" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
            d="M3 12l2-2m0 0l7-7 7 7M5 10v10a1 1 0 001 1h3m10-11l2 2m-2-2v10a1 1 0 01-1 1h-3m-6 0a1 1 0 001-1v-4a1 1 0 011-1h2a1 1 0 011 1v4a1 1 0 001 1m-6 0h6" />
        </svg>
        <span class="text-xs font-label">{{ t('nav.dashboard') }}</span>
      </router-link>
      <router-link to="/models"
        :class="['flex flex-col items-center justify-center transition-transform active:scale-95', route.name === 'models' ? 'text-primary' : 'text-on-surface-variant']">
        <svg class="w-6 h-6 mb-1" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
            d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-4l-4 4m0 0l-4-4m4 4V4" />
        </svg>
        <span class="text-xs font-label">{{ t('nav.models') }}</span>
      </router-link>
      <router-link to="/settings"
        :class="['flex flex-col items-center justify-center transition-transform active:scale-95', route.name === 'settings' ? 'text-primary' : 'text-on-surface-variant']">
        <svg class="w-6 h-6 mb-1" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
            d="M10.325 4.317c.426-1.756 2.924-1.756 3.35 0a1.724 1.724 0 002.573 1.066c1.543-.94 3.31.826 2.37 2.37a1.724 1.724 0 001.065 2.572c1.756.426 1.756 2.924 0 3.35a1.724 1.724 0 00-1.066 2.573c.94 1.543-.826 3.31-2.37 2.37a1.724 1.724 0 00-2.572 1.065c-.426 1.756-2.924 1.756-3.35 0a1.724 1.724 0 00-2.573-1.066c-1.543.94-3.31-.826-2.37-2.37a1.724 1.724 0 00-1.065-2.572c-1.756-.426-1.756-2.924 0-3.35a1.724 1.724 0 001.066-2.573c-.94-1.543.826-3.31 2.37-2.37.996.608 2.296.07 2.572-1.065z" />
        </svg>
        <span class="text-xs font-label">{{ t('nav.settings') }}</span>
      </router-link>
    </nav>
    <AppToast />
  </div>
</template>

<style>
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.3s ease, transform 0.3s ease;
}

.fade-enter-from {
  opacity: 0;
  transform: translateY(10px);
}

.fade-leave-to {
  opacity: 0;
  transform: translateY(-10px);
}
</style>
