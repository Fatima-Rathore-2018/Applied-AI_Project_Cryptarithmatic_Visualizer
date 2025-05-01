import type { Metadata } from 'next'
import './globals.css'

export const metadata: Metadata = {
  title: 'Cryptarithmetic Visualizer',
  icons: {
    icon: '<a href="https://www.flaticon.com/free-icons/problem-solver" title="problem solver icons">Problem solver icons created by Iconic Panda - Flaticon</a>'
  },
}

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode
}>) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  )
}
