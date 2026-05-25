import type { Metadata } from 'next'
import { ThemeProvider } from 'next-themes'
import { AuthProvider } from '@/contexts/AuthContext'
import '@/styles/globals.css'

export const metadata: Metadata = {
  title: 'Mizan — Pakistan Legal AI',
  description: 'AI-powered legal intelligence grounded in Pakistani law. Ask questions, analyze documents, draft contracts.',
  keywords: ['Pakistan law', 'legal AI', 'PPC', 'CrPC', 'Constitution of Pakistan', 'legal research'],
  openGraph: {
    title: 'Mizan — Pakistan Legal AI',
    description: 'AI-powered legal intelligence grounded in Pakistani law.',
    type: 'website',
  },
}

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en" suppressHydrationWarning>
      <body>
        <ThemeProvider
          attribute="class"
          defaultTheme="light"
          enableSystem
          disableTransitionOnChange={false}
        >
          <AuthProvider>
            {children}
          </AuthProvider>
        </ThemeProvider>
      </body>
    </html>
  )
}
