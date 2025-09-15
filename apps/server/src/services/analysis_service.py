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
            # Average logprob per token. logprobs are negative so closer to 0 = higher confidence
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

    async def search_analyses(self, query: str, limit: int = 50, offset: int = 0) -> List[Dict[str, Any]]:
        # Search database for analyses based on a topic or keyword with pagination.
        logger.info(
            f"Searching analyses for query: '{query}', limit: {limit}, offset: {offset}")

        if query:
            # Raw SQL is used for optimal performance with PostgreSQL array operations
            search_sql = """
            SELECT * FROM "Analysis" 
            WHERE 
                -- Search in text fields (case-insensitive)
                summary ILIKE $1
                OR title ILIKE $1
                -- Search in array fields using unnest for partial matching
                OR EXISTS (SELECT 1 FROM unnest(topics) AS t WHERE t ILIKE $1)
                OR EXISTS (SELECT 1 FROM unnest(keywords) AS k WHERE k ILIKE $1)
            ORDER BY "createdAt" DESC
            LIMIT $2 OFFSET $3
            """

            # Prepare the search pattern for ILIKE (case-insensitive partial match)
            search_pattern = f"%{query}%"

            # Execute the optimized raw SQL query with pagination
            analyses = await self.prisma.query_raw(
                search_sql,
                search_pattern,
                limit,
                offset
            )
        else:
            # No query so return all analyses with reasonable ordering and pagination
            analyses = await self.prisma.analysis.find_many(
                skip=offset,
                take=limit,
                order={"createdAt": "desc"}
            )
            # Convert to list of dicts for consistency with raw query result
            analyses = [analysis.model_dump() for analysis in analyses]

        logger.info(
            f"Found {len(analyses)} analyses for query: '{query}' (limit: {limit}, offset: {offset})")

        return analyses
