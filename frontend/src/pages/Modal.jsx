import { useState } from 'react'
import Card from '../components/Card'
import Modal from '../components/Modal'
import PageHeader from '../components/PageHeader'

/**
 * Demo of the shared Modal component — the same dialog the dashboard and
 * monitoring views open for detection details. Safe to delete once the team
 * no longer needs the reference.
 */
function ModalPage() {
  const [openDialog, setOpenDialog] = useState(null)

  const close = () => setOpenDialog(null)

  return (
    <>
      <PageHeader
        title="Modal"
        description="Reference for the shared dialog component."
      />

      <Card
        title="Shared dialog"
        description="Closes on Escape, on the backdrop, and on the close button"
        className="max-w-2xl"
      >
        <div className="flex flex-wrap gap-3">
          <button
            type="button"
            onClick={() => setOpenDialog('plain')}
            className="rounded-lg border border-slate-300 px-3 py-2 text-sm font-medium text-slate-700 hover:bg-slate-100"
          >
            Open plain dialog
          </button>

          <button
            type="button"
            onClick={() => setOpenDialog('confirm')}
            className="rounded-lg bg-brand-700 px-3 py-2 text-sm font-semibold text-white hover:bg-brand-800"
          >
            Open confirmation dialog
          </button>
        </div>
      </Card>

      <Modal
        open={openDialog === 'plain'}
        onClose={close}
        title="Plain dialog"
        description="Title, description, and a body"
      >
        <p className="text-sm leading-relaxed text-slate-600">
          Pass any content as children. The dialog sizes to its body and scrolls
          the page behind it only after it closes.
        </p>
      </Modal>

      <Modal
        open={openDialog === 'confirm'}
        onClose={close}
        title="Request inspection"
        description="Detection PP-2418 · Dosso corridor"
        footer={
          <>
            <button
              type="button"
              onClick={close}
              className="rounded-lg border border-slate-300 px-3 py-2 text-sm font-medium text-slate-700 hover:bg-slate-100"
            >
              Cancel
            </button>
            <button
              type="button"
              onClick={close}
              className="rounded-lg bg-brand-700 px-3 py-2 text-sm font-semibold text-white hover:bg-brand-800"
            >
              Confirm
            </button>
          </>
        }
      >
        <p className="text-sm leading-relaxed text-slate-600">
          Add a <code className="font-mono text-xs">footer</code> to get the
          action row. Buttons keep their own handlers, so the dialog stays
          unaware of what they do.
        </p>
      </Modal>
    </>
  )
}

export default ModalPage
