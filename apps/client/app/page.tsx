'use client'

import { useState, useMemo } from 'react'
import { useQuery } from '@tanstack/react-query'
import { useDispatch, useSelector } from 'react-redux'
import { Header } from '@/components/Header'
import { AnalysisModal } from '@/components/AnalysisModal'
import { AnalysisCard } from '@/components/AnalysisCard'
import { analysisAPI } from '@/lib/api'
import { RootState, analysisModalActions, searchActions } from '@/lib/store'
import { Analysis } from '@/lib/types'

export default function HomePage() {
  const dispatch = useDispatch()
  const { isOpen: isModalOpen } = useSelector((state: RootState) => state.analysisModal)
  const { query: searchQuery } = useSelector((state: RootState) => state.search)

  // Fetch analyses using React Query
  const {
    data: analyses = [],
    isLoading,
    error,
    refetch
  } = useQuery({
    queryKey: ['analyses'],
    queryFn: analysisAPI.getAnalyses,
  })

  // Filter analyses based on search query
  const filteredAnalyses = useMemo(() => {
    if (!searchQuery.trim()) return analyses

    const query = searchQuery.toLowerCase()
    return analyses.filter(analysis => 
      analysis.summary.toLowerCase().includes(query) ||
      analysis.topics.some(topic => topic.toLowerCase().includes(query)) ||
      analysis.keywords.some(keyword => keyword.toLowerCase().includes(query)) ||
      analysis.sentiment.toLowerCase().includes(query)
    )
  }, [analyses, searchQuery])

  const handleNewAnalysis = () => {
    dispatch(analysisModalActions.openModal())
  }

  const handleSearchChange = (query: string) => {
    dispatch(searchActions.setQuery(query))
  }

  const handleModalClose = () => {
    dispatch(analysisModalActions.closeModal())
  }

  const handleAnalysisComplete = (analysis: Analysis) => {
    // Refetch analyses to include the new one
    refetch()
  }

  const handleCardClick = (analysis: Analysis) => {
    // For now, we could open a modal or navigate to a detail page
    // Since you mentioned individual pages, we could implement navigation later
    console.log('Card clicked:', analysis)
  }

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <Header
        searchQuery={searchQuery}
        onSearchChange={handleSearchChange}
        onNewAnalysis={handleNewAnalysis}
      />

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
            <p className="text-red-800">Failed to load analyses. Please check your connection.</p>
            <button
              onClick={() => refetch()}
              className="mt-4 px-4 py-2 bg-red-600 text-white rounded-lg hover:bg-red-700 transition-colors"
            >
              Try Again
            </button>
          </div>
        )}

        {/* No Results */}
        {!isLoading && !error && filteredAnalyses.length === 0 && analyses.length === 0 && (
          <div className="text-center py-12">
            <div className="text-6xl mb-4">🧠</div>
            <h2 className="text-2xl font-bold text-gray-800 mb-2">No analyses yet</h2>
            <p className="text-gray-600 mb-6">
              Get started by analyzing your first piece of text
            </p>
            <button
              onClick={handleNewAnalysis}
              className="px-6 py-3 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors"
            >
              Start Analyzing
            </button>
          </div>
        )}

        {/* Search No Results */}
        {!isLoading && !error && filteredAnalyses.length === 0 && analyses.length > 0 && searchQuery && (
          <div className="text-center py-12">
            <div className="text-4xl mb-4">🔍</div>
            <h2 className="text-xl font-semibold text-gray-800 mb-2">No results found</h2>
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
                    {filteredAnalyses.length} result{filteredAnalyses.length !== 1 ? 's' : ''} 
                    {' '}for &quot;{searchQuery}&quot;
                  </>
                ) : (
                  <>Analysis History ({analyses.length})</>
                )}
              </div>
              {searchQuery && (
                <button
                  onClick={() => handleSearchChange('')}
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
      <AnalysisModal
        isOpen={isModalOpen}
        onClose={handleModalClose}
        onAnalysisComplete={handleAnalysisComplete}
      />
    </div>
  )
}