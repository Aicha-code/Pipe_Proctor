import { NavLink } from 'react-router'
import Logo from './Logo'
import { PATHS } from '../routes/paths'

const LINKS = [
  { to: PATHS.dashboard, label: 'Dashboard' },
  { to: PATHS.monitoring, label: 'Monitoring' },
  { to: PATHS.settings, label: 'Settings' },
  { to: PATHS.modal, label: 'Modal' },
]

function Sidebar() {
  return (
    <aside className="w-56 shrink-0 border-r border-slate-200 bg-white p-4">
      <Logo className="mb-6 px-1" />

      <nav className="flex flex-col gap-1">
        {LINKS.map(({ to, label }) => (
          <NavLink
            key={to}
            to={to}
            className={({ isActive }) =>
              `rounded-lg px-3 py-2 text-sm font-medium ${
                isActive
                  ? 'bg-brand-700 text-white'
                  : 'text-slate-600 hover:bg-slate-100'
              }`
            }
          >
            {label}
          </NavLink>
        ))}
      </nav>
    </aside>
  )
}

export default Sidebar
