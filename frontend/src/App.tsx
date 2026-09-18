import { Navigate, Route, Routes } from 'react-router-dom'
import { Layout } from './components/layout/Layout'
import Dashboard from './pages/Dashboard'
import FindingDetailsPage from './pages/FindingDetailsPage'
import Findings from './pages/Findings'
import Resources from './pages/Resources'

export default function App() {
  return (
    <Routes>
      <Route element={<Layout />}>
        <Route index element={<Navigate to="/dashboard" replace />} />
        <Route path="/dashboard" element={<Dashboard />} />
        <Route path="/findings" element={<Findings />} />
        <Route path="/findings/:findingId" element={<FindingDetailsPage />} />
        <Route path="/resources" element={<Resources />} />
        <Route path="*" element={<Navigate to="/dashboard" replace />} />
      </Route>
    </Routes>
  )
}
