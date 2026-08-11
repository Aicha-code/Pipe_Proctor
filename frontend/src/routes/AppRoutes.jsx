import { Navigate, Route, Routes } from 'react-router'
import PrivateLayout from '../layouts/PrivateLayout'
import Dashboard from '../pages/Dashboard'
import Login from '../pages/Login'
import Modal from '../pages/Modal'
import Monitoring from '../pages/Monitoring'
import NotFound from '../pages/NotFound'
import Settings from '../pages/Settings'
import ProtectedRoute from './ProtectedRoute'
import PublicRoute from './PublicRoute'
import { PATHS } from './paths'

function AppRoutes() {
  return (
    <Routes>
      {/* Public */}
      <Route element={<PublicRoute />}>
        <Route path={PATHS.login} element={<Login />} />
      </Route>

      {/* Protected */}
      <Route element={<ProtectedRoute />}>
        <Route element={<PrivateLayout />}>
          <Route path={PATHS.dashboard} element={<Dashboard />} />
          <Route path={PATHS.monitoring} element={<Monitoring />} />
          <Route path={PATHS.settings} element={<Settings />} />
          <Route path={PATHS.modal} element={<Modal />} />
        </Route>
      </Route>

      <Route path="/" element={<Navigate to={PATHS.dashboard} replace />} />
      <Route path="*" element={<NotFound />} />
    </Routes>
  )
}

export default AppRoutes
