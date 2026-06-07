<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useModelsStore } from '../store/models.store'
import { storeToRefs } from 'pinia'
import { LayoutGrid, List } from '@lucide/vue'
import ModelDownloadForm from '../components/ModelDownloadForm.vue'
import ModelGallery from '../components/ModelGallery.vue'

const store = useModelsStore()
const { models } = storeToRefs(store)

const isListView = ref(false)

onMounted(() => {
  store.fetchModels()
})
</script>

<template>
  <div class="space-y-8 w-full max-w-[1200px] mx-auto">
    <!-- Header Section -->
    <header class="hidden md:block">
      <h2 class="font-headline text-3xl text-on-surface mb-1 font-semibold tracking-tight">Model Hub</h2>
      <p class="text-on-surface-variant font-body text-sm">Manage and orchestrate your local machine learning environment.</p>
    </header>

    <div class="flex flex-col gap-8">
      <!-- Download Section -->
      <section>
        <ModelDownloadForm />
      </section>

      <!-- Grid/List Section -->
      <section>
        <div class="flex items-center justify-between mb-6">
          <h3 class="font-headline text-xl text-on-surface font-semibold">Downloaded Models</h3>
          <div class="flex items-center gap-4">
            
            <!-- List/Grid Toggle -->
            <div class="flex bg-surface-container-high rounded-lg p-1 border border-outline">
              <button @click="isListView = false" :class="!isListView ? 'bg-surface-container-low shadow text-primary' : 'text-on-surface-variant hover:text-on-surface'" class="p-1.5 rounded-md flex items-center justify-center transition-colors">
                <LayoutGrid class="w-[18px] h-[18px]" />
              </button>
              <button @click="isListView = true" :class="isListView ? 'bg-surface-container-low shadow text-primary' : 'text-on-surface-variant hover:text-on-surface'" class="p-1.5 rounded-md flex items-center justify-center transition-colors">
                <List class="w-[18px] h-[18px]" />
              </button>
            </div>

            <div class="flex items-center gap-2 px-3 py-1.5 glass rounded-full border border-outline text-[10px] font-label text-on-surface-variant">
              <span class="w-1.5 h-1.5 rounded-full bg-green-500"></span>
              Local System Online
            </div>
          </div>
        </div>

        <ModelGallery :models="models" :is-list-view="isListView" />
      </section>
    </div>
  </div>
</template>
