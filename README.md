<div align="center">

# AgentSync AI
### *AI ile güçlendirilmiş KOBİ / butik operasyon platformu*

[![Python](https://img.shields.io/badge/Python-3.10-blue?logo=python)](https://python.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.136-green?logo=fastapi)](https://fastapi.tiangolo.com)
[![CrewAI](https://img.shields.io/badge/CrewAI-Multi--Agent-orange)](https://crewai.com)
[![Gemini](https://img.shields.io/badge/Google-Gemini_1.5_Flash-red?logo=google)](https://ai.google.dev)
[![Docker](https://img.shields.io/badge/Docker-Compose-blue?logo=docker)](https://docker.com)

**YZTA 5.0 Hackathon — Takım AgentSync**

</div>

---

## Hackathon / jüri için özet (yarışma kurallarına uyum)

Bu repo, **YZTA 5.0 KOBİ operasyon problemi** kapsamında sunulacak şekilde düzenlenmiştir. Aşağıdaki başlıklar jüri değerlendirmesinde sık aranan kriterlerle hizalıdır.

| Kriter | Projede karşılığı |
|--------|-------------------|
| **Problem tanımı** | KOBİ/butik: sipariş takibi, şikayet, iade, stok farkındalığı, WhatsApp yoğunluğu. |
| **Çözüm ve yenilik** | Çoklu ajan (CrewAI + Gemini), Human-in-the-Loop (patron kararı), WhatsApp webhook, admin SPA. |
| **Yapay zeka etiği** | AI tek başına nihai iade vermez; `Manual Review` + `PATCH /return-items/{id}/decision` ile patron onayı. |
| **Teknik derinlik** | FastAPI, SQLAlchemy, Neon/SQLite, opsiyonel Twilio giden mesaj, TwiML cevap, demo zinciri. |
| **Tekrarlanabilirlik** | `requirements.txt`, `docker-compose`, mock veri scripti, `.env` şablonu, migrasyon SQL, `/health`. |
| **Dokümantasyon** | Bu README + `docs/` (demo senaryosu, tema notları, hackathon seçenekleri). |

**Demo senaryosu (video):** `docs/DEMO-VIDEO-SENARYOSU.md`  
**Tema / PDF notu:** `docs/TEMA-VE-DOKUMANLAR.md`  
**Ekip içi öncelik listesi:** `docs/HACKATHON-GELISTIRME-SECENEKLERI.md`

---

## Problem

KOBİ ve butik işletmeler günde uzun süre **“siparişim nerede?”**, **şikayet**, **iade** ve **stok** sorularıyla uğraşır. Bilgi dağınık; müşteri WhatsApp’tan yazar, veri panele düşmez veya geç düşer. İade kararları öznel ve hataya açıktır.

## Çözüm

**AgentSync AI**; şikayet/iade/sipariş verisini **tek backend**de toplar, **çoklu ajan** ile iade riskini değerlendirir, **patron onayını** API üzerinden destekler ve **WhatsApp webhook** (Twilio uyumlu) ile müşteri kanalını bağlar.

**Demo işletme:** *Linen Atölye Butik* — vitrin `app/static/index.html`, sabit iletişim `app/core/brand_config.py` içindedir.

---

## Mimari (yüksek seviye)

```
WhatsApp (Twilio) ──POST──► /webhook/whatsapp
                                │
                                ├─ ORD-xxxx-xxx ► sipariş sorgusu (DB)
                                └─ diğer metin ► parse_twilio_message + run_agent
                                        │
                                        ├─ şikayet ► complaints
                                        ├─ iade    ► return_items
                                        └─ (opsiyonel) AGENTSYNC_DEMO_CHAIN
                                              ► return_pipeline (CrewAI veya yedek mantık)
                                              ► (opsiyonel) otomatik onay + Twilio bildirimi

Admin SPA (/) ◄──► GET/PATCH REST (Swagger /docs)
Streamlit (8501) ◄──► Crew demo
PostgreSQL / SQLite ◄──► SQLAlchemy modelleri
```

**CrewAI zinciri (iade analizi):** Vision → Policy → Fraud → Decision (`app/agents/crew.py`). `GEMINI_API_KEY` yoksa veya model hata verirse `app/services/return_pipeline.py` içinde **demo / yedek** metin tabanlı karar üretilebilir (`AGENTSYNC_DEMO_FALLBACK_AI`, varsayılan açık).

---

## Kurulum

### Gereksinimler

- Python **3.10+**
- **Docker** (isteğe bağlı)
- **PostgreSQL** (Neon önerilir) veya yerel **SQLite**

### 1) Klonla

```bash
git clone https://github.com/omersemihuzun/AgentSync-Core.git
cd AgentSync-Core
```

### 2) Sanal ortam ve paketler

```bash
python -m venv .venv
# Windows:
.\.venv\Scripts\activate
# Linux/macOS:
source .venv/bin/activate

pip install -r requirements.txt
```

### 3) Ortam değişkenleri (`.env` — repoya ASLA commit etmeyin)

| Değişken | Zorunlu | Açıklama |
|----------|---------|----------|
| `DATABASE_URL` | Önerilir | Neon PostgreSQL veya `sqlite:///./agentsync.sqlite3` |
| `GEMINI_API_KEY` | İsteğe bağlı | CrewAI + Gemini; yoksa demo yedek mantık devreye girebilir |
| `TWILIO_ACCOUNT_SID`, `TWILIO_AUTH_TOKEN`, `TWILIO_WHATSAPP_FROM` | İsteğe bağlı | Giden WhatsApp (onay sonrası bildirim) |
| `AGENTSYNC_DEMO_CHAIN` | İsteğe bağlı | `1` ise webhook’ta iade sonrası otomatik AI pipeline |
| `AGENTSYNC_DEMO_AUTO_APPROVE` | İsteğe bağlı | `1` ise Approve + düşük riskte otomatik onay |
| `AGENTSYNC_DEMO_FALLBACK_AI` | İsteğe bağlı | `1` (varsayılan) Crew hata verirse yedek karar |

Örnek (yerel SQLite + demo zincir):

```env
DATABASE_URL=sqlite:///./agentsync.sqlite3
GEMINI_API_KEY=
AGENTSYNC_DEMO_CHAIN=1
AGENTSYNC_DEMO_AUTO_APPROVE=1
```

### 4) Veritabanı şeması (Neon kullanıyorsanız)

Eski Neon tablolarında `return_items.ai_reasoning` eksikse hata alırsınız. **Neon SQL Editor**’da çalıştırın:

`scripts/migrate_postgres_return_items.sql`

### 5) Mock veri

```bash
python scripts/generate_mock_data.py
```

Butik vitrini, şikayetler, iadeler, siparişler ve stok uyarıları yüklenir (iş hattı numarası demo şikayette kullanılır).

### 6) Çalıştırma

**Yerel:**

```bash
uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
```

**Docker:**

```bash
docker compose up --build
```

| Servis | URL |
|--------|-----|
| FastAPI + Admin SPA | http://localhost:8000 |
| Swagger | http://localhost:8000/docs |
| Streamlit | http://localhost:8501 |
| Sağlık | http://localhost:8000/health |

**Demo giriş (SPA):** `patron@agentsync.com` / `patron123` — giriş kartında ipucu metni de vardır.

---

## WhatsApp neden doğrudan `localhost`’a düşmez?

WhatsApp mesajları **Meta / Twilio bulutuna** gider. Senin makinen `localhost` ise internetten erişilemez. **Çözüm:** Twilio WhatsApp Sandbox (veya Business) + **ngrok** (veya deploy) ile `https://.../webhook/whatsapp` adresini Twilio’ya tanımlamak.

Yerel / jüri öncesi test için Twilio olmadan:

```bash
curl -s -X POST "http://127.0.0.1:8000/webhook/whatsapp?format=json" \
  -F "Body=iade: elbise rengi farkli" \
  -F "From=whatsapp:+905551112233"
```

`?format=json` → Postman/curl için JSON cevap. Gerçek Twilio isteğinde `X-Twilio-Signature` varsa yanıt **TwiML** ile müşteriye gidebilir.

---

## API uçları (özet)

| Method | Endpoint | Açıklama |
|--------|----------|----------|
| GET | `/health` | API + DB kontrolü |
| GET | `/complaints` | Şikayetler (JSON) |
| PATCH | `/complaints/{id}/status` | Şikayet durumu |
| GET | `/return-items` | İade listesi |
| POST | `/return-items/{id}/ai-analyze` | CrewAI analizi |
| PATCH | `/return-items/{id}/decision` | Patron onayı; Twilio doluysa müşteriye mesaj dener |
| GET | `/orders`, `/orders/{code}` | Siparişler |
| GET | `/products`, `/stock-alerts` | Stok / ürün |
| POST | `/webhook/whatsapp` | Twilio form webhook |

---

## Proje yapısı (güncel)

```
AgentSync-Core/
├── app/
│   ├── agents/
│   │   ├── agents.py, tasks.py, crew.py
│   │   ├── customer_agent.py      # WhatsApp metni → şikayet/iade + DB
│   │   └── tools/db_tools.py
│   ├── api/endpoints/v1.py        # REST
│   ├── core/
│   │   ├── database.py
│   │   └── brand_config.py        # Butik / WhatsApp sabitleri
│   ├── services/
│   │   ├── whatsapp_service.py    # Twilio form parse
│   │   ├── twilio_notify.py       # Giden WA (opsiyonel)
│   │   └── return_pipeline.py     # AI analiz + demo yedek + otomatik onay
│   ├── models/models.py
│   ├── static/index.html          # Stitch tabanlı SPA (Türkçe, API ile şikayet tablosu)
│   ├── frontend/dashboard.py      # Streamlit
│   └── main.py                    # Webhook, static, health
├── docs/
│   ├── DEMO-VIDEO-SENARYOSU.md
│   ├── TEMA-VE-DOKUMANLAR.md
│   └── HACKATHON-GELISTIRME-SECENEKLERI.md
├── scripts/
│   ├── generate_mock_data.py
│   ├── migrate_postgres_return_items.sql
│   └── ...
├── Dockerfile
├── docker-compose.yml
└── requirements.txt
```

---

## Güvenlik

- **`.env` dosyasını Git’e eklemeyin.** API anahtarları ve veritabanı parolası sızarsa hemen **Neon + Gemini + Twilio** anahtarlarını yenileyin.
- Jüriye yalnızca **örnek** `.env` satırlarını (değersiz) gösterin.

---

## Takım (yapanlar)

| İsim soyisim | Rol / katkı |
|--------------|-------------|
| **Ömer Semih UZUN** | Backend, AI ajanlar (CrewAI / Gemini), API, dokümantasyon |
| **Dilara Şenay** | Grup yönetimi, frontend & entegrasyon (WhatsApp / panel) |
| **Ahmet Yasir Duman** | WhatsApp webhook, mesaj parse, müşteri ajanı entegrasyonu |
| **Hayrunnisa Önel** | Proje geliştirme ve operasyon katkıları |

*(İletişim bilgileri public repoda paylaşılmaz.)*

---

## Lisans

MIT License — YZTA 5.0 Hackathon projesi.
