import { apiClient } from './api.service'

export interface HardwareInfo {
  cpu: {
    cores: number
    threads: number
    usage_percent: number
  }
  ram: {
    total_gb: number
    free_gb: number
    usage_percent: number
  }
  gpu: {
    available: boolean
    total_mb?: number
    free_mb?: number
    used_mb?: number
    error?: string
  }
}

export const HardwareService = {
  async getHardwareInfo(): Promise<HardwareInfo> {
    const response = await apiClient.get<HardwareInfo>('/hardware/')
    return response as unknown as HardwareInfo
  }
}
