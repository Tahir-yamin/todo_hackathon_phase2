FROM node:20-slim AS builder
# Install dependencies for Prisma/Next.js
RUN apt-get update && apt-get install -y openssl ca-certificates && rm -rf /var/lib/apt/lists/*
WORKDIR /app

# Copy dependency definitions
COPY package*.json ./
COPY prisma ./prisma/

# Install dependencies inside the container
RUN npm ci

# Build Arguments - SET BEFORE COPYING SOURCE
ARG NEXT_PUBLIC_API_URL
ARG NEXT_PUBLIC_APP_URL
ARG NEXT_PUBLIC_BETTER_AUTH_URL
ENV NEXT_PUBLIC_API_URL=$NEXT_PUBLIC_API_URL
ENV NEXT_PUBLIC_APP_URL=$NEXT_PUBLIC_APP_URL
ENV NEXT_PUBLIC_BETTER_AUTH_URL=$NEXT_PUBLIC_BETTER_AUTH_URL
ENV NEXT_TELEMETRY_DISABLED=1

# Copy the rest of the source code
COPY . .

# Remove .env.local so ENV variables take precedence
RUN rm -f .env.local .env.production .env.production.local

RUN npm run build

# Copy entrypoint script for runtime env var replacement
COPY docker-entrypoint.sh /usr/local/bin/
RUN chmod +x /usr/local/bin/docker-entrypoint.sh

# Expose the port Next.js runs on
EXPOSE 3000

# Use custom entrypoint that fixes hardcoded values
ENTRYPOINT ["/usr/local/bin/docker-entrypoint.sh"]
