# 🧠 LLM Knowledge Extractor

An intelligent text analysis platform that extracts meaningful insights from text using Large Language Models (LLMs). The system analyzes text for topics, sentiment, keywords, and provides a summary as well as confidence scores based on token probabilities.

## 🏗️ Architecture

This is a full-stack application built with:

- **Backend**: FastAPI server with Python ([`apps/server/`](./apps/server/README.md))
- **Frontend**: Next.js React application ([`apps/client/`](./apps/client/README.md))
- **Database**: PostgreSQL with Prisma ORM
- **AI/ML**: OpenAI GPT integration with optional mock mode for development
- **Infrastructure**: Docker & Docker Compose

## ✨ Features

- **Text Analysis**: Extract topics, sentiment, and summaries from any text
- **Confidence Scoring**: Calculate confidence scores using LLM token probabilities (logprobs)
- **Keyword Extraction**: Local spaCy-based keyword extraction
- **Search & Discovery**: Search through analyzed content
- **Mock Mode**: Development-friendly mock LLM responses (optional)
- **Real-time API**: RESTful API with automatic documentation

## 🎯 Design Choices

FastAPI provides automatic OpenAPI documentation and excellent async support for LLM streaming, while React Query handles data fetching with built-in caching and error handling. The system implements confidence scoring using OpenAI's logprobs (token probabilities) for mathematically grounded uncertainty quantification, and uses spaCy for local keyword extraction to identify the most frequent nouns without requiring additional LLM calls. PostgreSQL with Prisma ORM supports a type-safe data access layer and enables complex search operations using raw SQL for optimal performance, particularly for the array-based topic/keyword matching with partial text search. The containerized approach with Docker Compose ensures consistent development and deployment environments, while the mock LLM mode allows development and testing without API costs.

## 🚀 Quick Start

### Prerequisites

- Docker & Docker Compose
- OpenAI API key (optional for mock mode)

### 1. Clone & Setup

```bash
git clone <your-repo-url>
cd LLM_Knowledge_Extractor
```

### 2. Environment Configuration

Create a `.env` file in the root directory:

```env
# Database
POSTGRES_USER=your_db_username
POSTGRES_PASSWORD=your_db_password
POSTGRES_DB=your_db_name
DATABASE_URL=postgresql://your_db_username:your_db_password@db:5432/your_db_name

# LLM Configuration
LLM_API_KEY=your_openai_api_key_here
LLM_MOCK_ENABLED=true          # Set to false to use real OpenAI API
LLM_MODEL=your_preferred_model
LLM_MAX_TOKENS=1000
LLM_TEMPERATURE=0.3

# Frontend
NEXT_PUBLIC_API_URL=http://server:8000/api/v1
```

### 3. Launch All Services

```bash
docker-compose up -d --build
```

### 4. Initialize Database

```bash
# Create database tables
docker-compose exec server prisma migrate dev --name init

# Generate Prisma client
docker-compose exec server prisma generate
```

### 5. Access Applications

- **🖥️ Frontend**: http://localhost:3000
- **🚀 API Server**: http://localhost:8000
- **📚 API Docs**: http://localhost:8000/docs
- **🗄️ Database**: localhost:5432

## 📖 API Usage

### Analyze Text

```bash
curl -X POST http://localhost:8000/api/v1/analyze \
  -H "Content-Type: application/json" \
  -d '{
    "text": "Artificial intelligence is transforming healthcare by enabling faster diagnoses and personalized treatments."
  }'
```

### Search Analyses

```bash
curl "http://localhost:8000/api/v1/search?topic=healthcare"
```

### Example Response

```json
{
  "id": 1,
  "title": null,
  "topics": ["artificial intelligence", "healthcare", "diagnosis"],
  "sentiment": "positive",
  "keywords": ["intelligence", "healthcare", "treatments"],
  "summary": "AI is revolutionizing healthcare through improved diagnosis and personalized treatments.",
  "original_text": "Artificial intelligence is transforming...",
  "confidence_score": 94.5,
  "createdAt": "2025-09-15T00:00:00Z"
}
```

## 🧪 Testing

Run the test suite to verify everything works:

```bash
# Simple integration tests
docker-compose exec server python run_tests.py

# Full test suite
docker-compose exec server poetry run pytest tests/ -v
```

## 📁 Project Structure

```
LLM_Knowledge_Extractor/
├── README.md                 # This file - project overview
├── docker-compose.yml        # Multi-container configuration
├── .env                      # Environment variables
├── prisma/                   # Database schema & migrations
│   └── schema.prisma
└── apps/
    ├── server/               # FastAPI backend
    │   ├── README.md         # Server documentation
    │   ├── src/              # Source code
    │   ├── tests/            # Integration tests
    │   └── run_tests.py      # Test runner
    └── client/               # Next.js frontend
        ├── README.md         # Client documentation
        └── app/              # Next.js app directory
```

## 📚 Component Documentation

- **[Server Documentation](./apps/server/README.md)** - API details, development, deployment
- **[Client Documentation](./apps/client/README.md)** - Frontend setup, components, build process
- **[Testing Documentation](./apps/server/tests/README.md)** - Test structure and execution

## 🚀 Demo

- `You can view` - [Demo](https://www.loom.com/share/52466dac0ab84437b6eeb0ade0b8eae6?sid=8bbf84b1-907d-40f7-b384-57c190084bf6)
