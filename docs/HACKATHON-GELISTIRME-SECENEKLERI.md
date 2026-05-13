# AgentSync — Hackathon ekibi geliştirme seçenekleri

YZTA / KOBİ problemi ve jüri değerlendirmesi için öncelik sırası. Süre kısıtlı olduğundan her maddeye **etki / efor** notu verildi.

## Hızlı durum (Docker)

- API: `http://localhost:8000` — Swagger: `/docs`
- Streamlit demo: `http://localhost:8501`
- `docker compose up --build` çalıştıktan sonra bu adreslerden doğrula.

---

## P0 — Jüriye “bitti” gösteren hat (yüksek etki, düşük-orta efor)

| Seçenek | Ne kazanırsınız | Not |
|--------|------------------|-----|
| **3 dakikalık demo senaryosu** | Sipariş sorgusu (ORD-…) + iade/şikayet metni + (varsa) admin panelde 1 ekran | Tek metin dosyası + ekip provası; kod değil, sunum güveni. |
| **Uçtan uca tek video kaydı** | Canlı demo riskini azaltır | Yedek: internet kesilirse gösterilecek kısa ekran kaydı. |
| **README’de “Hackathon bölümü”** | Problem → çözüm → mimari → nasıl çalıştırılır | Jüri repo klonlarsa ilk 5 dakikada çalışır. |

---

## P1 — Teknik farklılaşma (AI / operasyon)

| Seçenek | Etki | Efor | Bağımlılık |
|--------|------|------|-------------|
| **`run_agent` → gerçek CrewAI / Gemini`** | “Rule-based değil, çoklu ajan” iddiası güçlenir | Orta–yüksek | API key, rate limit |
| **İade hattında Vision + DB tool (mevcut crew ile)** | README’deki mimariyle birebir örtüşür | Orta | `return_items` + görsel örnek |
| **WhatsApp → TwiML cevap** | Twilio’da gerçek kullanıcıya metin gider | Orta | Twilio sandbox / numara |
| **`parse_twilio_message` ile medya (ses/görsel) şeması** | Multimodal hikâye | Orta | Depolama / transkripsiyon maliyeti |

---

## P2 — Güvenilirlik ve “prod kokusu”

| Seçenek | Etki | Efor |
|--------|------|------|
| **Human-in-the-loop (patron onayı) tek ekran + API** | Hackathon temasına uygun etik / kontrol | Orta |
| **Sağlık endpoint’i + basit logging** | “Sistem izlenebilir” mesajı | Düşük |
| **Hata durumlarında anlamlı Türkçe mesaj** | Demo sırasında kırılma hissi azalır | Düşük |

---

## P3 — Paralel iş (ekip)

| Alan | Kim | Çıktı |
|------|-----|--------|
| **Demo + sunum** | 1 kişi | Script, zaman çizelgesi, yedek video |
| **Backend + AI** | 1–2 kişi | Webhook, agent, API stabilitesi |
| **UI / SPA** | 1 kişi | 2–3 kritik ekran “parlak” |
| **DevOps** | 0.5 kişi | Docker, `.env` örneği, çalıştırma kontrol listesi |

---

## Önerilen sprint sırası (yarışma modu)

1. P0 demo + README — **bugün**
2. En riskli teknik parça (genelde **AI veya Twilio canlı**) — **erken deneme**
3. P1’den **en fazla 1 büyük** özellik — kalan süreye göre
4. P2 sadece demo öncesi buffer varsa

---

## Bilinçli geri alma / branch notu

`develop` ile `main` farklı ilerlediyse: yarışma günü **hangi branch’in demo** olacağını sabitleyin; diğerine sadece cherry-pick veya tek merge ile çekin. İki hat aynı anda “gerçek” olmasın.

---

## Sonraki karar (ekip toplantısı 10 dk)

- [ ] Demo branch: `develop` / `main` / başka?
- [ ] Canlı Twilio şart mı, yoksa Postman + video yeterli mi?
- [ ] “Vay be” dedirtecek **tek** AI özelliği hangisi? (Çoklu seçim = süre biter.)
