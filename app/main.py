from fastapi import FastAPI, Request
import uvicorn

from app.models import models
from app.core.database import engine
from app.agents.customer_agent import run_agent

# Veritabanı tablolarını oluştur (Eğer yoksa)
models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="AgentSync AI API",
    description="Backend API for Multimodal KOBI Operations (WhatsApp & Web)",
    version="1.0.0"
)

@app.get("/")
def read_root():
    return {
        "status": "ok",
        "message": "AgentSync AI Backend is running."
    }

@app.post("/webhook/whatsapp")
async def whatsapp_webhook(request: Request):

    # Twilio form verisini al
    form_data = await request.form()

    # Mesaj bilgileri
    message = form_data.get("Body", "")
    sender = form_data.get("From", "")

    # Medya bilgileri
    media_url = form_data.get("MediaUrl0", None)
    media_type = form_data.get("MediaContentType0", None)

    # Terminal logları
    print("Parsed WhatsApp message:", message)
    print("Sender:", sender)
    print("Media URL:", media_url)
    print("Media Type:", media_type)

    # AI Agent çağır
    agent_response = run_agent(
        message=message,
        sender=sender
    )

    # API response
    return {
        "status": "received",
        "sender": sender,
        "message": message,
        "media_url": media_url,
        "media_type": media_type,
        "agent_response": agent_response
    }

if __name__ == "__main__":
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )