import { useMemo, useState } from 'react'
import AsyncBoundary from '../components/AsyncBoundary'
import Card from '../components/Card'
import CorridorMap from '../components/CorridorMap'
import DetectionDetail from '../components/DetectionDetail'
import DetectionTable from '../components/DetectionTable'
import Modal from '../components/Modal'
import PageHeader from '../components/PageHeader'
import { SearchIcon } from '../components/icons'
import { useAsyncData } from '../hooks/useAsyncData'
import { SEVERITY, SEVERITY_KEYS, STATUS, STATUS_KEYS } from '../lib/detections'
import { monitoringService } from '../services/monitoringService'

const selectClasses =
  'rounded-lg border border-slate-300 bg-white py-2 pl-3 pr-8 text-sm text-slate-700 focus:border-brand-500 focus:outline-none focus:ring-2 focus:ring-brand-500/25'

function matches(detection, { query, severity, status }) {
  if (severity !== 'all' && detection.severity !== severity) return false
  if (status !== 'all' && detection.status !== status) return false
  if (!query) return true

  const haystack =
    `${detection.id} ${detection.site} ${detection.type}`.toLowerCase()
  return haystack.includes(query.trim().toLowerCase())
}

function Monitoring() {
  const { data, error, isLoading } = useAsyncData(
    monitoringService.getDetections,
  )
  const [filters, setFilters] = useState({
    query: '',
    severity: 'all',
    status: 'all',
  })
  const [selected, setSelected] = useState(null)

  const visible = useMemo(
    () => (data ?? []).filter((detection) => matches(detection, filters)),
    [data, filters],
  )

  const update = (key) => (event) =>
    setFilters((current) => ({ ...current, [key]: event.target.value }))

  return (
    <>
      <PageHeader
        title="Monitoring"
        description="Every anomaly the model has flagged along the corridor."
      />

      <AsyncBoundary isLoading={isLoading} error={error}>
        {data && (
          <div className="space-y-6">
            <Card
              title="Corridor"
              description="Select a marker to open the detection"
            >
              <CorridorMap
                detections={visible}
                selectedId={selected?.id}
                onSelect={setSelected}
              />
            </Card>

            <Card bodyClassName="">
              <div className="flex flex-wrap items-center gap-3 border-b border-slate-100 p-4">
                <div className="relative min-w-56 flex-1">
                  <SearchIcon className="pointer-events-none absolute left-3 top-1/2 size-4 -translate-y-1/2 text-slate-400" />
                  <input
                    type="search"
                    value={filters.query}
                    onChange={update('query')}
                    placeholder="Search by ID, site, or type"
                    aria-label="Search detections"
                    className="w-full rounded-lg border border-slate-300 bg-white py-2 pl-9 pr-3 text-sm text-slate-900 placeholder:text-slate-400 focus:border-brand-500 focus:outline-none focus:ring-2 focus:ring-brand-500/25"
                  />
                </div>

                <select
                  value={filters.severity}
                  onChange={update('severity')}
                  aria-label="Filter by severity"
                  className={selectClasses}
                >
                  <option value="all">All severities</option>
                  {SEVERITY_KEYS.map((key) => (
                    <option key={key} value={key}>
                      {SEVERITY[key].label}
                    </option>
                  ))}
                </select>

                <select
                  value={filters.status}
                  onChange={update('status')}
                  aria-label="Filter by status"
                  className={selectClasses}
                >
                  <option value="all">All statuses</option>
                  {STATUS_KEYS.map((key) => (
                    <option key={key} value={key}>
                      {STATUS[key].label}
                    </option>
                  ))}
                </select>

                <p className="ml-auto text-sm text-slate-500">
                  {visible.length} of {data.length}
                </p>
              </div>

              <DetectionTable detections={visible} onSelect={setSelected} />
            </Card>
          </div>
        )}
      </AsyncBoundary>

      <Modal
        open={Boolean(selected)}
        onClose={() => setSelected(null)}
        title={selected ? `Detection ${selected.id}` : ''}
        description={selected ? selected.site : ''}
        footer={
          <>
            <button
              type="button"
              onClick={() => setSelected(null)}
              className="rounded-lg border border-slate-300 px-3 py-2 text-sm font-medium text-slate-700 hover:bg-slate-100"
            >
              Close
            </button>
            {/* TODO: post the inspection request once the backend exists. */}
            <button
              type="button"
              onClick={() => setSelected(null)}
              className="rounded-lg bg-brand-700 px-3 py-2 text-sm font-semibold text-white hover:bg-brand-800"
            >
              Request inspection
            </button>
          </>
        }
      >
        {selected && <DetectionDetail detection={selected} />}
      </Modal>
    </>
  )
}

export default Monitoring
