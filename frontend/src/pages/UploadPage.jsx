import { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { uploadResume, startSession } from '../services/api'
import { useSession } from '../context/SessionContext'

const ROLES = [
  { key: 'ai_ml', label: 'AI / ML Engineer' },
  { key: 'data_science', label: 'Data Science / Applied ML' },
]

export default function UploadPage() {
  const navigate = useNavigate()
  const { setSessionId, setResumeData, setRole } = useSession()

  const [file, setFile] = useState(null)
  const [role, setRoleLocal] = useState('')
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')

  async function handleSubmit() {
    if (!file || !role) {
      setError('Please upload a resume and select a role.')
      return
    }
    setLoading(true)
    setError('')
    try {
      const formData = new FormData()
      formData.append('file', file)
      const { data: resumeData } = await uploadResume(formData)

      const { data: session } = await startSession({
        role,
        resume_text: resumeData.resume_text,
        extracted_skills: resumeData.extracted_skills,
        candidate_name: resumeData.candidate_name,
      })

      setSessionId(session.id)
      setResumeData(resumeData)
      setRole(role)
      navigate(`/interview/${session.id}`)
    } catch (e) {
      setError('Something went wrong. Please try again.')
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="min-h-screen bg-gray-950 text-white flex items-center justify-center p-6">
      <div className="w-full max-w-md bg-gray-900 rounded-2xl p-8 shadow-xl">
        <h1 className="text-2xl font-bold mb-2">NexScreen</h1>
        <p className="text-gray-400 mb-8 text-sm">AI-powered technical interview screening</p>

        <div className="mb-6">
          <label className="block text-sm font-medium mb-2">Upload Resume (PDF)</label>
          <input
            type="file"
            accept=".pdf"
            onChange={(e) => setFile(e.target.files[0])}
            className="w-full text-sm text-gray-400 file:mr-4 file:py-2 file:px-4 file:rounded-lg file:border-0 file:bg-indigo-600 file:text-white hover:file:bg-indigo-500 cursor-pointer"
          />
          {file && <p className="text-xs text-gray-500 mt-1">{file.name}</p>}
        </div>

        <div className="mb-8">
          <label className="block text-sm font-medium mb-2">Select Role</label>
          <div className="space-y-2">
            {ROLES.map((r) => (
              <button
                key={r.key}
                onClick={() => setRoleLocal(r.key)}
                className={`w-full text-left px-4 py-3 rounded-lg border text-sm transition-colors ${
                  role === r.key
                    ? 'border-indigo-500 bg-indigo-600/20 text-white'
                    : 'border-gray-700 text-gray-400 hover:border-gray-500'
                }`}
              >
                {r.label}
              </button>
            ))}
          </div>
        </div>

        {error && <p className="text-red-400 text-sm mb-4">{error}</p>}

        <button
          onClick={handleSubmit}
          disabled={loading}
          className="w-full bg-indigo-600 hover:bg-indigo-500 disabled:bg-gray-700 disabled:text-gray-500 text-white font-medium py-3 rounded-lg transition-colors"
        >
          {loading ? 'Processing...' : 'Start Interview'}
        </button>
      </div>
    </div>
  )
}