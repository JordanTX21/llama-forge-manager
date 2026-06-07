import { apiClient } from '@/services/api.service'

export interface RecommendedConfig {
  ngl: number
  ctx_size: number
  threads: number
  threads_batch: number
  flash_attention: boolean
  cache_type_k: string
  cache_type_v: string
  batch_size: number
  ubatch_size: number
  thinking_mode: boolean
  jinja: boolean
  mlock: boolean
  no_mmap: boolean
}

export interface Recommendation {
  config: RecommendedConfig
  confidence: 'high' | 'medium' | 'low'
  tier: 'OPTIMAL' | 'GOOD' | 'CONSTRAINED'
  explanation: Record<string, string>
  hardware_summary: Record<string, string>
  model_summary: Record<string, string>
}

export const RecommendService = {
  async getRecommendation(
    modelPath: string,
    sizeMb: number,
    filename: string
  ): Promise<Recommendation> {
    return apiClient.post('/recommend/', {
      model_path: modelPath,
      model_size_mb: sizeMb,
      filename
    })
  }
}
