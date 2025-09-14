from typing import List, Optional
from pydantic import BaseModel, Field


class AnalysisRequest(BaseModel):
    text: str = Field(
        min_length=1, description="The unstructured text to be analyzed.")


class AnalysisResult(BaseModel):
    id: int
    title: Optional[str]
    topics: List[str]
    sentiment: str
    keywords: List[str]
    summary: str
    original_text: Optional[str]
    confidence_score: Optional[float]
    createdAt: str


class SearchResponse(BaseModel):
    analyses: List[AnalysisResult]
