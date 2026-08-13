import { useEffect, useState } from 'react'

/**
 * Runs a loader once on mount and tracks its state.
 *
 * `loader` must have a stable identity — pass a service method or a function
 * defined outside the component, not an inline arrow.
 */
export function useAsyncData(loader) {
  const [state, setState] = useState({
    data: null,
    error: null,
    isLoading: true,
  })

  useEffect(() => {
    let active = true
    setState({ data: null, error: null, isLoading: true })

    loader()
      .then((data) => {
        if (active) setState({ data, error: null, isLoading: false })
      })
      .catch((error) => {
        if (active) setState({ data: null, error, isLoading: false })
      })

    return () => {
      active = false
    }
  }, [loader])

  return state
}
