from fastapi import FastAPI, Request, Depends
from sqlalchemy.orm import Session
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import uvicorn
import os
from app.models import models
from app.core.database import engine, get_db
from app.api.endpoints.v1 import router as api_router

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
        incoming_msg = form_data.get("Body", "").strip()
        from_number = form_data.get("From", "")
        
        # Basit Regex/NLP Simülasyonu: Sipariş kodu ayıklama
        import re
        order_match = re.search(r"ORD-\d{4}-\d{3}", incoming_msg.upper())
        
        if order_match:
            order_code = order_match.group(0)
            order = db.query(models.Order).filter(models.Order.order_code == order_code).first()
            
            if order:
                response_msg = f"Merhaba! {order_code} nolu siparişinizin durumu: *{order.status}*.\n"
                if order.cargo_tracking_code:
                    response_msg += f"Kargo: {order.cargo_company} - Takip No: {order.cargo_tracking_code}"
                return {"message": response_msg}
            else:
                return {"message": f"Üzgünüm, {order_code} kodlu bir sipariş bulamadım."}
        
        return {"message": "Merhaba! Sipariş durumunuzu öğrenmek için 'Siparişim nerede? ORD-XXXX-XXX' şeklinde yazabilirsiniz."}
    except Exception as e:
        return {"error": str(e)}

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
