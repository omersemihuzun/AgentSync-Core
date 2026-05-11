"""
AgentSync AI — Mock Data Script (Genişletilmiş)
Çalıştır: python scripts/generate_mock_data.py
"""
import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from dotenv import load_dotenv
load_dotenv()

from app.core.database import SessionLocal, engine
from app.models.models import Base, Complaint, Expense, ReturnItem, Product, Order, StockAlert

Base.metadata.create_all(bind=engine)
db = SessionLocal()

# Temizle
for model in [StockAlert, Order, Product, ReturnItem, Expense, Complaint]:
    db.query(model).delete()
db.commit()
print("Eski veriler temizlendi.")

# ── Şikayetler ──────────────────────────────────────────────────────────────
complaints = [
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

# ── İade Talepleri ──────────────────────────────────────────────────────────
returns = [
    ReturnItem(order_id="ORD-992A", customer_name="Hasan Kurnaz", reason="Ürün hasarlı geldi", ai_risk_score=0.91, ai_verdict="Manual Review", ai_reasoning="Müşterinin geçmişte 3 iade talebi var. Yüksek risk skoru nedeniyle patron onayına sunuldu."),
    ReturnItem(order_id="ORD-845B", customer_name="Ayşe Yılmaz", reason="Etiketi koparılmış ürün iade edilemez", ai_risk_score=0.30, ai_verdict="Reject", ai_reasoning="Ürün etiketi koparılmış. KOBİ politikasına göre etiketsiz ürünler kesinlikle reddedilir."),
    ReturnItem(order_id="ORD-712C", customer_name="Mehmet Dürüst", reason="Kargoda cam kırıldı", ai_risk_score=0.05, ai_verdict="Approve", ai_reasoning="Müşteri geçmişi temiz. Kargo hasarı açıkça görülüyor. İade onaylandı."),
]
db.add_all(returns)

# ── Ürünler ─────────────────────────────────────────────────────────────────
products = [
    Product(sku="PRD-001", name="Organik Domates (1 kg)", category="Gıda", stock_quantity=45, low_stock_threshold=50, unit_price=18.90, supplier="Ege Çiftçi Kooperatifi"),
    Product(sku="PRD-002", name="El Yapımı Zeytinyağı (500ml)", category="Gıda", stock_quantity=120, low_stock_threshold=20, unit_price=89.00, supplier="Ege Çiftçi Kooperatifi"),
    Product(sku="PRD-003", name="Pamuklu Tişört (M)", category="Giyim", stock_quantity=8, low_stock_threshold=15, unit_price=149.90, supplier="Moda Tekstil Ltd."),
    Product(sku="PRD-004", name="Ahşap Çerçeve (A4)", category="Ev & Yaşam", stock_quantity=3, low_stock_threshold=10, unit_price=45.00, supplier="El Sanatları Atölyesi"),
    Product(sku="PRD-005", name="Organik Bal (250g)", category="Gıda", stock_quantity=67, low_stock_threshold=15, unit_price=120.00, supplier="Karadeniz Arıcılık"),
]
db.add_all(products)
db.flush()  # ID'leri almak için

# ── Siparişler ──────────────────────────────────────────────────────────────
orders = [
    Order(order_code="ORD-2024-001", customer_name="Zeynep Arslan", customer_phone="+905551112233", product_name="Organik Domates (1 kg)", quantity=3, total_price=56.70, status="Shipped", cargo_tracking_code="MNG123456789", cargo_company="MNG Kargo"),
    Order(order_code="ORD-2024-002", customer_name="Burak Koç", customer_phone="+905559876543", product_name="El Yapımı Zeytinyağı (500ml)", quantity=2, total_price=178.00, status="Pending"),
    Order(order_code="ORD-2024-003", customer_name="Selin Yıldız", customer_phone="+905553334455", product_name="Pamuklu Tişört (M)", quantity=1, total_price=149.90, status="Processing"),
    Order(order_code="ORD-2024-004", customer_name="Emre Demir", customer_phone="+905557778899", product_name="Ahşap Çerçeve (A4)", quantity=5, total_price=225.00, status="Delivered"),
    Order(order_code="ORD-2024-005", customer_name="Hasan Kurnaz", customer_phone="+905550001122", product_name="Organik Bal (250g)", quantity=2, total_price=240.00, status="Cancelled"),
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

print(f"✅ Mock veri başarıyla oluşturuldu!")
print(f"   - {len(complaints)} şikayet")
print(f"   - {len(expenses)} masraf")
print(f"   - {len(returns)} iade talebi")
print(f"   - {len(products)} ürün")
print(f"   - {len(orders)} sipariş")
print(f"   - {len(alerts)} stok uyarısı")
