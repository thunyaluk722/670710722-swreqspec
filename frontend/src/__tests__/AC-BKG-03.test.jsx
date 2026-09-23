import { render, screen } from '@testing-library/react'
import ConfirmBooking from '../pages/ConfirmBooking.jsx'

it('แสดงข้อความช่วงเวลาเต็มและตัวเลือกช่วงเวลา 3 รายการ', () => {
  const alternatives = [
    { id: 11, date: '2026-09-23', start_time: '10:30' },
    { id: 12, date: '2026-09-23', start_time: '11:00' },
    { id: 13, date: '2026-09-24', start_time: '09:00' },
  ]

  render(
    <ConfirmBooking
      slot={{ start_time: '09:00' }}
      alternatives={alternatives}
      onConfirm={() => {}}
      onCancel={() => {}}
      onSelectAlternative={() => {}}
    />,
  )

  expect(screen.getByText('ช่วงเวลาเต็ม')).toBeTruthy()
  expect(screen.getAllByText('2026-09-23').length).toBeGreaterThan(0)
  expect(screen.getAllByText('09:00').length).toBeGreaterThan(0)
})
