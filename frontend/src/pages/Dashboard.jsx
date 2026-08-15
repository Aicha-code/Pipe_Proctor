import { useState } from 'react'
import { Link } from 'react-router'
import AsyncBoundary from '../components/AsyncBoundary'
import Card from '../components/Card'
import CorridorMap from '../components/CorridorMap'
import DetectionDetail from '../components/DetectionDetail'
import DetectionTable from '../components/DetectionTable'
import DetectionsTrend from '../components/DetectionsTrend'
import Modal from '../components/Modal'
import PageHeader from '../components/PageHeader'
import SeverityBars from '../components/SeverityBars'
import StatCard from '../components/StatCard'
import {
  AlertIcon,
  GaugeIcon,
  LayersIcon,
  SatelliteIcon,
} from '../components/icons'
import { useAsyncData } from '../hooks/useAsyncData'
import { formatKm, formatRelativeDays } from '../lib/detections'
import {
  CORRIDOR_LENGTH_KM,
  monitoringService,
} from '../services/monitoringService'
import { PATHS } from '../routes/paths'

const RECENT_COUNT = 5

function Dashboard() {
  const { data, error, isLoading } = useAsyncData(monitoringService.getOverview)
  const [selected, setSelected] = useState(null)

  const active = data
    ? data.detections.filter((detection) => detection.status !== 'cleared')
    : []
  const highSeverity = active.filter(
    (detection) => detection.severity === 'high',
  )

  return (
    <>
      <PageHeader
        title="Dashboard"
        description="Corridor health at a glance, refreshed with every satellite pass."
      />

      <AsyncBoundary isLoading={isLoading} error={error}>
        {data && (
          <div className="space-y-6">
            <div className="grid gap-4 sm:grid-cols-2 xl:grid-cols-4">
              <StatCard
                label="Active detections"
                value={active.length}
                hint="Awaiting review or inspection"
                icon={AlertIcon}
              />
              <StatCard
                label="High severity"
                value={highSeverity.length}
                hint={
                  highSeverity.length > 0
                    ? `Nearest at ${formatKm(highSeverity[0].km)}`
                    : 'Nothing urgent on the corridor'
                }
                icon={GaugeIcon}
              />
              <StatCard
                label="Corridor scanned"
                value={`${CORRIDOR_LENGTH_KM.toLocaleString('en-US')} km`}
                hint="Full corridor on the last pass"
                icon={LayersIcon}
              />
              <StatCard
                label="Last satellite pass"
                value={formatRelativeDays(data.lastPass.capturedAt)}
                hint={`Next pass ${formatRelativeDays(data.lastPass.nextPassAt)}`}
                icon={SatelliteIcon}
              />
            </div>

            <div className="grid gap-6 lg:grid-cols-3">
              <Card
                title="Detections per week"
                description="Last 12 weeks across the full corridor"
                className="lg:col-span-2"
              >
                <DetectionsTrend data={data.trend} />
              </Card>

              <Card
                title="Active by severity"
                description={`${active.length} open or in review`}
              >
                <SeverityBars detections={active} />
              </Card>
            </div>

            <Card
              title="Corridor overview"
              description={`${data.detections.length} detections along ${CORRIDOR_LENGTH_KM.toLocaleString('en-US')} km`}
            >
              <CorridorMap
                detections={data.detections}
                selectedId={selected?.id}
                onSelect={setSelected}
              />
            </Card>

            <Card
              title="Recent detections"
              description="Newest first"
              bodyClassName=""
              action={
                <Link
                  to={PATHS.monitoring}
                  className="text-sm font-medium text-brand-700 hover:text-brand-800 hover:underline"
                >
                  View all
                </Link>
              }
            >
              <DetectionTable
                detections={data.detections.slice(0, RECENT_COUNT)}
                onSelect={setSelected}
              />
            </Card>
          </div>
        )}
      </AsyncBoundary>

      <Modal
        open={Boolean(selected)}
        onClose={() => setSelected(null)}
        title={selected ? `Detection ${selected.id}` : ''}
        description={selected ? selected.site : ''}
      >
        {selected && <DetectionDetail detection={selected} />}
      </Modal>
    </>
  )
}

export default Dashboard
