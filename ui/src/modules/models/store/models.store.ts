import { defineStore } from 'pinia'
import { ref } from 'vue'
import { ModelsService, type LocalModel } from '../services/models.service'

export const useModelsStore = defineStore('models', () => {
  const models = ref<LocalModel[]>([])
  const isDownloading = ref(false)
  const downloadProgress = ref(0)
  const downloadSpeed = ref('')
  const downloadEta = ref('')
  const downloadStatusText = ref('')
  const downloadedSize = ref('')
  const totalSize = ref('')

  let pollInterval: any = null

  const fetchModels = async () => {
    try {
      const res = await ModelsService.getLocalModels()
      models.value = res.models
    } catch (err) {
      console.error('Error fetching models', err)
    }
  }

  const startPolling = (repoId: string, filename: string) => {
    if (pollInterval) clearInterval(pollInterval)
    pollInterval = setInterval(async () => {
      try {
        const status = await ModelsService.getDownloadStatus(repoId, filename)
        if (status.status === 'downloading' || status.status === 'completed') {
          downloadProgress.value = status.progress
          downloadSpeed.value = status.speed
          downloadEta.value = status.eta
          downloadedSize.value = status.downloaded
          totalSize.value = status.total
          downloadStatusText.value = status.status === 'completed' ? 'Completed' : 'Downloading...'
        }
        
        if (status.status === 'completed' || status.status === 'error' || status.status === 'idle') {
          clearInterval(pollInterval)
          if (status.status === 'completed') {
            isDownloading.value = false
            setTimeout(fetchModels, 2000)
          } else if (status.status === 'error') {
            isDownloading.value = false
            downloadStatusText.value = 'Error'
          }
        }
      } catch (e) {
        console.error('Polling error', e)
      }
    }, 500)
  }

  const downloadModel = async (repoId: string, filename: string) => {
    isDownloading.value = true
    downloadProgress.value = 0
    downloadSpeed.value = ''
    downloadEta.value = ''
    downloadedSize.value = ''
    totalSize.value = ''
    downloadStatusText.value = 'Starting...'
    
    try {
      await ModelsService.downloadModel(repoId, filename)
      startPolling(repoId, filename)
    } catch (e) {
      isDownloading.value = false
      downloadStatusText.value = 'Failed to start'
    }
  }

  return { 
    models, 
    isDownloading, 
    downloadProgress,
    downloadSpeed,
    downloadEta,
    downloadStatusText,
    downloadedSize,
    totalSize,
    fetchModels, 
    downloadModel 
  }
})
