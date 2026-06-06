import { apiClient } from '@/services/api.service'

export interface HardwareStats {
  cpu: {
    cores: number;
    threads: number;
    usage_percent: number;
  };
  ram: {
    total_gb: number;
    free_gb: number;
    usage_percent: number;
  };
  gpu: {
    total_mb: number;
    free_mb: number;
    used_mb: number;
    available: boolean;
  };
}

export const DashboardService = {
  async getHardwareStats(): Promise<HardwareStats> {
    return apiClient.get('/hardware/')
  }
}
