import React, { useState } from 'react'

type SummaryResult = {
  summary?: string
  source?: string
  char_count?: number
  [key: string]: any
}

export default function UploadForm({ onSuccess }: { onSuccess: (data: SummaryResult) => void }) {
  const [file, setFile] = useState<File | null>(null)
  const [url, setUrl] = useState('')
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')

  const apiBase = process.env.NEXT_PUBLIC_API_BASE || 'http://localhost:8000'

  async function getErrorMessage(res: Response, fallback: string): Promise<string> {
    if (res.status === 413) {
      return 'This PDF is too large. Please use a file under 20 MB.'
    }
    try {
      const body = await res.json()
      return body?.detail || fallback
    } catch {
      return fallback
    }
  }

  async function handleSubmit(e: React.FormEvent) {
    e.preventDefault()
    setError('')
    if (!file && !url) {
      setError('Please provide a PDF file or a URL')
      return
    }
    const MAX_PDF_SIZE = 20 * 1024 * 1024 // 20 MB
    if (file && file.size > MAX_PDF_SIZE) {
      setError('This PDF is too large. Please use a file under 20 MB.')
      return
    }

    setLoading(true)
    try {
      let data

      if (url) {
        const res = await fetch(`${apiBase}/summarize/url`, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ url })
        })
        if (!res.ok) {
          const msg = await getErrorMessage(res, 'Could not summarize this URL. Please try another link.')
          throw new Error(msg)
        }
        data = await res.json()
      } else if (file) {
        const form = new FormData()
        form.append('file', file)
        const res = await fetch(`${apiBase}/summarize/pdf`, {
          method: 'POST',
          body: form
        })
        if (!res.ok) {
          const msg = await getErrorMessage(res, 'Could not summarize this PDF. Please try again.')
          throw new Error(msg)
        }
        data = await res.json()
      }

      if (data) {
        onSuccess(data)
      }
    } catch (err: any) {
      const message = err?.message || 'Submission failed'
      if (message === 'Failed to fetch' || message.includes('NetworkError')) {
        setError('Unable to connect. Please check your connection and that the server is running.')
      } else {
        setError(message)
      }
    } finally {
      setLoading(false)
    }
  }

  return (
    <form className="card" onSubmit={handleSubmit}>
      <label className="label">Upload PDF</label>
      <div className={`file-wrapper ${file ? 'has-file' : ''}`}>
        <input
          type="file"
          accept="application/pdf"
          onChange={(e) => setFile(e.target.files ? e.target.files[0] : null)}
        />
        <div className="file-zone">
          <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
            <path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4" />
            <polyline points="17 8 12 3 7 8" />
            <line x1="12" y1="3" x2="12" y2="15" />
          </svg>
          <span>{file ? file.name : 'Drop a PDF here or click to browse'}</span>
        </div>
      </div>

      <div className="divider"><span>or</span></div>

      <label className="label">Paste article URL</label>
      <input
        type="url"
        placeholder="https://example.com/article"
        value={url}
        onChange={(e) => setUrl(e.target.value)}
      />

      {error && <p className="error">{error}</p>}

      <button type="submit" className="btn" disabled={loading}>
        {loading ? 'Summarizing…' : 'Get summary'}
      </button>
    </form>
  )
}
