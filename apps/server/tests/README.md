# Server Integration Tests

This directory contains integration tests for the Knowledge Extractor API server.

## Test Structure

- `conftest.py` - Pytest configuration and fixtures
- `test_api_integration.py` - Main integration tests for API endpoints
- `README.md` - This file

## Running Tests

### Option 1: Simple Test Runner (Recommended)
```bash
# From the server directory
docker-compose exec server python run_tests.py
```

### Option 2: Full Pytest Suite
```bash
# From inside the container
docker-compose exec server poetry run pytest tests/ -v
```

### Option 3: Manual Testing
You can also test the endpoints manually:
```bash
# Health check
curl http://localhost:8000/

# Analyze text
curl -X POST http://localhost:8000/api/v1/analyze \
  -H "Content-Type: application/json" \
  -d '{"text": "Sample text to analyze"}'

# Search analyses
curl http://localhost:8000/api/v1/search?topic=keyword
```

## Test Configuration

The tests are configured to use **mock data** by default, which means:
- No real OpenAI API calls are made
- Consistent, predictable responses
- Fast execution
- No API costs

Mock mode is enabled via the `LLM_MOCK_ENABLED=true` environment variable.

## Test Coverage

The tests cover:

### Core Functionality
- ✅ Health check endpoint (`/`)
- ✅ Text analysis endpoint (`/api/v1/analyze`)
- ✅ Search endpoint (`/api/v1/search`)

### Data Validation
- ✅ Required fields presence
- ✅ Correct data types
- ✅ Response structure
- ✅ Confidence score calculation

### Error Handling
- ✅ Empty text validation
- ✅ Invalid request format
- ✅ Proper error responses

### Mock Data Behavior
- ✅ Consistent mock responses
- ✅ Database persistence
- ✅ Search functionality

## Adding New Tests

To add new tests:

1. Add test functions to `test_api_integration.py`
2. Use the provided fixtures (`client`, `sample_text`, `complex_text`)
3. Follow the naming convention: `test_*`
4. Use async/await for API calls

Example:
```python
async def test_new_feature(client: AsyncClient):
    response = await client.get("/api/v1/new-endpoint")
    assert response.status_code == 200
```

## Notes

- Tests use the mock LLM client for predictable results
- Database is shared with the running server
- Tests create real database entries (consider cleanup if needed)
- Confidence scores are calculated from mock logprobs