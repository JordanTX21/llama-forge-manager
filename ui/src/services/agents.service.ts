import { apiClient } from '@/services/api.service'

export interface AgentInfo {
  id: string;
  name: string;
  image: string;
}

export const AgentsService = {
  async getStatus(): Promise<{ installed: AgentInfo[] }> {
    return apiClient.get('/agents/status')
  },
  async configureAgent(agent_id: string, model_name: string, endpoint: string): Promise<any> {
    return apiClient.post('/agents/configure', { agent_id, model_name, endpoint })
  }
}
