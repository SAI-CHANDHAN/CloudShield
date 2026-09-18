import { useCallback, useEffect, useState } from 'react'
import { FindingTable } from '../components/findings/FindingTable'
import { ErrorState, LoadingState } from '../components/common/States'
import { SectionHeader } from '../components/common/SectionHeader'
import { api } from '../services/api'
import type { Finding } from '../types/cloudshield'

export default function Findings() { const [findings, setFindings] = useState<Finding[]>([]); const [loading, setLoading] = useState(true); const [error, setError] = useState(false); const load = useCallback(async () => { setLoading(true); setError(false); try { setFindings(await api.getFindings()) } catch { setError(true) } finally { setLoading(false) } }, []); useEffect(() => { void load() }, [load]); return <div className="animate-rise"><div className="mb-8"><p className="mb-2 text-[10px] font-bold uppercase tracking-[0.22em] text-cyan">CloudShield / Findings</p><h1 className="font-display text-3xl font-bold tracking-tight text-slate-950">Findings</h1><p className="mt-2 text-sm text-slate-500">Review and prioritize posture gaps across your environment.</p></div>{loading ? <LoadingState label="Loading findings" /> : error ? <ErrorState onRetry={() => void load()} /> : <><SectionHeader title={`${findings.length} finding${findings.length === 1 ? '' : 's'} returned`} /><FindingTable findings={findings} /></>}</div> }
