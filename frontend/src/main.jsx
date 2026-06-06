import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'
import { SessionProvider } from './context/SessionContext'
import App from './App'
import './index.css'

createRoot(document.getElementById('root')).render(
    <SessionProvider>
      <App />
    </SessionProvider>
  
  // <StrictMode>
  //   <SessionProvider>
  //     <App />
  //   </SessionProvider>
  // </StrictMode>
)