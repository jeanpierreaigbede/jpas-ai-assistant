import Head from 'next/head'
import { useState } from 'react'
import UploadForm from '../components/UploadForm'
import ResultView from '../components/ResultView'

type SummaryResult = {
  summary?: string
  source?: string
  char_count?: number
  [key: string]: any
}

export default function Home() {
  const systemName = process.env.NEXT_PUBLIC_SYSTEM_NAME || 'Assistant AI'
  const [result, setResult] = useState<SummaryResult | null>(null)

  return (
    <div>
      <Head>
        <title>{systemName}</title>
        <meta name="description" content="Assistant AI frontend" />
      </Head>

      <main className="container">
        <header className="intro-section">
          <h1 className="main-title">JPAS ASSISTANT</h1>
          <p className="intro-text">
            Welcome to JPAS Assistant, your intelligent article summarizer powered by advanced AI. Simply upload a PDF document or paste a URL, and our system will extract the key information and provide you with a concise, easy-to-understand summary. Whether you're researching, learning, or staying informed, JPAS Assistant transforms lengthy articles into actionable insights in seconds.
          </p>
        </header>
        <UploadForm onSuccess={setResult} />
        {result && <ResultView result={result} />}
      </main>
    </div>
  )
}
