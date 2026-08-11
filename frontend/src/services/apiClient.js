const BASE_URL = import.meta.env.VITE_API_URL ?? '/api'

export class ApiError extends Error {
  constructor(message, status) {
    super(message)
    this.name = 'ApiError'
    this.status = status
  }
}


export async function request(path, { method = 'GET', body, ...options } = {}) {
  const response = await fetch(`${BASE_URL}${path}`, {
    method,
    headers: { 'Content-Type': 'application/json', ...options.headers },
    body: body ? JSON.stringify(body) : undefined,
    ...options,
  })

  const payload = await response.json().catch(() => null)

  if (!response.ok) {
    throw new ApiError(payload?.message ?? 'Request failed', response.status)
  }

  return payload
}

export const apiClient = {
  get: (path, options) => request(path, { ...options, method: 'GET' }),
  post: (path, body, options) => request(path, { ...options, method: 'POST', body }),
  patch: (path, body, options) => request(path, { ...options, method: 'PATCH', body }),
  delete: (path, options) => request(path, { ...options, method: 'DELETE' }),
}
