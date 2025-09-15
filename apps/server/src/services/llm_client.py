import json
from typing import AsyncGenerator, Dict, Any, Optional
from openai import AsyncOpenAI
from ..config import settings
from ..utils.logging import logger
from ..utils.errors import llm_unavailable_error
from ..utils.prompts import get_analysis_messages


class LLMClient:

    # Uses a mock implementation for testing and a real client for production.
    def __init__(self, api_key: str, mock_enabled: bool):
        self.mock_enabled = mock_enabled
        if not self.mock_enabled:
            self.client: Optional[AsyncOpenAI] = AsyncOpenAI(api_key=api_key)
            self.model_name = settings.llm_model
        else:
            self.client: Optional[AsyncOpenAI] = None
            self.model_name = "mock_model"

    async def stream_analysis(self, text: str) -> AsyncGenerator[Dict[str, Any], None]:
        # Streams analysis results from the LLM as a generator of dicts with content and logprobs.
        if self.mock_enabled:
            logger.info("Using mock LLM response.")
            mock_data = {
                "summary": "This is a mock summary of the provided text, used for testing and development purposes. It simulates a fast, perfect response.",
                "title": "Mock Analysis Title",
                "topics": ["mocking", "testing", "development"],
                "sentiment": "neutral"
            }
            # Keep interface consistent with non-mock path
            yield {"content": json.dumps(mock_data), "logprobs": []}
            return

        # Type guard: client cannot be None
        if self.client is None:
            raise llm_unavailable_error()

        logger.info(
            f"Requesting analysis from OpenAI model: {self.model_name}")

        try:
            response_stream = await self.client.chat.completions.create(
                model=self.model_name,
                messages=get_analysis_messages(text),  # type: ignore
                max_tokens=settings.llm_max_tokens,
                temperature=settings.llm_temperature,
                stream=True,
                logprobs=True,
                response_format={"type": "json_object"}
            )

            # For this simple task, we'll wait for the full response since it's small.
            full_response_content = ""
            all_logprobs = []
            async for chunk in response_stream:
                # choices is a list. take the first incremental delta
                if getattr(chunk, "choices", None) and len(chunk.choices) > 0:
                    choice = chunk.choices[0]
                    # Content delta
                    if getattr(choice, "delta", None) and getattr(choice.delta, "content", None):
                        content = choice.delta.content
                        if content is not None:
                            full_response_content += content
                    # Logprobs per token
                    if getattr(choice, "logprobs", None) and getattr(choice.logprobs, "content", None):
                        for logprob_info in choice.logprobs.content:
                            # Defensive: ensure attribute exists
                            if hasattr(logprob_info, "logprob") and logprob_info.logprob is not None:
                                all_logprobs.append(logprob_info.logprob)

            yield {"content": full_response_content, "logprobs": all_logprobs}

        except Exception as e:
            logger.error(f"Error calling OpenAI API: {e}", exc_info=True)
            raise llm_unavailable_error()
