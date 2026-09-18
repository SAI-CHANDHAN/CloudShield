import type { Finding, Resource, RiskSummary, ScanResponse } from '../types/cloudshield'

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://127.0.0.1:8000'

async function request<T>(path: string, options?: RequestInit): Promise<T> {
  const response = await fetch(`${API_BASE_URL}${path}`, {
    ...options,
    headers: { 'Content-Type': 'application/json', ...options?.headers },
  })
  if (!response.ok) throw new Error(`CloudShield API request failed (${response.status})`)
  return response.json() as Promise<T>
}

export const api = {
  getHealth: () => request<{ status: string }>('/api/health'),
  getResources: () => request<Resource[]>('/api/resources'),
  getFindings: () => request<Finding[]>('/api/findings'),
  getFinding: (id: string) => request<Finding>(`/api/findings/${encodeURIComponent(id)}`),
  getRiskSummary: () => request<RiskSummary>('/api/risk/summary'),
  runScan: () => request<ScanResponse>('/api/scan', { method: 'POST' }),
}

export { API_BASE_URL }
