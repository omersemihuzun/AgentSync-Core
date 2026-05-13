"""
AgentSync AI — Mock Data Script (Genişletilmiş)
Çalıştır: python scripts/generate_mock_data.py
"""
import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass  # .env yoksa veya python-dotenv kurulu degilse varsayilan DATABASE_URL kullanilir

from app.core.database import SessionLocal, engine
from app.models.models import Base, Complaint, Expense, ReturnItem, Product, Order, StockAlert
from app.core.brand_config import BOUTIQUE_NAME, WHATSAPP_E164

Base.metadata.create_all(bind=engine)
db = SessionLocal()

# Temizle
for model in [StockAlert, Order, Product, ReturnItem, Expense, Complaint]:
    db.query(model).delete()
db.commit()
print("Eski veriler temizlendi.")

# ── Şikayetler ──────────────────────────────────────────────────────────────
complaints = [
    # Yarışma demo: işletme WhatsApp hattından gelen şikayet (panelde ilk sırada görünsün)
    Complaint(
        customer_name=WHATSAPP_E164,
        message=f"[{BOUTIQUE_NAME}] Elbise rengi siteden farklı geldi; değişim veya iade talep ediyorum.",
        urgency_level="High",
        sentiment="Negative",
        status="Pending",
    ),
    Complaint(customer_name="Hasan Kurnaz", message="Ürün bozuk geldi, para iadesi istiyorum!", urgency_level="Critical", sentiment="Negative", status="Pending"),
    Complaint(customer_name="Ayşe Yılmaz", message="Siparişim 5 gündür gelmedi, kargo nerede?", urgency_level="High", sentiment="Negative", status="Pending"),
    Complaint(customer_name="Mehmet Dürüst", message="Yanlış ürün gönderilmiş, değişim istiyorum.", urgency_level="Normal", sentiment="Neutral", status="Assigned", assigned_to="Müşteri Hizmetleri"),
    Complaint(customer_name="Fatma Güler", message="Ürün çok güzeldi, teşekkürler!", urgency_level="Low", sentiment="Positive", status="Resolved"),
    Complaint(customer_name="Ali Çelik", message="Fatura kesilmedi, yasal hakkım var!", urgency_level="High", sentiment="Negative", status="Pending"),
]
db.add_all(complaints)

# ── Masraflar ───────────────────────────────────────────────────────────────
expenses = [
    Expense(vendor_name="MNG Kargo", amount=2450.0, status="Approved"),
    Expense(vendor_name="Ambalaj A.Ş.", amount=890.50, status="Approved"),
    Expense(vendor_name="Elektrik Faturası", amount=3200.0, status="Approved"),
    Expense(vendor_name="Yurtiçi Kargo", amount=1750.0, status="Pending"),
    Expense(vendor_name="Depo Kirası", amount=8500.0, status="Approved"),
]
db.add_all(expenses)

# ── İade Talepleri (butik giyim senaryosu) ──────────────────────────────────
returns = [
    ReturnItem(order_id="ORD-992A", customer_name="Hasan Kurnaz", reason="İpek gömlek yanlış beden (M yerine S geldi)", ai_risk_score=0.91, ai_verdict="Manual Review", ai_reasoning="Müşterinin geçmişte 3 iade talebi var. Yüksek risk skoru nedeniyle patron onayına sunuldu."),
    ReturnItem(order_id="ORD-845B", customer_name="Ayşe Yılmaz", reason="Elbisede etiket kopuk — iade politikasına göre değerlendirme", ai_risk_score=0.30, ai_verdict="Reject", ai_reasoning="Etiket koparılmış. Butik iade kurallarına göre etiketsiz ürünler reddedilir."),
    ReturnItem(order_id="ORD-712C", customer_name="Mehmet Dürüst", reason="Kargoda kumaşta leke / hasar", ai_risk_score=0.05, ai_verdict="Approve", ai_reasoning="Müşteri geçmişi temiz. Kargo kaynaklı hasar. İade onaylandı."),
]
db.add_all(returns)

# ── Ürünler (butik vitrin) ──────────────────────────────────────────────────
products = [
    Product(sku="BTQ-001", name="Keten midi elbise (S)", category="Giyim", stock_quantity=4, low_stock_threshold=8, unit_price=1890.00, supplier="Lokal dikim"),
    Product(sku="BTQ-002", name="İpek gömlek (M)", category="Giyim", stock_quantity=12, low_stock_threshold=6, unit_price=1450.00, supplier="Lokal dikim"),
    Product(sku="BTQ-003", name="Yün blazer (L)", category="Giyim", stock_quantity=2, low_stock_threshold=5, unit_price=3290.00, supplier="Lokal dikim"),
    Product(sku="BTQ-004", name="Organik pamuk tişört (M)", category="Giyim", stock_quantity=18, low_stock_threshold=10, unit_price=390.00, supplier="Moda Tekstil Ltd."),
    Product(sku="BTQ-005", name="Şifon gece elbisesi (36)", category="Giyim", stock_quantity=6, low_stock_threshold=4, unit_price=2150.00, supplier="Lokal dikim"),
]
db.add_all(products)
db.flush()  # ID'leri almak için

# ── Siparişler (butik sipariş kodları) ───────────────────────────────────────
orders = [
    Order(order_code="ORD-2024-001", customer_name="Zeynep Arslan", customer_phone="+905551112233", product_name="Keten midi elbise (S)", quantity=1, total_price=1890.00, status="Shipped", cargo_tracking_code="MNG123456789", cargo_company="MNG Kargo"),
    Order(order_code="ORD-2024-002", customer_name="Burak Koç", customer_phone="+905559876543", product_name="İpek gömlek (M)", quantity=1, total_price=1450.00, status="Pending"),
    Order(order_code="ORD-2024-003", customer_name="Selin Yıldız", customer_phone="+905553334455", product_name="Yün blazer (L)", quantity=1, total_price=3290.00, status="Processing"),
    Order(order_code="ORD-2024-004", customer_name="Emre Demir", customer_phone="+905557778899", product_name="Organik pamuk tişört (M)", quantity=2, total_price=780.00, status="Delivered"),
    Order(order_code="ORD-2024-005", customer_name="Hasan Kurnaz", customer_phone="+905550001122", product_name="Şifon gece elbisesi (36)", quantity=1, total_price=2150.00, status="Cancelled"),
]
db.add_all(orders)

# ── Stok Uyarıları ──────────────────────────────────────────────────────────
# Eşiğin altındaki ürünler için otomatik uyarı oluştur
alerts = []
for p in products:
    if p.stock_quantity < p.low_stock_threshold:
        alerts.append(StockAlert(
            product_id=p.id,
            product_name=p.name,
            current_stock=p.stock_quantity,
            threshold=p.low_stock_threshold,
            ai_recommendation=f"'{p.name}' için stok kritik seviyede ({p.stock_quantity} adet). "
                               f"Geçmiş satış hızına göre tahmini {p.low_stock_threshold * 3} adet sipariş verilmesi önerilir. "
                               f"Tedarikçi: {p.supplier}",
            status="Open"
        ))
db.add_all(alerts)

db.commit()
db.close()

print("Mock veri basariyla olusturuldu!")
print(f"   - {len(complaints)} şikayet")
print(f"   - {len(expenses)} masraf")
print(f"   - {len(returns)} iade talebi")
print(f"   - {len(products)} ürün")
print(f"   - {len(orders)} sipariş")
print(f"   - {len(alerts)} stok uyarısı")
