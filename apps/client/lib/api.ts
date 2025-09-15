import axios from 'axios'
import { Analysis, AnalysisRequest } from './types'

// Create axios instance
const api = axios.create({
  baseURL: process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000/api/v1',
  headers: {
    'Content-Type': 'application/json',
  },
})

// API response interceptor for error handling
api.interceptors.response.use(
  (response) => response,
  (error) => {
    console.error('API Error:', error.response?.data || error.message)
    return Promise.reject(error)
  }
)

// API functions
export const analysisAPI = {
  // Analyze text
  analyze: async (request: AnalysisRequest): Promise<Analysis> => {
    const response = await api.post<Analysis>('/analyze', request)
    return response.data
  },

  // Get all analyses (for history)
  getAnalyses: async (): Promise<Analysis[]> => {
    const response = await api.get<Analysis[]>('/search')
    return response.data
  },

  // Search analyses by topic/keyword
  search: async (topic: string): Promise<Analysis[]> => {
    const response = await api.get<Analysis[]>(`/search?topic=${encodeURIComponent(topic)}`)
    return response.data
  },

  // Get single analysis by ID (if needed for individual pages)
  getAnalysis: async (id: number): Promise<Analysis> => {
    // Note: You'd need to add this endpoint to your FastAPI backend
    // For now, we'll get all and filter (not optimal but works)
    const analyses = await analysisAPI.getAnalyses()
    const analysis = analyses.find(a => a.id === id)
    if (!analysis) {
      throw new Error('Analysis not found')
    }
    return analysis
  }
}

export default api