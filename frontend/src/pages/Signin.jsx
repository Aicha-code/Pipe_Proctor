import { useState } from 'react'
import { Link, useLocation, useNavigate } from 'react-router'
import Logo from '../components/Logo'
import {
  AlertIcon,
  EyeIcon,
  EyeOffIcon,
  LockIcon,
  MailIcon,
  SpinnerIcon,
} from '../components/icons'
import { useAuth } from '../hooks/useAuth'
import { PATHS } from '../routes/paths'

const inputClasses =
  'w-full rounded-lg border border-slate-300 bg-white py-2.5 pl-10 pr-3 text-sm text-slate-900 placeholder:text-slate-400 focus:border-brand-500 focus:outline-none focus:ring-2 focus:ring-brand-500/25'

function Login() {
  const [form, setForm] = useState({ email: '', password: '' })
  const [showPassword, setShowPassword] = useState(false)
  const [error, setError] = useState('')
  const [isSubmitting, setIsSubmitting] = useState(false)

  const { login } = useAuth()
  const navigate = useNavigate()
  const location = useLocation()

  const redirectTo = location.state?.from?.pathname ?? PATHS.dashboard

  const handleChange = (event) => {
    const { name, value } = event.target
    setForm((current) => ({ ...current, [name]: value }))
    setError('')
  }

  const handleSubmit = async (event) => {
    event.preventDefault()
    setIsSubmitting(true)
    setError('')

    try {
      await login(form)
      navigate(redirectTo, { replace: true })
    } catch (submitError) {
      setError(submitError.message ?? 'Something went wrong. Please try again.')
      setIsSubmitting(false)
    }
  }

  return (
    <div className="flex min-h-screen bg-white">
      {/* Brand panel */}
      <aside className="relative hidden w-[45%] flex-col justify-between overflow-hidden bg-brand-800 p-12 text-white lg:flex">
        <div
          aria-hidden="true"
          className="absolute -right-24 -top-24 size-112 rounded-full bg-brand-500/25 blur-3xl"
        />
        <div
          aria-hidden="true"
          className="absolute -bottom-32 -left-20 size-96 rounded-full bg-brand-400/15 blur-3xl"
        />

        <Logo tone="onDark" className="relative" />

        <div className="relative max-w-md">
          <h2 className="text-3xl font-semibold leading-tight tracking-tight">
            Satellite-based threat detection for the Niger–Benin pipeline.
          </h2>
          <p className="mt-4 text-sm leading-relaxed text-brand-100">
            Monitor the corridor continuously, surface anomalies as they appear,
            and act before they become incidents.
          </p>
        </div>

        <p className="relative text-xs text-brand-200">
          © {new Date().getFullYear()} PipeProctor
        </p>
      </aside>

      {/* Form panel */}
      <main className="flex w-full flex-col justify-center px-6 py-12 lg:w-[55%] lg:px-20">
        <div className="mx-auto w-full max-w-sm">
          <Logo className="mb-10 lg:hidden" />

          <h1 className="text-2xl font-semibold tracking-tight text-slate-900">
            Sign in
          </h1>
          <p className="mt-2 text-sm text-slate-500">
            Welcome back. Enter your credentials to reach the dashboard.
          </p>

          {error && (
            <div
              role="alert"
              className="mt-6 flex items-start gap-2.5 rounded-lg border border-red-200 bg-red-50 p-3 text-sm text-red-700"
            >
              <AlertIcon className="mt-0.5 size-4 shrink-0" />
              <span>{error}</span>
            </div>
          )}

          <form onSubmit={handleSubmit} className="mt-6 space-y-5" noValidate>
            <div>
              <label
                htmlFor="email"
                className="mb-1.5 block text-sm font-medium text-slate-700"
              >
                Email
              </label>
              <div className="relative">
                <MailIcon className="pointer-events-none absolute left-3 top-1/2 size-4 -translate-y-1/2 text-slate-400" />
                <input
                  id="email"
                  name="email"
                  type="email"
                  required
                  autoComplete="email"
                  value={form.email}
                  onChange={handleChange}
                  placeholder="abuhendw@andrew.cmu.edu"
                  aria-invalid={Boolean(error)}
                  className={inputClasses}
                />
              </div>
            </div>

            <div>
              <label
                htmlFor="password"
                className="mb-1.5 block text-sm font-medium text-slate-700"
              >
                Password
              </label>
              <div className="relative">
                <LockIcon className="pointer-events-none absolute left-3 top-1/2 size-4 -translate-y-1/2 text-slate-400" />
                <input
                  id="password"
                  name="password"
                  type={showPassword ? 'text' : 'password'}
                  required
                  autoComplete="current-password"
                  value={form.password}
                  onChange={handleChange}
                  placeholder="********"
                  aria-invalid={Boolean(error)}
                  className={`${inputClasses} pr-11`}
                />
                <button
                  type="button"
                  onClick={() => setShowPassword((current) => !current)}
                  aria-label={showPassword ? 'Hide password' : 'Show password'}
                  className="absolute right-1 top-1/2 flex size-9 -translate-y-1/2 items-center justify-center rounded-md text-slate-400 hover:text-slate-600 focus:outline-none focus:ring-2 focus:ring-brand-500/25"
                >
                  {showPassword ? (
                    <EyeOffIcon className="size-4" />
                  ) : (
                    <EyeIcon className="size-4" />
                  )}
                </button>
              </div>
            </div>

            <div className="flex items-center justify-between">
              <label className="flex items-center gap-2 text-sm text-slate-600">
                <input
                  type="checkbox"
                  name="remember"
                  className="size-4 rounded border-slate-300 accent-brand-600"
                />
                Remember me
              </label>

              <Link
                to={PATHS.forgotPassword}
                className="text-sm font-medium text-brand-700 hover:text-brand-800 hover:underline"
              >
                Forgot password?
              </Link>
            </div>

            <button
              type="submit"
              disabled={isSubmitting}
              aria-busy={isSubmitting}
              className="flex w-full items-center justify-center gap-2 rounded-lg bg-brand-700 px-4 py-2.5 text-sm font-semibold text-white transition-colors hover:bg-brand-800 focus:outline-none focus:ring-2 focus:ring-brand-500/40 focus:ring-offset-2 disabled:cursor-not-allowed disabled:opacity-70"
            >
              {isSubmitting && (
                <SpinnerIcon className="size-4 animate-spin" strokeWidth={2.25} />
              )}
              {isSubmitting ? 'Signing in…' : 'Sign in'}
            </button>
          </form>

          <p className="mt-8 rounded-lg bg-slate-50 p-3 text-xs leading-relaxed text-slate-500">
            The auth API is not connected yet. <br></br>Any <b>valid email</b> with a <b>valid password of
            6 or more characters</b> signs you in.
          </p>
        </div>
      </main>
    </div>
  )
}

export default Login
