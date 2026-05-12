from fastapi import FastAPI, Request
import uvicorn
from app.models import models
from app.core.database import engine

# Veritabanı tablolarını oluştur (Eğer yoksa)
models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="AgentSync AI API",
    description="Backend API for Multimodal KOBI Operations (WhatsApp & Web)",
    version="1.0.0"
)

@app.get("/")
def read_root():
    return {"status": "ok", "message": "AgentSync AI Backend is running."}

@app.post("/webhook/whatsapp")
async def whatsapp_webhook(request: Request):
    form_data = await request.form()

    message = form_data.get("Body", "")
    sender = form_data.get("From", "")
    media_url = form_data.get("MediaUrl0", None)
    media_type = form_data.get("MediaContentType0", None)

    print("Parsed WhatsApp message:", message)
    print("Sender:", sender)
    print("Media URL:", media_url)
    print("Media Type:", media_type)

    # TODO: CrewAI entegrasyonu burada yapılacak
    # agent_response = run_agent(
    #     message=message,
    #     sender=sender,
    #     media_url=media_url,
    #     media_type=media_type
    # )

    return {
        "status": "received",
        "sender": sender,
        "message": message,
        "media_url": media_url,
        "media_type": media_type,
        "note": "Message parsed successfully. Waiting for CrewAI agent integration."
    }

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)