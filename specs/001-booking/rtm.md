# RTM: จองคิวตรวจสุขภาพ (Booking)
อ้างอิง: spec.md SPEC-BKG-001 Draft v2 | tasks.md | test-cases.md
สร้างด้วย /verify เมื่อ 2569-10-07 08:31 | test: 7 ผ่าน 0 ไม่ผ่าน

## 1. ตามรอยไปข้างหน้า (requirement ไป โค้ด ไป test)
| ID | AC | task | โค้ด (ไฟล์: ฟังก์ชัน) | test (ผล) | สถานะ |
|---|---|---|---|---|---|
| FR-BKG-01 | AC-BKG-05 ตรวจเฉพาะประสิทธิภาพ ไม่ตรวจช่วง 30 วัน/จำนวนที่นั่ง | T-02 เสร็จ; T-10, T-12 พร้อมทำ | `backend/app/slots/router.py:get_slots`; `backend/app/slots/service.py:list_available_slots` จำกัด 14 วัน | `test_AC_BKG_05` ผ่าน แต่ยิงทีละคำขอ ไม่ได้ทดสอบผู้ใช้พร้อมกัน | ช่องโหว่ (F-05, F-06) |
| FR-BKG-02 | AC-BKG-02 | T-04 พร้อมทำ | `backend/app/booking/service.py:create_booking` ยังไม่ตรวจจองซ้ำรายวัน | ไม่มี test ของ AC-BKG-02 | ยังไม่ถึง |
| FR-BKG-03 | AC-BKG-03 | T-05, T-11, T-12 พร้อมทำ | `backend/app/booking/service.py:create_booking` ตรวจเต็มเฉพาะเมื่อ `remaining < 0`; การเสนอช่วงใกล้เคียง/หน้าจอยังไม่มี | ไม่มี test ของ AC-BKG-03 | ยังไม่ถึง |
| FR-BKG-04 | AC-BKG-01 | T-03 เสร็จ; T-06 รอ Q-02 | `backend/app/booking/router.py:create_booking`; `backend/app/booking/service.py:create_booking`, `next_queue_no` | `test_AC_BKG_01`, `test_TC_BKG_01_1_booking_success`, `test_TC_BKG_01_2_booking_last_slot`, `test_TC_BKG_01_3_requires_authentication` ผ่าน; มีการ assert หมายเลขคิวทั้งที่รอ Q-02 และไม่มี test หน้าจอ | ช่องโหว่ (F-03, F-07) |
| FR-BKG-05 | AC-BKG-04 | T-07 พร้อมทำ | ยังไม่มี notifier, booking lookup หรือหน้าจอผลการจอง | ไม่มี test ของ AC-BKG-04 | ยังไม่ถึง |
| FR-BKG-06 | ไม่มี AC | T-02 เสร็จบางส่วน; T-10, T-12 พร้อมทำ | `backend/app/slots/service.py:list_available_slots` กรอง `package_code`; หน้าจอเปลี่ยนแพ็กเกจยังไม่มี | ไม่มี test การเปลี่ยนแพ็กเกจ | ช่องโหว่ (F-09) |
| NFR-PERF-01 | AC-BKG-05 | T-02 เสร็จ | `backend/app/slots/router.py:get_slots`; `backend/app/slots/service.py:list_available_slots` | `test_AC_BKG_05` ผ่าน; 200 request ทำงานเรียงลำดับ ไม่ใช่ผู้ใช้พร้อมกัน 200 คน | ช่องโหว่ (F-06) |
| NFR-SEC-01 | ไม่มี AC | ไม่มี task ที่ระบุ TLS | ไม่พบการตั้งค่า TLS ใน `backend/app/` หรือ `frontend/src/` | ไม่มี test | ยังไม่ถึง |
| NFR-REL-02 | AC-BKG-04 | T-07 พร้อมทำ | ยังไม่มีโค้ดส่งซ้ำ | ไม่มี test ของ AC-BKG-04 | ยังไม่ถึง |
| NFR-USE-01 | ไม่มี AC | T-10 พร้อมทำ; ไม่มี task ทดสอบผู้ใช้ 8 ใน 10 คน | ยังไม่มีหน้าจอการจองจริง | ไม่มี test/ผลทดสอบผู้ใช้ | ยังไม่ถึง |
| CON-TECH-01 | ไม่มี AC | T-01 เสร็จ | `backend/app/config.py:DATABASE_URL`; `backend/app/db/session.py:engine` | `test_T01_tables_created` ผ่านบน SQLite; ไม่มี test ยืนยันการตั้งค่าระบบจริงเป็น PostgreSQL | ช่องโหว่ (F-08) |
| DOM-PDPA-01 | AC-BKG-06 | T-01 เสร็จเฉพาะตาราง; T-08 พร้อมทำ | `backend/app/db/models.py:AuditLog`; ไม่พบ middleware/การบันทึก audit | ไม่มี test ของ AC-BKG-06 | ยังไม่ถึง |
| IF-IDP-01 | AC-BKG-01 | T-03 เสร็จ | `backend/app/auth/idp.py:get_verified_hn` | `test_TC_BKG_01_3_requires_authentication` ผ่านเฉพาะกรณีไม่มี header; การตรวจ token เป็นเพียงตรวจ prefix | ช่องโหว่ (F-01) |
| IF-HIS-01 | ไม่มี AC ตรง ๆ | T-01 เสร็จเฉพาะ schema; T-09 พร้อมทำ | `backend/app/booking/router.py:BookingRequest`, `create_booking`; ยังไม่มี HIS lookup และ log มี `national_id` | `test_T01_no_national_id` ผ่านเฉพาะการไม่มีคอลัมน์; ไม่มี `test_IF_HIS_01` | ช่องโหว่ (F-02) |
| IF-NOT-01 | AC-BKG-04 | T-07 พร้อมทำ | ยังไม่มีโค้ด queue/การส่งข้อความ | ไม่มี test ของ AC-BKG-04 | ยังไม่ถึง |

## 2. ตามรอยย้อนกลับ (โค้ด ไป requirement)
| โค้ด (ไฟล์: ฟังก์ชัน หรือ endpoint) | อ้าง ID | ตรงกับข้อความใน spec ไหม | หมายเหตุ |
|---|---|---|---|
| `backend/app/main.py:lifespan`, `app` | CON-TECH-01, FR-BKG-01, FR-BKG-04 | บางส่วน | สร้างตารางและรวม router; ยังไม่มีการรวม audit, HIS, notify หรือ booking lookup |
| `backend/app/config.py:DATABASE_URL`, `backend/app/db/session.py:engine` | CON-TECH-01 | ไม่ตรงเมื่อไม่มี env | ค่าเริ่มต้นเป็น SQLite แม้ CON-TECH-01 กำหนด PostgreSQL (F-08) |
| `backend/app/db/migrations/001_init.py:upgrade`, `backend/app/db/models.py:Slot`, `Booking`, `AuditLog` | FR-BKG-01, FR-BKG-04, IF-HIS-01, DOM-PDPA-01, CON-TECH-01 | บางส่วน | มีตารางและไม่มีคอลัมน์ national_id ใน bookings; audit log ยังไม่มีการบันทึก/การคงข้อมูล 1 ปี และ queue_no ยังมีรูปแบบไม่ตัดสิน |
| `backend/app/auth/idp.py:get_verified_hn` | IF-IDP-01 | ไม่ตรง | รับ header ที่ขึ้นต้นด้วยค่าคงที่แล้วถือส่วนที่เหลือเป็น HN โดยไม่ตรวจผลจาก IDP จริง (F-01) |
| `backend/app/slots/router.py:get_slots` | FR-BKG-01, FR-BKG-06 | บางส่วน | ส่งวัน เวลา และ remaining; ไม่มี authentication; ยังไม่พบข้อกำหนดให้ปกป้อง endpoint นี้โดย AC แต่ IF-IDP-01 ระบุการตรวจยืนยันตัวตนก่อนเข้าถึงข้อมูลผู้รับบริการ |
| `backend/app/slots/service.py:list_available_slots` | FR-BKG-01, FR-BKG-06 | ไม่ตรงทั้งหมด | กรอง package/remaining ได้ แต่หน้าต่างเวลา 14 วันไม่ตรง 30 วัน (F-05) |
| `backend/app/booking/router.py:BookingRequest`, `create_booking` (`POST /bookings`) | FR-BKG-04, IF-IDP-01, IF-HIS-01 | ไม่ตรงทั้งหมด | `national_id` รับเข้าได้แต่ไม่ส่ง HIS และถูกเขียนลง log (F-02); ส่งกลับ queue_no; การส่งข้อความยังไม่มี |
| `backend/app/booking/router.py:cancel_booking` (`DELETE /bookings/{booking_id}`) | ไม่มี ID รองรับ | ไม่ตรง | การยกเลิกคิวอยู่ใน Out of scope (F-04) |
| `backend/app/booking/service.py:next_queue_no` | FR-BKG-04, Q-02 | ไม่ตรง | กำหนดรูปแบบ A001 และรีเซ็ตตามวัน ทั้งที่ Q-02 ยังเปิดอยู่ (F-03) |
| `backend/app/booking/service.py:create_booking` | FR-BKG-02, FR-BKG-03, FR-BKG-04 | บางส่วน | บันทึกและตัดที่นั่ง; capacity check ให้ผ่านเมื่อ remaining เท่ากับ 0; T-04/T-05 ยังพร้อมทำ จึงยังไม่ประเมินเป็นข้อค้นพบ |
| `backend/app/booking/service.py:cancel_booking` | ไม่มี ID รองรับ | ไม่ตรง | คืนที่นั่งและเปลี่ยนสถานะเพื่อยกเลิก ซึ่งอยู่ใน Out of scope (F-04) |
| `frontend/src/api/client.js:api.getSlots`, `api.createBooking` | FR-BKG-01, FR-BKG-03, FR-BKG-04 | บางส่วน | มี client สำหรับ GET/POST แต่ยังไม่มี UI เรียกใช้; POST ไม่ส่ง auth header |
| `frontend/src/App.jsx:App`, `frontend/src/main.jsx` | ไม่มี feature AC ที่ทำเสร็จ | ไม่ตรง/ยังไม่สมบูรณ์ | เป็นเพียงโครงเริ่มต้น ไม่ใช่หน้าจอเลือกเวลา ยืนยัน หรือผลการจอง |
| `backend/tests/test_AC_BKG_01.py:test_TC_BKG_01_1_booking_success`, `test_TC_BKG_01_2_booking_last_slot`, `test_TC_BKG_01_3_requires_authentication`, `test_AC_BKG_01` | AC-BKG-01 | บางส่วน | TC ตรวจฐานข้อมูลได้บางส่วน แต่ assert queue_no ที่ระบุว่ารอ Q-02 และไม่มีการตรวจการแสดงผลบนหน้าจอ; test เดิมตรวจแค่ status 201 (F-07) |
| `backend/tests/test_AC_BKG_05.py:test_AC_BKG_05` | AC-BKG-05, NFR-PERF-01 | ไม่ครบ | ตรวจ p95 จาก request เรียงลำดับ ไม่จำลองผู้ใช้พร้อมกัน 200 คน (F-06) |
| `backend/tests/test_T01_schema.py:test_T01_tables_created`, `test_T01_no_national_id` | CON-TECH-01, DOM-PDPA-01, IF-HIS-01 | บางส่วน | ตรวจ schema บน SQLite และการไม่มีคอลัมน์ national_id เท่านั้น |
| `backend/tests/conftest.py:client`, `make_slot` | ใช้เตรียม test | ไม่ใช่ production behavior | fixture override DB เป็น SQLite และกำหนด AUTH จำลอง |
| `frontend/src/__tests__/setup.test.jsx` | ไม่มี AC | ไม่เกี่ยวกับ AC | ตรวจเพียงโครงหน้าเปิดได้ ไม่ใช่ test ของ requirement |

## 3. ข้อค้นพบ
ชนิด: AC ไม่มี test / test อ่อน / โค้ดไม่มี FR / FR ไม่มี AC / เดา Q-xx / ละเมิด Constraint / ตัวเลขไม่ตรง spec / อ้าง ID ผิดเรื่อง

| F-ID | ชนิด | อยู่ที่ | ขัดกับ | รายละเอียด | ทีมตัดสิน |
|---|---|---|---|---|---|
| F-01 | ละเมิด Constraint | `backend/app/auth/idp.py:get_verified_hn` | IF-IDP-01 | การตรวจสอบเพียง prefix ที่เป็นค่าคงที่ทำให้ผู้ส่ง header รูปแบบเดียวกันแต่ไม่ได้รับการยืนยันจาก IDP ถูกยอมรับเป็น HN; ยังไม่มีการตรวจผลจากระบบยืนยันตัวตน | |
| F-02 | ละเมิด Constraint | `backend/app/booking/router.py:BookingRequest`, `create_booking` | IF-HIS-01 | API รับ national_id แต่ไม่ได้ค้น HIS ด้วยค่านั้น และเขียนค่านั้นลง application log โดยไม่จำเป็น; constraint ระบุให้ใช้ HIS แล้วอ้างอิงภายในด้วย HN | |
| F-03 | เดา Q-xx | `backend/app/booking/service.py:next_queue_no` | Q-02 | กำหนดเลขคิวเป็น A001 และนับใหม่รายวันทั้งที่ Q-02 ยังไม่ตอบ; ใช้รูปแบบตัวอย่างในคำถามเป็นพฤติกรรมจริง | |
| F-04 | โค้ดไม่มี FR | `backend/app/booking/router.py:cancel_booking`; `backend/app/booking/service.py:cancel_booking` | Out of scope | มี DELETE endpoint และ logic ยกเลิก/คืนที่นั่ง ทั้งที่การยกเลิกคิว (UC-02) ระบุชัดว่าอยู่ใน Out of scope | |
| F-05 | ตัวเลขไม่ตรง spec | `backend/app/slots/service.py:DAYS_AHEAD` | FR-BKG-01 | กำหนดช่วงค้นหา 14 วัน ขณะที่ FR-BKG-01 กำหนดให้แสดงช่วงภายใน 30 วันข้างหน้า | |
| F-06 | test อ่อน | `backend/tests/test_AC_BKG_05.py:test_AC_BKG_05` | AC-BKG-05, NFR-PERF-01 | วนเรียก 200 requests ทีละรายการ ไม่ได้จำลองผู้ใช้พร้อมกัน 200 คนตาม Given จึงไม่ยืนยัน p95 ภายใต้ concurrency ที่กำหนด | |
| F-07 | test อ่อน | `backend/tests/test_AC_BKG_01.py` | AC-BKG-01, Q-02 | test ใหม่ assert ว่ามี queue_no ทั้งที่ test case ระบุ (รอ Q-02) และไม่ได้ตรวจการแสดงเลขคิวใน UI; test เดิม `test_AC_BKG_01` ตรวจเพียง status 201 ไม่ตรวจผลบันทึก | |
| F-08 | ละเมิด Constraint | `backend/app/config.py:DATABASE_URL` | CON-TECH-01 | เมื่อไม่ได้ตั้ง DATABASE_URL ระบบเลือก SQLite โดยเงียบ แม้ constraint กำหนด PostgreSQL; ไม่มี guard ป้องกันการเริ่มระบบจริงด้วยค่าเริ่มต้นนี้ | |
| F-09 | FR ไม่มี AC | `specs/001-booking/spec.md` | FR-BKG-06 | FR-BKG-06 ไม่มี AC สำหรับการเปลี่ยนแพ็กเกจและตรวจช่วงว่างใหม่; AC-BKG-05 ตรวจเฉพาะประสิทธิภาพ ไม่ได้ตรวจ FR นี้ | |

## 4. แก้แล้ว
| F-ID | แก้อย่างไร | รู้ได้อย่างไร |
|---|---|---|
