from crewai import Task
from textwrap import dedent

class AgentSyncTasks:
    def analyze_image_task(self, agent, image_description):
        return Task(
            description=dedent(f"""
                Müşteri bir fotoğraf gönderdi. Sistemin görüntü tanıma modülü fotoğraftan şu taslağı çıkardı:
                '{image_description}'
                
                Görev: Bu taslağı dikkatlice incele. Üründe belirgin bir defo, yırtık veya kırık var mı? Ürünün orijinal markasına ait etiketi üzerinde mi koparılmış mı?
                Sonucunu net ve kısa bir hasar tespit raporu olarak yaz.
            """),
            expected_output="Ürünün fiziksel hasar ve etiket durumunu belirten 2-3 cümlelik kesin bir tespit raporu.",
            agent=agent
        )
        
    def check_policy_task(self, agent):
        return Task(
            description=dedent("""
                Önceki ajanın (Vision Agent) hazırladığı hasar raporunu oku. 
                Şirketin İade Kurallarına (Policy) göre iadenin kabul edilip edilemeyeceğini kontrol et:
                - KURAL 1: Etiketi koparılmış veya eksik olan ürünler KESİNLİKLE REDDEDİLİR.
                - KURAL 2: Kullanıcı hatası olmayan yırtık, kırık, ezik ürünler kabul edilir.
                
                Görev: Bu iade talebi kurallara uygun mu değil mi? Kararını ve nedenini belirt.
            """),
            expected_output="İadenin şirket kurallarına uygunluğuna dair kesin onay (Approve) veya ret (Reject) kararı.",
            agent=agent
        )
        
    def analyze_fraud_task(self, agent, customer_name):
        return Task(
            description=dedent(f"""
                'Get Customer History' veritabanı aracını (Tool) kullanarak tam olarak '{customer_name}' isimli müşterinin geçmişini sorgula.
                Müşterinin geçmişte yaptığı iade sayılarına bak.
                Eğer çok fazla (3 veya daha fazla) iadesi varsa bu müşteri şüphelidir ve Yüksek Risk grubundadır.
                
                Görev: Müşterinin suistimal potansiyelini değerlendir.
            """),
            expected_output="Müşterinin geçmiş davranışlarına dayanan bir Risk Skoru ve Analiz Raporu.",
            agent=agent
        )
        
    def final_decision_task(self, agent):
        return Task(
            description=dedent("""
                1. Policy Agent'ın hazırladığı kural uygunluk kararını incele.
                2. Fraud Agent'ın hazırladığı müşteri risk analiz raporunu incele.
                
                Görev: Tüm bu veriler ışığında bir 'Nihai Karar' ver.
                Nihai Karar Mantığı:
                - Eğer ürün kurallara UYMUYORSA (Örn: etiketi kopmuş): Kesinlikle REJECT.
                - Eğer ürün kurallara UYUYOR ama Müşteri YÜKSEK RİSKLİ ise: MANUAL REVIEW (Patron incelemeli).
                - Eğer ürün kurallara UYUYOR ve Müşteri RİSKSİZ ise: APPROVE (Anında İade Onayı).
                
                Çıktında şu iki bölüm mutlaka olsun:
                1. FINAL DECISION: [Approve / Reject / Manual Review]
                2. WHATSAPP MESSAGE: Patronun telefonuna gidecek 1-2 cümlelik özet (Örn: 'Patron, Hasan Kurnaz isimli müşteri yırtık gömlek iadesi istedi. Ürün kurallara uygun ama bu müşterinin geçmişte 3 iadesi daha var. İadeyi manuel onayınıza sunuyorum.').
            """),
            expected_output="Nihai karar (APPROVE/REJECT/MANUAL REVIEW) ve Patron için WhatsApp mesaj taslağı.",
            agent=agent
        )
