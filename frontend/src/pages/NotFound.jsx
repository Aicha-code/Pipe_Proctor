import { Link } from 'react-router'
import Logo from '../components/Logo'
import { PATHS } from '../routes/paths'

function NotFound() {
  return (
    <div className="flex min-h-screen flex-col items-center justify-center gap-6 bg-slate-50 px-6 text-center">
      <Logo />

      <div>
        <p className="font-mono text-sm text-slate-400">404</p>
        <h1 className="mt-1 text-2xl font-semibold tracking-tight text-slate-900">
          Page not found
        </h1>
        <p className="mt-2 text-sm text-slate-500">
          That route is not part of the corridor.
        </p>
      </div>

      <Link
        to={PATHS.dashboard}
        className="rounded-lg bg-brand-700 px-4 py-2.5 text-sm font-semibold text-white hover:bg-brand-800"
      >
        Back to dashboard
      </Link>
    </div>
  )
}

export default NotFound
