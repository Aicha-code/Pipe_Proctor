import { useState } from 'react'
import { useLocation, useNavigate } from 'react-router'
import { useAuth } from '../hooks/useAuth'
import { PATHS } from '../routes/paths'

function Login() {
  const [email, setEmail] = useState('')
  const { login } = useAuth()
  const navigate = useNavigate()
  const location = useLocation()

  const redirectTo = location.state?.from?.pathname ?? PATHS.dashboard

  const handleSubmit = (event) => {
    event.preventDefault()
    login(email)
    navigate(redirectTo, { replace: true })
  }

  return (
    <div className="flex min-h-screen items-center justify-center bg-slate-50 p-6">
      <form
        onSubmit={handleSubmit}
        className="w-full max-w-sm space-y-4 rounded-lg bg-white p-6 shadow"
      >
        <h1 className="text-2xl font-semibold text-slate-900">Login</h1>

        <input
          type="email"
          required
          value={email}
          onChange={(event) => setEmail(event.target.value)}
          placeholder="you@example.com"
          className="w-full rounded border border-slate-300 px-3 py-2"
        />

        <button
          type="submit"
          className="w-full rounded bg-slate-900 px-3 py-2 text-white"
        >
          Sign in
        </button>
      </form>
    </div>
  )
}

export default Login
