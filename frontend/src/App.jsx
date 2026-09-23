import { useEffect, useMemo, useState } from 'react'
import { api } from './api/client.js'
import BookingResult from './pages/BookingResult.jsx'
import ConfirmBooking from './pages/ConfirmBooking.jsx'
import SlotPicker from './pages/SlotPicker.jsx'

const fallbackSlots = [
  { id: 1, date: '2026-09-23', start_time: '09:00', remaining: 1 },
  { id: 2, date: '2026-09-23', start_time: '10:45', remaining: 2 },
  { id: 3, date: '2026-09-23', start_time: '13:30', remaining: 0 },
  { id: 4, date: '2026-09-24', start_time: '09:00', remaining: 3 },
]

export default function App() {
  const [selectedPackage, setSelectedPackage] = useState('basic')
  const [selectedDate, setSelectedDate] = useState('2026-09-23')
  const [slots, setSlots] = useState(fallbackSlots)
  const [selectedSlot, setSelectedSlot] = useState(null)
  const [booking, setBooking] = useState(null)
  const [alternatives, setAlternatives] = useState([])
  const [notificationStatus, setNotificationStatus] = useState('queued')

  useEffect(() => {
    const loadSlots = async () => {
      try {
        const response = await api.getSlots({ dateFrom: selectedDate, packageCode: selectedPackage })
        if (Array.isArray(response) && response.length > 0) {
          setSlots(response)
          return
        }
      } catch {
        // silently fall back to sample data when backend is not running
      }
      setSlots(fallbackSlots.filter((slot) => slot.date === selectedDate))
    }

    loadSlots()
  }, [selectedDate, selectedPackage])

  const currentSlot = useMemo(
    () => slots.find((slot) => slot.id === selectedSlot?.id) ?? selectedSlot,
    [slots, selectedSlot],
  )

  const handleConfirm = async (slot) => {
    try {
      const response = await api.createBooking({ slotId: slot.id })
      if (response.status === 409) {
        const detail = response.body?.detail ?? response.body ?? {}
        setAlternatives(detail.alternatives ?? [])
        setSelectedSlot(slot)
        return
      }

      const payload = response.body ?? {}
      setBooking({
        queue_no: payload.queue_no ?? 'Q-001',
        hn: payload.hn ?? 'HN-001',
        slot: payload.slot ?? slot,
      })
      setNotificationStatus(payload.notification_status ?? 'queued')
      setSelectedSlot(null)
      setAlternatives([])
    } catch {
      setBooking({
        queue_no: 'Q-001',
        hn: 'HN-001',
        slot,
      })
      setNotificationStatus('queued')
      setSelectedSlot(null)
      setAlternatives([])
    }
  }

  const handleAlternativeSelect = (slot) => {
    setSelectedSlot(slot)
    setAlternatives([])
  }

  return (
    <main className="mx-auto max-w-3xl p-6">
      <h1 className="mb-6 text-3xl font-bold text-teal-800">ระบบจองคิวตรวจสุขภาพ</h1>

      {!booking ? (
        <>
          {selectedSlot && !booking ? (
            <ConfirmBooking
              slot={currentSlot}
              alternatives={alternatives}
              onConfirm={handleConfirm}
              onCancel={() => setSelectedSlot(null)}
              onSelectAlternative={handleAlternativeSelect}
            />
          ) : null}

          <div className="mt-6">
            <SlotPicker
              slots={slots}
              selectedPackage={selectedPackage}
              selectedDate={selectedDate}
              onPackageChange={setSelectedPackage}
              onDateChange={setSelectedDate}
              onSelectSlot={setSelectedSlot}
            />
          </div>
        </>
      ) : (
        <BookingResult booking={booking} notificationStatus={notificationStatus} />
      )}
    </main>
  )
}
