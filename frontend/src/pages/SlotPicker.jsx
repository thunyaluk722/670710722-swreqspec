export default function SlotPicker({ slots = [], selectedPackage = 'basic', onPackageChange, selectedDate, onDateChange, onSelectSlot }) {
  return (
    <section className="rounded-2xl border border-slate-200 bg-white p-6 shadow-sm">
      <div className="mb-4 flex flex-col gap-3 md:flex-row md:items-center md:justify-between">
        <div>
          <p className="text-sm font-medium uppercase tracking-[0.2em] text-teal-700">เลือกแพ็กเกจ</p>
          <h2 className="mt-1 text-xl font-bold text-slate-800">จองคิวตรวจสุขภาพ</h2>
        </div>
        <label className="flex items-center gap-2 text-sm text-slate-700">
          <span>วันที่</span>
          <input
            type="date"
            value={selectedDate}
            onChange={(event) => onDateChange(event.target.value)}
            className="rounded-lg border border-slate-300 px-2 py-1"
          />
        </label>
      </div>

      <div className="mb-6 flex gap-3">
        {['basic', 'premium'].map((pkg) => (
          <button
            key={pkg}
            type="button"
            onClick={() => onPackageChange(pkg)}
            className={[
              'rounded-full px-4 py-2 text-sm font-semibold transition',
              selectedPackage === pkg
                ? 'bg-teal-600 text-white shadow'
                : 'bg-slate-100 text-slate-700 hover:bg-slate-200',
            ].join(' ')}
          >
            {pkg === 'basic' ? 'แพ็กเกจทั่วไป' : 'แพ็กเกจพิเศษ'}
          </button>
        ))}
      </div>

      <div className="grid gap-3">
        {slots.length === 0 ? (
          <div className="rounded-xl border border-dashed border-slate-300 p-4 text-sm text-slate-500">
            ยังไม่มีช่วงเวลาว่างในวันที่เลือก
          </div>
        ) : (
          slots.map((slot) => (
            <button
              key={slot.id}
              type="button"
              onClick={() => onSelectSlot(slot)}
              className="flex items-center justify-between rounded-xl border border-slate-200 bg-slate-50 p-4 text-left transition hover:border-teal-400 hover:bg-teal-50"
            >
              <div>
                <div className="text-sm text-slate-500">{slot.date}</div>
                <div className="mt-1 text-lg font-bold text-slate-800">{slot.start_time}</div>
              </div>
              <div className="text-right">
                <div className="text-xs uppercase tracking-[0.2em] text-slate-500">ที่นั่งคงเหลือ</div>
                <div className="text-2xl font-bold text-teal-700">{slot.remaining}</div>
              </div>
            </button>
          ))
        )}
      </div>
    </section>
  )
}
