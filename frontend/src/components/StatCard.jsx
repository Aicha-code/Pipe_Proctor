/** One headline number, with a short line of context under it. */
function StatCard({ label, value, hint, icon: Icon }) {
  return (
    <div className="rounded-xl border border-slate-200 bg-white p-5">
      <div className="flex items-center justify-between gap-3">
        <p className="text-xs font-medium uppercase tracking-wide text-slate-500">
          {label}
        </p>
        {Icon && <Icon className="size-4 shrink-0 text-slate-400" />}
      </div>

      <p className="mt-3 text-3xl font-semibold tracking-tight text-slate-900">
        {value}
      </p>

      {hint && <p className="mt-1 text-xs text-slate-500">{hint}</p>}
    </div>
  )
}

export default StatCard
