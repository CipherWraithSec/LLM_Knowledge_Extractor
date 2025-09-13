import json
from typing import List
from fastapi import APIRouter, Depends, HTTPException, status, Query
from fastapi.responses import StreamingResponse
from prisma import errors as prisma_errors

from ....models.analysis import AnalysisRequest, AnalysisResult
from ..dependencies import get_analysis_service
from ....services.analysis_service import AnalysisService
from ....core.logging import logger

analysis_router = APIRouter(tags=["analysis"])


@analysis_router.post("/analyze", response_model=AnalysisResult)
async def analyze_text(
    request: AnalysisRequest,
    analysis_service: AnalysisService = Depends(get_analysis_service)
):

    # Performs text analysis using the provided AnalysisService.processes it with an LLM, stores the results and returns them.
    if not request.text:
        # Input validation
        logger.warning("Received empty text input.")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={"message": "Input text cannot be empty."}
        )

    try:
        # Delegate the core logic to the service layer.
        analysis = await analysis_service.perform_analysis(request.text)
        return AnalysisResult.model_validate(analysis)
    except Exception as e:
        # Catch any unexpected errors from the service layer.
        logger.error(f"Analysis failed: {e}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )


@analysis_router.get("/search", response_model=List[AnalysisResult])
async def search_analyses(
    topic: str = Query(
        None, description="Search analyses by a key topic or keyword."),
    analysis_service: AnalysisService = Depends(get_analysis_service)
):
    """
    Searches for stored analyses matching a given topic or keyword.
    """
    # Delegate the search logic to the service layer.
    analyses = await analysis_service.search_analyses(topic)
    return [AnalysisResult.model_validate(res) for res in analyses]
