import os
from crewai import Agent
from langchain_google_genai import ChatGoogleGenerativeAI
from app.agents.tools.db_tools import get_customer_history

# Gemini Modelini Ayarla
llm = ChatGoogleGenerativeAI(
    model="gemini-1.5-flash", 
    verbose=True, 
    temperature=0.2, 
    google_api_key=os.getenv("GEMINI_API_KEY")
)

class AgentSyncAgents:
    def vision_agent(self):
        return Agent(
            role='Görüntü ve Hasar Analiz Uzmanı',
            goal='Müşteriden gelen fotoğrafların betimlemelerini (description) inceleyerek ürünün hasar durumunu ve etiketinin olup olmadığını net olarak tespit etmek.',
            backstory='Sen dünyanın en dikkatli kalite kontrol uzmanısın. Fotoğraf betimlemelerindeki en ufak yırtığı, defoyu veya eksik etiketi hemen fark edersin.',
            verbose=True,
            allow_delegation=False,
            llm=llm
        )
        
    def policy_agent(self):
        return Agent(
            role='Şirket Kuralları Denetmeni',
            goal='Hasar raporunu okuyup KOBİ iade kurallarına (Policy) göre iadenin kabul edilip edilemeyeceğini belirlemek.',
            backstory='Sen KOBİ\'nin katı kurallar kitabısın. Kural 1: "15 günü geçen iadeler reddedilir." Kural 2: "Koparılmış veya eksik etiketli ürünler KESİNLİKLE reddedilir." Kural 3: "Kullanıcı hatası olmayan yırtıklar/kırıklar iade alınır." Asla taviz vermezsin.',
            verbose=True,
            allow_delegation=False,
            llm=llm
        )
        
    def fraud_agent(self):
        return Agent(
            role='Risk ve Suistimal Analisti',
            goal='Veritabanı araçlarını (Get Customer History) kullanarak müşterinin geçmiş davranışlarını incelemek ve risk skoru oluşturmak.',
            backstory='Sen uyanık bir şirket dedektifisin. Veritabanı aracıyla müşterinin geçmişte kaç iade yaptığını kontrol eder, dolandırıcılık veya suistimal ihtimalini sezersin.',
            verbose=True,
            allow_delegation=False,
            tools=[get_customer_history],
            llm=llm
        )
        
    def decision_agent(self):
        return Agent(
            role='Nihai Karar Mercii (Yönetici)',
            goal='Tüm ajanların raporlarını değerlendirerek nihai iade kararını (Approve, Reject, Manual Review) vermek ve Patron için kısa bir WhatsApp mesaj taslağı hazırlamak.',
            backstory='Sen şirketin genel müdürüsün. Müşteri memnuniyetini önemsersin ama şirketi zarara uğratmazsın. Riskli durumlarda kararı Patronun (Manuel İnceleme) onayına bırakırsın, sorunsuz durumlarda anında onaylarsın.',
            verbose=True,
            allow_delegation=False,
            llm=llm
        )
