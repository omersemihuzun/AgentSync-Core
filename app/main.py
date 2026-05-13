from fastapi import FastAPI, Request
import uvicorn
from fastapi import Response
from twilio.twiml.messaging_response import MessagingResponse
from app.models import models
from app.core.database import engine
from app.agents.customer_agent import run_agent
from app.api.scheduler import router as scheduler_router 

# Veritabanı tablolarını oluştur (Eğer yoksa)
models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="AgentSync AI API",
    description="Backend API for Multimodal KOBI Operations (WhatsApp & Web)",
    version="1.0.0"
)

app.include_router(scheduler_router)

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
    
    # Mesaj ve gönderen bilgileri
    incoming_msg = form_data.get('Body', '')
    sender = form_data.get('From', '')
    
    # Medya (Fotoğraf) bilgisi (Senin vizyon senaryon için çok kritik!)
    media_url = form_data.get('MediaUrl0', None)

    # Terminal logları (Sistemi izleyebilmen için)
    print("Müşteriden Gelen Mesaj:", incoming_msg)
    print("Müşteri Numarası:", sender)
    if media_url: print("Görsel URL:", media_url)

    # Ajanımızı (Yapay Zekayı) çalıştırıyoruz
    agent_response = run_agent(incoming_msg, sender, media_url)

    # TWILIO'NUN İSTEDİĞİ XML FORMATINA ÇEVİRME
    twiml = MessagingResponse()
    twiml.message(agent_response)
    
    return Response(content=str(twiml), media_type="application/xml")

if __name__ == "__main__":
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )