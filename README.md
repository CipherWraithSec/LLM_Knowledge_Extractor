# LLM Knowledge Extractor

A multi-container project with:
- Python FastAPI server (`apps/server`)
- Next.js client (`apps/client`)
- PostgreSQL database

## Prerequisites

- Docker & Docker Compose installed
- `.env` file at project root with:
  ```dotenv
  # PostgreSQL
  POSTGRES_USER=your_user
  POSTGRES_PASSWORD=your_password
  POSTGRES_DB=your_db

  # (Optional) Any other variables used by server or client
  ```

## Setup & Run (Development)

1. Clone the repo:
   ```bash
   git clone https://github.com/your-org/LLM_Knowledge_Extractor.git
   cd LLM_Knowledge_Extractor
   ```

2. Create and populate `.env` (see Prerequisites).

3. Start all services with hot-reload:
   ```bash
   docker-compose up -d --build
   ```

4. Access services:
   - Server (FastAPI): http://localhost:8000
   - Client (Next.js): http://localhost:3000

Changes to `apps/server` or `apps/client` are automatically reflected via Uvicorn and Next.js dev servers.

## Database & Prisma

1. Ensure your `.env` contains a `DATABASE_URL`, for example:
   ```dotenv
   DATABASE_URL=postgresql://your_user:your_password@db:5432/your_db
   ```

2. Create/apply migrations and generate the Prisma client:
   ```bash
   docker-compose exec server prisma migrate dev --schema=prisma/schema.prisma --name init
   docker-compose exec server prisma generate --schema=prisma/schema.prisma
   ```

3. Use the generated client in your FastAPI code. A sample endpoint is available:
   ```bash
   curl http://localhost:8000/analyses
   ```

## Installing Dependencies

### Client (Node.js)

Inside the running container:
```bash
docker-compose exec client npm install <package-name> --save
```
This updates `package.json` and installs into the container’s `node_modules`.

### Server (Python)

Inside the running container:
```bash
docker-compose exec server poetry add <package-name>
```
Then restart the server to pick up new packages:
```bash
docker-compose restart server
```

## Production

For production builds:

```bash
# Client:
docker-compose exec client npm run build
# Server (rebuild image without --reload):
docker-compose up -d --build server
```

Remove `--reload` flag from the server command in `docker-compose.yml` for production.

