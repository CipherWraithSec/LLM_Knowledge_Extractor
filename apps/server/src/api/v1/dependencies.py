# Import prisma from the main endpoint file, or better, from a database module.
from ..v1.endpoints.analysis import prisma
from ...services.analysis_service import AnalysisService
from ...services.llm_client import LLMClient
from ...utils.keywords import extract_nouns
from ...core.logging import logger
from ...config import settings


# Dependency injection functions for the endpoints

def get_llm_client() -> LLMClient:
    # initializes a singleton instance of the LLM client
    return LLMClient(api_key=settings.llm_api_key, mock_enabled=settings.llm_mock_enabled)


def get_analysis_service(
    llm_client: LLMClient = Depends(get_llm_client)
) -> AnalysisService:
    # Provides an instance of AnalysisService with its dependencies injected.
    return AnalysisService(prisma=prisma, llm_client=llm_client, keyword_extractor=extract_nouns)
