'use client'

import { Card, CardContent, CardHeader } from '@/components/ui/card'
import { Badge } from '@/components/ui/badge'
import { Analysis, SENTIMENT_EMOJIS, getConfidenceColor, formatDate } from '@/lib/types'

interface AnalysisCardProps {
  analysis: Analysis
  onClick?: () => void
}

export function AnalysisCard({ analysis, onClick }: AnalysisCardProps) {
  const maxSummaryLength = 150
  const truncatedSummary = analysis.summary.length > maxSummaryLength
    ? analysis.summary.substring(0, maxSummaryLength) + '...'
    : analysis.summary

  return (
    <Card
      className="hover:shadow-lg transition-shadow cursor-pointer border border-gray-200 hover:border-blue-300"
      onClick={onClick}
    >
      <CardHeader className="pb-3">
        <div className="flex items-start justify-between">
          <div className="flex-1">
            <h3 className="font-semibold text-lg text-gray-900 line-clamp-2">
              {analysis.title || 'Text Analysis'}
            </h3>
          </div>
          <div className="text-sm text-gray-500 ml-4 whitespace-nowrap">
            {formatDate(analysis.createdAt)}
          </div>
        </div>
      </CardHeader>
      
      <CardContent className="space-y-4">
        {/* Summary */}
        <div className="text-gray-700 text-sm leading-relaxed">
          {truncatedSummary}
        </div>

        {/* Topics */}
        <div className="flex flex-wrap gap-2">
          {analysis.topics.slice(0, 3).map((topic, index) => (
            <Badge
              key={index}
              variant="outline"
              className="text-xs bg-blue-50 text-blue-700 border-blue-200"
            >
              {topic}
            </Badge>
          ))}
          {analysis.topics.length > 3 && (
            <Badge variant="outline" className="text-xs text-gray-500">
              +{analysis.topics.length - 3} more
            </Badge>
          )}
        </div>

        {/* Sentiment and Confidence */}
        <div className="flex items-center justify-between pt-2 border-t">
          <div className="flex items-center space-x-2">
            <span className="text-lg">{SENTIMENT_EMOJIS[analysis.sentiment]}</span>
            <span className="text-sm font-medium capitalize text-gray-700">
              {analysis.sentiment}
            </span>
          </div>
          <div className={`text-sm font-medium ${getConfidenceColor(analysis.confidence_score)}`}>
            {analysis.confidence_score != null 
              ? `${analysis.confidence_score.toFixed(1)}% Confidence`
              : 'No Confidence Score'
            }
          </div>
        </div>
      </CardContent>
    </Card>
  )
}