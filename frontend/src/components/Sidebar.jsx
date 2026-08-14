import { NavLink } from 'react-router'
import Logo from './Logo'
import { GaugeIcon, LayersIcon, MapPinIcon, SlidersIcon } from './icons'
import { PATHS } from '../routes/paths'

const LINKS = [
  { to: PATHS.dashboard, label: 'Dashboard', icon: GaugeIcon },
  { to: PATHS.monitoring, label: 'Monitoring', icon: MapPinIcon },
  { to: PATHS.settings, label: 'Settings', icon: SlidersIcon },
  { to: PATHS.modal, label: 'Modal', icon: LayersIcon },
]

/** Collapses to icons on narrow screens rather than disappearing. */
function Sidebar() {
  return (
    <aside className="w-16 shrink-0 border-r border-slate-200 bg-white p-3 md:w-56 md:p-4">
      {/* Wrappers carry the responsive display so they never fight the
          Logo's own `inline-flex`. */}
      <div className="mb-6 hidden md:block">
        <Logo className="px-1" />
      </div>
      <div className="mb-6 flex justify-center md:hidden">
        <Logo showWordmark={false} />
      </div>

      <nav className="flex flex-col gap-1">
        {LINKS.map(({ to, label, icon: Icon }) => (
          <NavLink
            key={to}
            to={to}
            title={label}
            className={({ isActive }) =>
              `flex items-center justify-center gap-2.5 rounded-lg px-3 py-2 text-sm font-medium md:justify-start ${
                isActive
                  ? 'bg-brand-700 text-white'
                  : 'text-slate-600 hover:bg-slate-100'
              }`
            }
          >
            <Icon className="size-4 shrink-0" />
            <span className="hidden md:inline">{label}</span>
          </NavLink>
        ))}
      </nav>
    </aside>
  )
}

export default Sidebar
