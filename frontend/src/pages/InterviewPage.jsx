import { useState, useEffect } from 'react'
import { useParams, useNavigate } from 'react-router-dom'
import { getNextQuestion, submitAnswer } from '../services/api'
import ReactMarkdown from 'react-markdown'

const TOTAL_QUESTIONS = 5

export default function InterviewPage() {
  const { sessionId } = useParams()
  const navigate = useNavigate()

  const [question, setQuestion] = useState(null)
  const [answer, setAnswer] = useState('')
  const [loading, setLoading] = useState(false)
  const [submitting, setSubmitting] = useState(false)
  const [questionNumber, setQuestionNumber] = useState(1)
  const [loadError, setLoadError] = useState('')
  const [submitError, setSubmitError] = useState('')

  useEffect(() => {
    fetchNextQuestion()
  }, [])

  async function fetchNextQuestion() {
    setLoading(true)
    setLoadError('')
    try {
      const { data } = await getNextQuestion(sessionId)
      setQuestion(data)
      setAnswer('')
    } catch (e) {
      setLoadError('Failed to load question.')
    } finally {
      setLoading(false)
    }
  }

  async function handleSubmit() {
    if (!answer.trim()) {
      setSubmitError('Please enter an answer.')
      return
    }
    setSubmitting(true)
    setSubmitError('')
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
      setSubmitError('Failed to submit answer. Please try again.')
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
            style={{ width: `${(questionNumber / TOTAL_QUESTIONS) * 100}%` }}
          />
        </div>

        <div className="bg-gray-900 rounded-2xl p-8 shadow-xl mb-6 min-h-[120px] flex items-center">
          {loading ? (
            <div className="flex items-center gap-3 text-gray-400 text-sm">
              <div className="w-4 h-4 border-2 border-gray-600 border-t-indigo-400 rounded-full animate-spin" />
              Generating question...
            </div>
          ) : loadError ? (
            <div className="w-full">
              <p className="text-red-400 text-sm mb-4">{loadError}</p>
              <button
                onClick={fetchNextQuestion}
                className="px-4 py-2 bg-indigo-600 hover:bg-indigo-500 text-white text-sm rounded-lg transition-colors"
              >
                Retry
              </button>
            </div>
          ) : (
            <div className="text-lg leading-relaxed">
              <ReactMarkdown>{question?.question_text}</ReactMarkdown>
            </div>
          )}
        </div>

        <div className="mb-4">
          <textarea
            value={answer}
            onChange={(e) => { setAnswer(e.target.value); setSubmitError('') }}
            placeholder="Type your answer here..."
            rows={6}
            disabled={loading || !!loadError}
            className="w-full bg-gray-900 border border-gray-700 rounded-xl p-4 text-sm text-white placeholder-gray-500 focus:outline-none focus:border-indigo-500 resize-none disabled:opacity-50"
          />
        </div>

        {submitError && <p className="text-red-400 text-sm mb-4">{submitError}</p>}

        <button
          onClick={handleSubmit}
          disabled={submitting || loading || !!loadError}
          className="w-full bg-indigo-600 hover:bg-indigo-500 disabled:bg-gray-700 disabled:text-gray-500 text-white font-medium py-3 rounded-lg transition-colors"
        >
          {submitting ? (
            <span className="flex items-center justify-center gap-2">
              <div className="w-4 h-4 border-2 border-gray-500 border-t-white rounded-full animate-spin" />
              Submitting...
            </span>
          ) : questionNumber >= TOTAL_QUESTIONS ? 'Finish Interview' : 'Next Question'}
        </button>
      </div>
    </div>
  )
}