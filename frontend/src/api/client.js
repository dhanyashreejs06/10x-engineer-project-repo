// Clean API abstraction layer
// All backend calls go through here

const BASE_URL = '/api'

async function request(path, options = {}) {
  const res = await fetch(`${BASE_URL}${path}`, {
    headers: { 'Content-Type': 'application/json', ...options.headers },
    ...options,
    body: options.body ? JSON.stringify(options.body) : undefined
  })

  if (!res.ok) {
    const err = await res.json().catch(() => ({ detail: 'Something went wrong' }))
    throw new Error(err.detail || `Error ${res.status}`)
  }

  // 204 No Content
  if (res.status === 204) return null
  return res.json()
}

// ── Prompts ──────────────────────────────────────────────

export const promptsApi = {
  list: (params = {}) => {
    const query = new URLSearchParams()
    if (params.collection_id) query.set('collection_id', params.collection_id)
    if (params.search)        query.set('search', params.search)
    if (params.tag)           query.set('tag', params.tag)
    const qs = query.toString()
    return request(`/prompts${qs ? `?${qs}` : ''}`)
  },

  get: (id) => request(`/prompts/${id}`),

  create: (data) => request('/prompts', { method: 'POST', body: data }),

  update: (id, data) => request(`/prompts/${id}`, { method: 'PUT', body: data }),

  patch: (id, data) => request(`/prompts/${id}`, { method: 'PATCH', body: data }),

  delete: (id) => request(`/prompts/${id}`, { method: 'DELETE' })
}

// ── Collections ──────────────────────────────────────────

export const collectionsApi = {
  list: () => request('/collections'),

  get: (id) => request(`/collections/${id}`),

  create: (data) => request('/collections', { method: 'POST', body: data }),

  delete: (id) => request(`/collections/${id}`, { method: 'DELETE' })
}