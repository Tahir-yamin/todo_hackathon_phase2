/** @type {import('next').NextConfig} */
const nextConfig = {
  async rewrites() {
    return [
      {
        source: '/tasks/:path*',
        destination: 'http://127.0.0.1:8001/tasks/:path*',
      },
      {
        source: '/health',
        destination: 'http://127.0.0.1:8001/health',
      },
      {
        source: '/',
        destination: 'http://127.0.0.1:8001/',
      }
    ]
  },
}

module.exports = nextConfig