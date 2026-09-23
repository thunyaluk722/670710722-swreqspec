# Tasks: จองคิวตรวจสุขภาพ (Booking)

- Feature: จองคิวตรวจสุขภาพ (Booking)
- Spec ID: SPEC-BKG-001
- อ้างอิง: [plan.md](./plan.md)
- วันที่: 2569-09-23

มีทั้งหมด 15 task โดย 5 task ต้องรอคำตอบของ Open Question Q-02
งานที่รอ Q-02 เกี่ยวกับวิธีออกและแสดงหมายเลขคิว ส่วนงานอื่นสามารถทำตามสัญญาใน plan.md ได้

## รายการ task

### T-01 สร้างตารางและ migration
- รองรับ: CON-TECH-01, DOM-PDPA-01, IF-HIS-01, FR-BKG-01, FR-BKG-02, FR-BKG-04
- ตรวจด้วย: ไม่มี AC ตรง ๆ เป็นงานพื้นฐานของ T-02, T-03, T-04, T-07 และ T-08
- ไฟล์ที่แตะ: `backend/app/db/models.py`, `backend/app/db/session.py`, `backend/app/db/migrations/001_init.py`, `backend/tests/conftest.py`
- ต้องทำหลัง: ไม่มี
- เสร็จเมื่อ: migration สร้างตาราง `slots`, `bookings` และ `audit_logs` ได้ และตาราง `bookings` ไม่มีคอลัมน์เลขบัตรประชาชน
- สถานะ: เสร็จ รอทีมตรวจ

### T-02 สร้างการตรวจสิทธิ์ผู้รับบริการ
- รองรับ: IF-IDP-01
- ตรวจด้วย: ไม่มี AC ตรง ๆ เป็นงานพื้นฐานของ T-03, T-04, T-07 และ T-08
- ไฟล์ที่แตะ: `backend/app/auth/idp.py`, `backend/app/main.py`, `backend/tests/test_auth.py`
- ต้องทำหลัง: T-01
- เสร็จเมื่อ: ทุก endpoint ที่แตะข้อมูลผู้รับบริการตรวจผลยืนยันตัวตนก่อนดำเนินการ และ test การปฏิเสธผู้ที่ยังไม่ยืนยันผ่าน
- สถานะ: พร้อมทำ

### T-03 สร้าง API ค้นช่วงเวลาว่าง
- รองรับ: FR-BKG-01, FR-BKG-06
- ตรวจด้วย: ไม่มี AC ตรง ๆ เป็นงานพื้นฐานของ T-10 และ T-12
- ไฟล์ที่แตะ: `backend/app/slots/service.py`, `backend/app/slots/router.py`, `backend/app/main.py`, `backend/tests/test_slots.py`
- ต้องทำหลัง: T-01, T-02
- เสร็จเมื่อ: `GET /slots` คืนช่วงเวลาภายใน 30 วันพร้อมที่นั่งคงเหลือ และเปลี่ยน `package_code` แล้วคำนวณผลใหม่ได้
- สถานะ: พร้อมทำ

### T-04 สร้างการจองและตัดที่นั่ง
- รองรับ: FR-BKG-04, IF-HIS-01
- ตรวจด้วย: ไม่มี AC ตรง ๆ เป็นงานพื้นฐานของ T-05, T-06 และ T-07
- ไฟล์ที่แตะ: `backend/app/booking/service.py`, `backend/app/booking/router.py`, `backend/app/main.py`, `backend/tests/test_booking_create.py`
- ต้องทำหลัง: T-01, T-02
- เสร็จเมื่อ: `POST /bookings` บันทึก booking ด้วย HN และลด `remaining` ของช่วงเวลาที่เลือกลงอย่างถูกต้อง
- สถานะ: รอ Q-02

### T-05 ป้องกันการจองซ้ำในวันเดียวกัน
- รองรับ: FR-BKG-02
- ตรวจด้วย: AC-BKG-02
- ไฟล์ที่แตะ: `backend/app/booking/service.py`, `backend/app/booking/router.py`, `backend/tests/test_AC_BKG_02.py`
- ต้องทำหลัง: T-04
- เสร็จเมื่อ: `test_AC_BKG_02` ผ่าน โดยคำขอจองซ้ำถูกปฏิเสธและตอบหมายเลขคิวเดิม
- สถานะ: รอ Q-02

### T-06 เสนอช่วงเวลาใกล้เคียงเมื่อเต็ม
- รองรับ: FR-BKG-03
- ตรวจด้วย: AC-BKG-03
- ไฟล์ที่แตะ: `backend/app/slots/service.py`, `backend/app/booking/service.py`, `backend/app/booking/router.py`, `backend/tests/test_AC_BKG_03.py`
- ต้องทำหลัง: T-03, T-04
- เสร็จเมื่อ: `test_AC_BKG_03` ผ่าน โดยตอบ 409 พร้อม 3 ช่วงที่ใกล้ที่สุดในวันเดียวกันหรือวันถัดไป และไม่สร้าง booking ซ้อน
- สถานะ: พร้อมทำ

### T-07 จัดคิวส่งข้อความยืนยันและส่งซ้ำ
- รองรับ: FR-BKG-05, IF-NOT-01, NFR-REL-02
- ตรวจด้วย: AC-BKG-04
- ไฟล์ที่แตะ: `backend/app/notify/queue.py`, `backend/app/booking/service.py`, `backend/tests/test_AC_BKG_04.py`
- ต้องทำหลัง: T-04
- เสร็จเมื่อ: `test_AC_BKG_04` ผ่าน โดย booking ยังถูกบันทึกและงานส่งซ้ำมีเวลาครบกำหนดไม่เกิน 5 นาทีตาม ASM-03
- สถานะ: รอ Q-02

### T-08 บันทึก audit log
- รองรับ: DOM-PDPA-01
- ตรวจด้วย: AC-BKG-06
- ไฟล์ที่แตะ: `backend/app/audit/middleware.py`, `backend/app/main.py`, `backend/tests/test_AC_BKG_06.py`
- ต้องทำหลัง: T-01, T-02
- เสร็จเมื่อ: `test_AC_BKG_06` ผ่าน โดยการเปิดดู booking สร้าง log ที่มีผู้เข้าถึง เวลา และ HN และกำหนด retention ไม่น้อยกว่า 1 ปี
- สถานะ: พร้อมทำ

### T-09 สร้างการค้น HN จาก HIS
- รองรับ: IF-HIS-01
- ตรวจด้วย: ไม่มี AC ตรง ๆ เป็นงานพื้นฐานของ T-04 และ T-12
- ไฟล์ที่แตะ: `backend/app/his/client.py`, `backend/app/booking/router.py`, `backend/app/main.py`, `backend/tests/test_patient_lookup.py`
- ต้องทำหลัง: T-02
- เสร็จเมื่อ: `GET /patients/lookup` ส่งเลขบัตรไปยัง HIS เพื่อคืน HN และเลขบัตรไม่ถูกเก็บใน booking
- สถานะ: พร้อมทำ

### T-10 สร้างหน้าจอเลือกแพ็กเกจและช่วงเวลา
- รองรับ: FR-BKG-01, FR-BKG-06, NFR-USE-01
- ตรวจด้วย: ไม่มี AC ตรง ๆ เป็นงานพื้นฐานของ T-11 และ T-12
- ไฟล์ที่แตะ: `frontend/src/pages/SlotPicker.jsx`, `frontend/src/api/client.js`, `frontend/src/App.jsx`, `frontend/src/__tests__/SlotPicker.test.jsx`
- ต้องทำหลัง: ไม่มี
- เสร็จเมื่อ: หน้าจอแสดงช่วงเวลาจาก API จำลองภายใน 30 วันและโหลดช่วงเวลาใหม่เมื่อเปลี่ยนแพ็กเกจ
- สถานะ: พร้อมทำ

### T-11 สร้างหน้ายืนยันและแสดงช่วงเวลาเต็ม
- รองรับ: FR-BKG-03, FR-BKG-04
- ตรวจด้วย: AC-BKG-03
- ไฟล์ที่แตะ: `frontend/src/pages/ConfirmBooking.jsx`, `frontend/src/App.jsx`, `frontend/src/__tests__/AC-BKG-03.test.jsx`
- ต้องทำหลัง: T-10
- เสร็จเมื่อ: `AC-BKG-03.test.jsx` ผ่าน โดย API จำลองตอบ 409 แล้วหน้าจอแสดง “ช่วงเวลาเต็ม” และตัวเลือก 3 ช่วง
- สถานะ: พร้อมทำ

### T-12 สร้างหน้าจอแสดงผลการจอง
- รองรับ: FR-BKG-04, FR-BKG-05
- ตรวจด้วย: AC-BKG-01, AC-BKG-04
- ไฟล์ที่แตะ: `frontend/src/pages/BookingResult.jsx`, `frontend/src/App.jsx`, `frontend/src/__tests__/AC-BKG-01.test.jsx`, `frontend/src/__tests__/AC-BKG-04.test.jsx`
- ต้องทำหลัง: T-10
- เสร็จเมื่อ: หน้าจอแสดงผลตอบกลับของการจองและยังแสดงหมายเลขคิวเมื่อ API แจ้งว่าส่งข้อความไม่สำเร็จ
- สถานะ: รอ Q-02

### T-13 เชื่อมหน้าจอกับ API จริง
- รองรับ: FR-BKG-01, FR-BKG-03, FR-BKG-04, FR-BKG-05
- ตรวจด้วย: ไม่มี AC ตรง ๆ เป็นงานเชื่อมต่อของ T-10, T-11, T-12, T-03, T-06 และ T-07
- ไฟล์ที่แตะ: `frontend/src/api/client.js`, `frontend/src/App.jsx`, `frontend/vite.config.js`
- ต้องทำหลัง: T-03, T-06, T-07, T-10, T-11, T-12
- เสร็จเมื่อ: หน้าจอเรียก `GET /slots` และ `POST /bookings` ผ่าน `/api` และแสดงผลสำเร็จ/409/ส่งข้อความไม่สำเร็จได้ตรงกับสัญญา API
- สถานะ: รอ Q-02

### T-14 ทำให้การรับส่งข้อมูลใช้ TLS
- รองรับ: NFR-SEC-01
- ตรวจด้วย: ไม่มี AC ตรง ๆ เป็นงานพื้นฐานด้านคุณภาพของ T-13
- ไฟล์ที่แตะ: `backend/app/config.py`, `frontend/vite.config.js`, `backend/tests/test_security_transport.py`
- ต้องทำหลัง: T-13
- เสร็จเมื่อ: การตั้งค่าและ test ยืนยันว่าการรับส่งข้อมูลการจองบังคับใช้ TLS 1.2 ขึ้นไป
- สถานะ: พร้อมทำ

### T-15 ทดสอบประสิทธิภาพและความง่ายในการใช้งาน
- รองรับ: NFR-PERF-01, NFR-USE-01
- ตรวจด้วย: AC-BKG-05
- ไฟล์ที่แตะ: `backend/tests/test_AC_BKG_05.py`, `frontend/src/__tests__/NFR-USE-01.test.jsx`
- ต้องทำหลัง: T-03, T-10, T-13
- เสร็จเมื่อ: `test_AC_BKG_05` วัดผู้ใช้พร้อมกัน 200 คนและ p95 ไม่เกิน 2 วินาที และการทดสอบผู้ใช้ใหม่ 10 คนพบความสำเร็จอย่างน้อย 8 คนภายใน 3 นาที
- สถานะ: พร้อมทำ

## ตารางตรวจความครบของ Acceptance Criteria

| AC ID | task ที่ตรวจ AC นี้ |
|---|---|
| AC-BKG-01 | T-12 |
| AC-BKG-02 | T-05 |
| AC-BKG-03 | T-06, T-11 |
| AC-BKG-04 | T-07, T-12 |
| AC-BKG-05 | T-15 |
| AC-BKG-06 | T-08 |

## ตารางตรวจความครบของ Constraints

| Constraint ID | task ที่ทำให้เป็นจริง |
|---|---|
| CON-TECH-01 | T-01 |
| DOM-PDPA-01 | T-01, T-08 |
| IF-IDP-01 | T-02 |
| IF-HIS-01 | T-01, T-04, T-09 |
| IF-NOT-01 | T-07, T-13 |

## สิ่งที่ยังไม่ทำ

- Q-02 หมายเลขคิวรีเซ็ตรายวัน หรือนับต่อเนื่อง และมีรูปแบบอย่างไร (เช่น A001) ยังต้องถามเจ้าหน้าที่เวชระเบียน
  - task ที่รอ: T-04, T-05, T-07, T-12 และ T-13
  - จนกว่าจะได้คำตอบ จะยังไม่กำหนดวิธีออกเลขคิวหรือรูปแบบการแสดงเลขคิว
