# Development Dockerfile for Next.js
FROM node:18-alpine

WORKDIR /app

# Copy package files
COPY package.json package-lock.json ./

# Install dependencies
RUN npm ci

# Copy source code (this will be overridden by volume mount in development)
COPY . .

# Expose the development server port
EXPOSE 3000

# Default command for development
CMD ["npm", "run", "dev"]
