"""
İade talebi: CrewAI analizi + (demo) API yoksa kural tabanli yedek karar.
"""
from __future__ import annotations

import os
from typing import Any, Optional

from sqlalchemy.orm import Session

from app.models.models import ReturnItem


def _verdict_from_text(result_str: str) -> tuple[str, float]:
    u = result_str.upper()
    if "APPROVE" in u:
        return "Approve", 0.1
    if "REJECT" in u:
        return "Reject", 0.85
    if "MANUAL" in u:
        return "Manual Review", 0.6
    return "Manual Review", 0.5


def _fallback_verdict(reason: str) -> tuple[str, float]:
    """GEMINI / Crew calismazsa demo videosu icin mantikli varsayilan."""
    t = (reason or "").lower()
    if any(w in t for w in ("renk", "farklı", "farkli", "beden", "yanlış", "yanlis", "kargo hasar", "hasarlı", "hasarli", "defolu", "kırık", "kirik")):
        return "Approve", 0.12
    if "etiket" in t and ("kop" in t or "yok" in t or "çıkar" in t or "cikar" in t):
        return "Reject", 0.88
    return "Manual Review", 0.55


def analyze_return_item_db(db: Session, return_id: int, *, allow_fallback: bool = True) -> dict[str, Any]:
    item = db.query(ReturnItem).filter(ReturnItem.id == return_id).first()
    if not item:
        return {"success": False, "error": "İade talebi bulunamadı"}

    verdict: str
    score: float
    result_str: str
    used_fallback = False

    try:
        from app.agents.crew import AgentSyncCrew

        crew = AgentSyncCrew(
            customer_name=item.customer_name or "Müşteri",
            image_description=item.reason or "Açıklama yok",
        )
        result = crew.run()
        result_str = str(result)
        verdict, score = _verdict_from_text(result_str)
    except Exception as exc:
        if not allow_fallback or os.getenv("AGENTSYNC_DEMO_FALLBACK_AI", "1").lower() not in ("1", "true", "yes"):
            raise
        used_fallback = True
        result_str = f"[DEMO_FALLBACK] CrewAI calismadi ({str(exc)[:200]}). Metin tabanli on degerlendirme."
        verdict, score = _fallback_verdict(item.reason or "")

    item.ai_verdict = verdict
    item.ai_risk_score = score
    item.ai_reasoning = result_str[:1000]
    db.commit()
    db.refresh(item)

    out: dict[str, Any] = {
        "success": True,
        "return_id": return_id,
        "verdict": verdict,
        "risk_score": score,
        "reasoning": result_str,
        "demo_fallback": used_fallback,
    }
    return out


def maybe_auto_approve_for_demo(db: Session, item: ReturnItem) -> Optional[dict[str, Any]]:
    """
    AGENTSYNC_DEMO_AUTO_APPROVE=1 ve AI Approve + dusuk risk ise status Approved yapar.
    """
    if os.getenv("AGENTSYNC_DEMO_AUTO_APPROVE", "").lower() not in ("1", "true", "yes"):
        return None
    if (item.ai_verdict or "") != "Approve":
        return None
    if (item.ai_risk_score or 1.0) > 0.35:
        return None
    item.status = "Approved"
    db.commit()
    return {"demo_auto_approved": True, "final_status": "Approved"}
