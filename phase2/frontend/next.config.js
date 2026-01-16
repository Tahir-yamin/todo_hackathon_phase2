/** @type {import('next').NextConfig} */
const nextConfig = {
  async rewrites() {
    return [
      {
        // Proxy all /api requests EXCEPT /api/auth (handled by Better-Auth locally)
        source: '/api/:path((?!auth).*)',
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