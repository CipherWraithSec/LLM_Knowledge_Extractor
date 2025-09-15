# 🚀 FastAPI Server

The backend service for the LLM Knowledge Extractor, built with FastAPI, Python, and PostgreSQL.

## 🏗️ Architecture

- **Framework**: FastAPI with async/await support
- **Database**: PostgreSQL with Prisma ORM
- **AI/ML**: OpenAI GPT integration with mock mode
- **NLP**: spaCy for local keyword extraction
- **Containerization**: Docker with Poetry dependency management

## ✨ Features

- **RESTful API** with automatic OpenAPI documentation
- **Text Analysis** with LLM integration (OpenAI GPT)
- **Confidence Scoring** using token probabilities (logprobs)
- **Mock Mode** for development without API costs
- **Database Persistence** with full CRUD operations
- **Search Functionality** for analyzing stored content
- **Modular Architecture** with clean separation of concerns

## 📁 Project Structure

```
server/
├── README.md                 # This file
├── main.py                   # FastAPI application entry point
├── run_tests.py              # Test runner script
├── pytest.ini               # Test configuration
├── pyproject.toml           # Poetry dependencies & config
├── Dockerfile               # Container configuration
├── prisma/                  # Database schema & migrations
│   └── schema.prisma
├── src/
│   ├── api/                 # API routes & dependencies
│   │   └── v1/
│   │       ├── dependencies.py
│   │       └── routes/
│   │           └── analysis.py
│   ├── config.py            # Settings & environment variables
│   ├── db/                  # Database connection & utilities
│   │   └── database.py
│   ├── models/              # Pydantic request/response models
│   │   └── analysis.py
│   ├── services/            # Business logic layer
│   │   ├── analysis_service.py
│   │   └── llm_client.py
│   └── utils/               # Utilities & helpers
│       ├── errors.py
│       ├── keywords.py
│       ├── logging.py
│       └── prompts.py
└── tests/                   # Integration tests
    ├── conftest.py
    ├── test_api_integration.py
    └── README.md
```

## 🚀 Quick Start

### Prerequisites

- Docker & Docker Compose (recommended)
- OR: Python 3.11+, PostgreSQL, Poetry

### Using Docker (Recommended)

From the root directory:

```bash
# Start all services
docker-compose up -d --build

# Initialize database
docker-compose exec server prisma migrate dev --name init
docker-compose exec server prisma generate

# Access server
curl http://localhost:8000/
```

### Local Development

```bash
# Install dependencies
poetry install

# Set up environment variables (see Configuration)
cp .env.example .env

# Start PostgreSQL (locally or via Docker)
# Update DATABASE_URL in .env accordingly

# Run database migrations
poetry run prisma migrate dev --name init
poetry run prisma generate

# Start the server
poetry run uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

## ⚙️ Configuration

The server uses environment variables for configuration. Create a `.env` file in the root directory:

```env
# Database Configuration
DATABASE_URL=postgresql://user:password@localhost:5432/dbname

# LLM Configuration
LLM_API_KEY=your_openai_api_key_here
LLM_MOCK_ENABLED=true              # Set to false for production
LLM_MODEL=gpt-4o-mini              # OpenAI model to use
LLM_MAX_TOKENS=1000                # Max tokens per request
LLM_TEMPERATURE=0.3                # Creativity level (0-2)
```

### Configuration Options

- **`DATABASE_URL`**: PostgreSQL connection string
- **`LLM_API_KEY`**: OpenAI API key for real LLM requests
- **`LLM_MOCK_ENABLED`**: Use mock responses (true) or real API (false)
- **`LLM_MODEL`**: OpenAI model name (gpt-4o-mini, gpt-4, etc.)
- **`LLM_MAX_TOKENS`**: Maximum tokens for LLM responses
- **`LLM_TEMPERATURE`**: Randomness in LLM responses (0.0-2.0)

## 📖 API Documentation

### Interactive Documentation

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

### Core Endpoints

#### Health Check
```bash
GET /
# Response: {"message": "Server is running"}
```

#### Analyze Text
```bash
POST /api/v1/analyze
Content-Type: application/json

{
  "text": "Your text to analyze here"
}
```

**Response:**
```json
{
  "id": 1,
  "title": "Extracted title or null",
  "topics": ["topic1", "topic2", "topic3"],
  "sentiment": "positive|neutral|negative",
  "keywords": ["keyword1", "keyword2", "keyword3"],
  "summary": "Brief summary of the text",
  "original_text": "Original input text",
  "confidence_score": 94.5,
  "createdAt": "2025-09-15T00:00:00Z"
}
```

#### Search Analyses
```bash
GET /api/v1/search?topic=keyword
# Returns array of matching analyses
```

## 🧪 Testing

### Run Tests

```bash
# Simple integration tests (recommended)
docker-compose exec server python run_tests.py

# Full pytest suite
docker-compose exec server poetry run pytest tests/ -v

# Run specific test
docker-compose exec server poetry run pytest tests/test_api_integration.py::TestAnalysisEndpoint::test_analyze_text_success -v
```

### Test Structure

- **Integration Tests**: Test full API endpoints with mock data
- **Mock Mode**: Tests use predictable mock LLM responses
- **Database**: Tests use the same database as development
- **Fixtures**: Reusable test data and client configurations

See [Testing Documentation](./tests/README.md) for details.

## 🔧 Development

### Adding Dependencies

```bash
# Add production dependency
docker-compose exec server poetry add package-name

# Add development dependency  
docker-compose exec server poetry add --group dev package-name

# Restart server to pick up changes
docker-compose restart server
```

### Database Operations

```bash
# Create migration
docker-compose exec server prisma migrate dev --name migration-name

# Reset database (development only!)
docker-compose exec server prisma db push --force-reset

# View data with Prisma Studio
docker-compose exec server prisma studio
```

### Code Structure

The codebase follows a layered architecture:

1. **Routes** (`api/v1/routes/`) - HTTP endpoints and request handling
2. **Services** (`services/`) - Business logic and external integrations
3. **Models** (`models/`) - Request/response schemas and validation
4. **Utils** (`utils/`) - Shared utilities and helpers

### Key Components

#### LLM Client (`services/llm_client.py`)
- Handles OpenAI API integration
- Supports mock mode for development
- Streams responses and extracts logprobs for confidence scoring

#### Analysis Service (`services/analysis_service.py`)
- Orchestrates text analysis workflow
- Combines LLM results with local keyword extraction
- Calculates confidence scores from logprobs
- Persists results to database

#### Prompts (`utils/prompts.py`)
- Centralized prompt management
- Easy to modify and version control
- Supports different analysis types

### Adding New Features

1. **Define models** in `models/` for request/response schemas
2. **Create service methods** in `services/` for business logic
3. **Add API routes** in `api/v1/routes/` for HTTP endpoints
4. **Write tests** in `tests/` for new functionality
5. **Update documentation** in this README

## 🐛 Debugging

### View Logs

```bash
# All logs
docker-compose logs -f server

# Recent logs only
docker-compose logs --tail=50 server

# Follow logs in real-time
docker-compose logs -f server | grep ERROR
```

### Common Issues

**Import Errors**: Make sure to restart the server after adding dependencies
**Database Connection**: Check DATABASE_URL format and database availability
**LLM Errors**: Verify API key and model availability, or enable mock mode
**Port Conflicts**: Ensure port 8000 is available

### Development Tools

- **Database Browser**: http://localhost:8000/docs (Prisma Studio)
- **API Explorer**: http://localhost:8000/docs (Swagger UI)
- **Log Monitoring**: `docker-compose logs -f server`

## 🚀 Production Deployment

### Configuration

1. Set `LLM_MOCK_ENABLED=false`
2. Provide valid OpenAI API key
3. Use production database URL
4. Remove `--reload` from uvicorn command

### Performance Considerations

- **Database Connection Pooling**: Configure appropriate pool size
- **LLM Rate Limits**: Implement request throttling if needed  
- **Caching**: Consider Redis for frequently accessed data
- **Monitoring**: Add health checks and metrics collection

### Security

- **Environment Variables**: Never commit API keys to version control
- **Database Access**: Use least-privilege database users
- **API Security**: Implement authentication/authorization as needed
- **Input Validation**: All inputs are validated via Pydantic models

## 📚 Related Documentation

- **[Project Overview](../../README.md)** - Full project setup and architecture
- **[Testing Guide](./tests/README.md)** - Detailed testing information
- **[Client Documentation](../client/README.md)** - Frontend integration guide