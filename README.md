# 🧠 LLM Knowledge Extractor

An intelligent text analysis platform that extracts meaningful insights from text using Large Language Models (LLMs). The system analyzes text for topics, sentiment, keywords, and provides a summary as well as confidence scores based on token probabilities.

## 🏗️ Architecture

This is a full-stack application built with:

- **Backend**: FastAPI server with Python ([`apps/server/`](./apps/server/README.md))
- **Frontend**: Next.js React application ([`apps/client/`](./apps/client/README.md))
- **Database**: PostgreSQL with Prisma ORM
- **AI/ML**: OpenAI GPT integration with mock mode for development
- **Infrastructure**: Docker & Docker Compose

## ✨ Features

- **Text Analysis**: Extract topics, sentiment, and summaries from any text
- **Confidence Scoring**: Calculate confidence scores using LLM token probabilities (logprobs)
- **Keyword Extraction**: Local spaCy-based keyword extraction
- **Search & Discovery**: Search through analyzed content
- **Mock Mode**: Development-friendly mock LLM responses
- **Real-time API**: RESTful API with automatic documentation

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
POSTGRES_USER=brian
POSTGRES_PASSWORD=brian123
POSTGRES_DB=jouster_db
DATABASE_URL=postgresql://brian:brian123@db:5432/jouster_db

# LLM Configuration
LLM_API_KEY=your_openai_api_key_here
LLM_MOCK_ENABLED=true          # Set to false to use real OpenAI API
LLM_MODEL=gpt-4o-mini
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

## 🎯 Design Choices

I chose a full-stack architecture with FastAPI and React to demonstrate both backend API and frontend UI capabilities within the time constraints. FastAPI provides automatic OpenAPI documentation and excellent async support for LLM streaming, while React Query handles data fetching with built-in caching and error handling. PostgreSQL with Prisma ORM enables complex search operations using raw SQL for optimal performance, particularly for the array-based topic/keyword matching with partial text search. The containerized approach with Docker Compose ensures consistent development and deployment environments, while the mock LLM mode allows development and testing without API costs. This architecture balances rapid development with production-ready patterns, creating a scalable foundation that could easily handle real-world usage.

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

## 🔧 Development

### Adding Dependencies

**Python (Server)**:

```bash
docker-compose exec server poetry add <package-name>
docker-compose restart server
```

**Node.js (Client)**:

```bash
docker-compose exec client npm install <package-name>
```

### Database Operations

```bash
# Reset database
docker-compose exec server prisma db push --force-reset

# View data
docker-compose exec server prisma studio
```

### Logs & Debugging

```bash
# View all logs
docker-compose logs -f

# View specific service logs
docker-compose logs -f server
docker-compose logs -f client
```

## 🚀 Production Deployment

For production deployment:

1. Set `LLM_MOCK_ENABLED=false` in `.env`
2. Provide real OpenAI API key
3. Remove `--reload` from server command in `docker-compose.yml`
4. Build production client: `docker-compose exec client npm run build`

## 🤝 Contributing

1. Follow the existing code structure
2. Add tests for new features
3. Update relevant README files
4. Ensure all tests pass before submitting

## 📄 License

[Your License Here]

## 🆘 Support

- **Issues**: Create GitHub issues for bugs or feature requests
- **API Docs**: Visit http://localhost:8000/docs for interactive API documentation
- **Testing**: See [testing documentation](./apps/server/tests/README.md) for troubleshooting
