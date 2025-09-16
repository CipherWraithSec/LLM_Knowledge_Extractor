"use client";

import { Copy, Calendar, Hash, TrendingUp } from "lucide-react";
import { toast } from "sonner";
import {
  Dialog,
  DialogContent,
  DialogHeader,
  DialogTitle,
} from "@/components/ui/dialog";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import {
  SENTIMENT_EMOJIS,
  getConfidenceColor,
  formatDate,
} from "@/lib/types";
import { useAppDispatch } from "@/app/hooks/redux";
import {
  closeModal,
  useAnalysisDetail,
} from "@/lib/redux/features/analysisDetail/analysisDetailSlice";

export function AnalysisDetailModal() {
  const dispatch = useAppDispatch();
  const { isOpen, analysis } = useAnalysisDetail();

  const handleOnOpenChange = (open: boolean) => {
    if (!open) {
      dispatch(closeModal());
    }
  };

  const handleCopyToClipboard = async (text: string, label: string) => {
    try {
      await navigator.clipboard.writeText(text);
      toast.success(`${label} copied to clipboard!`);
    } catch (error) {
      toast.error("Failed to copy to clipboard");
    }
  };

  if (!analysis) return null;

  return (
    <Dialog open={isOpen} onOpenChange={handleOnOpenChange}>
      <DialogContent className="max-w-4xl max-h-[90vh] flex flex-col">
        <DialogHeader className="flex-shrink-0">
          <DialogTitle className="text-2xl text-blue-600 font-bold flex items-center gap-2">
            <Hash className="h-6 w-6" />
            Analysis #{analysis.id}
          </DialogTitle>
        </DialogHeader>

        <div className="flex flex-col space-y-6 overflow-y-auto flex-1 min-h-0 px-1">
          {/* Analysis Header */}
          <div className="bg-gradient-to-r from-blue-50 to-blue-100 rounded-lg p-6">
            <div className="flex items-center justify-between mb-4">
              <div className="flex items-center space-x-4">
                <div className="flex items-center space-x-2">
                  <span className="text-3xl">
                    {SENTIMENT_EMOJIS[analysis.sentiment]}
                  </span>
                  <div>
                    <p className="text-lg font-semibold capitalize">
                      {analysis.sentiment} Sentiment
                    </p>
                    <p
                      className={`text-sm font-medium ${getConfidenceColor(
                        analysis.confidence_score
                      )}`}
                    >
                      {analysis.confidence_score != null
                        ? `${analysis.confidence_score.toFixed(1)}% Confidence`
                        : 'No Confidence Score'
                      }
                    </p>
                  </div>
                </div>
              </div>
              <div className="flex items-center text-sm text-gray-500">
                <Calendar className="h-4 w-4 mr-1" />
                {formatDate(analysis.createdAt)}
              </div>
            </div>
            
            {analysis.title && (
              <div>
                <h3 className="text-lg font-semibold text-gray-900 mb-2">
                  Title:
                </h3>
                <p className="text-gray-700 font-medium">{analysis.title}</p>
              </div>
            )}
          </div>

          {/* Summary Section */}
          <div className="bg-white rounded-lg p-6 border shadow-sm">
            <div className="flex items-center justify-between mb-4">
              <h3 className="text-lg font-semibold text-gray-900">
                <TrendingUp className="h-5 w-5 inline mr-2" />
                Summary
              </h3>
              <Button
                variant="ghost"
                size="sm"
                onClick={() => handleCopyToClipboard(analysis.summary, "Summary")}
                className="flex items-center gap-1"
              >
                <Copy className="h-3 w-3" />
                Copy
              </Button>
            </div>
            <div className="bg-gray-50 rounded-md p-4 border">
              <p className="text-gray-700 leading-relaxed">{analysis.summary}</p>
            </div>
          </div>

          {/* Topics Section */}
          <div className="bg-white rounded-lg p-6 border shadow-sm">
            <h3 className="text-lg font-semibold text-gray-900 mb-4">
              🏷️ Topics ({analysis.topics.length})
            </h3>
            <div className="flex flex-wrap gap-2">
              {analysis.topics.map((topic, index) => (
                <Badge
                  key={index}
                  variant="secondary"
                  className="bg-blue-100 text-blue-800 px-3 py-1 text-sm font-medium"
                >
                  {topic}
                </Badge>
              ))}
            </div>
          </div>

          {/* Keywords Section */}
          <div className="bg-white rounded-lg p-6 border shadow-sm">
            <h3 className="text-lg font-semibold text-gray-900 mb-4">
              🔑 Keywords ({analysis.keywords.length})
            </h3>
            <div className="bg-gray-50 rounded-md p-4 border">
              <p className="text-gray-600">
                {analysis.keywords.join(" • ")}
              </p>
            </div>
          </div>

          {/* Original Text Section */}
          {analysis.original_text && (
            <div className="bg-white rounded-lg p-6 border shadow-sm">
              <div className="flex items-center justify-between mb-4">
                <h3 className="text-lg font-semibold text-gray-900">
                  📄 Original Text
                </h3>
                <Button
                  variant="ghost"
                  size="sm"
                  onClick={() => handleCopyToClipboard(analysis.original_text!, "Original text")}
                  className="flex items-center gap-1"
                >
                  <Copy className="h-3 w-3" />
                  Copy
                </Button>
              </div>
              <div className="bg-gray-50 rounded-md p-4 border max-h-60 overflow-y-auto">
                <p className="text-gray-700 text-sm font-mono leading-relaxed whitespace-pre-wrap">
                  {analysis.original_text}
                </p>
              </div>
            </div>
          )}
        </div>
      </DialogContent>
    </Dialog>
  );
}