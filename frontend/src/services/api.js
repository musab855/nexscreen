import axios from 'axios'

const api = axios.create({
  baseURL: import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000',
})

export const uploadResume = (formData) =>
  api.post('/api/v1/resume/upload', formData)

export const startSession = (data) =>
  api.post('/api/v1/session/start', data)

export const getNextQuestion = (sessionId) =>
  api.get(`/api/v1/interview/${sessionId}/next`)

export const submitAnswer = (sessionId, data) =>
  api.post(`/api/v1/interview/${sessionId}/answer`, data)

export const getReport = (sessionId) =>
  api.get(`/api/v1/report/${sessionId}`)