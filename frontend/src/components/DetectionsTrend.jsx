import {
  Area,
  AreaChart,
  CartesianGrid,
  ResponsiveContainer,
  Tooltip,
  XAxis,
  YAxis,
} from 'recharts'

const axisTick = { fontSize: 12, fill: '#94a3b8' }

function TrendTooltip({ active, payload, label }) {
  if (!active || !payload?.length) return null

  return (
    <div className="rounded-lg border border-slate-200 bg-white px-3 py-2 shadow-sm">
      <p className="text-xs text-slate-500">Week of {label}</p>
      <p className="text-sm font-semibold text-slate-900">
        {payload[0].value} detections
      </p>
    </div>
  )
}

/**
 * Twelve weeks of detection volume. One series, so no legend — the card
 * title says what is plotted.
 */
function DetectionsTrend({ data }) {
  return (
    <ResponsiveContainer width="100%" height={240}>
      <AreaChart data={data} margin={{ top: 8, right: 8, bottom: 0, left: -24 }}>
        <CartesianGrid vertical={false} stroke="#e2e8f0" />
        <XAxis
          dataKey="week"
          tickLine={false}
          axisLine={false}
          tick={axisTick}
          tickMargin={8}
          interval="preserveStartEnd"
          minTickGap={24}
        />
        <YAxis
          allowDecimals={false}
          tickLine={false}
          axisLine={false}
          tick={axisTick}
          width={48}
        />
        <Tooltip
          content={<TrendTooltip />}
          cursor={{ stroke: '#cbd5e1', strokeWidth: 1 }}
        />
        <Area
          type="monotone"
          dataKey="detections"
          stroke="var(--color-brand-600)"
          strokeWidth={2}
          fill="var(--color-brand-600)"
          fillOpacity={0.1}
          dot={false}
          activeDot={{ r: 4, strokeWidth: 2, stroke: '#ffffff' }}
        />
      </AreaChart>
    </ResponsiveContainer>
  )
}

export default DetectionsTrend
