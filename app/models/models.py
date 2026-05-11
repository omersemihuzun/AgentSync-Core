from sqlalchemy import Column, Integer, String, Float, DateTime, Text, Boolean, ForeignKey
from sqlalchemy.sql import func
from app.core.database import Base


class Complaint(Base):
    """Müşteri şikayetleri — WhatsApp veya web panelinden geliyor."""
    __tablename__ = "complaints"

    id = Column(Integer, primary_key=True, index=True)
    customer_name = Column(String, index=True)
    message = Column(Text, nullable=False)
    urgency_level = Column(String, default="Normal")  # Low, Normal, High, Critical
    sentiment = Column(String, default="Neutral")     # Positive, Neutral, Negative
    status = Column(String, default="Pending")        # Pending, Assigned, Resolved
    assigned_to = Column(String, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class Expense(Base):
    """Masraf ve fatura kayıtları."""
    __tablename__ = "expenses"

    id = Column(Integer, primary_key=True, index=True)
    vendor_name = Column(String, index=True)
    amount = Column(Float, nullable=False)
    date_recorded = Column(DateTime(timezone=True), server_default=func.now())
    source_image = Column(String, nullable=True)  # WhatsApp image ID or URL
    status = Column(String, default="Approved")


class ReturnItem(Base):
    """İade talepleri — AI tarafından analiz ediliyor."""
    __tablename__ = "return_items"

    id = Column(Integer, primary_key=True, index=True)
    order_id = Column(String, index=True)
    customer_name = Column(String)
    reason = Column(Text)
    ai_risk_score = Column(Float, default=0.0)     # 0.0=Güvenli, 1.0=Yüksek Risk
    ai_verdict = Column(String, nullable=True)      # Approve, Reject, Manual Review
    ai_reasoning = Column(Text, nullable=True)      # AI'ın karar gerekçesi (tam metin)
    status = Column(String, default="Pending")      # Pending, Approved, Rejected
    created_at = Column(DateTime(timezone=True), server_default=func.now())


# ── YENI TABLOLAR — Sipariş & Stok Takibi ────────────────────────────────────

class Product(Base):
    """Ürün kataloğu ve stok bilgisi."""
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    sku = Column(String, unique=True, index=True)    # Stok Kodu: PRD-001
    name = Column(String, nullable=False)
    category = Column(String, default="Genel")       # Giyim, Gıda, Elektronik...
    stock_quantity = Column(Integer, default=0)
    low_stock_threshold = Column(Integer, default=10)  # Altına düşünce kritik uyarı
    unit_price = Column(Float, nullable=False)
    supplier = Column(String, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())


class Order(Base):
    """Müşteri siparişleri."""
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, index=True)
    order_code = Column(String, unique=True, index=True)  # ORD-2024-001
    customer_name = Column(String, nullable=False)
    customer_phone = Column(String, nullable=True)         # WhatsApp entegrasyonu için
    product_name = Column(String, nullable=False)
    quantity = Column(Integer, default=1)
    total_price = Column(Float, nullable=False)
    status = Column(String, default="Pending")  # Pending, Processing, Shipped, Delivered, Cancelled
    cargo_tracking_code = Column(String, nullable=True)
    cargo_company = Column(String, nullable=True)          # MNG, Yurtiçi, PTT...
    ai_summary = Column(Text, nullable=True)               # AI günlük özet notu
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())


class StockAlert(Base):
    """AI tarafından üretilen kritik stok uyarıları."""
    __tablename__ = "stock_alerts"

    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, ForeignKey("products.id"))
    product_name = Column(String)
    current_stock = Column(Integer)
    threshold = Column(Integer)
    ai_recommendation = Column(Text, nullable=True)  # AI'ın yenileme önerisi metni
    status = Column(String, default="Open")           # Open, Acknowledged, Resolved
    created_at = Column(DateTime(timezone=True), server_default=func.now())
