from sqlalchemy import Column, Integer, String, Float, DateTime, Text, Boolean
from sqlalchemy.sql import func
from app.core.database import Base

class Complaint(Base):
    __tablename__ = "complaints"
    
    id = Column(Integer, primary_key=True, index=True)
    customer_name = Column(String, index=True)
    message = Column(Text, nullable=False)
    urgency_level = Column(String, default="Normal") # Low, Normal, High, Critical
    sentiment = Column(String, default="Neutral") # Positive, Neutral, Negative
    status = Column(String, default="Pending") # Pending, Assigned, Resolved
    assigned_to = Column(String, nullable=True) # Worker name or department
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class Expense(Base):
    __tablename__ = "expenses"

    id = Column(Integer, primary_key=True, index=True)
    vendor_name = Column(String, index=True)
    amount = Column(Float, nullable=False)
    date_recorded = Column(DateTime(timezone=True), server_default=func.now())
    source_image = Column(String, nullable=True) # WhatsApp image ID or URL
    status = Column(String, default="Approved")

class ReturnItem(Base):
    __tablename__ = "return_items"

    id = Column(Integer, primary_key=True, index=True)
    order_id = Column(String, index=True)
    customer_name = Column(String)
    reason = Column(Text)
    ai_risk_score = Column(Float, default=0.0) # 0.0 (Safe) to 1.0 (High Risk/Fraud)
    ai_verdict = Column(String, nullable=True) # Approve, Reject, Manual Review
    status = Column(String, default="Pending") # Pending, Approved, Rejected
    created_at = Column(DateTime(timezone=True), server_default=func.now())
