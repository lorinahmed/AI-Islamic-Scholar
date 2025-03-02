'use client'

import { useState } from 'react'

interface Source {
  reference: string
  text: string
  context: Record<string, string>
  chapter: string
}

interface Response {
  sources: Source[]
  reasoning: string
  confidence: number
}

export default function Home() {
  const [question, setQuestion] = useState('')
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')
  const [result, setResult] = useState<Response | null>(null)

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    setLoading(true)
    setError('')
    setResult(null)

    try {
      const response = await fetch('/api/ask', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ question }),
      })

      const data = await response.json()
      if (!response.ok) throw new Error(data.error)
      setResult(data)
    } catch (err) {
      setError(err instanceof Error ? err.message : 'An error occurred')
    } finally {
      setLoading(false)
    }
  }

  return (
    <main className="min-h-screen p-8 max-w-4xl mx-auto">
      <div className="space-y-6">
        {/* Purpose Section */}
        <div className="bg-orange-50 p-6 rounded-lg border-l-4 border-orange-500">
          <h2 className="text-xl font-bold mb-3">Research Project: AI Reasoning with Religious Texts</h2>
          <p className="mb-3">
            This tool demonstrates how artificial intelligence can analyze and reason with religious texts using RAG 
            (Retrieval Augmented Generation) and analogical reasoning (Qiyas). It shows the AI's process of:
          </p>
          <ul className="list-disc pl-5 space-y-1">
            <li>Finding relevant verses from the source text</li>
            <li>Understanding the context of these verses</li>
            <li>Applying analogical reasoning to contemporary questions</li>
          </ul>
        </div>

        {/* Disclaimer */}
        <div className="bg-blue-50 p-6 rounded-lg border-l-4 border-blue-500">
          <strong>Important Note:</strong>
          <p>
            This is an experimental AI tool for research purposes only. It should not be used as a substitute for 
            proper Islamic scholarship. Always consult qualified Islamic scholars for religious guidance.
          </p>
        </div>

        {/* Question Form */}
        <div className="bg-white p-6 rounded-lg shadow">
          <h1 className="text-2xl font-bold mb-4">Islamic AI Assistant</h1>
          <form onSubmit={handleSubmit} className="space-y-4">
            <textarea
              value={question}
              onChange={(e) => setQuestion(e.target.value)}
              placeholder="Type your question here..."
              className="w-full p-3 border rounded-lg h-32"
              required
            />
            <button
              type="submit"
              disabled={loading}
              className="bg-blue-500 hover:bg-blue-600 text-white px-6 py-2 rounded-lg 
                       disabled:bg-gray-400 transition-colors"
            >
              {loading ? 'Processing...' : 'Ask Question'}
            </button>
          </form>
        </div>

        {/* Error Message */}
        {error && (
          <div className="bg-red-50 text-red-700 p-4 rounded-lg">
            {error}
          </div>
        )}

        {/* Results */}
        {result && (
          <div className="bg-white p-6 rounded-lg shadow space-y-6">
            <div>
              <h2 className="text-xl font-bold mb-4">📚 Relevant Sources:</h2>
              {result.sources.map((source, index) => (
                <div key={index} className="bg-gray-50 p-4 rounded-lg mb-4">
                  <h3 className="font-bold">Verse {source.reference}</h3>
                  <p className="mt-2"><strong>Text:</strong> {source.text}</p>
                  <div className="mt-2">
                    <strong>Context:</strong>
                    {Object.entries(source.context).map(([ref, text]) => (
                      <p key={ref} className="ml-4 mt-1">
                        {ref}: {text}
                      </p>
                    ))}
                  </div>
                  <p className="mt-2"><strong>Chapter:</strong> {source.chapter}</p>
                </div>
              ))}
            </div>

            <div>
              <h2 className="text-xl font-bold mb-2">🤔 AI Reasoning Process:</h2>
              <p className="whitespace-pre-wrap">{result.reasoning}</p>
            </div>

            <div>
              <h2 className="text-xl font-bold mb-2">📊 Confidence Score:</h2>
              <p>{result.confidence}</p>
            </div>
          </div>
        )}
      </div>
    </main>
  )
} 