import { CheckCircle2, Play, RefreshCw } from 'lucide-react'
import { useEffect, useState } from 'react'
import { api } from '../services/api'
import type { Finding, Resource, RiskSummary } from '../types/cloudshield'
import { ErrorState, LoadingState } from '../components/common/States'
import { SectionHeader } from '../components/common/SectionHeader'
import { FindingsTrend } from '../components/dashboard/FindingsTrend'
import { RecentFindings } from '../components/dashboard/RecentFindings'
import { RiskScoreCard } from '../components/dashboard/RiskScoreCard'
import { SecurityOverview } from '../components/dashboard/SecurityOverview'
import { SeverityBreakdown } from '../components/dashboard/SeverityBreakdown'

export default function Dashboard() { const [summary, setSummary] = useState<RiskSummary | null>(null); const [findings, setFindings] = useState<Finding[]>([]); const [resources, setResources] = useState<Resource[]>([]); const [loading, setLoading] = useState(true); const [scanning, setScanning] = useState(false); const [error, setError] = useState(false); const [notice, setNotice] = useState<string | null>(null)
  const load = async () => { setLoading(true); setError(false); try { const [nextSummary, nextFindings, nextResources] = await Promise.all([api.getRiskSummary(), api.getFindings(), api.getResources()]); setSummary(nextSummary); setFindings(nextFindings); setResources(nextResources) } catch { setError(true) } finally { setLoading(false) } }
  useEffect(() => { void load() }, [])
  const scan = async () => { setScanning(true); setNotice(null); try { await api.runScan(); await load(); setNotice('Security scan completed.') } catch { setNotice('The security scan could not be completed. Please try again.') } finally { setScanning(false) } }
  if (loading) return <LoadingState label="Loading your security posture" />
  if (error || !summary) return <ErrorState onRetry={() => void load()} />
  return <div className="animate-rise"><div className="mb-8 flex flex-col justify-between gap-5 sm:flex-row sm:items-end"><div><p className="mb-2 text-[10px] font-bold uppercase tracking-[0.22em] text-cyan">CloudShield / Overview</p><h1 className="font-display text-3xl font-bold tracking-tight text-slate-950 sm:text-4xl">Security Overview</h1><p className="mt-2 text-sm text-slate-500">Real-time visibility into your cloud security posture.</p></div><button onClick={() => void scan()} disabled={scanning} className="inline-flex items-center justify-center gap-2 rounded-xl bg-ink px-4 py-3 text-sm font-bold text-white shadow-lg shadow-ink/10 transition hover:-translate-y-0.5 hover:bg-slate-800 disabled:cursor-wait disabled:opacity-70"><span className={scanning ? 'animate-spin' : ''}>{scanning ? <RefreshCw size={16} /> : <Play size={16} fill="currentColor" />}</span>{scanning ? 'Scanning environment...' : 'Run security scan'}</button></div>{notice && <div className={`mb-5 flex items-center gap-2 rounded-xl border px-4 py-3 text-sm font-semibold ${notice.includes('completed') ? 'border-emerald-100 bg-emerald-50 text-emerald-700' : 'border-rose-100 bg-rose-50 text-rose-700'}`}><CheckCircle2 size={16} />{notice}</div>}<div className="grid gap-5 xl:grid-cols-[1.12fr_1fr]"><RiskScoreCard summary={summary} /><SeverityBreakdown summary={summary} /></div><div className="mt-5"><SectionHeader eyebrow="Posture at a glance" title="Security overview" /><SecurityOverview summary={summary} resources={resources} /></div><div className="mt-8 grid gap-5 xl:grid-cols-[1.12fr_1fr]"><RecentFindings findings={findings} /><FindingsTrend /></div></div>
}
