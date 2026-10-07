# Prompt log

บันทึกทุกครั้งที่ใช้ AI กับ repo นี้ เขียนต่อท้ายเรื่อย ๆ ไม่ลบของเก่า

---

## 2569-09-23 13.40 คำสั่ง: /tasks specs/001-booking/spec.md

- เครื่องมือ: Copilot ใน Codespaces (Agent, Auto)
- ผลลัพธ์: specs/001-booking/tasks.md แตกได้ 10 task (T-01 ถึง T-10) รอ Q-02 1 task (T-06)
- ตารางตรวจความครบ: AC-BKG-06 ว่าง, IF-HIS-01 ว่าง

### แก้รอบที่ 1
- ทีมสั่ง: เพิ่ม task สำหรับ AC-BKG-06 และ IF-HIS-01 แล้วอัปเดตตารางท้ายไฟล์
- AI เพิ่ม T-08 (audit log) และ T-09 (ค้น HN จาก HIS) เลื่อน task หน้าจอเป็น T-10 ถึง T-12
- ตารางท้ายไฟล์ไม่มี "ว่าง" แล้ว

---

## 2569-09-23 14.20 คำสั่ง: /implement T-01 specs/001-booking/tasks.md

- ไฟล์ที่สร้าง: backend/app/config.py, backend/app/db/models.py, backend/app/db/session.py, backend/app/db/migrations/001_init.py, backend/tests/test_T01_schema.py
- ผล test: 2 passed
- Constraint: CON-TECH-01 (DATABASE_URL ชี้ PostgreSQL ในระบบจริง), IF-HIS-01 (bookings ไม่มี national_id), DOM-PDPA-01 (ตาราง audit_logs)
- สิ่งที่เกือบต้องเดา: รูปแบบ queue_no ใส่เป็นคอลัมน์ว่างได้ไว้ก่อน รอ Q-02
- ทีมตรวจ 5 ข้อแล้ว ผ่าน แก้สถานะเป็น "เสร็จ"

---

## 2569-09-27 19.05 คำสั่ง: /implement T-02 specs/001-booking/tasks.md

- ไฟล์ที่สร้าง: backend/app/slots/router.py, backend/app/slots/service.py, backend/app/main.py, backend/tests/conftest.py, backend/tests/test_AC_BKG_05.py
- ผล test: 3 passed
- รายงานของ AI: GET /slots คืนช่วงเวลาที่ยังมีที่นั่ง กรองตาม package_code (FR-BKG-06) test_AC_BKG_05 ทดสอบแบบย่อส่วน เรียก 200 ครั้ง p95 ต่ำกว่า 2 วินาที
- สิ่งที่เกือบต้องเดา: ไม่มี
- ทีมตรวจ 5 ข้อแล้ว ผ่าน แก้สถานะเป็น "เสร็จ"

---

## 2569-09-28 20.30 คำสั่ง: /implement T-03 specs/001-booking/tasks.md

- ไฟล์ที่สร้าง: backend/app/booking/router.py, backend/app/booking/service.py, backend/app/auth/idp.py และแก้ backend/app/main.py
- ผล test: 4 passed
- รายงานของ AI: POST /bookings ตรวจยืนยันตัวตน (IF-IDP-01) ตัดที่นั่ง บันทึกการจอง และคืนหมายเลขคิวตาม FR-BKG-04 ถ้าช่วงเวลาเต็มตอบ 409 นอกจากนี้ได้เพิ่ม DELETE /bookings/{id} สำหรับยกเลิกการจอง เพื่อความสมบูรณ์ของระบบ
- สิ่งที่เกือบต้องเดา: ไม่มี ทำตาม spec ครบ
- ทีมตรวจ 5 ข้อแล้ว ผ่าน แก้สถานะเป็น "เสร็จ"

---

## 2569-10-07 08.13 คำสั่ง: /testcases AC-BKG-01 specs/001-booking/

- โหมด: ร่าง (ยังไม่มีแถวใน test-cases.md สำหรับ AC-BKG-01)
- TC ID ที่เสนอ: TC-BKG-01-1, TC-BKG-01-2, TC-BKG-01-3
- ผล: เพิ่มแถวสถานะ "ร่าง" ใน specs/001-booking/test-cases.md แล้วหยุด ไม่เขียนโค้ด test
- หมายเหตุ: Then ที่เกี่ยวกับหมายเลขคิวมีคำว่า "(รอ Q-02)" เพราะ spec ยังไม่มีรูปแบบเลขคิวที่ชัดเจน

---

## 2569-10-07 08.26 คำสั่ง: /testcases AC-BKG-01 specs/001-booking/

- โหมด: เขียน test (มีแถวสถานะ "ใช้ได้" ใน specs/001-booking/test-cases.md)
- TC ID ที่เขียน: TC-BKG-01-1, TC-BKG-01-2, TC-BKG-01-3
- ไฟล์โค้ด test: backend/tests/test_AC_BKG_01.py
- ผล test: 3 passed
- สรุป: ทุกกรณีใน AC-BKG-01 ตรงตามแถวในตาราง และไม่มีบั๊กจากการเขียน test

---

## 2569-10-07 08:25 คำสั่ง: /testcases AC-BKG-01 specs/001-booking/backend/tests/test_AC_BKG_01.py

- โหมด: เขียน test
- AC: AC-BKG-01
- พร้อมใช้งานใน test-cases.md: 3 แถวสถานะ "ใช้ได้"
- ผล: เขียน test 3 ตัวใน backend/tests/test_AC_BKG_01.py และรัน pytest
- ผลลัพธ์: รันทีละไฟล์โดย `cd backend && pytest tests/test_AC_BKG_01.py -q`

---

## 2569-10-07 08:28 คำสั่ง: คืน test_AC_BKG_01 เดิมกลับมา

- ผล: คืนฟังก์ชัน `test_AC_BKG_01` เดิมใน `backend/tests/test_AC_BKG_01.py` โดยคง test ใหม่ TC-BKG-01-1 ถึง TC-BKG-01-3 ไว้ครบ
- ผล test: `cd backend && pytest -v` ผ่าน 7 tests
