import { Navigate, Outlet, useLocation } from 'react-router'
import { useAuth } from '../hooks/useAuth'
import { PATHS } from './paths'

function ProtectedRoute() {
  const { isAuthenticated } = useAuth()
  const location = useLocation()

  if (!isAuthenticated) {
    // Remember where the user was headed so login can send them back.
    return <Navigate to={PATHS.signin} state={{ from: location }} replace />
  }

  return <Outlet />
}

export default ProtectedRoute
