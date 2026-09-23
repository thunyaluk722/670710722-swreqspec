export default function BookingResult({ booking, notificationStatus = 'queued' }) {
  const statusText = notificationStatus === 'failed' ? 'ส่งข้อความไม่สำเร็จ แต่บันทึกการจองแล้ว' : 'การจองสำเร็จ'

  return (
    <section className="rounded-2xl border border-teal-200 bg-teal-50 p-6 shadow-sm">
      <div className="text-sm uppercase tracking-[0.2em] text-teal-700">หมายเลขคิว</div>
      <div className="mt-2 text-4xl font-black text-teal-800">{booking?.queue_no ?? 'Q-001'}</div>
      <p className="mt-3 text-slate-700">{statusText}</p>
      <div className="mt-5 rounded-xl border border-teal-200 bg-white p-4 text-sm text-slate-600">
        <div>HN: {booking?.hn ?? 'HN-001'}</div>
        <div className="mt-1">วันที่: {booking?.slot?.date ?? '2026-09-23'}</div>
        <div className="mt-1">เวลา: {booking?.slot?.start_time ?? '09:00'}</div>
      </div>
    </section>
  )
}
