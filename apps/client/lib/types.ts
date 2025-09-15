import { z } from 'zod'

// Analysis data structure matching your FastAPI backend
export interface Analysis {
  id: number
  title: string | null
  topics: string[]
  sentiment: 'positive' | 'negative' | 'neutral'
  keywords: string[]
  summary: string
  original_text: string
  confidence_score: number
  createdAt: string
}

// API request/response schemas
export const AnalysisRequestSchema = z.object({
  text: z.string().min(1, 'Text cannot be empty').max(10000, 'Text too long')
})

export type AnalysisRequest = z.infer<typeof AnalysisRequestSchema>

// API response types
export interface ApiResponse<T> {
  data: T
  success: boolean
  message?: string
}

// Search/filter types
export interface SearchFilters {
  query: string
  sentiment?: 'positive' | 'negative' | 'neutral'
  dateFrom?: string
  dateTo?: string
}

// Pagination types
export interface PaginationParams {
  limit?: number
  offset?: number
}

export interface SearchParams extends PaginationParams {
  query?: string
}

// Infinite query pagination for React Query
export interface InfiniteQueryPage {
  data: Analysis[]
  nextOffset?: number
  hasMore: boolean
}

// UI state types
export interface AnalysisModalState {
  isOpen: boolean
  text: string
}

export interface SearchState {
  query: string
  filters: SearchFilters
  isSearching: boolean
  pagination: {
    limit: number
  }
}

// Sentiment emoji mapping
export const SENTIMENT_EMOJIS: Record<string, string> = {
  positive: '😊',
  negative: '😟',
  neutral: '😐'
}

// Confidence level colors
export const getConfidenceColor = (score: number): string => {
  if (score >= 90) return 'text-green-600'
  if (score >= 70) return 'text-yellow-600'
  return 'text-red-600'
}

// Date formatting helper
export const formatDate = (dateString: string): string => {
  const date = new Date(dateString)
  return date.toLocaleDateString('en-US', {
    month: 'short',
    day: 'numeric',
    hour: 'numeric',
    minute: '2-digit',
    hour12: true
  })
}