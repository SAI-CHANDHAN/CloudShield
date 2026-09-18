import type { FindingStatus, Severity } from '../../types/cloudshield'

const severityStyles: Record<Severity, string> = { CRITICAL: 'bg-rose-50 text-rose-700 ring-rose-600/10', HIGH: 'bg-orange-50 text-orange-700 ring-orange-600/10', MEDIUM: 'bg-amber-50 text-amber-700 ring-amber-600/10', LOW: 'bg-sky-50 text-sky-700 ring-sky-600/10', INFO: 'bg-slate-100 text-slate-600 ring-slate-500/10' }
const statusStyles: Record<FindingStatus, string> = { OPEN: 'bg-rose-50 text-rose-700', RESOLVED: 'bg-emerald-50 text-emerald-700', SUPPRESSED: 'bg-slate-100 text-slate-600' }
export function SeverityBadge({ severity }: { severity: Severity }) { return <span className={`inline-flex items-center gap-1.5 rounded-md px-2 py-1 text-[10px] font-bold tracking-wide ring-1 ring-inset ${severityStyles[severity]}`}><span className="h-1.5 w-1.5 rounded-full bg-current" />{severity}</span> }
export function StatusBadge({ status }: { status: FindingStatus }) { return <span className={`rounded-md px-2 py-1 text-[10px] font-bold tracking-wide ${statusStyles[status]}`}>{status}</span> }
