import type { ReactNode } from 'react'

export function SectionHeader({ eyebrow, title, action }: { eyebrow?: string; title: string; action?: ReactNode }) { return <div className="mb-5 flex items-end justify-between gap-4"><div>{eyebrow && <p className="mb-1 text-[10px] font-bold uppercase tracking-[0.2em] text-cyan">{eyebrow}</p>}<h2 className="font-display text-lg font-bold tracking-tight text-slate-900">{title}</h2></div>{action}</div> }
