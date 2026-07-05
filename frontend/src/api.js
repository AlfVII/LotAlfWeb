// Thin fetch wrapper around the FastAPI backend.
// In dev, Vite proxies /api -> http://localhost:8000 (see vite.config.js).
const BASE = import.meta.env.VITE_API_BASE || ''

function authHeaders() {
  const t = localStorage.getItem('lotalf_token')
  return t ? { Authorization: `Bearer ${t}` } : {}
}

async function req(path, opts = {}) {
  const res = await fetch(BASE + path, {
    ...opts,
    headers: { 'Content-Type': 'application/json', ...authHeaders(), ...(opts.headers || {}) },
  })
  if (!res.ok) {
    const err = await res.json().catch(() => ({ detail: res.statusText }))
    throw new Error(err.detail || 'Error de servidor')
  }
  const ct = res.headers.get('content-type') || ''
  return ct.includes('application/json') ? res.json() : res.text()
}

function qs(obj) {
  const parts = Object.entries(obj || {})
    .filter(([, v]) => v != null && v !== '')
    .map(([k, v]) => `${k}=${encodeURIComponent(v)}`)
  return parts.length ? `?${parts.join('&')}` : ''
}

export const api = {
  // reference (SQLite)
  regions: () => req('/api/reference/regions'),
  provinces: (region) => req('/api/reference/provinces' + qs({ region })),
  towns: (province) => req('/api/reference/towns' + qs({ province })),
  // auth
  login: (password) => req('/api/auth/login', { method: 'POST', body: JSON.stringify({ password }) }),
  me: () => req('/api/auth/me'),
  // comments
  comments: () => req('/api/comments'),
  addComment: (c) => req('/api/comments', { method: 'POST', body: JSON.stringify(c) }),
  // numbers
  number: (n) => req('/api/numbers/' + n),
  hundred: (base) => req('/api/numbers/hundred/' + base),
  filtered: (filters, limit) => req('/api/numbers/filtered', { method: 'POST', body: JSON.stringify({ filters, limit }) }),
  updateNumber: (n, data) => req('/api/numbers/' + n, { method: 'PUT', body: JSON.stringify(data) }),
  // administraciones
  retailerMap: (params) => req('/api/retailers/map' + qs(params)),
  retailerOne: (params) => req('/api/retailers/one' + qs(params)),
  retailerImage: (params) => req('/api/retailers/image' + qs(params)),
  saveRetailer: (data) => req('/api/retailers', { method: 'PUT', body: JSON.stringify(data) }),
  // stats
  statsNumbers: () => req('/api/stats/numbers'),
  statsRetailers: () => req('/api/stats/retailers'),
  // scanner (Plustek D620)
  scanDuplex: () => req('/api/scan/duplex', { method: 'POST' }),
  scanDecimo: () => req('/api/scan/decimo', { method: 'POST' }),
}
