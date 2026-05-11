from fastapi import FastAPI, Request
import uvicorn

app = FastAPI(
    title="AgentSync AI API",
    description="Backend API for Multimodal KOBI Operations (WhatsApp & Web)",
    version="1.0.0"
)

@app.get("/")
def read_root():
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
