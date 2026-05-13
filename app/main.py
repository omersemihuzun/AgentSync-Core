import os
import re
import uvicorn
from fastapi import FastAPI, Request, Depends
from fastapi.responses import FileResponse, PlainTextResponse
from fastapi.staticfiles import StaticFiles
from sqlalchemy import text
from sqlalchemy.orm import Session

from app.agents.customer_agent import run_agent
from app.api.endpoints.v1 import router as api_router
from app.core.database import engine, get_db
from app.models import models
from app.services.whatsapp_service import parse_twilio_message


def _want_twilio_reply(request: Request) -> bool:
    if request.query_params.get("format") == "json":
        return False
    return bool(request.headers.get("X-Twilio-Signature"))


def _twiml_body(text: str) -> PlainTextResponse:
    from twilio.twiml.messaging_response import MessagingResponse

    tw = MessagingResponse()
    body = (text or ".").strip()[:1500] or "."
    tw.message(body)
    return PlainTextResponse(str(tw), media_type="application/xml")


# Veritabanı tablolarını oluştur (Bağlantı yoksa hata verme, devam et)
try:
    models.Base.metadata.create_all(bind=engine)
except Exception as e:
    print(f"[WARN] DB bağlantısı kurulamadı (okul ağı?): {e}")
    print("[INFO] API static dosyaları serve etmeye devam edecek.")


app = FastAPI(
    title="AgentSync AI API",
    description="KOBİ operasyonlarını otomatikleştiren çoklu ajan yapay zeka sistemi",
    version="1.0.0"
)

# API router'ı bağla
app.include_router(api_router)

# Static dosyaları serve et (Stitch SPA)
_static_dir = os.path.join(os.path.dirname(__file__), "..", "app", "static")
if os.path.isdir(_static_dir):
    app.mount("/static", StaticFiles(directory=_static_dir), name="static")

@app.get("/health", tags=["Sistem"])
def health(db: Session = Depends(get_db)):
    """README / operasyon: API ve veritabanı canlı mı kontrolü."""
    try:
        db.execute(text("SELECT 1"))
        return {"status": "ok", "database": "connected"}
    except Exception as exc:
        return {"status": "degraded", "database": "error", "detail": str(exc)}


@app.get("/")
def read_root():
    index = os.path.join(_static_dir, "index.html")
    if os.path.isfile(index):
        return FileResponse(index)
    return {"status": "ok", "message": "AgentSync AI Backend is running."}

# WhatsApp Webhook - Gerçek zamanlı sipariş sorgulama simülasyonu
@app.post("/webhook/whatsapp", tags=["WhatsApp Entegrasyonu"])
async def whatsapp_webhook(request: Request, db: Session = Depends(get_db)):
    """
    Twilio veya benzeri bir servisten gelen WhatsApp mesajlarını karşılar.
    Örnek: 'Siparişim nerede? ORD-2024-001'
    """
    try:
        form_data = await request.form()
        fd = {k: v for k, v in form_data.multi_items()}
        parsed = parse_twilio_message(fd)
        incoming_msg = (parsed.get("content") or parsed.get("body") or "").strip()
        from_number = parsed.get("sender") or fd.get("From", "")

        # Sipariş kodu varsa önce mevcut DB akışı (develop davranışı korunur)
        order_match = re.search(r"ORD-\d{4}-\d{3}", incoming_msg.upper())

        if order_match:
            order_code = order_match.group(0)
            order = db.query(models.Order).filter(models.Order.order_code == order_code).first()

            if order:
                response_msg = f"Merhaba! {order_code} nolu siparişinizin durumu: *{order.status}*.\n"
                if order.cargo_tracking_code:
                    response_msg += f"Kargo: {order.cargo_company} - Takip No: {order.cargo_tracking_code}"
                if _want_twilio_reply(request):
                    return _twiml_body(response_msg)
                return {"message": response_msg}
            msg = f"Üzgünüm, {order_code} kodlu bir sipariş bulamadım."
            if _want_twilio_reply(request):
                return _twiml_body(msg)
            return {"message": msg}

        # Sipariş kodu yoksa müşteri ajanı (ekip: run_agent)
        agent_response = run_agent(message=incoming_msg, sender=from_number, db=db)
        reply_lines = [agent_response.get("response") or ""]
        if agent_response.get("return_item_id"):
            reply_lines.append(f"Kayit no: {agent_response['return_item_id']}")
        if agent_response.get("complaint_id"):
            reply_lines.append(f"Sikayet no: {agent_response['complaint_id']}")
        twilio_text = "\n".join(x for x in reply_lines if x).strip()

        payload = {
            "message": agent_response.get("response", ""),
            "priority": agent_response.get("priority"),
            "sender": from_number,
            "parsed_type": parsed.get("type"),
            "media_url": parsed.get("media_url"),
            "complaint_id": agent_response.get("complaint_id"),
            "return_item_id": agent_response.get("return_item_id"),
            "urgency_level": agent_response.get("urgency_level"),
            "hitl": agent_response.get("hitl"),
            "db_note": agent_response.get("db_note"),
        }

        # Demo / video: WhatsApp iadesi -> otomatik AI zinciri (+ istege bagli otomatik onay)
        if os.getenv("AGENTSYNC_DEMO_CHAIN", "").lower() in ("1", "true", "yes"):
            rid = agent_response.get("return_item_id")
            if rid:
                try:
                    from app.services.return_pipeline import analyze_return_item_db, maybe_auto_approve_for_demo

                    ai_out = analyze_return_item_db(db, int(rid), allow_fallback=True)
                    payload["ai_pipeline"] = ai_out
                    item = db.query(models.ReturnItem).filter(models.ReturnItem.id == int(rid)).first()
                    if item:
                        auto = maybe_auto_approve_for_demo(db, item)
                        if auto:
                            payload["demo_auto_approve"] = auto
                            from app.services.twilio_notify import send_whatsapp

                            to_addr = (item.customer_name or "").strip()
                            if to_addr:
                                send_whatsapp(
                                    to_addr,
                                    "Iade talebiniz degerlendirildi: ONAY (demo). Detaylar icin tesekkurler.",
                                )
                            extra = "\nAI: " + (item.ai_verdict or "") + " (risk " + str(item.ai_risk_score or 0) + ")"
                            if payload.get("message"):
                                payload["message"] = str(payload["message"]) + extra
                            twilio_text = twilio_text + extra
                except Exception as exc:
                    payload["ai_pipeline_error"] = str(exc)[:400]

        if _want_twilio_reply(request):
            return _twiml_body(twilio_text)
        return {k: v for k, v in payload.items() if v is not None}
    except Exception as e:
        if _want_twilio_reply(request):
            return _twiml_body(f"Gecici hata. Lutfen tekrar deneyin. ({e})")
        return {"error": str(e)}

if __name__ == "__main__":
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
