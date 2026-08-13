import { useNavigate } from 'react-router'
import { useAuth } from '../hooks/useAuth'
import { PATHS } from '../routes/paths'

function Navbar() {
  const { user, logout } = useAuth()
  const navigate = useNavigate()

  const handleLogout = async () => {
    await logout()
    navigate(PATHS.signin, { replace: true })
  }

  return (
    <header className="flex items-center justify-between gap-4 border-b border-slate-200 bg-white px-6 py-3">
      <div className="min-w-0">
        <p className="truncate text-sm font-medium text-slate-900">
          {user?.name}
        </p>
        <p className="truncate text-xs text-slate-500">
          {user?.role} · {user?.email}
        </p>
      </div>

      <button
        type="button"
        onClick={handleLogout}
        className="shrink-0 rounded-lg border border-slate-300 px-3 py-1.5 text-sm text-slate-700 hover:bg-slate-100"
      >
        Log out
      </button>
    </header>
  )
}

export default Navbar
