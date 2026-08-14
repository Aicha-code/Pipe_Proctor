import { AlertIcon, SpinnerIcon } from './icons'

/**
 * Renders the loading and error states around any `useAsyncData` result, so
 * pages only have to describe the happy path.
 */
function AsyncBoundary({ isLoading, error, children }) {
  if (isLoading) {
    return (
      <div className="flex items-center justify-center gap-2.5 rounded-xl border border-slate-200 bg-white py-20 text-sm text-slate-500">
        <SpinnerIcon className="size-4 animate-spin" strokeWidth={2.25} />
        Loading corridor data…
      </div>
    )
  }

  if (error) {
    return (
      <div
        role="alert"
        className="flex items-start gap-2.5 rounded-xl border border-red-200 bg-red-50 p-4 text-sm text-red-700"
      >
        <AlertIcon className="mt-0.5 size-4 shrink-0" />
        <span>{error.message ?? 'Could not load corridor data.'}</span>
      </div>
    )
  }

  return children
}

export default AsyncBoundary
