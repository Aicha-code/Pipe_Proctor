import { SEVERITY, SEVERITY_KEYS } from '../lib/detections'

/**
 * Open detections split by severity. Plain bars rather than a chart library:
 * three labelled rows do not need an axis.
 */
function SeverityBars({ detections }) {
  const counts = SEVERITY_KEYS.map((key) => ({
    key,
    label: SEVERITY[key].label,
    bar: SEVERITY[key].bar,
    count: detections.filter((detection) => detection.severity === key).length,
  }))

  const max = Math.max(...counts.map(({ count }) => count), 1)

  return (
    <ul className="space-y-4">
      {counts.map(({ key, label, bar, count }) => (
        <li key={key}>
          <div className="flex items-baseline justify-between text-sm">
            <span className="text-slate-600">{label}</span>
            <span className="font-semibold tabular-nums text-slate-900">
              {count}
            </span>
          </div>

          <div className="mt-1.5 h-2 rounded-full bg-slate-100">
            <div
              className={`h-2 rounded-full ${bar}`}
              style={{ width: `${(count / max) * 100}%` }}
            />
          </div>
        </li>
      ))}
    </ul>
  )
}

export default SeverityBars
