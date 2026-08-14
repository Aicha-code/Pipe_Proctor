/**
 * Display metadata for a detection. Severity and status keys come from the
 * API; everything the UI needs to render them lives here so pages, tables,
 * charts, and the corridor map all label them the same way.
 */

/** Ordered high → low, which is the order the UI lists them in. */
export const SEVERITY_KEYS = ['high', 'medium', 'low']

export const SEVERITY = {
  high: {
    label: 'High',
    bar: 'bg-severity-high',
    dot: 'bg-severity-high',
    pill: 'bg-red-50 text-red-700 ring-red-200',
  },
  medium: {
    label: 'Medium',
    bar: 'bg-severity-medium',
    dot: 'bg-severity-medium',
    pill: 'bg-amber-50 text-amber-800 ring-amber-200',
  },
  low: {
    label: 'Low',
    bar: 'bg-severity-low',
    dot: 'bg-severity-low',
    pill: 'bg-brand-50 text-brand-800 ring-brand-200',
  },
}

export const STATUS_KEYS = ['open', 'reviewing', 'cleared']

export const STATUS = {
  open: { label: 'Open', pill: 'bg-slate-100 text-slate-700 ring-slate-200' },
  reviewing: { label: 'In review', pill: 'bg-blue-50 text-blue-700 ring-blue-200' },
  cleared: { label: 'Cleared', pill: 'bg-brand-50 text-brand-800 ring-brand-200' },
}

/** `412` → `KM 412` — the corridor position, as operators refer to it. */
export function formatKm(km) {
  return `KM ${km.toLocaleString('en-US')}`
}

export function formatCoords({ lat, lon }) {
  const ns = lat >= 0 ? 'N' : 'S'
  const ew = lon >= 0 ? 'E' : 'W'
  return `${Math.abs(lat).toFixed(3)}° ${ns}, ${Math.abs(lon).toFixed(3)}° ${ew}`
}

export function formatDate(iso) {
  return new Date(iso).toLocaleDateString('en-GB', {
    day: '2-digit',
    month: 'short',
    year: 'numeric',
  })
}

const relative = new Intl.RelativeTimeFormat('en', { numeric: 'auto' })

/** Coarse "3 days ago" for lists — detections arrive at most twice a week. */
export function formatRelativeDays(iso, now = Date.now()) {
  const days = Math.round((new Date(iso).getTime() - now) / 86_400_000)
  return relative.format(days, 'day')
}
