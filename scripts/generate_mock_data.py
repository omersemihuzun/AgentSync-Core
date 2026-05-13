import sys
import os
from datetime import datetime, timedelta
import random

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from app.core.database import SessionLocal, engine
from app.models import models

models.Base.metadata.create_all(bind=engine)

def create_mock_data():
    db = SessionLocal()
    
    # Temizlik
    db.query(models.Complaint).delete()
    db.query(models.ReturnItem).delete()
    db.query(models.Expense).delete()
    db.query(models.Order).delete()     # YENİ
    db.query(models.Product).delete()   # YENİ
    
    
    fraud_customer = "Hasan Kurnaz"
    for i in range(3):
        db.add(models.ReturnItem(order_id=f"ORD-FRAUD-{i}", customer_name=fraud_customer, reason="Kumaşta yırtık var.", ai_risk_score=0.9, ai_verdict="Manual Review", status="Rejected"))
    db.add(models.Complaint(customer_name=fraud_customer, message="Acil paramı iade edin!!", urgency_level="Critical", sentiment="Negative", status="Pending"))
    
    db.add(models.ReturnItem(order_id="ORD-TAG-404", customer_name="Ayşe Yılmaz", reason="Etiketi yok.", ai_risk_score=0.6, ai_verdict="Reject", status="Pending"))
    db.add(models.Complaint(customer_name="Mehmet Dürüst", message="Kırık geldi.", urgency_level="High", sentiment="Negative", status="Pending"))

    
    orders = [
        models.Order(order_code="ORD-101", customer_name="Ali Veli", status="Kargoda", cargo_company="Yurtiçi Kargo", tracking_no="1A2B3C"),
        models.Order(order_code="ORD-102", customer_name="Ayşe Yılmaz", status="Hazırlanıyor", cargo_company=None, tracking_no=None),
        models.Order(order_code="ORD-103", customer_name="Mehmet Demir", status="Teslim Edildi", cargo_company="Aras Kargo", tracking_no="4D5E6F"),
        models.Order(order_code="ORD-104", customer_name="Fatma Kaya", status="Kargoda", cargo_company="MNG Kargo", tracking_no="7G8H9I"),
        models.Order(order_code="ORD-105", customer_name="Emre Çelik", status="Hazırlanıyor", cargo_company=None, tracking_no=None),
        models.Order(order_code="ORD-106", customer_name="Zeynep Arslan", status="Teslim Edildi", cargo_company="PTT Kargo", tracking_no="J1K2L3"),
        models.Order(order_code="ORD-107", customer_name="Burak Şahin", status="Kargoda", cargo_company="Sürat Kargo", tracking_no="M4N5O6"),
    ]
    db.bulk_save_objects(orders)

    
    products = [
        models.Product(name="Siyah Tişört", stock=5, critical_limit=10, order_amount=50), # KRİTİK ÜRÜN
        models.Product(name="Mavi Kot", stock=3, critical_limit=15, order_amount=30),     # KRİTİK ÜRÜN
        models.Product(name="Güneş Gözlüğü", stock=45, critical_limit=10, order_amount=20) # GÜVENLİ ÜRÜN
    ]
    db.bulk_save_objects(products)

    db.commit()
    db.close()
    print("Sipariş ve Stok verileri dahil tüm Mock veriler başarıyla eklendi!")

if __name__ == "__main__":
    create_mock_data()