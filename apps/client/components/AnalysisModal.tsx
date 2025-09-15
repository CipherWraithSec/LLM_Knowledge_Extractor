"use client";

import { useState } from "react";
import { useMutation } from "@tanstack/react-query";
import { X, Loader2 } from "lucide-react";
import {
  Dialog,
  DialogContent,
  DialogHeader,
  DialogTitle,
} from "@/components/ui/dialog";
import { Button } from "@/components/ui/button";
import { Textarea } from "@/components/ui/textarea";
import { Badge } from "@/components/ui/badge";
import { analysisAPI } from "@/lib/api";
import {
  Analysis,
  AnalysisRequestSchema,
  SENTIMENT_EMOJIS,
  getConfidenceColor,
  formatDate,
} from "@/lib/types";

interface AnalysisModalProps {
  isOpen: boolean;
  onClose: () => void;
  onAnalysisComplete?: (analysis: Analysis) => void;
}

export function AnalysisModal({
  isOpen,
  onClose,
  onAnalysisComplete,
}: AnalysisModalProps) {
  const [text, setText] = useState("");
  const [result, setResult] = useState<Analysis | null>(null);

  const analysisMutation = useMutation({
    mutationFn: analysisAPI.analyze,
    onSuccess: (data) => {
      setResult(data);
      onAnalysisComplete?.(data);
    },
    onError: (error) => {
      console.error("Analysis failed:", error);
    },
  });

  const handleAnalyze = () => {
    // Validate input
    try {
      const validatedData = AnalysisRequestSchema.parse({ text });
      analysisMutation.mutate(validatedData);
    } catch (error) {
      console.error("Validation failed:", error);
    }
  };

  const handleClose = () => {
    setText("");
    setResult(null);
    analysisMutation.reset();
    onClose();
  };

  const isAnalyzing = analysisMutation.isPending;

  return (
    <Dialog open={isOpen} onOpenChange={handleClose}>
      <DialogContent className="max-w-2xl max-h-[90vh] flex flex-col">
        <DialogHeader className="flex-shrink-0">
          <DialogTitle className="text-center text-2xl text-blue-600 font-bold">
            Text Analysis
          </DialogTitle>
          <button
            onClick={handleClose}
            className="absolute right-4 top-4 rounded-sm opacity-70 ring-offset-background transition-opacity hover:opacity-100 focus:outline-none focus:ring-2 focus:ring-ring focus:ring-offset-2"
          >
            <X className="h-4 w-4" />
          </button>
        </DialogHeader>

        <div className="flex flex-col space-y-4 overflow-y-auto flex-1 min-h-0">
          {/* Description */}
          <div className="text-center text-gray-600 px-4">
            Input your text below, and our system will provide summary and more!
          </div>

          {/* Text Input Area - Top Section */}
          <div className="px-4">
            <Textarea
              placeholder="Paste or type your text here..."
              value={text}
              onChange={(e) => setText(e.target.value)}
              className="min-h-[200px] max-h-[300px] overflow-y-auto text-sm font-mono resize-none border-2 border-gray-300 focus:border-blue-500"
              disabled={isAnalyzing}
            />
          </div>

          {/* Analyze Button - Middle Section */}
          <div className="px-4">
            <Button
              onClick={handleAnalyze}
              disabled={!text.trim() || isAnalyzing}
              className="w-full py-3 bg-blue-600 hover:bg-blue-700 text-white font-medium text-lg"
            >
              {isAnalyzing ? (
                <>
                  <Loader2 className="mr-2 h-5 w-5 animate-spin" />
                  Analyzing...
                </>
              ) : (
                "Analyze Text"
              )}
            </Button>
          </div>

          {/* Results Section - Bottom */}
          {result && (
            <div className="px-4 pb-4">
              <div className="bg-gray-50 rounded-lg p-6 space-y-4">
                {/* Results Header */}
                <div className="flex items-center justify-between">
                  <h3 className="text-lg font-semibold">Analysis Results</h3>
                  <div className="flex items-center space-x-4">
                    <div className="flex items-center space-x-1">
                      <span className="text-2xl">
                        {SENTIMENT_EMOJIS[result.sentiment]}
                      </span>
                      <span className="capitalize font-medium">
                        {result.sentiment}
                      </span>
                    </div>
                    <div
                      className={`font-medium ${getConfidenceColor(
                        result.confidence_score
                      )}`}
                    >
                      {result.confidence_score.toFixed(1)}% Confidence
                    </div>
                  </div>
                </div>

                {/* Summary */}
                <div>
                  <h4 className="font-semibold text-gray-900 mb-2">Summary:</h4>
                  <div className="bg-white rounded-md p-4 border text-gray-700 leading-relaxed max-h-[200px] overflow-y-auto">
                    {result.summary}
                  </div>
                </div>

                {/* Topics */}
                <div>
                  <h4 className="font-semibold text-gray-900 mb-2">
                    🏷️ Topics:
                  </h4>
                  <div className="flex flex-wrap gap-2 max-h-[120px] overflow-y-auto">
                    {result.topics.map((topic, index) => (
                      <Badge
                        key={index}
                        variant="secondary"
                        className="bg-blue-100 text-blue-800 flex-shrink-0"
                      >
                        {topic}
                      </Badge>
                    ))}
                  </div>
                </div>

                {/* Keywords */}
                <div>
                  <h4 className="font-semibold text-gray-900 mb-2">
                    🔑 Keywords:
                  </h4>
                  <div className="text-gray-600 max-h-[80px] overflow-y-auto">
                    {result.keywords.join(" • ")}
                  </div>
                </div>

                {/* Timestamp */}
                <div className="text-sm text-gray-500">
                  ⏰ Analyzed: {formatDate(result.createdAt)}
                </div>
              </div>
            </div>
          )}

          {/* Error State */}
          {analysisMutation.isError && (
            <div className="px-4 pb-4">
              <div className="bg-red-50 border border-red-200 rounded-lg p-4">
                <div className="text-red-800">
                  Analysis failed. Please try again or check your connection.
                </div>
              </div>
            </div>
          )}
        </div>
      </DialogContent>
    </Dialog>
  );
}
