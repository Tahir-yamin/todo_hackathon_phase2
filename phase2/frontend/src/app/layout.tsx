import type { Metadata } from 'next'
// import { Inter } from 'next/font/google' // Commented out for Docker build
import './globals.css'

// const inter = Inter({ subsets: ['latin'] })

export const metadata: Metadata = {
  title: 'TODO - Task Management',
  description: 'AI-powered task management with Kanban and smart features',
}

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="en">
      <body className="font-sans">{children}</body>
    </html>
  )
}