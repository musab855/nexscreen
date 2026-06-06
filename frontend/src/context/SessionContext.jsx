import { createContext, useContext, useState } from 'react'

const SessionContext = createContext(null)

export function SessionProvider({ children }) {
  const [sessionId, setSessionId] = useState(null)
  const [resumeData, setResumeData] = useState(null)
  const [role, setRole] = useState(null)

  return (
    <SessionContext.Provider value={{ sessionId, setSessionId, resumeData, setResumeData, role, setRole }}>
      {children}
    </SessionContext.Provider>
  )
}

export function useSession() {
  return useContext(SessionContext)
}