# Use a single-stage build for simplicity
FROM python:3.11-alpine

# Set the working directory
WORKDIR /app

# Install system dependencies and Poetry installer
RUN apk add --no-cache curl build-base \
    && curl -sSL https://install.python-poetry.org | python3 -

# Add Poetry to PATH
ENV PATH="/root/.local/bin:$PATH"

# Copy dependency metadata and install Python dependencies
COPY pyproject.toml poetry.lock ./
RUN poetry config virtualenvs.create false \
    && poetry install --no-interaction --no-ansi --only main

# Copy application code
COPY . .

# Copy local SpaCy model if available, otherwise download it
RUN if [ -d "./models/en_core_web_sm" ]; then \
        echo "Using local SpaCy model"; \
    else \
        echo "Downloading SpaCy model..." && python -m spacy download en_core_web_sm; \
    fi

# Install Node.js for Prisma CLI and OpenSSL for Prisma Engine
RUN apk add --no-cache nodejs npm openssl openssl-dev libc6-compat


# Expose application port
EXPOSE 8000

# Start the FastAPI server with Uvicorn
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]

