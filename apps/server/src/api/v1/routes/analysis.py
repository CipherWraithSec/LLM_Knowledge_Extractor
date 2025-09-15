import json
from typing import List
from fastapi import APIRouter, Depends, HTTPException, status, Query
from fastapi.responses import StreamingResponse
from prisma import errors as prisma_errors

from ....models.analysis import AnalysisRequest, AnalysisResult
from ..dependencies import get_analysis_service
from ....services.analysis_service import AnalysisService
from ....utils.logging import logger
from ....utils.errors import empty_text_error, analysis_failed_error

analysis_router = APIRouter(tags=["analysis"])


# POST /analyze
@analysis_router.post("/analyze", response_model=AnalysisResult)
async def analyze_text(
    request: AnalysisRequest,
    analysis_service: AnalysisService = Depends(get_analysis_service)
):

    # Performs text analysis using the provided AnalysisService.processes it with an LLM, stores the results and returns them.
    if not request.text.strip():
        # Input validation
        logger.warning("Received empty text input.")
        raise empty_text_error()

    try:
        # Delegate the core logic to the service layer.
        analysis = await analysis_service.perform_analysis(request.text)
        return AnalysisResult.model_validate(analysis)
    except Exception as e:
        # Any unexpected errors from the service layer.
        logger.error("Analysis failed: {}", str(e), exc_info=True)
        raise analysis_failed_error()


# GET /search
@analysis_router.get("/search", response_model=List[AnalysisResult])
async def search_analyses(
    topic: str = Query(
        None, description="Search analyses by a key topic or keyword."),
    limit: int = Query(
        50, ge=1, le=200, description="Maximum number of results to return (1-200)"),
    offset: int = Query(
        0, ge=0, description="Number of results to skip for pagination"),
    analysis_service: AnalysisService = Depends(get_analysis_service)
):
    # Searches for stored analyses matching a given topic or keyword.
    # Delegate the search logic to the service layer.
    analyses = await analysis_service.search_analyses(topic, limit=limit, offset=offset)
    return [AnalysisResult.model_validate(res) for res in analyses]
