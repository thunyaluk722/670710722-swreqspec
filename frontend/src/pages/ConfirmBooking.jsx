export default function ConfirmBooking({ slot, alternatives = [], onConfirm, onCancel, onSelectAlternative }) {
  const isFull = alternatives.length > 0

  return (
    <section className="rounded-2xl border border-orange-200 bg-orange-50 p-6 shadow-sm">
      <h2 className="text-xl font-bold text-slate-800">ยืนยันการจอง</h2>

      {isFull ? (
        <>
          <p className="mt-3 font-medium text-orange-700">ช่วงเวลาเต็ม</p>
          <p className="mt-2 text-sm text-slate-600">กรุณาเลือกช่วงเวลาที่ยังว่าง 3 ตัวเลือกที่ใกล้ที่สุด</p>
          <div className="mt-5 grid gap-3">
            {alternatives.slice(0, 3).map((option) => (
              <button
                key={option.id}
                type="button"
                onClick={() => onSelectAlternative(option)}
                className="rounded-xl border border-orange-200 bg-white p-3 text-left hover:border-orange-400"
              >
                <div className="text-sm text-slate-500">{option.date}</div>
                <div className="mt-1 text-lg font-bold text-slate-800">{option.start_time}</div>
              </button>
            ))}
          </div>
        </>
      ) : (
        <>
          <p className="mt-3 text-sm text-slate-600">
            คุณกำลังจองช่วงเวลา <span className="font-bold text-slate-800">{slot?.start_time}</span>
          </p>
          <div className="mt-5 flex gap-3">
            <button
              type="button"
              onClick={() => onConfirm(slot)}
              className="rounded-xl bg-teal-600 px-4 py-2 font-semibold text-white hover:bg-teal-700"
            >
              ยืนยันการจอง
            </button>
            <button
              type="button"
              onClick={onCancel}
              className="rounded-xl border border-slate-300 bg-white px-4 py-2 font-semibold text-slate-700 hover:bg-slate-100"
            >
              กลับ
            </button>
          </div>
        </>
      )}
    </section>
  )
}
