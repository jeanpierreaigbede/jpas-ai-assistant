import React from 'react'
import ReactMarkdown from 'react-markdown'

type Result = {
  summary?: string
  source?: string
  char_count?: number
  [key: string]: any
}

function stripTldr(text: string): string {
  return text
    .replace(/^\*\*TL;DR:?\*\*[:\s]*/i, '')
    .replace(/^TL;DR:?\s*/i, '')
    .trim()
}

export default function ResultView({ result }: { result: Result }) {
  const summary = stripTldr(result.summary || 'No summary provided.')

  return (
    <div className="card result-card">
      <h2 className="result-title">Summary</h2>
      <div className="summary-content">
        <ReactMarkdown>{summary}</ReactMarkdown>
      </div>

      {result.source && (
        <div className="source-info">
          <h3>Source</h3>
          <p>{result.source}</p>
          {result.char_count && (
            <p className="char-count">Article length: {result.char_count} characters</p>
          )}
        </div>
      )}
    </div>
  )
}
