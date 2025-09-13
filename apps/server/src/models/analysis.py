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
    confidence_score: Optional[float]
    createdAt: str


class SearchResponse(BaseModel):
    analyses: List[AnalysisResult]


# from fastapi import APIRouter, HTTPException
# from app.services.analysis import analyze_text, search_analyses

# router = APIRouter()


# @router.post("/analyze", response_model=AnalyzeResponse)
# async def analyze(request: AnalyzeRequest):
#     if not request.text.strip():
#         raise HTTPException(status_code=400, detail="Input text cannot be empty.")
#     try:
#         result = await analyze_text(request.text)
#         return result
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))
# @router.get("/search", response_model=SearchResponse)
# async def search(topic: str):
#     try:
#         results = await search_analyses(topic)
#         return {"analyses": results}
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))
