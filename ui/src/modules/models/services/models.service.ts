import { apiClient } from '@/services/api.service'

export interface LocalModel {
  id: string;
  author: string;
  repo: string;
  filename: string;
  size_mb: number;
  path: string;
}

export interface HFModel {
  _id: string;
  id: string;
  downloads: number;
  tags: string[];
}

export interface HFFile {
  type: string;
  path: string;
  size: number;
}

export const ModelsService = {
  async getLocalModels(): Promise<{models: LocalModel[]}> {
    return apiClient.get('/huggingface/local')
  },
  
  async downloadModel(repoId: string, filename: string): Promise<any> {
    return apiClient.post('/huggingface/download', { repo_id: repoId, filename })
  },

  async searchHFModels(query: string): Promise<HFModel[]> {
    if (!query) return []
    const url = `https://huggingface.co/api/models?search=${encodeURIComponent(query)}&filter=gguf&sort=downloads&direction=-1&limit=10`
    const res = await fetch(url)
    if (!res.ok) throw new Error('Failed to fetch from Hugging Face')
    return await res.json()
  },

  async getHFModelFiles(repoId: string): Promise<HFFile[]> {
    if (!repoId) return []
    const url = `https://huggingface.co/api/models/${repoId}/tree/main`
    const res = await fetch(url)
    if (!res.ok) throw new Error('Failed to fetch files from Hugging Face')
    const files: any[] = await res.json()
    return files.filter(f => f.type === 'file' && f.path.endsWith('.gguf'))
  },

  getFileStats(file: HFFile | null, hardwareInfo: any) {
    if (!file || !hardwareInfo) return null
    
    const fileSizeGb = file.size / (1024 * 1024 * 1024)
    const contextBufferGb = 1.5
    const totalNeededGb = fileSizeGb + contextBufferGb
    
    const vramGb = hardwareInfo.gpu.available && hardwareInfo.gpu.free_mb ? hardwareInfo.gpu.free_mb / 1024 : 0
    const ramGb = hardwareInfo.ram.free_gb
    const totalAvailableGb = vramGb + ramGb

    const ramPercentage = totalAvailableGb > 0 ? Math.min(Math.round((totalNeededGb / totalAvailableGb) * 100), 999) : 100
    
    let speed = ''
    let status = ''
    let statusColor = ''
    let bg = ''
    let score = 0
    
    if (totalNeededGb <= vramGb) {
      speed = '~55 tok/s'
      status = 'RUNS WELL'
      statusColor = 'text-green-500'
      bg = 'bg-green-500/10'
      score = 82
    } else if (totalNeededGb <= (vramGb + ramGb)) {
      if (vramGb > 0 && totalNeededGb <= vramGb + (ramGb * 0.5)) {
        speed = '~33 tok/s'
        status = 'DECENT'
        statusColor = 'text-yellow-400'
        bg = 'bg-yellow-400/10'
        score = 61
      } else if (vramGb > 0) {
        speed = '~26 tok/s'
        status = 'TIGHT FIT'
        statusColor = 'text-orange-400'
        bg = 'bg-orange-400/10'
        score = 48
      } else {
        speed = '~12 tok/s'
        status = 'BARELY RUNS'
        statusColor = 'text-red-400'
        bg = 'bg-red-400/10'
        score = 23
      }
    } else {
      speed = '0 tok/s'
      status = 'TOO HEAVY'
      statusColor = 'text-red-600'
      bg = 'bg-red-600/10'
      score = 0
    }

    if (file.path.toLowerCase().includes('mmproj') || file.path.toLowerCase().includes('vision')) {
      speed = 'VISION'
    }

    return { tier: status, speed, desc: `Requires ~${totalNeededGb.toFixed(1)}GB total memory.`, color: statusColor, bg, score, ramPercentage, sizeGb: fileSizeGb }
  }
}
