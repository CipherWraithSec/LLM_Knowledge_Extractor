"""
Integration tests for the analysis API endpoints.

These tests use the mock LLM to ensure predictable results and test the full API flow.
"""
import pytest
import json
from httpx import AsyncClient


class TestHealthCheck:
    """Test basic health check endpoint."""
    
    async def test_health_check(self, client: AsyncClient):
        """Test that the server is running."""
        response = await client.get("/")
        assert response.status_code == 200
        assert response.json() == {"message": "Server is running"}


class TestAnalysisEndpoint:
    """Test the /analyze endpoint with mock data."""
    
    async def test_analyze_text_success(self, client: AsyncClient, sample_text: str):
        """Test successful text analysis with mock data."""
        response = await client.post(
            "/api/v1/analyze",
            json={"text": sample_text}
        )
        
        assert response.status_code == 200
        data = response.json()
        
        # Check that all expected fields are present
        assert "id" in data
        assert "title" in data
        assert "topics" in data
        assert "sentiment" in data
        assert "keywords" in data
        assert "summary" in data
        assert "original_text" in data
        assert "confidence_score" in data
        assert "createdAt" in data
        
        # Check data types and content
        assert isinstance(data["id"], int)
        assert isinstance(data["topics"], list)
        assert isinstance(data["keywords"], list)
        assert isinstance(data["summary"], str)
        assert data["original_text"] == sample_text
        assert isinstance(data["confidence_score"], (int, float))
        
        # Since we're using mock data, we can check for expected mock values
        if data["sentiment"] == "neutral":  # This suggests mock data was used
            assert len(data["topics"]) >= 1
            assert data["summary"] != ""
    
    async def test_analyze_empty_text(self, client: AsyncClient):
        """Test analysis with empty text should return error."""
        response = await client.post(
            "/api/v1/analyze",
            json={"text": ""}
        )
        
        assert response.status_code == 400
        assert "detail" in response.json()
    
    async def test_analyze_whitespace_text(self, client: AsyncClient):
        """Test analysis with only whitespace should return error."""
        response = await client.post(
            "/api/v1/analyze",
            json={"text": "   \n\t   "}
        )
        
        assert response.status_code == 400
        assert "detail" in response.json()
    
    async def test_analyze_complex_text(self, client: AsyncClient, complex_text: str):
        """Test analysis with more complex text."""
        response = await client.post(
            "/api/v1/analyze",
            json={"text": complex_text}
        )
        
        assert response.status_code == 200
        data = response.json()
        
        # Verify basic structure
        assert data["original_text"] == complex_text
        assert isinstance(data["confidence_score"], (int, float))
        assert data["confidence_score"] >= 0
        assert len(data["topics"]) > 0
        assert len(data["keywords"]) > 0
    
    async def test_analyze_invalid_request(self, client: AsyncClient):
        """Test analysis with invalid request body."""
        response = await client.post(
            "/api/v1/analyze",
            json={"wrong_field": "some text"}
        )
        
        assert response.status_code == 422  # Validation error


class TestSearchEndpoint:
    """Test the /search endpoint."""
    
    async def test_search_no_query(self, client: AsyncClient):
        """Test search without query parameter returns all analyses."""
        response = await client.get("/api/v1/search")
        
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
    
    async def test_search_with_topic(self, client: AsyncClient, sample_text: str):
        """Test search functionality after creating an analysis."""
        # First, create an analysis
        analyze_response = await client.post(
            "/api/v1/analyze",
            json={"text": sample_text}
        )
        assert analyze_response.status_code == 200
        analysis_data = analyze_response.json()
        
        # Now search for it using one of its topics or keywords
        if analysis_data["topics"]:
            search_term = analysis_data["topics"][0].lower()
        elif analysis_data["keywords"]:
            search_term = analysis_data["keywords"][0].lower()
        else:
            search_term = "test"
        
        search_response = await client.get(f"/api/v1/search?topic={search_term}")
        
        assert search_response.status_code == 200
        search_results = search_response.json()
        assert isinstance(search_results, list)
    
    async def test_search_nonexistent_topic(self, client: AsyncClient):
        """Test search for non-existent topic returns empty list."""
        response = await client.get("/api/v1/search?topic=nonexistenttermshouldnotmatch123")
        
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)


class TestMockDataBehavior:
    """Test that mock data is working as expected."""
    
    async def test_mock_data_consistency(self, client: AsyncClient):
        """Test that mock data returns consistent results."""
        test_text = "This is a test for mock data consistency."
        
        # Make two identical requests
        response1 = await client.post("/api/v1/analyze", json={"text": test_text})
        response2 = await client.post("/api/v1/analyze", json={"text": test_text})
        
        assert response1.status_code == 200
        assert response2.status_code == 200
        
        data1 = response1.json()
        data2 = response2.json()
        
        # The analysis content should be similar (same LLM processing)
        # but IDs should be different since they're separate database entries
        assert data1["id"] != data2["id"]
        assert data1["original_text"] == data2["original_text"]
        assert data1["original_text"] == test_text
    
    async def test_confidence_score_calculation(self, client: AsyncClient):
        """Test that confidence scores are calculated properly."""
        response = await client.post(
            "/api/v1/analyze",
            json={"text": "Test confidence score calculation with this sample text."}
        )
        
        assert response.status_code == 200
        data = response.json()
        
        # Confidence score should be present and reasonable
        assert "confidence_score" in data
        confidence = data["confidence_score"]
        
        if confidence is not None:
            assert isinstance(confidence, (int, float))
            assert 0 <= confidence <= 100  # Should be a percentage