import { Navbar }      from '@/components/layout/Navbar'
import { Footer }      from '@/components/layout/Footer'
import { Hero }        from '@/components/landing/Hero'
import { StatsBar }    from '@/components/landing/StatsBar'
import { Features }    from '@/components/landing/Features'
import { ChatPreview } from '@/components/landing/ChatPreview'

export default function HomePage() {
  return (
    <div className="min-h-screen flex flex-col" style={{ background: 'var(--bg-page)' }}>
      <Navbar />
      <main className="flex-1">
        <Hero />
        <StatsBar />
        <Features />
        <ChatPreview />
      </main>
      <Footer />
    </div>
  )
}
