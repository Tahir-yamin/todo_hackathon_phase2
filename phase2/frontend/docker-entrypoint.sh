#!/bin/sh
# Runtime Environment Variable Replacement
# This script replaces hardcoded values in Next.js build with actual env vars

echo "🔧 Replacing hardcoded IP with runtime environment variables..."

# Find all JavaScript files in .next directory
find /app/.next -type f -name "*.js" -exec sed -i \
  "s|http://20.246.145.132:3000|${NEXT_PUBLIC_BETTER_AUTH_URL:-http://localhost:30000}|g" {} +

echo "✅ Runtime replacement complete!"

# Start Next.js
exec npm start
