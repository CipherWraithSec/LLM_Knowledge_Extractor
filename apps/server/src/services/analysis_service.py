import json
import math
from prisma import Prisma
from typing import Callable, List, Dict, Any
from ..services.llm_client import LLMClient
from ..models.analysis import AnalysisResult
from ..utils.logging import logger
from ..utils.errors import llm_unavailable_error, database_error


class AnalysisService:

    # Service layer handling text analysis logic, integrating LLM calls and database operations.

    def __init__(self, prisma: Prisma, llm_client: LLMClient, keyword_extractor: Callable[[str], List[str]]):
        self.prisma = prisma
        self.llm_client = llm_client
        self.keyword_extractor = keyword_extractor

    async def perform_analysis(self, text: str) -> Dict[str, Any]:

        logger.info("Starting analysis for input text.")

        # 1. Call the LLM to get summary, title, topics, and sentiment.
        llm_response = None
        full_response_content = ""
        all_logprobs = []
        try:
            async for response_data in self.llm_client.stream_analysis(text):
                full_response_content += response_data["content"]
                if response_data["logprobs"]:
                    all_logprobs.extend(response_data["logprobs"])
        except Exception as e:
            logger.error(f"LLM streaming failed: {e}", exc_info=True)
            raise llm_unavailable_error()

        # 2. Calculate confidence score from logprobs
        confidence_score = None
        if all_logprobs:
            # Average logprob per token. logprobs are negative, closer to 0 = higher confidence
            avg_logprob = sum(all_logprobs) / len(all_logprobs)

           # Convert to percentage confidence score (0-100)
            raw_confidence = math.exp(avg_logprob)
            confidence_score = min(100.0, max(0.0, raw_confidence * 100))

            logger.info(
                f"Calculated confidence: avg_logprob={avg_logprob:.4f}, raw_confidence={raw_confidence:.4f}, final_score={confidence_score:.2f}%")

        # 3. Parse the LLM's streaming response content.
        try:
            llm_output = json.loads(full_response_content)
        except json.JSONDecodeError:
            logger.error(
                f"Failed to parse LLM response as JSON: {full_response_content}")
            raise llm_unavailable_error()

        # 4. Perform local, CPU-bound keyword extraction.
        keywords = self.keyword_extractor(text)

        # 5. Persist the analysis to the database.
        try:
            analysis_data = {
                "summary": llm_output.get("summary", ""),
                "title": llm_output.get("title"),
                "topics": llm_output.get("topics", []),
                "sentiment": llm_output.get("sentiment", "unknown"),
                "keywords": keywords,
                "original_text": text,
                "confidence_score": confidence_score
            }
            analysis = await self.prisma.analysis.create(data=analysis_data)
        except Exception as e:
            logger.error(
                f"Failed to save analysis to database: {e}", exc_info=True)
            raise database_error()

        logger.info(f"Successfully performed and saved analysis for text.")
        # Convert Prisma object to dict for the API response
        return analysis.model_dump()

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
        # Convert Prisma objects to dicts for the API response
        return [analysis.model_dump() for analysis in analyses]
