import json
from prisma import Prisma
from typing import Callable, List, Dict, Any
from ..services.llm_client import LLMClient
from ..models.analysis import AnalysisResult
from ..utils.logging import logger
from ..utils.errors import llm_unavailable_error, database_error


class AnalysisService:

    # Orchestrates LLM calls, keyword extraction, and database persistence.

    def __init__(self, prisma: Prisma, llm_client: LLMClient, keyword_extractor: Callable[[str], List[str]]):
        self.prisma = prisma
        self.llm_client = llm_client
        self.keyword_extractor = keyword_extractor

    async def perform_analysis(self, text: str) -> Dict[str, Any]:

        logger.info("Starting analysis for input text.")

        # 1. Call the LLM to get summary, title, topics, and sentiment.
        full_response = ""
        try:
            async for chunk in self.llm_client.stream_analysis(text):
                full_response += chunk
        except Exception as e:
            logger.error(f"LLM streaming failed: {e}", exc_info=True)
            raise llm_unavailable_error()

        # 2. Parse the LLM's streaming response.
        try:
            llm_output = json.loads(full_response)
        except json.JSONDecodeError:
            logger.error(f"Failed to parse LLM JSON: {full_response}")
            raise llm_unavailable_error()

        # 3. Perform local, CPU-bound keyword extraction.
        # Performance optimization to avoid using the LLM for a
        # simple, deterministic task.
        keywords = self.keyword_extractor(text)

        # 4. Persist the analysis to the database.
        try:
            # Prepare the data to be saved - includes both LLM output and extracted keywords
            analysis_data = {
                "summary": llm_output.get("summary", ""),
                "title": llm_output.get("title"),  # Can be None
                "topics": llm_output.get("topics", []),
                "sentiment": llm_output.get("sentiment", "unknown"),
                "keywords": keywords,
                "original_text": text,  # Store the original input text for reference
                # LLM confidence if provided
                "confidence_score": llm_output.get("confidence_score"),
                # Note: createdAt is handled by database default
            }
            analysis = await self.prisma.analysis.create(data=analysis_data)
        except Exception as e:
            logger.error(
                f"Failed to save analysis to database: {e}", exc_info=True)
            raise database_error()

        logger.info(f"Successfully performed and saved analysis for text.")
        return analysis

    async def search_analyses(self, query: str) -> List[Dict[str, Any]]:
        # Search database for analyses based on a topic or keyword.
        logger.info(f"Searching analyses for query: '{query}'.")

        # Build the where clause for Prisma query
        if query:
            where_clause = {
                "OR": [
                    {"topics": {"has": query}},
                    {"keywords": {"has": query}},
                ]
            }
        else:
            where_clause = {}

        analyses = await self.prisma.analysis.find_many(where=where_clause)

        logger.info(f"Found {len(analyses)} analyses for query: '{query}'.")
        return analyses
