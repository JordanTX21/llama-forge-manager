import { apiClient } from '@/services/api.service'

export interface RunModelOptions {
  model_path: string;
  alias: string;
  ctx_size: number;
  ngl: number;
  port: number;
  flash_attention: boolean;
  thinking_mode: boolean;
}

export interface CommandConfig {
  filename: string;
  model_path: string;
  mmproj_path: string;
  alias: string;
  ctx_size: number;
  ngl: number;
  port: number;
  flash_attention: boolean;
  thinking_mode: boolean;

  threads: number;
  threads_batch: number;
  np: number;
  cr: string;
  crb: string;
  cpu_strict: boolean;
  cpu_strict_batch: boolean;

  batch_size: number;
  ubatch_size: number;
  prio: number;
  prio_batch: number;
  poll: number;
  poll_batch: number;

  cache_type_k: string;
  cache_type_v: string;
  kv_unified: boolean;
  no_mmap: boolean;
  mlock: boolean;

  ncmoe: number;
  spec_type: string;
  spec_draft_n_max: number;

  temp: number;
  top_p: number;
  top_k: number;
  min_p: number;
  presence_penalty: number;
  repeat_penalty: number;

  jinja: boolean;
  raw_content?: string;
}

export const SettingsService = {
  async startModel(options: RunModelOptions): Promise<any> {
    return apiClient.post('/runner/start', options)
  },
  async startSwap(): Promise<any> {
    return apiClient.post('/runner/swap')
  },
  async getCommands(): Promise<CommandConfig[]> {
    return apiClient.get('/commands/')
  },
  async saveCommand(config: CommandConfig): Promise<any> {
    return apiClient.post('/commands/', config)
  },
  async runCommand(filename: string): Promise<any> {
    return apiClient.post('/runner/command', { filename })
  }
}
