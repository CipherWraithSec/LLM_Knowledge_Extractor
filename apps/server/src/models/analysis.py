from typing import List, Optional
from pydantic import BaseModel, Field


class AnalysisRequest(BaseModel):
    text: str = Field(
        min_length=1, description="The unstructured text to be analyzed.")


class AnalysisResult(BaseModel):
    """Model representing the result of text analysis.
    
    This model matches the database schema and is used for API responses.
    All optional fields use proper typing without default initialization
    to avoid potential data inconsistencies.
    """
    id: int
    title: Optional[str]  # Can be None if LLM doesn't provide a title
    topics: List[str]     # Array of topic strings from LLM
    sentiment: str        # Required sentiment classification 
    keywords: List[str]   # Array of keywords from SpaCy extraction
    summary: str          # Required summary text from LLM
    original_text: Optional[str]      # Original input text (optional)
    confidence_score: Optional[float] # Analysis confidence (optional)
    createdAt: str        # Timestamp of when analysis was created


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
