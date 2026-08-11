import { Navigate, Outlet } from 'react-router'
import { useAuth } from '../hooks/useAuth'
import { PATHS } from './paths'

function PublicRoute() {
  const { isAuthenticated } = useAuth()

  if (isAuthenticated) {
    return <Navigate to={PATHS.dashboard} replace />
  }

  return <Outlet />
}

export default PublicRoute
