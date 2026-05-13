"""
Twilio WhatsApp ile disari mesaj (patron onayi sonrasi musteri bildirimi).
.env: TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN, TWILIO_WHATSAPP_FROM=whatsapp:+1...
"""
from __future__ import annotations

import os
from typing import Optional


def twilio_outbound_configured() -> bool:
    return bool(
        os.getenv("TWILIO_ACCOUNT_SID")
        and os.getenv("TWILIO_AUTH_TOKEN")
        and os.getenv("TWILIO_WHATSAPP_FROM")
    )


def normalize_whatsapp_to(to: str) -> Optional[str]:
    t = (to or "").strip()
    if not t:
        return None
    if t.lower().startswith("whatsapp:"):
        return t
    if t.startswith("+"):
        return f"whatsapp:{t}"
    digits = "".join(c for c in t if c.isdigit())
    if len(digits) >= 10:
        return f"whatsapp:+{digits}"
    return None


def send_whatsapp(to: str, body: str) -> tuple[bool, Optional[str]]:
    if not twilio_outbound_configured():
        return False, "Twilio .env eksik (TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN, TWILIO_WHATSAPP_FROM)"
    dest = normalize_whatsapp_to(to)
    if not dest:
        return False, "Gecersiz alici (whatsapp:+... beklenir)"

    try:
        from twilio.rest import Client

        sid = os.environ["TWILIO_ACCOUNT_SID"]
        token = os.environ["TWILIO_AUTH_TOKEN"]
        from_wa = os.environ["TWILIO_WHATSAPP_FROM"]
        client = Client(sid, token)
        msg = client.messages.create(from_=from_wa, to=dest, body=body[:1600])
        return True, msg.sid
    except Exception as exc:
        return False, str(exc)
