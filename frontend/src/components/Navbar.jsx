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
    <header className="flex items-center justify-between border-b border-slate-200 bg-white px-6 py-3">
      <h2 className="text-sm font-medium text-slate-500">{user?.email}</h2>

      <button
        type="button"
        onClick={handleLogout}
        className="rounded border border-slate-300 px-3 py-1.5 text-sm text-slate-700 hover:bg-slate-100"
      >
        Log out
      </button>
    </header>
  )
}

export default Navbar
