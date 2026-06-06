import { useState, useEffect } from 'react'
import { useParams, useNavigate } from 'react-router-dom'
import { getNextQuestion, submitAnswer } from '../services/api'
import { useSession } from '../context/SessionContext'

export default function InterviewPage() {
  const { sessionId } = useParams()
  const navigate = useNavigate()
  const { resumeData } = useSession()

  const [question, setQuestion] = useState(null)
  const [answer, setAnswer] = useState('')
  const [loading, setLoading] = useState(false)
  const [submitting, setSubmitting] = useState(false)
  const [questionNumber, setQuestionNumber] = useState(1)
  const [error, setError] = useState('')

  const TOTAL_QUESTIONS = 5

  useEffect(() => {
    fetchNextQuestion()
  }, [])

  async function fetchNextQuestion() {
    setLoading(true)
    setError('')
    try {
      const { data } = await getNextQuestion(sessionId)
      setQuestion(data)
      setAnswer('')
    } catch (e) {
      setError('Failed to load question. Click retry.')
      setLoading(false)
      return
    }
    setLoading(false)
  }

  async function handleSubmit() {
    if (!answer.trim()) {
      setError('Please enter an answer.')
      return
    }
    setSubmitting(true)
    setError('')
    try {
      await submitAnswer(sessionId, {
        question_id: question.id,
        answer_text: answer,
      })

      if (questionNumber >= TOTAL_QUESTIONS) {
        navigate(`/report/${sessionId}`)
      } else {
        setQuestionNumber((n) => n + 1)
        fetchNextQuestion()
      }
    } catch (e) {
      setError('Failed to submit answer. Please try again.')
    } finally {
      setSubmitting(false)
    }
  }

  return (
    <div className="min-h-screen bg-gray-950 text-white flex items-center justify-center p-6">
      <div className="w-full max-w-2xl">
        <div className="flex items-center justify-between mb-8">
          <h1 className="text-xl font-bold">NexScreen</h1>
          <span className="text-sm text-gray-400">Question {questionNumber} of {TOTAL_QUESTIONS}</span>
        </div>

        <div className="w-full bg-gray-800 rounded-full h-1.5 mb-8">
          <div
            className="bg-indigo-500 h-1.5 rounded-full transition-all"
            style={{ width: `${((questionNumber) / TOTAL_QUESTIONS) * 100}%` }}
          />
        </div>

        <div className="bg-gray-900 rounded-2xl p-8 shadow-xl mb-6">
          {loading ? (
            <div className="text-gray-400 text-sm animate-pulse">Generating question...</div>
          ) : (
            <p className="text-lg leading-relaxed">{question?.question_text}</p>
          )}
        </div>

        <div className="mb-6">
          <textarea
            value={answer}
            onChange={(e) => setAnswer(e.target.value)}
            placeholder="Type your answer here..."
            rows={6}
            className="w-full bg-gray-900 border border-gray-700 rounded-xl p-4 text-sm text-white placeholder-gray-500 focus:outline-none focus:border-indigo-500 resize-none"
          />
        </div>

        {error && (
          <div className="mb-4">
            <p className="text-red-400 text-sm mb-2">{error}</p>
            <button
              onClick={fetchNextQuestion}
              className="text-sm text-indigo-400 hover:text-indigo-300"
            >
              Retry
            </button>
          </div>
        )}

        <button
          onClick={handleSubmit}
          disabled={submitting || loading}
          className="w-full bg-indigo-600 hover:bg-indigo-500 disabled:bg-gray-700 disabled:text-gray-500 text-white font-medium py-3 rounded-lg transition-colors"
        >
          {submitting ? 'Submitting...' : questionNumber >= TOTAL_QUESTIONS ? 'Finish Interview' : 'Next Question'}
        </button>
      </div>
    </div>
  )
}