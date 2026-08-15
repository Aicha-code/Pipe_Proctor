import { useState } from 'react'
import Card from '../components/Card'
import PageHeader from '../components/PageHeader'
import { CheckIcon } from '../components/icons'
import { useAuth } from '../hooks/useAuth'
import { SEVERITY, SEVERITY_KEYS } from '../lib/detections'

const fieldClasses =
  'w-full rounded-lg border border-slate-300 bg-white px-3 py-2 text-sm text-slate-900 focus:border-brand-500 focus:outline-none focus:ring-2 focus:ring-brand-500/25 disabled:bg-slate-50 disabled:text-slate-500'

const DEFAULTS = {
  minConfidence: 65,
  alertFrom: 'medium',
  revisitDays: '6',
  emailAlerts: true,
  smsAlerts: false,
  weeklyDigest: true,
}

function Row({ label, hint, htmlFor, children }) {
  return (
    <div className="grid gap-2 sm:grid-cols-3 sm:items-start sm:gap-4">
      <div className="sm:col-span-1">
        <label
          htmlFor={htmlFor}
          className="text-sm font-medium text-slate-700"
        >
          {label}
        </label>
        {hint && <p className="mt-0.5 text-xs text-slate-500">{hint}</p>}
      </div>
      <div className="sm:col-span-2">{children}</div>
    </div>
  )
}

function Checkbox({ name, checked, onChange, label, hint }) {
  return (
    <label className="flex items-start gap-2.5">
      <input
        type="checkbox"
        name={name}
        checked={checked}
        onChange={onChange}
        className="mt-0.5 size-4 rounded border-slate-300 accent-brand-600"
      />
      <span>
        <span className="block text-sm text-slate-700">{label}</span>
        {hint && <span className="block text-xs text-slate-500">{hint}</span>}
      </span>
    </label>
  )
}

function Settings() {
  const { user } = useAuth()
  const [form, setForm] = useState(DEFAULTS)
  const [isSaved, setIsSaved] = useState(false)

  const handleChange = (event) => {
    const { name, type, value, checked } = event.target
    setForm((current) => ({
      ...current,
      [name]: type === 'checkbox' ? checked : value,
    }))
    setIsSaved(false)
  }

  const handleSubmit = (event) => {
    event.preventDefault()
    // TODO: persist through the settings endpoint once the backend exists.
    setIsSaved(true)
  }

  return (
    <>
      <PageHeader
        title="Settings"
        description="Tune what the system flags and how your team hears about it."
      />

      <form onSubmit={handleSubmit} className="max-w-3xl space-y-6">
        <Card title="Account" description="Read-only until the backend is connected">
          <div className="space-y-5">
            <Row label="Name" htmlFor="name">
              <input
                id="name"
                className={fieldClasses}
                value={user?.name ?? ''}
                disabled
                readOnly
              />
            </Row>
            <Row label="Email" htmlFor="email">
              <input
                id="email"
                className={fieldClasses}
                value={user?.email ?? ''}
                disabled
                readOnly
              />
            </Row>
            <Row label="Role" htmlFor="role">
              <input
                id="role"
                className={fieldClasses}
                value={user?.role ?? ''}
                disabled
                readOnly
              />
            </Row>
          </div>
        </Card>

        <Card
          title="Detection thresholds"
          description="What the model has to see before it raises a detection"
        >
          <div className="space-y-5">
            <Row
              label="Minimum confidence"
              hint="Lower catches more, at the cost of false alarms."
              htmlFor="minConfidence"
            >
              <div className="flex items-center gap-3">
                <input
                  id="minConfidence"
                  name="minConfidence"
                  type="range"
                  min="40"
                  max="95"
                  step="5"
                  value={form.minConfidence}
                  onChange={handleChange}
                  className="w-full accent-brand-600"
                />
                <span className="w-12 shrink-0 text-right font-mono text-sm tabular-nums text-slate-900">
                  {form.minConfidence}%
                </span>
              </div>
            </Row>

            <Row
              label="Alert from severity"
              hint="Anything below is logged but stays silent."
              htmlFor="alertFrom"
            >
              <select
                id="alertFrom"
                name="alertFrom"
                value={form.alertFrom}
                onChange={handleChange}
                className={fieldClasses}
              >
                {SEVERITY_KEYS.map((key) => (
                  <option key={key} value={key}>
                    {SEVERITY[key].label} and above
                  </option>
                ))}
              </select>
            </Row>

            <Row
              label="Revisit cadence"
              hint="Sentinel-1 revisits the corridor every 6 to 12 days."
              htmlFor="revisitDays"
            >
              <select
                id="revisitDays"
                name="revisitDays"
                value={form.revisitDays}
                onChange={handleChange}
                className={fieldClasses}
              >
                <option value="6">Every pass (~6 days)</option>
                <option value="12">Every other pass (~12 days)</option>
              </select>
            </Row>
          </div>
        </Card>

        <Card title="Notifications" description="Who gets told, and how">
          <div className="space-y-4">
            <Checkbox
              name="emailAlerts"
              checked={form.emailAlerts}
              onChange={handleChange}
              label="Email alerts"
              hint="Sent as soon as a pass is processed."
            />
            <Checkbox
              name="smsAlerts"
              checked={form.smsAlerts}
              onChange={handleChange}
              label="SMS alerts"
              hint="High severity only, for on-call field leads."
            />
            <Checkbox
              name="weeklyDigest"
              checked={form.weeklyDigest}
              onChange={handleChange}
              label="Weekly digest"
              hint="Monday summary of every detection and its status."
            />
          </div>
        </Card>

        <div className="flex items-center gap-3">
          <button
            type="submit"
            className="rounded-lg bg-brand-700 px-4 py-2.5 text-sm font-semibold text-white hover:bg-brand-800 focus:outline-none focus:ring-2 focus:ring-brand-500/40 focus:ring-offset-2"
          >
            Save changes
          </button>

          {isSaved && (
            <span
              role="status"
              className="inline-flex items-center gap-1.5 text-sm text-brand-800"
            >
              <CheckIcon className="size-4" />
              Saved locally — not yet sent to a backend.
            </span>
          )}
        </div>
      </form>
    </>
  )
}

export default Settings
