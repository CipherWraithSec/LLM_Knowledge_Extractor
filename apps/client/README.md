# 🖥️ Next.js Client

The frontend application for the LLM Knowledge Extractor, built with Next.js 15 and TypeScript.

## 🏗️ Architecture

- **Framework**: Next.js 15 with App Router
- **Language**: TypeScript
- **Styling**: Tailwind CSS
- **UI State Manager**: Redux toolkit
- **Cache and pagination**: React Query
- **API Integration**: REST API calls to FastAPI backend
- **Containerization**: Docker for development and production

## ✨ Features

- **Text Analysis Interface**: User-friendly form for text input and analysis
- **Results Display**: Comprehensive view of analysis results (topics, sentiment, keywords)
- **Search Functionality**: Browse and search through previous analyses
- **Responsive Design**: Works on desktop and mobile devices
- **Real-time Updates**: Live connection with the backend API

## 🚀 Quick Start

### Using Docker (Recommended)

From the project root directory:

```bash
# Start all services including client
docker-compose up -d --build

# Access the application
open http://localhost:3000
```

### Local Development

```bash
# Install dependencies
npm install

# Set up environment variables
echo "NEXT_PUBLIC_API_URL=http://localhost:8000/api/v1" > .env.local

# Start development server
npm run dev

# Access the application
open http://localhost:3000
```

## ⚙️ Configuration

Environment variables for the client:

```env
# API Configuration
NEXT_PUBLIC_API_URL=http://localhost:8000/api/v1  # Backend API URL
```

### Environment Files

- `.env.local` - Local development overrides
- `.env` - Default environment variables (in project root)

## 📁 Project Structure

```
client/
├── README.md              # This file
├── package.json           # Node.js dependencies
├── next.config.ts         # Next.js configuration
├── tsconfig.json          # TypeScript configuration
├── tailwind.config.ts     # Tailwind CSS configuration
├── postcss.config.mjs     # PostCSS configuration
├── Dockerfile             # Container configuration
└── app/                   # Next.js App Router
    ├── layout.tsx         # Root layout
    ├── page.tsx           # Home page
    ├── globals.css        # Global styles
    └── components/        # React components (if any)
```

## 🔧 Development

### Adding Dependencies

```bash
# Add production dependency
docker-compose exec client npm install package-name

# Add development dependency
docker-compose exec client npm install --save-dev package-name

# Or if working locally
npm install package-name
```

### Available Scripts

```bash
# Development server with hot reload
npm run dev

# Production build
npm run build

# Start production server
npm run start

# Lint code
npm run lint
```

### API Integration

The client communicates with the FastAPI backend at `NEXT_PUBLIC_API_URL`.

Example API calls:

```typescript
// Analyze text
const response = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/analyze`, {
  method: "POST",
  headers: { "Content-Type": "application/json" },
  body: JSON.stringify({ text: userInput }),
});

// Search analyses
const results = await fetch(
  `${process.env.NEXT_PUBLIC_API_URL}/search?topic=keyword`
);
```

## 🚀 Production Build

```bash
# Build for production
docker-compose exec client npm run build

# Or locally
npm run build
npm run start
```

### Production Deployment

1. **Environment Variables**: Set production API URL
2. **Build Optimization**: Next.js automatically optimizes for production
3. **Static Assets**: Served efficiently with proper caching headers
4. **Container**: Use production Dockerfile configuration

## 🐛 Debugging

### Common Issues

- **API Connection**: Check NEXT_PUBLIC_API_URL and backend availability
- **CORS Issues**: Ensure backend allows frontend origin
- **Build Errors**: Check TypeScript compilation and import paths
- **Styling Issues**: Verify Tailwind CSS configuration and classes

### View Logs

```bash
# Client logs
docker-compose logs -f client

# Build logs
docker-compose exec client npm run build
```

## 📚 Related Documentation

- **[Project Overview](../../README.md)** - Full project setup and architecture
- **[Server Documentation](../server/README.md)** - Backend API reference
- **[Testing Documentation](../server/tests/README.md)** - API testing information
