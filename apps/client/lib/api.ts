import axios from "axios";
import { Analysis, AnalysisRequest } from "./types";

// Create axios instance
const api = axios.create({
  baseURL: process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000/api/v1",
  headers: {
    "Content-Type": "application/json",
  },
});

// API response interceptor for error handling
api.interceptors.response.use(
  (response) => response,
  (error) => {
    console.error("API Error:", error.response?.data || error.message);
    return Promise.reject(error);
  }
);

// API functions
export const analysisAPI = {
  // Analyze text
  analyze: async (request: AnalysisRequest): Promise<Analysis> => {
    const response = await api.post<Analysis>("/analyze", request);
    return response.data;
  },

  // Search analyses (replaces getAnalyses - empty query returns all)
  search: async (query?: string): Promise<Analysis[]> => {
    const searchParams = query ? `?topic=${encodeURIComponent(query)}` : '';
    const response = await api.get<Analysis[]>(`/search${searchParams}`);
    return response.data;
  },
};

export default api;
