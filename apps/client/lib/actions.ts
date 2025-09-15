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

// Search parameters interface
export interface SearchParams {
  query?: string;
  limit?: number;
  offset?: number;
}

// API functions
export const analysisAPI = {
  // Analyze text
  analyze: async (request: AnalysisRequest): Promise<Analysis> => {
    const response = await api.post<Analysis>("/analyze", request);
    return response.data;
  },

  // Search analyses with pagination support
  search: async (params: SearchParams = {}): Promise<Analysis[]> => {
    const searchParams = new URLSearchParams();

    if (params.query) {
      searchParams.append("topic", params.query);
    }

    if (params.limit !== undefined) {
      searchParams.append("limit", params.limit.toString());
    }

    if (params.offset !== undefined) {
      searchParams.append("offset", params.offset.toString());
    }

    const queryString = searchParams.toString();
    const url = `/search${queryString ? `?${queryString}` : ""}`;

    const response = await api.get<Analysis[]>(url);
    return response.data;
  },
};

export default api;
