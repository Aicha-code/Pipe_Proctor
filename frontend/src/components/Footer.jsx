function Footer() {
  return (
    <footer className="flex flex-wrap items-center justify-between gap-2 border-t border-slate-200 px-6 py-4 text-xs text-slate-500">
      <p>© {new Date().getFullYear()} PipeProctor — Carnegie Mellon University Africa</p>
      <p>Sentinel-1 SAR · Niger–Benin corridor</p>
    </footer>
  )
}

export default Footer
