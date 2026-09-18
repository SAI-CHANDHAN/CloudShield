import { Database, Search } from 'lucide-react'
import { useCallback, useEffect, useMemo, useState } from 'react'
import { EmptyState, ErrorState, LoadingState } from '../components/common/States'
import { SectionHeader } from '../components/common/SectionHeader'
import { api } from '../services/api'
import type { Resource } from '../types/cloudshield'

export default function Resources() {
  const [resources, setResources] = useState<Resource[]>([])
  const [query, setQuery] = useState('')
  const [type, setType] = useState('ALL')
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(false)

  const load = useCallback(async () => {
    setLoading(true)
    setError(false)
    try {
      setResources(await api.getResources())
    } catch {
      setError(true)
    } finally {
      setLoading(false)
    }
  }, [])

  useEffect(() => { void load() }, [load])

  const types = [...new Set(resources.map((resource) => resource.resource_type))]
  const filtered = useMemo(() => resources.filter((resource) => {
    const searchable = `${resource.resource_id} ${resource.name || ''} ${resource.provider}`.toLowerCase()
    return searchable.includes(query.toLowerCase()) && (type === 'ALL' || resource.resource_type === type)
  }), [resources, query, type])

  return (
    <div className="animate-rise">
      <div className="mb-8">
        <p className="mb-2 text-[10px] font-bold uppercase tracking-[0.22em] text-cyan">CloudShield / Resources</p>
        <h1 className="font-display text-3xl font-bold tracking-tight text-slate-950">Resources</h1>
        <p className="mt-2 text-sm text-slate-500">Inventory of discovered cloud resources in the connected environment.</p>
      </div>
      {loading ? <LoadingState label="Loading resources" /> : error ? <ErrorState onRetry={() => void load()} /> : (
        <>
          <SectionHeader
            title={`${resources.length} resource${resources.length === 1 ? '' : 's'} discovered`}
            action={<div className="flex gap-2">
              <div className="relative">
                <Search className="absolute left-3 top-1/2 -translate-y-1/2 text-slate-400" size={15} />
                <input value={query} onChange={(event) => setQuery(event.target.value)} placeholder="Search resources" className="w-44 rounded-lg border border-slate-200 bg-white py-2 pl-9 pr-3 text-xs outline-none focus:border-cyan" aria-label="Search resources" />
              </div>
              <select value={type} onChange={(event) => setType(event.target.value)} className="rounded-lg border border-slate-200 bg-white px-3 py-2 text-xs font-semibold text-slate-600" aria-label="Filter by resource type">
                <option value="ALL">All types</option>
                {types.map((item) => <option key={item}>{item}</option>)}
              </select>
            </div>}
          />
          {filtered.length === 0 ? <div className="rounded-2xl border border-slate-200 bg-white"><EmptyState label={resources.length ? 'No resources match these filters.' : 'No resources returned by the backend.'} /></div> : (
            <div className="grid gap-4 sm:grid-cols-2 xl:grid-cols-3">
              {filtered.map((resource) => <div key={`${resource.provider}-${resource.resource_id}`} className="rounded-2xl border border-slate-200 bg-white p-5 shadow-sm transition hover:-translate-y-0.5 hover:shadow-md">
                <div className="mb-5 flex items-start justify-between"><div className="grid h-10 w-10 place-items-center rounded-xl bg-cyan/10 text-cyan"><Database size={18} /></div><span className="rounded-md bg-slate-100 px-2 py-1 text-[10px] font-bold uppercase tracking-wide text-slate-500">{resource.resource_type}</span></div>
                <p className="truncate font-mono text-sm font-bold text-slate-800" title={resource.resource_id}>{resource.resource_id}</p>
                <p className="mt-1 truncate text-xs text-slate-400">{resource.name || 'Unnamed resource'}</p>
                <div className="mt-5 grid grid-cols-2 gap-3 border-t border-slate-100 pt-4 text-xs"><div><p className="text-[10px] uppercase tracking-wider text-slate-400">Provider</p><p className="mt-1 font-semibold text-slate-600">{resource.provider}</p></div><div><p className="text-[10px] uppercase tracking-wider text-slate-400">Region</p><p className="mt-1 font-semibold text-slate-600">{resource.region || 'Not reported'}</p></div></div>
              </div>)}
            </div>
          )}
        </>
      )}
    </div>
  )
}
