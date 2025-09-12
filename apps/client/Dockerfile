# --- Stage 1: Install dependencies ---
FROM node:18-alpine AS deps
WORKDIR /app
# Correct the COPY path to be relative to the build context
COPY package.json package-lock.json ./
RUN npm ci

# --- Stage 2: Build the Next.js app ---
FROM node:18-alpine AS builder
WORKDIR /app
COPY --from=deps /app/node_modules ./node_modules
# Correct the COPY path to be relative to the build context
COPY . .
RUN npm run build

# --- Stage 3: Run the Next.js production server ---
FROM node:18-alpine AS runner
WORKDIR /app
ENV NODE_ENV production
COPY --from=builder /app/.next ./.next
COPY --from=builder /app/node_modules ./node_modules
# Correct the COPY path to be relative to the build context
COPY --from=builder /app/package.json ./package.json
EXPOSE 3000
CMD ["npm", "start"]
