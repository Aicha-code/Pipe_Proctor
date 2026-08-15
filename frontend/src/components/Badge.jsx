import { SEVERITY, STATUS } from '../lib/detections'

const base =
  'inline-flex items-center gap-1.5 rounded-full px-2 py-0.5 text-xs font-medium ring-1 ring-inset'

/**
 * Severity always ships as dot + word: the colours alone are not a reliable
 * channel, so the label carries the meaning and the dot reinforces it.
 */
export function SeverityBadge({ severity }) {
  const { label, pill, dot } = SEVERITY[severity]

  return (
    <span className={`${base} ${pill}`}>
      <span className={`size-1.5 rounded-full ${dot}`} aria-hidden="true" />
      {label}
    </span>
  )
}

export function StatusBadge({ status }) {
  const { label, pill } = STATUS[status]

  return <span className={`${base} ${pill}`}>{label}</span>
}
