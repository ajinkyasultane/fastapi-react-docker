import { useEffect, useState } from 'react'
import Dashboard from './pages/Dashboard'
import './index.css'

export default function App() {
  const [health, setHealth] = useState<any>(null)

  useEffect(() => {
    fetch('/health')
      .then(r => r.json())
      .then(setHealth)
      .catch(() => setHealth({ status: 'error' }))
  }, [])

  return (
    <div className="min-h-screen p-6">
      <header className="mb-6">
        <h1 className="text-2xl font-bold">Admin Dashboard</h1>
        <p className="text-sm text-gray-600">Backend health: {health?.status}</p>
      </header>
      <Dashboard />
    </div>
  )
}
