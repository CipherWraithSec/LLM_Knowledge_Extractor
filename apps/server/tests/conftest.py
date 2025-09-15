"""
Test configuration and fixtures.
"""
import pytest
import asyncio
import os
from httpx import AsyncClient

# Ensure we're using mock mode for tests
os.environ['LLM_MOCK_ENABLED'] = 'true'


@pytest.fixture(scope="session")
def event_loop():
    """Create an instance of the default event loop for the test session."""
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    yield loop
    loop.close()


@pytest.fixture
async def client():
    """Create an async test client for the running server."""
    # Test against the running server in the container
    async with AsyncClient(base_url="http://localhost:8000") as ac:
        yield ac


@pytest.fixture
def sample_text():
    """Sample text for testing analysis."""
    return "Artificial intelligence is transforming the healthcare industry by enabling faster diagnosis and personalized treatment plans."


@pytest.fixture
def complex_text():
    """More complex text for testing."""
    return """
    Climate change represents one of the most significant challenges of our time. 
    Rising global temperatures, melting ice caps, and extreme weather events are clear indicators 
    of environmental disruption. Governments worldwide must implement sustainable policies 
    to reduce carbon emissions and promote renewable energy sources.
    """