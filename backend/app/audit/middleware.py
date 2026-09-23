from __future__ import annotations

import json
from datetime import datetime

from fastapi import Request

from app.db.models import AuditLog
from app.db.session import SessionLocal


async def audit_middleware(request: Request, call_next):
    """DOM-PDPA-01: write audit entries for booking-related access."""
    body = await request.body()
    if body:
        request._body = body

    response = await call_next(request)

    if request.url.path.startswith('/bookings') or request.url.path.startswith('/slots'):
        hn = request.headers.get('X-HN')
        if request.method == 'POST' and request.url.path == '/bookings' and body:
            try:
                payload = json.loads(body)
                hn = payload.get('hn', hn)
            except json.JSONDecodeError:
                hn = hn
        if hn:
            db = SessionLocal()
            try:
                db.add(
                    AuditLog(
                        actor_id=request.headers.get('X-Actor-Id', 'system'),
                        action=f'{request.method} {request.url.path}',
                        hn=hn,
                        accessed_at=datetime.utcnow(),
                    )
                )
                db.commit()
            finally:
                db.close()
    return response
