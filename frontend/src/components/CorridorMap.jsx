import {
  BORDER_KM,
  CORRIDOR_LENGTH_KM,
  WAYPOINTS,
} from '../services/monitoringService'
import { SEVERITY, SEVERITY_KEYS } from '../lib/detections'

// Schematic geometry: the corridor is drawn straightened, so distance along
// the line is corridor kilometres rather than ground position.
const WIDTH = 1000
const HEIGHT = 140
const PADDING = 28
const LINE_Y = 62
const MARKER_Y = LINE_Y - 20

const toX = (km) => PADDING + (km / CORRIDOR_LENGTH_KM) * (WIDTH - PADDING * 2)

/** Keeps the first and last labels inside the viewBox instead of clipping. */
const anchorFor = (km) => {
  if (km === 0) return 'start'
  if (km === CORRIDOR_LENGTH_KM) return 'end'
  return 'middle'
}

function CorridorMap({ detections, selectedId, onSelect }) {
  return (
    <div>
      {/* Below the min-width the labels would shrink past legibility, so the
          schematic scrolls instead of squashing. */}
      <div className="overflow-x-auto">
      <svg
        viewBox={`0 0 ${WIDTH} ${HEIGHT}`}
        className="w-full min-w-[44rem]"
        role="img"
        aria-label={`Schematic of the ${CORRIDOR_LENGTH_KM} kilometre corridor with ${detections.length} detections marked`}
      >
        {/* Country legs, split at the Gaya border crossing. */}
        <line
          x1={toX(0)}
          y1={LINE_Y}
          x2={toX(BORDER_KM)}
          y2={LINE_Y}
          stroke="#cbd5e1"
          strokeWidth="6"
          strokeLinecap="round"
        />
        <line
          x1={toX(BORDER_KM)}
          y1={LINE_Y}
          x2={toX(CORRIDOR_LENGTH_KM)}
          y2={LINE_Y}
          stroke="#e2e8f0"
          strokeWidth="6"
          strokeLinecap="round"
        />
        <line
          x1={toX(BORDER_KM)}
          y1={LINE_Y - 9}
          x2={toX(BORDER_KM)}
          y2={LINE_Y + 9}
          stroke="#94a3b8"
          strokeWidth="1.5"
        />

        <text
          x={toX(BORDER_KM / 2)}
          y="14"
          textAnchor="middle"
          fill="#94a3b8"
          fontSize="11"
          letterSpacing="0.06em"
        >
          NIGER
        </text>
        <text
          x={toX((BORDER_KM + CORRIDOR_LENGTH_KM) / 2)}
          y="14"
          textAnchor="middle"
          fill="#94a3b8"
          fontSize="11"
          letterSpacing="0.06em"
        >
          BENIN
        </text>

        {WAYPOINTS.map(({ km, label }) => (
          <g key={km}>
            <line
              x1={toX(km)}
              y1={LINE_Y + 8}
              x2={toX(km)}
              y2={LINE_Y + 16}
              stroke="#cbd5e1"
              strokeWidth="1.5"
            />
            <text
              x={toX(km)}
              y={LINE_Y + 32}
              textAnchor={anchorFor(km)}
              fill="#64748b"
              fontSize="12"
            >
              {label}
            </text>
            <text
              x={toX(km)}
              y={LINE_Y + 48}
              textAnchor={anchorFor(km)}
              fill="#94a3b8"
              fontSize="11"
            >
              {km.toLocaleString('en-US')} km
            </text>
          </g>
        ))}

        {detections.map((detection) => {
          const isSelected = detection.id === selectedId

          return (
            <g
              key={detection.id}
              onClick={() => onSelect?.(detection)}
              className={onSelect ? 'cursor-pointer' : undefined}
            >
              {/* Oversized transparent target so the small dot stays clickable. */}
              <circle cx={toX(detection.km)} cy={MARKER_Y} r="14" fill="transparent" />
              <line
                x1={toX(detection.km)}
                y1={MARKER_Y + 6}
                x2={toX(detection.km)}
                y2={LINE_Y - 5}
                stroke="#cbd5e1"
                strokeWidth="1.5"
              />
              <circle
                cx={toX(detection.km)}
                cy={MARKER_Y}
                r={isSelected ? 8 : 6}
                fill={`var(--color-severity-${detection.severity})`}
                stroke="#ffffff"
                strokeWidth="2"
              />
              {isSelected && (
                <circle
                  cx={toX(detection.km)}
                  cy={MARKER_Y}
                  r="12"
                  fill="none"
                  stroke={`var(--color-severity-${detection.severity})`}
                  strokeWidth="1.5"
                  opacity="0.5"
                />
              )}
            </g>
          )
        })}
      </svg>
      </div>

      <div className="mt-2 flex flex-wrap items-center gap-x-5 gap-y-2 border-t border-slate-100 pt-3 text-xs text-slate-600">
        {SEVERITY_KEYS.map((key) => (
          <span key={key} className="inline-flex items-center gap-1.5">
            <span
              className={`size-2.5 rounded-full ${SEVERITY[key].dot}`}
              aria-hidden="true"
            />
            {SEVERITY[key].label}
          </span>
        ))}
        <span className="ml-auto text-slate-400">
          Straightened schematic — position is distance along the corridor
        </span>
      </div>
    </div>
  )
}

export default CorridorMap
