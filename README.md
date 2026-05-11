# AgentSync AI (AgentSync-Core)

## YZTA 5.0 Hackathon Projesi

AgentSync AI, KOBİ'lerin satış sonrası operasyonlarını (iade, şikayet) ve depo yönetimlerini tek bir merkezden otonom ajanlarla yönetmesini sağlayan akıllı bir platformdur.

### Temel Özellikler
1. **Çoklu Ajan (Multi-Agent) Sistemi:** Şikayet analizi, risk analizi ve otonom görevlendirme işlemleri CrewAI altyapısıyla çalışır.
2. **WhatsApp & Multimodal Arayüz:** Yöneticiler WhatsApp üzerinden sesli mesaj göndererek veya belge/fiş fotoğrafı atarak sistemi klavye kullanmadan yönetebilir. (Whisper & Gemini Vision destekli)
3. **Merkezi Dashboard:** Streamlit tabanlı, FastAPI ile haberleşen hızlı analitik paneli.

### Kurulum (Development)

```bash
# 1. Kütüphaneleri kurun
pip install -r requirements.txt

# 2. .env dosyasını oluşturun ve API anahtarlarınızı girin
# GEMINI_API_KEY=your_key
# TWILIO_AUTH_TOKEN=your_token

# 3. FastAPI sunucusunu başlatın
uvicorn main:app --reload
```
