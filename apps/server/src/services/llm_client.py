import os
import httpx
import json
from typing import AsyncGenerator
from openai import AsyncOpenAI
from ..config import settings
from ..core.logging import logger


class LLMClient:
    # Client for interacting with the LLM (OpenAI) API. Supports streaming responses.
    # Uses a mock implementation for testing and a real client for production.
    def __init__(self, api_key: str, mock_enabled: bool):
        self.mock_enabled = mock_enabled
        if not self.mock_enabled:
            # Use AsyncOpenAI for non-blocking I/O.
            self.client = AsyncOpenAI(api_key=api_key)
            self.model_name = settings.llm_model  # Use the specified model
        else:
            self.client = None
            self.model_name = "mock_model"  # Fallback for mock

    async def stream_analysis(self, text: str) -> AsyncGenerator[str, None]:
       # Streams analysis results from the LLM as a generator of strings.
        if self.mock_enabled:
            logger.info("Using mock LLM response.")
            # Yields a complete, valid JSON string for mock response.
            mock_data = {
                "summary": "This is a mock summary of the provided text, used for testing and development purposes. It simulates a fast, perfect response.",
                "title": "Mock Analysis Title",
                "topics": ["mocking", "testing", "development"],
                "sentiment": "neutral",
                "confidence_score": 0.95  # High confidence for mock data
            }
            yield json.dumps(mock_data)
            return

        logger.info(
            f"Requesting analysis from OpenAI model: {self.model_name}")

        try:
            response_stream = await self.client.chat.completions.create(
                model=self.model_name,
                messages=[
                    {
                        "role": "system",
                        "content": (
                            "You are a knowledge extractor. "
                            "You will receive a block of text and must return a JSON object. "
                            "The JSON must have these keys: 'summary', 'title', 'topics', 'sentiment', and 'confidence_score'. "
                            "The summary should be 1-2 sentences. "
                            "The title should be extracted from the text if available (or null if none). "
                            "The topics array should contain 3 key topics from the text. "
                            "The sentiment must be one of 'positive', 'neutral', or 'negative'. "
                            "The confidence_score should be a float between 0.0 and 1.0 indicating your confidence in the analysis. "
                            "Return only the raw JSON, without any other commentary."
                        )
                    },
                    {"role": "user", "content": text}
                ],
                stream=True,
                response_format={"type": "json_object"}
            )

            # The AI SDK protocol uses a specific format (SSE), but we will handle parsing
            # the chunks and yield them as a single JSON object once complete.
            # For this simple task, waiting for the full response is fine, as it's small.
            # For a more complex streaming protocol, this generator would yield SSE events.
            full_response = ""
            async for chunk in response_stream:
                if chunk.choices and chunk.choices[0].delta and chunk.choices[0].delta.content:
                    full_response += chunk.choices[0].delta.content

            yield full_response

        except Exception as e:
            logger.error(f"Error calling OpenAI API: {e}", exc_info=True)
            raise e
