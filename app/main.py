from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import uvicorn
import os
from app.models import models
from app.core.database import engine

# Veritabanı tablolarını oluştur (Bağlantı yoksa hata verme, devam et)
try:
    models.Base.metadata.create_all(bind=engine)
except Exception as e:
    print(f"[WARN] DB bağlantısı kurulamadı (okul ağı?): {e}")
    print("[INFO] API static dosyaları serve etmeye devam edecek.")


app = FastAPI(
    title="AgentSync AI API",
    description="Backend API for Multimodal KOBI Operations (WhatsApp & Web)",
    version="1.0.0"
)

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

# Placeholder for Twilio Webhook
@app.post("/webhook/whatsapp")
async def whatsapp_webhook(request: Request):
    # This endpoint will receive messages from WhatsApp via Twilio
    # It will extract text/audio/images and pass them to CrewAI agents
    form_data = await request.form()
    # TODO: Process the incoming message
    return {"status": "received"}

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
