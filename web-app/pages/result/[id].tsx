import { useRouter } from 'next/router'
import { useEffect, useState } from 'react'
import ResultView from '../../components/ResultView'

export default function ResultPage() {
  const router = useRouter()
  const [result, setResult] = useState<any>(null)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    const stored = localStorage.getItem('lastResult')
    if (stored) {
      try {
        setResult(JSON.parse(stored))
      } catch (e) {
        console.error('Failed to parse stored result', e)
      }
    }
    setLoading(false)
  }, [])

  if (loading) return <p>Loading...</p>
  if (!result) return <p>No result found. Please submit a URL or PDF first.</p>

  return (
    <main className="container">
      <ResultView result={result} />
    </main>
  )
}
