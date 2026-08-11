import { useCallback, useMemo, useState } from 'react'
import { authService } from '../services/authService'
import { AuthContext } from './auth-context'

const STORAGE_KEY = 'pipeproctor.session'

function readStoredSession() {
  try {
    const raw = localStorage.getItem(STORAGE_KEY)
    return raw ? JSON.parse(raw) : null
  } catch {
    return null
  }
}

function AuthProvider({ children }) {
  const [session, setSession] = useState(readStoredSession)

  const login = useCallback(async (credentials) => {
    const nextSession = await authService.login(credentials)
    localStorage.setItem(STORAGE_KEY, JSON.stringify(nextSession))
    setSession(nextSession)
    return nextSession.user
  }, [])

  const logout = useCallback(async () => {
    await authService.logout()
    localStorage.removeItem(STORAGE_KEY)
    setSession(null)
  }, [])

  const value = useMemo(
    () => ({
      user: session?.user ?? null,
      token: session?.token ?? null,
      isAuthenticated: Boolean(session?.token),
      login,
      logout,
    }),
    [session, login, logout],
  )

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>
}

export default AuthProvider
