import { Activity, ArrowUpRight, Bell, ChevronRight, Cloud, LayoutDashboard, Network, Radar, Server, ShieldCheck, Siren } from 'lucide-react'
import { NavLink, Outlet } from 'react-router-dom'

const navItems = [
  { label: 'Overview', to: '/dashboard', icon: LayoutDashboard },
  { label: 'Findings', to: '/findings', icon: Radar },
  { label: 'Resources', to: '/resources', icon: Server },
]

const comingSoon = [
  { label: 'Incidents', icon: Siren },
  { label: 'Attack Paths', icon: Network },
]

export function Layout() {
  return (
    <div className="min-h-screen bg-canvas text-slate-900">
      <aside className="fixed inset-y-0 left-0 z-30 hidden w-[252px] flex-col bg-ink text-white lg:flex">
        <div className="flex h-20 items-center gap-3 border-b border-white/10 px-7">
          <div className="grid h-9 w-9 place-items-center rounded-xl bg-cyan text-ink shadow-lg shadow-cyan/20"><ShieldCheck size={21} strokeWidth={2.5} /></div>
          <div><p className="font-display text-[17px] font-bold tracking-tight">CloudShield</p><p className="text-[10px] uppercase tracking-[0.18em] text-slate-400">Cloud security posture</p></div>
        </div>
        <div className="px-4 pt-8">
          <p className="mb-3 px-3 text-[10px] font-bold uppercase tracking-[0.2em] text-slate-500">Workspace</p>
          <nav className="space-y-1" aria-label="Main navigation">
            {navItems.map(({ label, to, icon: Icon }) => <NavLink key={to} to={to} className={({ isActive }) => `group flex items-center gap-3 rounded-xl px-3 py-3 text-sm font-medium transition ${isActive ? 'bg-white/10 text-white shadow-inner' : 'text-slate-400 hover:bg-white/5 hover:text-white'}`}><Icon size={18} /><span>{label}</span><ChevronRight className="ml-auto opacity-0 transition group-[.active]:opacity-60" size={15} /></NavLink>)}
            {comingSoon.map(({ label, icon: Icon }) => <div key={label} className="flex items-center gap-3 rounded-xl px-3 py-3 text-sm font-medium text-slate-500"><Icon size={18} /><span>{label}</span><span className="ml-auto rounded-full border border-white/10 px-2 py-0.5 text-[9px] uppercase tracking-wider text-slate-500">Soon</span></div>)}
          </nav>
        </div>
        <div className="mt-auto px-5 pb-6">
          <div className="rounded-2xl border border-white/10 bg-white/[0.04] p-4"><div className="mb-3 flex items-center gap-2 text-xs font-semibold text-slate-300"><span className="h-2 w-2 rounded-full bg-emerald-400 shadow-[0_0_0_3px_rgba(52,211,153,0.12)]" /> System status</div><p className="text-xs text-slate-500">All systems operational</p><div className="mt-4 flex items-center gap-2 text-[10px] text-slate-600"><Activity size={13} /> API connected locally</div></div>
        </div>
      </aside>
      <div className="lg:pl-[252px]"><header className="sticky top-0 z-20 flex h-20 items-center justify-between border-b border-slate-200/80 bg-canvas/90 px-5 backdrop-blur-xl sm:px-8"><div className="flex items-center gap-3 lg:hidden"><div className="grid h-8 w-8 place-items-center rounded-lg bg-ink text-cyan"><ShieldCheck size={18} /></div><span className="font-display font-bold">CloudShield</span></div><div className="hidden lg:block"><p className="text-xs font-medium text-slate-400">Workspace / <span className="text-slate-600">Security posture</span></p></div><div className="flex items-center gap-4"><button className="relative rounded-lg p-2 text-slate-500 hover:bg-white hover:text-slate-800" aria-label="Notifications"><Bell size={18} /><span className="absolute right-1.5 top-1.5 h-1.5 w-1.5 rounded-full bg-cyan" /></button><div className="hidden h-7 w-px bg-slate-200 sm:block" /><div className="flex items-center gap-2"><div className="grid h-8 w-8 place-items-center rounded-full bg-slate-200 text-xs font-bold text-slate-600">CS</div><span className="hidden text-sm font-semibold text-slate-700 sm:block">Security team</span></div></div></header><main className="mx-auto max-w-[1440px] px-5 py-8 sm:px-8 lg:px-10"><Outlet /></main></div>
    </div>
  )
}
