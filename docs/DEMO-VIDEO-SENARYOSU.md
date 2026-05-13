# Demo video senaryosu (WhatsApp → sistem → AI → onay)

Bu akış **Linen Atölye Butik** ve iş hattı **`+90 545 829 48 10`** (`whatsapp:+905458294810`) ile anlatılır.

## Ön koşullar

1. Sanal ortam + bağımlılıklar: `pip install -r requirements.txt`
2. Mock veri: `python scripts/generate_mock_data.py`
3. Sunucu: `uvicorn app.main:app --reload --host 127.0.0.1 --port 8000`
4. **Otomatik zincir (video için önerilir)** — `.env` dosyasına ekleyin:
   ```env
   AGENTSYNC_DEMO_CHAIN=1
   AGENTSYNC_DEMO_AUTO_APPROVE=1
   ```
   - `AGENTSYNC_DEMO_CHAIN`: iade mesajı webhook’tan düştükten sonra arka planda **AI analizi** tetiklenir.
   - `AGENTSYNC_DEMO_AUTO_APPROVE`: sonuç **Approve** ve risk eşiğin altındaysa kayıt **Approved** olur (Twilio anahtarları varsa kısa WA metni denenir).
5. **GEMINI_API_KEY** yoksa bile demo çalışır: `AGENTSYNC_DEMO_FALLBACK_AI=1` (varsayılan 1) ile metin tabanlı yedek karar üretilir.

## OBS / ekran kaydı sırası (önerilen 2–3 dk)

| # | Ekranda ne | Ne yapıyorsun |
|---|----------------|----------------|
| 1 | Tarayıcı `http://127.0.0.1:8000` | Giriş: `patron@agentsync.com` / `patron123` |
| 2 | **Şikayetler** | Listenin API’den dolduğunu göster (üstte butik hattı kaydı). |
| 3 | Terminal veya Postman | Aşağıdaki **iade** isteğini at (senaryo: müşteri mesaj atıyor). |
| 4 | `http://127.0.0.1:8000/docs` | `GET /return-items` — yeni satır, `ai_verdict`, `ai_risk_score`, `status`. |
| 5 | (Zincir kapalıysa) | `POST /return-items/{id}/ai-analyze` sonra `PATCH /return-items/{id}/decision?status=Approved` ile patron onayı göster. |

### Terminal — müşteri iadesi (Twilio imzası yok → JSON)

```powershell
curl.exe -s -X POST "http://127.0.0.1:8000/webhook/whatsapp?format=json" ^
  -F "Body=Merhaba, elbise rengi siteden farkli geldi, iade istiyorum" ^
  -F "From=whatsapp:+905458294810"
```

Beklenen (demo zinciri açıkken): JSON içinde `return_item_id`, `ai_pipeline` (`verdict`, `risk_score`), isteğe bağlı `demo_auto_approve`.

### Şikayet (şikayet tablosuna düşer)

```powershell
curl.exe -s -X POST "http://127.0.0.1:8000/webhook/whatsapp?format=json" ^
  -F "Body=sikayet: kargo gecikti" ^
  -F "From=whatsapp:+905458294810"
```

## Jüriye tek cümle

“Müşteri WhatsApp’tan iade/şikayet yazar; kayıt panele düşer; çoklu ajan iadeyi değerlendirir; müşteri haklıysa onay ve bildirim hattı devreye girer.”
