import { useState, useEffect } from 'react'
import { useParams } from 'react-router-dom'
import { getReport } from '../services/api'

export default function ReportPage() {
  const { sessionId } = useParams()
  const [report, setReport] = useState(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')

  useEffect(() => {
    async function fetchReport() {
      try {
        const { data } = await getReport(sessionId)
        setReport(data)
      } catch (e) {
        setError('Failed to generate report.')
      } finally {
        setLoading(false)
      }
    }
    fetchReport()
  }, [])

  if (loading) return (
    <div className="min-h-screen bg-gray-950 text-white flex items-center justify-center">
      <p className="text-gray-400 animate-pulse">Generating your report...</p>
    </div>
  )

  if (error) return (
  <div className="min-h-screen bg-gray-950 text-white flex items-center justify-center flex-col gap-4">
    <p className="text-red-400">{error}</p>
    <button
      onClick={() => { setError(''); setLoading(true); fetchReport(); }}
      className="text-sm text-indigo-400 hover:text-indigo-300"
    >
      Retry
    </button>
  </div>
)

  const insights = report?.insights || {}

  const scoreColor = insights.technical_score >= 7
    ? 'text-green-400'
    : insights.technical_score >= 5
    ? 'text-yellow-400'
    : 'text-red-400'

  const recommendationColor = {
    hire: 'bg-green-600/20 text-green-400 border-green-600',
    consider: 'bg-yellow-600/20 text-yellow-400 border-yellow-600',
    reject: 'bg-red-600/20 text-red-400 border-red-600',
  }[insights.recommendation] || 'bg-gray-700 text-gray-400 border-gray-600'

  return (
    <div className="min-h-screen bg-gray-950 text-white p-6">
      <div className="max-w-2xl mx-auto">
        <div className="flex items-center justify-between mb-8">
          <h1 className="text-xl font-bold">NexScreen</h1>
          <span className={`px-3 py-1 rounded-full border text-sm font-medium capitalize ${recommendationColor}`}>
            {insights.recommendation}
          </span>
        </div>

        <div className="bg-gray-900 rounded-2xl p-6 mb-4">
          <h2 className="text-sm text-gray-400 mb-2">Overall Summary</h2>
          <p className="text-sm leading-relaxed">{report?.summary_text}</p>
        </div>

        <div className="bg-gray-900 rounded-2xl p-6 mb-4 flex items-center justify-between">
          <h2 className="text-sm text-gray-400">Technical Score</h2>
          <span className={`text-3xl font-bold ${scoreColor}`}>
            {insights.technical_score}<span className="text-base text-gray-500">/10</span>
          </span>
        </div>

        <div className="grid grid-cols-2 gap-4 mb-4">
          <div className="bg-gray-900 rounded-2xl p-6">
            <h2 className="text-sm text-gray-400 mb-3">Strengths</h2>
            <ul className="space-y-2">
              {(insights.strengths || []).map((s, i) => (
                <li key={i} className="text-sm text-green-400 flex items-start gap-2">
                  <span>✓</span><span>{s}</span>
                </li>
              ))}
            </ul>
          </div>

          <div className="bg-gray-900 rounded-2xl p-6">
            <h2 className="text-sm text-gray-400 mb-3">Areas for Improvement</h2>
            <ul className="space-y-2">
              {(insights.areas_for_improvement || []).map((a, i) => (
                <li key={i} className="text-sm text-yellow-400 flex items-start gap-2">
                  <span>→</span><span>{a}</span>
                </li>
              ))}
            </ul>
          </div>
        </div>

        <button
          onClick={() => window.location.href = '/'}
          className="w-full bg-indigo-600 hover:bg-indigo-500 text-white font-medium py-3 rounded-lg transition-colors"
        >
          Start New Interview
        </button>
      </div>
    </div>
  )
}