// API client for BrainDump backend
const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000';

export interface DumpRequest {
  user_input: string;
  user_id: string;
  tags?: string[];
}

export interface DumpResponse {
  plan: string[];
  reset_tip: string;
  motivation: string;
  stress_score: number;
}

export interface HealthResponse {
  ok: boolean;
}

class ApiClient {
  private baseUrl: string;

  constructor(baseUrl: string) {
    this.baseUrl = baseUrl;
  }

  private async request<T>(
    endpoint: string,
    options: RequestInit = {}
  ): Promise<T> {
    const url = `${this.baseUrl}${endpoint}`;
    
    const config: RequestInit = {
      headers: {
        'Content-Type': 'application/json',
        ...options.headers,
      },
      ...options,
    };

    try {
      const response = await fetch(url, config);
      
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
      
      return await response.json();
    } catch (error) {
      console.error('API request failed:', error);
      throw error;
    }
  }

  async healthCheck(): Promise<HealthResponse> {
    return this.request<HealthResponse>('/health');
  }

  async createDump(dumpData: DumpRequest): Promise<DumpResponse> {
    return this.request<DumpResponse>('/dump', {
      method: 'POST',
      body: JSON.stringify(dumpData),
    });
  }

  async getRecentEntries(userId: string, limit: number = 5): Promise<any[]> {
    return this.request<any[]>(`/recent/${userId}?limit=${limit}`);
  }
}

export const apiClient = new ApiClient(API_BASE_URL);
