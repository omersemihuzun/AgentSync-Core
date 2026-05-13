"""
AgentSync AI — REST API Endpoint'leri
Tüm tablolar için GET/POST/PATCH desteği.
"""
from fastapi import APIRouter, Depends, HTTPException
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session
from typing import Optional
from app.core.database import SessionLocal
from app.models.models import Complaint, Expense, ReturnItem, Product, Order, StockAlert

router = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# ── Şikayetler ──────────────────────────────────────────────────────────────

@router.get("/complaints", tags=["Şikayetler"])
def list_complaints(status: Optional[str] = None, db: Session = Depends(get_db)):
    """Tüm şikayetleri listeler. Opsiyonel: ?status=Pending"""
    q = db.query(Complaint)
    if status:
        q = q.filter(Complaint.status == status)
    return jsonable_encoder(q.order_by(Complaint.created_at.desc()).all())


@router.patch("/complaints/{complaint_id}/status", tags=["Şikayetler"])
def update_complaint_status(complaint_id: int, status: str, assigned_to: Optional[str] = None, db: Session = Depends(get_db)):
    """Şikayet durumunu günceller."""
    c = db.query(Complaint).filter(Complaint.id == complaint_id).first()
    if not c:
        raise HTTPException(status_code=404, detail="Şikayet bulunamadı")
    c.status = status
    if assigned_to:
        c.assigned_to = assigned_to
    db.commit()
    return {"success": True, "id": complaint_id, "new_status": status}


# ── İade Talepleri ──────────────────────────────────────────────────────────

@router.get("/return-items", tags=["İade Talepleri"])
def list_returns(db: Session = Depends(get_db)):
    """Tüm iade taleplerini AI kararıyla birlikte listeler."""
    return jsonable_encoder(db.query(ReturnItem).order_by(ReturnItem.created_at.desc()).all())


@router.post("/return-items/{return_id}/ai-analyze", tags=["İade Talepleri"])
def ai_analyze_return(return_id: int, db: Session = Depends(get_db)):
    """Belirli bir iade talebini CrewAI ajanlarıyla analiz eder ve sonucu DB'ye yazar."""
    from app.services.return_pipeline import analyze_return_item_db

    out = analyze_return_item_db(db, return_id, allow_fallback=True)
    if not out.get("success"):
        raise HTTPException(status_code=404, detail=out.get("error", "Bulunamadı"))
    return out


@router.patch("/return-items/{return_id}/decision", tags=["İade Talepleri"])
def human_decision(return_id: int, status: str, db: Session = Depends(get_db)):
    """Patron manuel olarak iade kararını onaylar/reddeder (Human-in-the-Loop)."""
    from app.services.twilio_notify import send_whatsapp

    item = db.query(ReturnItem).filter(ReturnItem.id == return_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="İade talebi bulunamadı")
    if status not in ["Approved", "Rejected"]:
        raise HTTPException(status_code=400, detail="Geçersiz durum. 'Approved' veya 'Rejected' olmalı.")
    item.status = status
    db.commit()

    whatsapp_notify = None
    to_addr = (item.customer_name or "").strip()
    if to_addr and ("whatsapp:" in to_addr.lower() or to_addr.startswith("+")):
        if status == "Approved":
            body = "Merhaba, iade talebiniz onaylandi. Kargo/geri odeme adimlari icin kisa surede bilgilendirileceksiniz."
        else:
            body = "Merhaba, iade talebiniz uygun gorulmedi. Detay icin musteri hizmetlerimizle iletisime gecebilirsiniz."
        ok, detail = send_whatsapp(to_addr, body)
        whatsapp_notify = {"attempted": True, "sent": ok, "detail": detail}

    out = {"success": True, "id": return_id, "final_status": status}
    if whatsapp_notify is not None:
        out["whatsapp_notify"] = whatsapp_notify
    return out


# ── Ürünler & Stok ──────────────────────────────────────────────────────────

@router.get("/products", tags=["Ürün & Stok"])
def list_products(low_stock_only: bool = False, db: Session = Depends(get_db)):
    """Ürün listesi. ?low_stock_only=true ile sadece kritik stokları gösterir."""
    q = db.query(Product)
    if low_stock_only:
        q = q.filter(Product.stock_quantity < Product.low_stock_threshold)
    return q.all()


@router.get("/stock-alerts", tags=["Ürün & Stok"])
def list_stock_alerts(db: Session = Depends(get_db)):
    """AI tarafından üretilen açık stok uyarılarını listeler."""
    return db.query(StockAlert).filter(StockAlert.status == "Open").all()


# ── Siparişler ──────────────────────────────────────────────────────────────

@router.get("/orders", tags=["Siparişler"])
def list_orders(status: Optional[str] = None, customer_name: Optional[str] = None, db: Session = Depends(get_db)):
    """Siparişleri listeler. Filtreleme: ?status=Pending veya ?customer_name=Ahmet"""
    q = db.query(Order)
    if status:
        q = q.filter(Order.status == status)
    if customer_name:
        q = q.filter(Order.customer_name.ilike(f"%{customer_name}%"))
    return q.order_by(Order.created_at.desc()).all()


@router.get("/orders/{order_code}", tags=["Siparişler"])
def get_order_by_code(order_code: str, db: Session = Depends(get_db)):
    """WhatsApp entegrasyonu için: 'siparişim nerede?' sorgusunu karşılar."""
    order = db.query(Order).filter(Order.order_code == order_code).first()
    if not order:
        raise HTTPException(status_code=404, detail=f"'{order_code}' kodlu sipariş bulunamadı.")
    return order


@router.patch("/orders/{order_id}/status", tags=["Siparişler"])
def update_order_status(order_id: int, status: str, cargo_tracking_code: Optional[str] = None, db: Session = Depends(get_db)):
    """Sipariş durumunu günceller (kargo kodu opsiyonel)."""
    order = db.query(Order).filter(Order.id == order_id).first()
    if not order:
        raise HTTPException(status_code=404, detail="Sipariş bulunamadı")
    order.status = status
    if cargo_tracking_code:
        order.cargo_tracking_code = cargo_tracking_code
    db.commit()
    return {"success": True, "order_code": order.order_code, "new_status": status}


# ── Masraflar ───────────────────────────────────────────────────────────────

@router.get("/expenses", tags=["Masraflar"])
def list_expenses(db: Session = Depends(get_db)):
    return db.query(Expense).order_by(Expense.date_recorded.desc()).all()
