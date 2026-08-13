/**
 * The one surface every panel in the app sits on. Pass `title` to get the
 * header row; leave it out for a bare surface.
 */
function Card({ title, description, action, className = '', bodyClassName = 'p-5', children }) {
  return (
    <section
      className={`rounded-xl border border-slate-200 bg-white ${className}`}
    >
      {(title || action) && (
        <header className="flex items-start justify-between gap-4 border-b border-slate-100 px-5 py-4">
          <div>
            {title && (
              <h2 className="text-sm font-semibold text-slate-900">{title}</h2>
            )}
            {description && (
              <p className="mt-0.5 text-xs text-slate-500">{description}</p>
            )}
          </div>
          {action}
        </header>
      )}

      <div className={bodyClassName}>{children}</div>
    </section>
  )
}

export default Card
