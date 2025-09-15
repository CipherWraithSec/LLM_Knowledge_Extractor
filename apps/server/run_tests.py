#!/usr/bin/env python3
"""
Simple test runner to verify our API endpoints work with mock data.
"""
import asyncio
import json
from httpx import AsyncClient


async def test_health_check():
    """Test that the server is running."""
    print("Testing health check endpoint...")
    async with AsyncClient(base_url="http://localhost:8000") as client:
        response = await client.get("/")
        assert response.status_code == 200
        assert response.json() == {"message": "Server is running"}
        print("✅ Health check passed")


async def test_analyze_endpoint():
    """Test the analyze endpoint with mock data."""
    print("Testing analyze endpoint...")
    sample_text = "Artificial intelligence is transforming the healthcare industry by enabling faster diagnosis and personalized treatment plans."
    
    async with AsyncClient(base_url="http://localhost:8000") as client:
        response = await client.post(
            "/api/v1/analyze",
            json={"text": sample_text}
        )
        
        assert response.status_code == 200
        data = response.json()
        
        # Check that all expected fields are present
        required_fields = ["id", "title", "topics", "sentiment", "keywords", "summary", "original_text", "confidence_score", "createdAt"]
        for field in required_fields:
            assert field in data, f"Missing field: {field}"
        
        # Check data types and content
        assert isinstance(data["id"], int)
        assert isinstance(data["topics"], list)
        assert isinstance(data["keywords"], list)
        assert isinstance(data["summary"], str)
        assert data["original_text"] == sample_text
        assert isinstance(data["confidence_score"], (int, float)) or data["confidence_score"] is None
        
        print("✅ Analyze endpoint passed")
        print(f"   - ID: {data['id']}")
        print(f"   - Sentiment: {data['sentiment']}")
        print(f"   - Topics: {data['topics']}")
        print(f"   - Keywords: {data['keywords']}")
        print(f"   - Confidence Score: {data['confidence_score']}")
        
        return data


async def test_search_endpoint(created_analysis):
    """Test the search endpoint."""
    print("Testing search endpoint...")
    
    async with AsyncClient(base_url="http://localhost:8000") as client:
        # Test search without query
        response = await client.get("/api/v1/search")
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        print(f"✅ Search (no query) passed - found {len(data)} analyses")
        
        # Test search with topic
        if created_analysis["keywords"]:
            search_term = created_analysis["keywords"][0].lower()
            response = await client.get(f"/api/v1/search?topic={search_term}")
            assert response.status_code == 200
            search_results = response.json()
            assert isinstance(search_results, list)
            print(f"✅ Search (with topic '{search_term}') passed - found {len(search_results)} results")


async def test_empty_text_validation():
    """Test that empty text returns proper error."""
    print("Testing empty text validation...")
    
    async with AsyncClient(base_url="http://localhost:8000") as client:
        response = await client.post(
            "/api/v1/analyze",
            json={"text": ""}
        )
        
        assert response.status_code == 400
        assert "detail" in response.json()
        print("✅ Empty text validation passed")


async def main():
    """Run all tests."""
    print("🧪 Starting API Integration Tests")
    print("="*50)
    
    try:
        await test_health_check()
        created_analysis = await test_analyze_endpoint()
        await test_search_endpoint(created_analysis)
        await test_empty_text_validation()
        
        print("\n" + "="*50)
        print("🎉 All tests passed! Your API is working correctly with mock data.")
        
    except Exception as e:
        print(f"\n❌ Test failed: {e}")
        print("Make sure your server is running and mock is enabled.")
        return 1
    
    return 0


if __name__ == "__main__":
    exit_code = asyncio.run(main())