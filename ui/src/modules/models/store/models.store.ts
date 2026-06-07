import { defineStore } from 'pinia'
import { ref } from 'vue'
import { ModelsService, type LocalModel } from '../services/models.service'

export const useModelsStore = defineStore('models', () => {
  const models = ref<LocalModel[]>([])
  const isDownloading = ref(false)

  const fetchModels = async () => {
    try {
      const res = await ModelsService.getLocalModels()
      models.value = res.models
    } catch (err) {
      console.error('Error fetching models', err)
    }
  }

  const downloadModel = async (repoId: string, filename: string) => {
    isDownloading.value = true
    try {
      await ModelsService.downloadModel(repoId, filename)
      setTimeout(fetchModels, 2000)
    } finally {
      isDownloading.value = false
    }
  }

  return { models, isDownloading, fetchModels, downloadModel }
})
