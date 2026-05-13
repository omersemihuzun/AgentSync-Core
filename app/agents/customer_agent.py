"""
WhatsApp / müşteri mesajları — README hedefiyle uyumlu operasyon katmanı:
- Şikayet → `complaints` tablosu + aciliyet
- İade niyeti → `return_items` (CrewAI analizi /return-items/{id}/ai-analyze ile devam)
- Genel mesaj → kritik stok özeti (KOBİ farkındalığı)
"""
from __future__ import annotations

from typing import Any, Optional

from sqlalchemy.orm import Session

from app.models.models import Complaint, Product, ReturnItem


def _wa_identity(sender: str) -> tuple[str, str]:
    """
    Twilio icin tam adres (whatsapp:+E164) ve panelde kisa etiket.
    """
    s = (sender or "").strip()
    if not s:
        return "", "WhatsApp Musteri"
    low = s.lower()
    if low.startswith("whatsapp:"):
        return s, s.split(":", 1)[-1][:32]
    if s.startswith("+"):
        return f"whatsapp:{s}", s[1:20]
    return s, s[:48]


def _low_stock_lines(db: Session, limit: int = 5) -> list[str]:
    rows = (
        db.query(Product)
        .filter(Product.stock_quantity < Product.low_stock_threshold)
        .order_by(Product.stock_quantity.asc())
        .limit(limit)
        .all()
    )
    out: list[str] = []
    for p in rows:
        out.append(f"{p.name} (SKU {p.sku}): stok {p.stock_quantity}, eşik {p.low_stock_threshold}")
    return out


def _complaint_urgency(text: str) -> str:
    t = text.lower()
    if any(x in t for x in ("kritik", "acil", "mahkeme", "dolandır")):
        return "Critical"
    if any(x in t for x in ("şikayet", "gecikme", "kırık", "bozuk", "iade", "kötü")):
        return "High"
    if any(x in t for x in ("soru", "bilgi", "nerede")):
        return "Normal"
    return "Normal"


def run_agent(message: str, sender: str, db: Optional[Session] = None) -> dict[str, Any]:
    """
    WhatsApp mesajını işler; varsa DB'ye yazar (README: şikayet sınıflama, iade kaydı, stok farkındalığı).
    """
    text = (message or "").strip()
    sender_key = (sender or "").strip()
    wa_to, short_label = _wa_identity(sender_key)
    db_contact = wa_to or short_label
    out: dict[str, Any] = {"priority": "LOW", "response": "Mesajınız alındı.", "hitl": None}

    if not text:
        out["response"] = "Boş mesaj alındı. Sipariş için örnek: ORD-2024-001"
        return out

    low: list[str] = []
    if db is not None:
        try:
            low = _low_stock_lines(db)
        except Exception:
            db.rollback()
            low = []

    tl = text.lower()

    # ── Şikayet ─────────────────────────────────────────────────────────────
    if any(k in tl for k in ("şikayet", "sikayet", "şikâyet", "memnun değil", "memnuniyetsiz")):
        out["priority"] = "HIGH"
        out["response"] = "Şikayetiniz alındı. Öncelikli olarak inceleniyor."
        if db is not None:
            try:
                urg = _complaint_urgency(text)
                c = Complaint(
                    customer_name=db_contact,
                    message=text,
                    urgency_level=urg,
                    sentiment="Negative",
                    status="Pending",
                )
                db.add(c)
                db.commit()
                db.refresh(c)
                out["complaint_id"] = c.id
                out["urgency_level"] = urg
                if urg in ("High", "Critical"):
                    out["hitl"] = "Yüksek öncelik — patron / operasyon onayı önerilir."
            except Exception as exc:
                db.rollback()
                out["db_note"] = f"Kayıt yazılamadı: {exc}"
        return out

    # ── İade niyeti ─────────────────────────────────────────────────────────
    if "iade" in tl:
        out["priority"] = "MEDIUM"
        out["response"] = "İade süreciniz başlatıldı."
        if db is not None:
            try:
                ri = ReturnItem(
                    order_id="WHATSAPP-UNKNOWN",
                    customer_name=db_contact,
                    reason=text,
                    status="Pending",
                )
                db.add(ri)
                db.commit()
                db.refresh(ri)
                out["return_item_id"] = ri.id
                out["response"] = (
                    f"İade talebiniz kayda alındı (ID: {ri.id}). "
                    f"AI analizi için: POST /return-items/{ri.id}/ai-analyze"
                )
                out["hitl"] = "CrewAI (Vision->Policy->Fraud->Decision) analizi panel veya API uzerinden tetiklenir."
            except Exception as exc:
                db.rollback()
                out["db_note"] = f"Kayıt yazılamadı: {exc}"
        return out

    # ── Stok / operasyon farkındalığı ───────────────────────────────────────
    if any(k in tl for k in ("stok", "tükendi", "kalmadı", "ürün")) and low:
        out["priority"] = "LOW"
        out["response"] = "Stok durumu (kritik ürünler): " + " | ".join(low[:3])
        out["low_stock_skus"] = len(low)
        return out

    # ── Varsayılan: kritik stok varsa kısa hatırlatma ───────────────────────
    if low:
        out["response"] = (
            "Mesajınız alındı. "
            + f"Not: {len(low)} üründe kritik stok altı var; panelden stok uyarılarına bakın."
        )
        out["low_stock_preview"] = low[:3]

    return out
