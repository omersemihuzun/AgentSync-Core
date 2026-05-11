import sys
import os
from datetime import datetime, timedelta
import random

# Proje kök dizinini Python yoluna ekle
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.core.database import SessionLocal, engine
from app.models import models

# Veritabanı tablolarını oluştur (Henüz yoksa)
models.Base.metadata.create_all(bind=engine)

def create_mock_data():
    db = SessionLocal()
    
    # Mevcut verileri temizle
    db.query(models.Complaint).delete()
    db.query(models.ReturnItem).delete()
    db.query(models.Expense).delete()
    
    # --- 1. MÜŞTERİ SENARYOLARI (ReturnItems & Complaints) ---

    # Senaryo 1: Suistimalci Müşteri (Yüksek Risk)
    fraud_customer = "Hasan Kurnaz"
    # Geçmiş 3 iade
    for i in range(3):
        db.add(models.ReturnItem(
            order_id=f"ORD-FRAUD-{i}",
            customer_name=fraud_customer,
            reason="Kumaşta yırtık var.",
            ai_risk_score=0.9,
            ai_verdict="Manual Review",
            status="Rejected"
        ))
    
    # Şu anki şikayeti
    db.add(models.Complaint(
        customer_name=fraud_customer,
        message="Dün aldığım gömlek yırtık çıktı, acil paramı iade edin yoksa sizi şikayet ederim!!",
        urgency_level="Critical",
        sentiment="Negative",
        status="Pending"
    ))

    # Senaryo 2: Kural İhlali (Etiket Koparılmış)
    db.add(models.ReturnItem(
        order_id="ORD-TAG-404",
        customer_name="Ayşe Yılmaz",
        reason="Ürünü bir kez giydim ama bedeni uymadı, etiketi yok.",
        ai_risk_score=0.6,
        ai_verdict="Reject - Missing Tag",
        status="Pending"
    ))
    db.add(models.Complaint(
        customer_name="Ayşe Yılmaz",
        message="Ürün dar geldi iade etmek istiyorum, etiketi yanlışlıkla attım sorun olmaz umarım.",
        urgency_level="Normal",
        sentiment="Neutral",
        status="Pending"
    ))

    # Senaryo 3: Sorunsuz Haklı İade
    db.add(models.ReturnItem(
        order_id="ORD-SAFE-202",
        customer_name="Mehmet Dürüst",
        reason="Kargoda ezilmiş, cam fanus kırık geldi.",
        ai_risk_score=0.0,
        ai_verdict="Approve",
        status="Pending"
    ))
    db.add(models.Complaint(
        customer_name="Mehmet Dürüst",
        message="Merhaba, kargo paketini yeni açtım fakat içindeki ürün kırılmış. Fotoğrafları ekte gönderdim.",
        urgency_level="High",
        sentiment="Negative",
        status="Pending"
    ))

    # --- 2. GİDER (Expense) SENARYOLARI ---
    expenses = [
        ("Yurtiçi Kargo", 450.50),
        ("Kırtasiye Malzemeleri", 120.00),
        ("Aylık Sunucu Masrafı", 850.00),
        ("Depo Elektrik Faturası", 1200.00)
    ]

    for vendor, amount in expenses:
        db.add(models.Expense(
            vendor_name=vendor,
            amount=amount,
            date_recorded=datetime.now() - timedelta(days=random.randint(1, 10)),
            status="Approved"
        ))

    db.commit()
    db.close()
    print("Mock veriler basariyla veritabanina eklendi!")

if __name__ == "__main__":
    create_mock_data()
