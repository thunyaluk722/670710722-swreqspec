# Test cases: AC-BKG-01
# TC-BKG-01-1: ทางปกติ
# TC-BKG-01-2: ขอบ
# TC-BKG-01-3: ทางผิด
from app.db.models import Booking, Slot
from tests.conftest import AUTH


def test_TC_BKG_01_1_booking_success(client, make_slot, db):
    # Given: ผู้ใช้ยืนยันตัวตนแล้ว และช่วง 09.00 น. มีที่นั่งว่าง 1 ที่
    slot = make_slot(start="09:00", remaining=1)

    # When: ผู้ใช้ยืนยันการจองช่วง 09.00 น.
    res = client.post("/bookings", json={"slot_id": slot.id}, headers=AUTH)

    # Then: บันทึกสำเร็จ; แสดงหมายเลขคิว (รอ Q-02); ที่นั่งว่างของช่วงนั้นเป็น 0
    assert res.status_code == 201
    data = res.json()
    assert "queue_no" in data
    assert isinstance(data["queue_no"], str) and data["queue_no"]
    assert db.get(Slot, slot.id).remaining == 0
    assert db.query(Booking).count() == 1


def test_TC_BKG_01_2_booking_last_slot(client, make_slot, db):
    # Given: ผู้ใช้ยืนยันตัวตนแล้ว และช่วง 09.00 น. เหลือที่นั่งว่างอย่างตรง 1 ที่
    slot = make_slot(start="09:00", remaining=1)

    # When: ผู้ใช้ยืนยันการจองช่วง 09.00 น. เป็นการจองครั้งสุดท้ายก่อนช่วงเต็ม
    res = client.post("/bookings", json={"slot_id": slot.id}, headers=AUTH)

    # Then: บันทึกสำเร็จ; แสดงหมายเลขคิว (รอ Q-02); ที่นั่งว่างของช่วงนั้นลดจาก 1 เป็น 0 และไม่ติดลบ
    assert res.status_code == 201
    assert "queue_no" in res.json()
    slot_after = db.get(Slot, slot.id)
    assert slot_after.remaining == 0
    assert slot_after.remaining >= 0
    assert db.query(Booking).count() == 1


def test_TC_BKG_01_3_requires_authentication(client, make_slot, db):
    # Given: ผู้ใช้ยังไม่ได้ยืนยันตัวตน และ/หรือระบบยังไม่ได้รับผลยืนยันตัวตนจากระบบยืนยันตัวตน
    slot = make_slot(start="09:00", remaining=1)

    # When: ผู้ใช้พยายามยืนยันการจองช่วง 09.00 น.
    res = client.post("/bookings", json={"slot_id": slot.id})

    # Then: ปฏิเสธการจอง; ไม่บันทึกข้อมูลการจอง; ไม่แสดงหมายเลขคิว; ที่นั่งว่างยังคงเหมือนเดิม
    assert res.status_code == 401
    assert res.json()["detail"] == "ยังไม่ได้ยืนยันตัวตน"
    assert db.query(Booking).count() == 0
    assert db.get(Slot, slot.id).remaining == 1


def test_AC_BKG_01(client, make_slot):
    """AC-BKG-01: ยืนยันตัวตนแล้ว และช่วง 09.00 น. มีที่นั่งว่าง จองแล้วต้องสำเร็จ"""
    slot = make_slot(start="09:00", remaining=1)

    res = client.post("/bookings", json={"slot_id": slot.id}, headers=AUTH)

    assert res.status_code == 201
