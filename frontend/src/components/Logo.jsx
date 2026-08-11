// AI generated, we can either keep it, or work on a logo if we have enough time

function Logo({ className = '', showWordmark = true, tone = 'brand' }) {
  const markTone =
    tone === 'onDark' ? 'bg-white/15 text-white' : 'bg-brand-600 text-white'
  const textTone = tone === 'onDark' ? 'text-white' : 'text-slate-900'

  return (
    <span className={`inline-flex items-center gap-2.5 ${className}`}>
      <span
        className={`flex size-9 shrink-0 items-center justify-center rounded-lg ${markTone}`}
      >
        {/* Pipeline segment crossing a scan sweep. */}
        <svg
          viewBox="0 0 24 24"
          fill="none"
          stroke="currentColor"
          strokeWidth="1.9"
          strokeLinecap="round"
          className="size-5"
          aria-hidden="true"
        >
          <path d="M3 15h5l3-6 3 6h5" />
          <circle cx="11" cy="9" r="1.6" fill="currentColor" stroke="none" />
        </svg>
      </span>

      {showWordmark && (
        <span className={`text-lg font-semibold tracking-tight ${textTone}`}>
          PipeProctor
        </span>
      )}
    </span>
  )
}

export default Logo
