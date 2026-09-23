from __future__ import annotations

from datetime import datetime, timedelta


class NotificationQueue:
    """Simple async queue used to retry failed SMS/LINE delivery."""

    def __init__(self):
        self.items = []

    def enqueue(self, booking_id: int, hn: str, attempts: int = 0):
        item = {
            'booking_id': booking_id,
            'hn': hn,
            'attempts': attempts,
            'queued_at': datetime.utcnow(),
            'retry_at': datetime.utcnow() + timedelta(minutes=5),
        }
        self.items.append(item)
        return item

    def get_pending(self, now: datetime | None = None):
        now = now or datetime.utcnow()
        return [item for item in self.items if item['retry_at'] <= now]


notification_queue = NotificationQueue()


def queue_notification(booking_id: int, hn: str):
    """FR-BKG-05 / IF-NOT-01: enqueue retry items without blocking the booking flow."""
    return notification_queue.enqueue(booking_id, hn)
