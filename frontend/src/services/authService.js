import { ApiError } from './apiClient'

const MOCK_DELAY_MS = 700
const MIN_PASSWORD_LENGTH = 6

const wait = (ms) => new Promise((resolve) => setTimeout(resolve, ms))

/**
 * Stands in for the real endpoint until the backend exists. Accepts any
 * well-formed email with a password of at least MIN_PASSWORD_LENGTH chars.
 */
async function mockLogin({ email, password }) {
  await wait(MOCK_DELAY_MS)

  if (!email.includes('@') || password.length < MIN_PASSWORD_LENGTH) {
    throw new ApiError('Invalid email or password.', 401)
  }

  return {
    token: `mock-token-${Date.now()}`,
    user: {
      email,
      name: email.split('@')[0],
      role: 'Admin',
    },
  }
}

export const authService = {
  /**
   * Resolves to { token, user }.
   * TODO: swap the mock for `apiClient.post('/auth/login', credentials)`.
   */
  login: (credentials) => mockLogin(credentials),

  /** TODO: swap for `apiClient.post('/auth/logout')`. or the real API when the backend is ready */
  logout: async () => {
    await wait(0)
  },
}
