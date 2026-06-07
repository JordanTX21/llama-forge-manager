import { apiClient } from '@/services/api.service'

export interface LocalModel {
  id: string;
  author: string;
  repo: string;
  filename: string;
  size_mb: number;
  path: string;
}

export const ModelsService = {
  async getLocalModels(): Promise<{models: LocalModel[]}> {
    return apiClient.get('/huggingface/local')
  },
  
  async downloadModel(repoId: string, filename: string): Promise<any> {
    return apiClient.post('/huggingface/download', { repo_id: repoId, filename })
  }
}
