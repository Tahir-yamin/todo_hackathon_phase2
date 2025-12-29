# STAGE 1: Dependencies
FROM node:20-slim AS deps
RUN apt-get update && apt-get install -y openssl ca-certificates
WORKDIR /app

# Copy package files and Prisma schema
COPY phase2/frontend/package*.json ./
COPY phase2/frontend/prisma ./prisma/

# Install dependencies with retries
RUN for i in 1 2 3; do npm install && break || sleep 5; done

# STAGE 2: Builder
FROM node:20-slim AS builder
WORKDIR /app

# Copy dependencies from deps stage
COPY --from=deps /app/node_modules ./node_modules

# Copy all frontend source code
COPY phase2/frontend ./

# Build Next.js in standalone mode
ENV NEXT_TELEMETRY_DISABLED=1

# Build-time environment variables (NEXT_PUBLIC_* are embedded at build time)
ARG NEXT_PUBLIC_API_URL=http://localhost:8000
ARG NEXT_PUBLIC_APP_URL=http://localhost:3000
ARG BETTER_AUTH_URL=http://localhost:3000
ENV NEXT_PUBLIC_API_URL=$NEXT_PUBLIC_API_URL
ENV NEXT_PUBLIC_APP_URL=$NEXT_PUBLIC_APP_URL
ENV BETTER_AUTH_URL=$BETTER_AUTH_URL

# Skip Google Fonts download during build (network timeout issue)
ENV NEXT_FONT_GOOGLE_MOCKED_RESPONSES='[{"url":"https://fonts.googleapis.com/css2?family=Inter:wght@100..900&display=swap","content":"/* mocked */"}]'

# Generate Prisma client
RUN npx prisma generate

RUN npm run build

# Ensure public folder exists for COPY in next stage
RUN mkdir -p public

# STAGE 3: Runner
FROM node:20-slim AS runner
RUN apt-get update && apt-get install -y openssl ca-certificates && rm -rf /var/lib/apt/lists/*
WORKDIR /app

ENV NODE_ENV=production
ENV NEXT_TELEMETRY_DISABLED=1

# Create non-root user for security
RUN groupadd --system --gid 1001 nodejs
RUN useradd --system --uid 1001 nextjs

# Copy built application
COPY --from=builder /app/public ./public
COPY --from=builder --chown=nextjs:nodejs /app/.next/standalone ./
COPY --from=builder --chown=nextjs:nodejs /app/.next/static ./.next/static

# Copy Prisma client (not included in standalone build)
COPY --from=builder --chown=nextjs:nodejs /app/node_modules/.prisma ./node_modules/.prisma
COPY --from=builder --chown=nextjs:nodejs /app/node_modules/@prisma ./node_modules/@prisma

USER nextjs

EXPOSE 3000

ENV PORT=3000
ENV HOSTNAME="0.0.0.0"

CMD ["node", "server.js"]
