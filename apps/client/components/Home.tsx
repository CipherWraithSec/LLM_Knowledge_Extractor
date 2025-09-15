"use client";

import { Header } from "@/components/Header";
import { AnalysisModal } from "@/components/AnalysisModal";
import { AnalysisCard } from "@/components/AnalysisCard";
import { Analysis } from "@/lib/types";
import { useAppDispatch } from "@/app/hooks/redux";
import { useSearch, setQuery } from "@/lib/redux/features/search/searchSlice";
import { useAnalysisQuery } from "@/app/hooks/useAnalysis";

export default function Home() {
  const dispatch = useAppDispatch();
  const { query: searchQuery } = useSearch();

  // Use server-side search with debouncing and caching
  const { data: analyses = [], isLoading, error, refetch } = useAnalysisQuery();

  // Server handles filtering, so we use analyses directly
  const filteredAnalyses = analyses;

  const handleCardClick = (analysis: Analysis) => {
    // For now, we could open a modal or navigate to a detail page
    // Since you mentioned individual pages, we could implement navigation later
    console.log("Card clicked:", analysis);
  };

  const handleSearchClear = () => {
    dispatch(setQuery(""));
  };

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <Header />

      {/* Main Content */}
      <main className="container mx-auto px-4 py-8">
        {/* Loading State */}
        {isLoading && (
          <div className="text-center py-12">
            <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600 mx-auto"></div>
            <p className="mt-4 text-gray-600">Loading analyses...</p>
          </div>
        )}

        {/* Error State */}
        {error && (
          <div className="bg-red-50 border border-red-200 rounded-lg p-6 text-center">
            <p className="text-red-800">
              Failed to load analyses. Please check your connection.
            </p>
            <button
              onClick={() => refetch()}
              className="mt-4 px-4 py-2 bg-red-600 text-white rounded-lg hover:bg-red-700 transition-colors"
            >
              Try Again
            </button>
          </div>
        )}

        {/* No Results */}
        {!isLoading &&
          !error &&
          filteredAnalyses.length === 0 &&
          !searchQuery && (
            <div className="text-center py-12">
              <div className="text-6xl mb-4">🧠</div>
              <h2 className="text-2xl font-bold text-gray-800 mb-2">
                No analyses yet
              </h2>
              <p className="text-gray-600 mb-6">
                Get started by analyzing your first piece of text
              </p>
            </div>
          )}

        {/* Search No Results */}
        {!isLoading &&
          !error &&
          filteredAnalyses.length === 0 &&
          searchQuery && (
            <div className="text-center py-12">
              <div className="text-4xl mb-4">🔍</div>
              <h2 className="text-xl font-semibold text-gray-800 mb-2">
                No results found
              </h2>
              <p className="text-gray-600">
                No analyses match your search for &quot;{searchQuery}&quot;
              </p>
            </div>
          )}

        {/* Analysis Grid */}
        {!isLoading && !error && filteredAnalyses.length > 0 && (
          <div className="space-y-6">
            {/* Results Info */}
            <div className="flex items-center justify-between">
              <div className="text-lg font-semibold text-gray-800">
                {searchQuery ? (
                  <>
                    {filteredAnalyses.length} result
                    {filteredAnalyses.length !== 1 ? "s" : ""} for &quot;
                    {searchQuery}&quot;
                  </>
                ) : (
                  <>Analysis History ({filteredAnalyses.length})</>
                )}
              </div>
              {searchQuery && (
                <button
                  onClick={handleSearchClear}
                  className="text-sm text-blue-600 hover:text-blue-800 transition-colors"
                >
                  Clear search
                </button>
              )}
            </div>

            {/* Cards Grid */}
            <div className="grid gap-6 md:grid-cols-2 lg:grid-cols-3">
              {filteredAnalyses.map((analysis) => (
                <AnalysisCard
                  key={analysis.id}
                  analysis={analysis}
                  onClick={() => handleCardClick(analysis)}
                />
              ))}
            </div>
          </div>
        )}
      </main>

      {/* Analysis Modal */}
      <AnalysisModal />
    </div>
  );
}
