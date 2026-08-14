import { SeverityBadge, StatusBadge } from './Badge'
import {
  formatCoords,
  formatDate,
  formatKm,
} from '../lib/detections'

function Field({ label, children, mono = false }) {
  return (
    <div>
      <dt className="text-xs uppercase tracking-wide text-slate-500">{label}</dt>
      <dd
        className={`mt-1 text-sm text-slate-900 ${mono ? 'font-mono' : ''}`}
      >
        {children}
      </dd>
    </div>
  )
}

/** Body of the detection dialog. */
function DetectionDetail({ detection }) {
  return (
    <div className="space-y-5">
      <div className="flex flex-wrap items-center gap-2">
        <SeverityBadge severity={detection.severity} />
        <StatusBadge status={detection.status} />
        <span className="text-xs text-slate-500">
          {Math.round(detection.confidence * 100)}% confidence
        </span>
      </div>

      <p className="text-sm leading-relaxed text-slate-600">{detection.note}</p>

      <dl className="grid grid-cols-2 gap-4">
        <Field label="Site">{detection.site}</Field>
        <Field label="Corridor position" mono>
          {formatKm(detection.km)}
        </Field>
        <Field label="Coordinates" mono>
          {formatCoords(detection.coords)}
        </Field>
        <Field label="Type">{detection.type}</Field>
        <Field label="Detected">{formatDate(detection.detectedAt)}</Field>
        <Field label="Satellite pass" mono>
          {detection.pass}
        </Field>
      </dl>
    </div>
  )
}

export default DetectionDetail
