# app/api/scheduler.py
from fastapi import APIRouter
from app.agents.customer_agent import send_daily_summary_to_manager

router = APIRouter()

@router.post("/trigger-daily-summary", tags=["Scheduler"])
def trigger_daily_summary():
    """Günlük sipariş özetini yöneticiye WhatsApp ile gönderir."""
    result = send_daily_summary_to_manager()
    return {"status": "ok", "message": result}