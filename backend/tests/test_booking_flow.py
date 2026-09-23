from __future__ import annotations


def test_ac_bkg_01_creates_booking_and_reduces_remaining(client):
    slots_response = client.get('/slots?date_from=2026-09-23&package_code=basic')
    assert slots_response.status_code == 200
    slots = slots_response.json()
    chosen = next(slot for slot in slots if slot['remaining'] > 0)

    response = client.post('/bookings', json={'hn': 'HN-001', 'slot_id': chosen['id']})
    assert response.status_code == 200
    body = response.json()
    assert body['status'] == 'created'
    assert body['queue_no']
    assert body['slot']['remaining'] == 0


def test_ac_bkg_02_rejects_duplicate_same_day_booking(client):
    slots_response = client.get('/slots?date_from=2026-09-23&package_code=basic')
    slots = slots_response.json()
    chosen = next(slot for slot in slots if slot['remaining'] > 0)

    first = client.post('/bookings', json={'hn': 'HN-001', 'slot_id': chosen['id']})
    assert first.status_code == 200

    second = client.post('/bookings', json={'hn': 'HN-001', 'slot_id': chosen['id']})
    assert second.status_code == 409
    payload = second.json()['detail']
    assert payload['status'] == 'duplicate'
    assert payload['queue_no']


def test_ac_bkg_03_returns_alternatives_when_slot_is_full(client):
    slots_response = client.get('/slots?date_from=2026-09-23&package_code=basic')
    slots = slots_response.json()
    chosen = next(slot for slot in slots if slot['remaining'] > 0)

    client.post('/bookings', json={'hn': 'HN-001', 'slot_id': chosen['id']})
    response = client.post('/bookings', json={'hn': 'HN-002', 'slot_id': chosen['id']})
    assert response.status_code == 409
    payload = response.json()['detail']
    assert payload['status'] == 'full'
    assert len(payload['alternatives']) >= 1
    assert 'ช่วงเวลาเต็ม' in payload['message']


def test_ac_bkg_06_records_audit_log_for_access(client):
    client.get('/slots?date_from=2026-09-23&package_code=basic', headers={'X-Actor-Id': 'A-1', 'X-HN': 'HN-001'})
    response = client.get('/bookings/1', headers={'X-Actor-Id': 'A-1', 'X-HN': 'HN-001'})
    assert response.status_code == 404
