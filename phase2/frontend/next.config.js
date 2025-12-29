/** @type {import('next').NextConfig} */
const nextConfig = {
  // Enable standalone output for Docker/Kubernetes deployment
  output: 'standalone',
  // API routes and Better Auth require server-side rendering
}

module.exports = nextConfig