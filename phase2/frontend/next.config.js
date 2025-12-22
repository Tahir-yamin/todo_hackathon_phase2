/** @type {import('next').NextConfig} */
const nextConfig = {
  output: 'export',
  basePath: process.env.NODE_ENV === 'production' ? '/todo_hackathon_phase2' : '',
  assetPrefix: process.env.NODE_ENV === 'production' ? '/todo_hackathon_phase2/' : '',
  images: {
    unoptimized: true,
  },
}

module.exports = nextConfig