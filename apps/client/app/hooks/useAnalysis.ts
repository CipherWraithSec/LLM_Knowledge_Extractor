"use client";

import {
  useQuery,
  useMutation,
  useQueryClient,
  useInfiniteQuery,
} from "@tanstack/react-query";
import useDebounce from "./useDebounce";
import { useSearch } from "@/lib/redux/features/search/searchSlice";
import { analysisAPI } from "@/lib/api";
import { Analysis, AnalysisRequest } from "@/lib/types";

export const QUERY_KEYS = {
  analyses: "analyses",
  search: (query: string) => ["analyses", "search", query],
} as const;

// Search analyses with infinite scrolling
export const useAnalysisQuery = () => {
  const { query, pagination } = useSearch();

  const debouncedSearch = useDebounce(query, 300);
  const normalizedQuery = debouncedSearch.trim();

  return useInfiniteQuery({
    queryKey: QUERY_KEYS.search(normalizedQuery),
    queryFn: ({ pageParam = 0 }) => {
      return analysisAPI.search({
        query: normalizedQuery || undefined,
        limit: pagination.limit,
        offset: pageParam,
      });
    },
    initialPageParam: 0,
    getNextPageParam: (lastPage, allPages, lastPageParam) => {
      // If the last page has fewer items than the limit, there are no more pages
      if (lastPage.length < pagination.limit) {
        return undefined; // No more pages
      }
      // Calculate next offset
      const nextOffset = lastPageParam + pagination.limit;
      return nextOffset;
    },
    getPreviousPageParam: (firstPage, allPages, firstPageParam) => {
      return firstPageParam <= 0
        ? undefined
        : firstPageParam - pagination.limit;
    },
  });
};

// creating new analyses with automatic cache invalidation
export const useAnalysisMutation = () => {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: (request: AnalysisRequest) => analysisAPI.analyze(request),

    onSuccess: (newAnalysis: Analysis) => {
      // Invalidate all search-related queries to ensure fresh data
      queryClient.invalidateQueries({
        queryKey: [QUERY_KEYS.analyses, "search"],
        exact: false,
      });
    },

    onError: (error) => {
      console.error("Failed to create analysis:", error);
    },
  });
};

// Getting a specific analysis by ID
export const useAnalysis = (id: number, enabled = true) => {
  return useQuery({
    queryKey: [QUERY_KEYS.analyses, "single", id],
    queryFn: async () => {
      const analyses = await analysisAPI.search({});
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
