/** @type {import('next').NextConfig} */
const nextConfig = {
  async rewrites() {
    return [
      {
        source: '/api/:path*',
        destination: process.env.NEXT_PUBLIC_API_URL
          ? `${process.env.NEXT_PUBLIC_API_URL}/api/:path*`
          : 'http://backend-service:8000/api/:path*', // Internal K8s DNS fallback
      },
    ];
  },
  // Enable standalone output for Docker/Kubernetes deployment
  output: 'standalone',
  // API routes and Better Auth require server-side rendering
}

module.exports = nextConfig