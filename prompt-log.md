# Prompt log

บันทึกทุกครั้งที่ใช้ AI กับ repo นี้ เขียนต่อท้ายเรื่อย ๆ ไม่ต้องลบของเก่า

---

## 2569-09-16 08:17 คำสั่ง: /plan

- เครื่องมือ: Copilot ใน VS Code
- ไฟล์: `specs/001-booking/spec.md` (Draft v1)
- ผลลัพธ์: `specs/001-booking/plan.md`
- การตัดสินใจ: ทีมอนุญาตให้ร่างแผนต่อแม้ spec ยังเป็น Draft v1 โดยคง Open Questions ไว้ และไม่ตอบคำถามแทนทีม
- Constraint ที่ AI ยังไม่ได้ใช้: ไม่มี ทุก Constraint ใน spec ถูกระบุใน plan แล้ว
- สิ่งที่ AI บอกว่าอยากเดาแต่ไม่ได้เดา:
  - เกณฑ์และขอบเขตของ “ช่วงเวลาใกล้เคียง” (`Q-01`)
  - กติกาการรีเซ็ตหรือการนับต่อเนื่องของหมายเลขคิว (`Q-02`)

---

## 2569-09-23 คำสั่ง: /tasks specs/001-booking/spec.md

- เครื่องมือ: Copilot ใน VS Code
- ไฟล์: `specs/001-booking/spec.md`, `specs/001-booking/plan.md`
- ผลลัพธ์: สร้าง `specs/001-booking/tasks.md` จำนวน 15 task เรียงตามการพึ่งพา พร้อมตารางตรวจ AC และ Constraint ครบถ้วน
- การตัดสินใจ: คง Q-02 เป็น Open Question และทำเครื่องหมาย task ที่เกี่ยวกับการออกหรือแสดงหมายเลขคิวเป็น `รอ Q-02` โดยไม่เดาคำตอบ
- การทดสอบที่ระบุ: AC-BKG-01 ถึง AC-BKG-06 ถูกผูกกับ task ครบทุกตัว รวมถึง NFR-PERF-01, NFR-SEC-01 และ NFR-USE-01

---

## 2569-09-23 คำสั่ง: /implement T-01 specs/001-booking/tasks.md

- ไฟล์ที่สร้างหรือแก้: `backend/app/db/models.py`, `backend/app/db/session.py`, `backend/app/db/migrations/001_init.py`, `backend/app/db/migrations/__init__.py`, `backend/tests/conftest.py`
- ผลลัพธ์: เพิ่ม schema สำหรับ `slots`, `bookings` และ `audit_logs`; ตาราง `bookings` อ้างอิงผู้รับบริการด้วย HN และไม่มีเลขบัตรประชาชน; `queue_no` เว้นว่างได้จนกว่า Q-02 จะมีคำตอบ
- ผล test: `cd backend && pytest` ผ่าน 4 tests
- สิ่งที่เกือบต้องเดา: ไม่ได้เดารูปแบบหมายเลขคิว เนื่องจากยังติด Q-02; คงฟิลด์ `queue_no` ให้ nullable ตาม plan.md
