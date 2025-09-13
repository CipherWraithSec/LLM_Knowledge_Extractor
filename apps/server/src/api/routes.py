from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Optional
# from app.services.analysis import analyze_text, search_analyses

router = APIRouter()


class AnalyzeRequest(BaseModel):
    text: str


class AnalyzeResponse(BaseModel):
    title: Optional[str]
    topics: List[str]
    sentiment: str
    keywords: List[str]
    confidence_score: Optional[float]


class SearchResponse(BaseModel):
    analyses: List[AnalyzeResponse]


@router.post("/analyze", response_model=AnalyzeResponse)
# async def analyze(request: AnalyzeRequest):
#     if not request.text.strip():
#         raise HTTPException(status_code=400, detail="Input text cannot be empty.")
#     try:
#         result = await analyze_text(request.text)
#         return result
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))
@router.get("/search", response_model=SearchResponse)
# async def search(topic: str):
#     try:
#         results = await search_analyses(topic)
#         return {"analyses": results}
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))
