FROM node:20-slim AS builder
# Install dependencies for Prisma/Next.js
RUN apt-get update && apt-get install -y openssl ca-certificates && rm -rf /var/lib/apt/lists/*
WORKDIR /app

# Copy dependency definitions
COPY package*.json ./
COPY prisma ./prisma/

# Install dependencies inside the container
RUN npm ci

# Copy the rest of the source code
COPY . .

# Build Arguments
ARG NEXT_PUBLIC_API_URL
ARG NEXT_PUBLIC_APP_URL
ENV NEXT_PUBLIC_API_URL=$NEXT_PUBLIC_API_URL
ENV NEXT_PUBLIC_APP_URL=$NEXT_PUBLIC_APP_URL
ENV NEXT_TELEMETRY_DISABLED=1

RUN npm run build

# Expose the port Next.js runs on
EXPOSE 3000

# Start the production server
CMD ["npm", "start"]
