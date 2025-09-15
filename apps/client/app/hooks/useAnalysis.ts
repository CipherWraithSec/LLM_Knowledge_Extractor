"use client";

import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query";
import useDebounce from "./useDebounce";
import { useSearch } from "@/lib/redux/features/search/searchSlice";
import { analysisAPI } from "@/lib/api";
import { Analysis, AnalysisRequest } from "@/lib/types";

export const QUERY_KEYS = {
  analyses: "analyses",
  search: (query: string) => ["analyses", "search", query],
  all: () => ["analyses", "search", "all"],
} as const;

// Search analyses
export const useAnalysisQuery = () => {
  const { query } = useSearch();

  const debouncedSearch = useDebounce(query, 300);

  const normalizedQuery = debouncedSearch.trim();

  // Dynamic query key based on search term
  const queryKey = normalizedQuery
    ? QUERY_KEYS.search(normalizedQuery)
    : QUERY_KEYS.all();

  return useQuery({
    queryKey,
    queryFn: () => analysisAPI.search(normalizedQuery || undefined),
    staleTime: 5 * 60 * 1000, // 5 minutes - data considered fresh
    gcTime: 10 * 60 * 1000, // 10 minutes - cache retention time
    refetchOnWindowFocus: false,
    refetchOnReconnect: true,
  });
};

// creating new analyses with automatic cache invalidation
export const useCreateAnalysis = () => {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: (request: AnalysisRequest) => analysisAPI.analyze(request),

    onSuccess: (newAnalysis: Analysis) => {
      // Invalidate all search-related queries to ensure fresh data
      queryClient.invalidateQueries({
        queryKey: [QUERY_KEYS.analyses, "search"],
        exact: false,
      });

      // Optionally, optimistically update specific queries
      // queryClient.setQueryData(QUERY_KEYS.all(), (oldData: Analysis[] | undefined) => {
      //   return oldData ? [newAnalysis, ...oldData] : [newAnalysis];
      // });
    },

    onError: (error) => {
      console.error("Failed to create analysis:", error);
      // Could add toast notification here
    },
  });
};

// Getting a specific analysis by ID
export const useAnalysis = (id: number, enabled = true) => {
  return useQuery({
    queryKey: [QUERY_KEYS.analyses, "single", id],
    queryFn: async () => {
      const analyses = await analysisAPI.search();
      const analysis = analyses.find((a) => a.id === id);
      if (!analysis) {
        throw new Error(`Analysis with ID ${id} not found`);
      }
      return analysis;
    },
    enabled: enabled && !!id,
    staleTime: 10 * 60 * 1000, // Single analyses stay fresh longer
  });
};
