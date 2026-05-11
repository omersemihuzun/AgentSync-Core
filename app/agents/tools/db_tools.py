import os
from langchain.tools import tool
from app.core.database import SessionLocal
from app.models.models import ReturnItem, Complaint

@tool("Get Customer History")
def get_customer_history(customer_name: str) -> str:
    """
    Veritabanından belirli bir müşterinin geçmiş iade (Return) ve şikayet (Complaint) 
    kayıtlarını bulup risk analizi için bir özet döner.
    """
    db = SessionLocal()
    try:
        returns = db.query(ReturnItem).filter(ReturnItem.customer_name == customer_name).all()
        complaints = db.query(Complaint).filter(Complaint.customer_name == customer_name).all()
        
        return_count = len(returns)
        complaint_count = len(complaints)
        
        if return_count == 0 and complaint_count == 0:
            return f"{customer_name} isimli müşterinin geçmiş kaydı bulunmamaktadır. Risk skoru: Düşük (Güvenilir Müşteri)."
            
        history = f"Müşteri ({customer_name}) Geçmiş Analizi:\n"
        history += f"- Toplam geçmiş iade talebi: {return_count}\n"
        history += f"- Toplam geçmiş şikayet: {complaint_count}\n"
        
        # Risk tespiti için basit bir kural motoru
        if return_count >= 3:
            history += "-> UYARI: Bu müşteri sistemde sık sık iade talebinde bulunuyor. YÜKSEK RİSK. Kesinlikle manuel inceleme önerilir."
        else:
            history += "-> Risk: Normal."
            
        return history
    except Exception as e:
        return f"Veritabanı sorgusunda hata oluştu: {str(e)}"
    finally:
        db.close()
