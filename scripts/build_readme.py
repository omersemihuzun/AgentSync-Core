# AgentSync AI — Eksiksiz README
# Bu dosya yarışma gereksinimlerine göre hazırlanmıştır.

readme = """
<div align="center">

# 🤖 AgentSync AI
### *AI ile Güçlendirilmiş KOBİ Operasyon Platformu*

[![Python](https://img.shields.io/badge/Python-3.10-blue?logo=python)](https://python.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.136-green?logo=fastapi)](https://fastapi.tiangolo.com)
[![CrewAI](https://img.shields.io/badge/CrewAI-Multi--Agent-orange)](https://crewai.com)
[![Gemini](https://img.shields.io/badge/Google-Gemini_1.5_Flash-red?logo=google)](https://ai.google.dev)
[![Docker](https://img.shields.io/badge/Docker-Compose-blue?logo=docker)](https://docker.com)

**YZTA 5.0 Hackathon — Takım AgentSync**

</div>

---

## 🎯 Problem

KOBİ sahipleri günde 2-3 saatini "siparişim nerede?", "bu ürün stokta var mı?" ve müşteri şikayetlerine
cevap vermekle harcıyor. Stok tükenmesi fark edildiğinde müşteri zaten kaybedilmiş oluyor.
Kargo gecikmeleri müşteriye ulaşmadan önce işletmeye ulaşmıyor.

## 💡 Çözüm

AgentSync AI, bu operasyonel kaosa **4 uzman yapay zeka ajanı** ile müdahale eder:

- Müşteri şikayetlerini **otomatik sınıflandırır** ve aciliyetini belirler
- İade taleplerini **görüntü analizi + kural motoru + dolandırıcılık tespiti** ile değerlendirir
- Kritik stok seviyelerini **proaktif olarak tespit** eder ve yenileme önerir
- **WhatsApp üzerinden** patrona karar onayı gönderir (Human-in-the-Loop)

---

## 🏗️ Sistem Mimarisi

```
┌─────────────────────────────────────────────────────────────────┐
│                        KULLANICI KATMANI                         │
│  ┌──────────────┐    ┌───────────────┐    ┌──────────────────┐  │
│  │  WhatsApp    │    │  Admin Panel  │    │  Streamlit Demo  │  │
│  │  (Twilio)    │    │  (Stitch SPA) │    │  (CrewAI Live)   │  │
│  └──────┬───────┘    └──────┬────────┘    └────────┬─────────┘  │
└─────────┼──────────────────┼─────────────────────┼─────────────┘
          │                  │                      │
┌─────────▼──────────────────▼──────────────────────▼─────────────┐
│                     FastAPI BACKEND (Python)                      │
│  POST /webhook/whatsapp   GET /orders   GET /complaints          │
│  POST /return-items/{id}/ai-analyze     PATCH /orders/{id}       │
└─────────────────────────────┬───────────────────────────────────┘
                              │
┌─────────────────────────────▼───────────────────────────────────┐
│                    CrewAI AJAN KATMANI                            │
│                                                                   │
│  ┌────────────┐  ┌─────────────┐  ┌────────────┐  ┌──────────┐ │
│  │VisionAgent │→ │PolicyAgent  │→ │FraudAgent  │→ │Decision  │ │
│  │Görüntü     │  │Kural        │  │Risk        │  │Agent     │ │
│  │Analizi     │  │Denetimi     │  │Tespiti     │  │Nihai     │ │
│  │(Gemini)    │  │(KOBİ Pol.)  │  │(DB Sorgu)  │  │Karar     │ │
│  └────────────┘  └─────────────┘  └────────────┘  └──────────┘ │
└─────────────────────────────┬───────────────────────────────────┘
                              │
┌─────────────────────────────▼───────────────────────────────────┐
│              PostgreSQL (Neon.tech — Frankfurt)                   │
│  complaints │ return_items │ orders │ products │ stock_alerts    │
└─────────────────────────────────────────────────────────────────┘
```

---

## 🤖 Yapay Zeka Yaklaşımı

### Çoklu Ajan Mimarisi (CrewAI + Google Gemini 1.5 Flash)

| Ajan | Görev | Teknoloji |
|------|-------|-----------|
| **VisionAgent** | Fotoğraftaki hasarı ve etiketi tespit eder | Gemini 1.5 Flash |
| **PolicyAgent** | KOBİ'nin iade kurallarına göre karar üretir | Gemini + RAG-benzeri kural motoru |
| **FraudAgent** | Müşterinin geçmişini DB'den sorgular, risk skoru çıkarır | Gemini + LangChain Custom Tool |
| **DecisionAgent** | Diğer 3 ajanın raporunu okur, nihai karar verir + WhatsApp mesajı hazırlar | Gemini |

### Human-in-the-Loop
AI otonom karar vermez. Riskli durumlarda patron WhatsApp'tan onay verir.
- `Approve`: AI güvenli gördü → Otomatik onay
- `Reject`: Kural ihlali → Otomatik ret
- `Manual Review`: Riskli müşteri → **Patron onayı gerekir**

---

## 🚀 Kurulum

### Gereksinimler
- Python 3.10+
- Docker & Docker Compose
- Neon.tech PostgreSQL hesabı (veya yerel PostgreSQL)

### 1. Klonla
```bash
git clone https://github.com/omersemihuzun/AgentSync-Core.git
cd AgentSync-Core
```

### 2. .env Dosyasını Oluştur
```env
DATABASE_URL=postgresql://...   # Ekip liderinden al
GEMINI_API_KEY=...              # Google AI Studio'dan al
TWILIO_AUTH_TOKEN=...           # Opsiyonel
```

### 3. Docker ile Başlat (Önerilen)
```bash
docker compose up --build
```

| Servis | URL |
|--------|-----|
| 🔧 FastAPI Backend | http://localhost:8000 |
| 📊 Admin Panel (SPA) | http://localhost:8000 |
| 🤖 Streamlit Demo | http://localhost:8501 |
| 📖 API Docs (Swagger) | http://localhost:8000/docs |

### 4. Mock Veriyi Yükle
```bash
python scripts/generate_mock_data.py
```

---

## 📡 API Endpoint'leri

| Method | Endpoint | Açıklama |
|--------|----------|----------|
| GET | `/complaints` | Şikayetleri listele |
| GET | `/orders` | Siparişleri listele |
| GET | `/orders/{code}` | Sipariş sorgula (WhatsApp için) |
| GET | `/products` | Ürün kataloğu |
| GET | `/stock-alerts` | Kritik stok uyarıları |
| POST | `/return-items/{id}/ai-analyze` | **AI ile iade analizi başlat** |
| PATCH | `/return-items/{id}/decision` | Patron kararını kaydet |
| POST | `/webhook/whatsapp` | Twilio WhatsApp webhook |

---

## 🗂️ Proje Yapısı

```
AgentSync-Core/
├── app/
│   ├── agents/
│   │   ├── agents.py       # CrewAI ajan tanımları (Gemini)
│   │   ├── tasks.py        # Görev direktifleri
│   │   ├── crew.py         # Orkestrasyon sınıfı
│   │   └── tools/
│   │       └── db_tools.py # LangChain Custom Tool (DB sorgu)
│   ├── api/
│   │   └── endpoints/
│   │       └── v1.py       # REST API endpoint'leri
│   ├── core/
│   │   └── database.py     # SQLAlchemy + Neon bağlantısı
│   ├── frontend/
│   │   └── dashboard.py    # Streamlit Canlı Demo
│   ├── models/
│   │   └── models.py       # Veritabanı modelleri
│   ├── static/
│   │   └── index.html      # Stitch SPA (Admin Panel)
│   └── main.py             # FastAPI giriş noktası
├── scripts/
│   ├── generate_mock_data.py
│   └── build_spa.py
├── Dockerfile
├── docker-compose.yml
└── requirements.txt
```

---

## 👥 Takım

| İsim | Rol |
|------|-----|
| Ömer Semih Uzun | Backend & AI Ajanlar |
| *(ekip arkadaşı)* | ....|

---

## 📄 Lisans

MIT License — YZTA 5.0 Hackathon projesi
"""

with open("README.md", "w", encoding="utf-8") as f:
    f.write(readme.strip())

print("README.md oluşturuldu!")
