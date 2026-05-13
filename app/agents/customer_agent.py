import os
import base64
import smtplib
import requests
from email.message import EmailMessage
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage
from dotenv import load_dotenv

from app.core.database import SessionLocal
from app.models import models
from twilio.rest import Client

load_dotenv()
USER_STATES = {}


# ─────────────────────────────────────────────
# YARDIMCI FONKSİYONLAR
# ─────────────────────────────────────────────

def notify_manager(details: str, customer_sender: str, media_url: str = None):
    """Yöneticiye WhatsApp bildirimi gönderir."""
    try:
        client = Client(os.getenv("TWILIO_ACCOUNT_SID"), os.getenv("TWILIO_AUTH_TOKEN"))
        body = (
            f"🚨 *SİSTEM BİLDİRİMİ*\n\n"
            f"👤 Müşteri: {customer_sender}\n"
            f"📋 Durum: {details}"
        )
        if media_url:
            body += f"\n🖼️ Görsel: {media_url}"
        client.messages.create(
            body=body,
            from_=os.getenv("TWILIO_WHATSAPP_FROM"),
            to=os.getenv("MANAGER_PHONE"),
        )
    except Exception as e:
        print(f"[Bildirim Hatası] {e}")


def send_supplier_email(products_to_order: str) -> bool:
    """Tedarikçiye profesyonel stok sipariş maili gönderir."""
    try:
        msg = EmailMessage()
        msg["Subject"] = "📦 Acil Stok Yenileme Talebi – AgentSync"
        msg["From"] = os.getenv("EMAIL_USER")
        msg["To"] = "onelhayrunnisa7@gmail.com"

        email_body = f"""\
Sayın Tedarikçimiz,

Umarız bu ileti sizi iyi bulur.

Sistemimiz tarafından gerçekleştirilen otomatik stok takibi sonucunda, \
aşağıdaki ürünlerin kritik stok seviyesinin altına düştüğü tespit edilmiştir. \
Operasyonel sürekliliğimizi koruyabilmek adına söz konusu ürünler için \
en kısa sürede sipariş işlemi başlatılmasına ihtiyaç duyulmaktadır.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📦 SİPARİŞ EDİLECEK ÜRÜNLER:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
{products_to_order}
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Sipariş onayı ve tahmini teslimat tarihi hakkında bilgi vermenizi rica eder, \
değerli iş birliğiniz için teşekkür ederiz.

Saygılarımızla,
AgentSync Operasyon Ekibi 🚀
"""
        msg.set_content(email_body)

        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls()
            server.login(os.getenv("EMAIL_USER"), os.getenv("EMAIL_PASS"))
            server.send_message(msg)
        return True
    except Exception as e:
        print(f"[Mail Hatası] {e}")
        return False


def send_daily_summary_to_manager() -> str:
    """
    Yöneticiye günlük sipariş özetini WhatsApp ile gönderir.
    Bu fonksiyon hem scheduler hem de Swagger endpoint'inden çağrılabilir.
    """
    db = SessionLocal()
    try:
        total = db.query(models.Order).count()
        kargoda = db.query(models.Order).filter(models.Order.status == "Kargoda").count()
        hazirlaniyor = db.query(models.Order).filter(models.Order.status == "Hazırlanıyor").count()
        teslim_edildi = db.query(models.Order).filter(models.Order.status == "Teslim Edildi").count()

        summary = (
            f"☀️ *Günaydın! Günlük Sipariş Özeti*\n\n"
            f"📦 Toplam Sipariş: {total}\n"
            f"🔧 Hazırlanıyor: {hazirlaniyor}\n"
            f"🚚 Kargoda: {kargoda}\n"
            f"✅ Teslim Edildi: {teslim_edildi}\n\n"
            f"⏰ Sistem sorunsuz çalışıyor. İyi günler dileriz!"
        )

        try:
            client = Client(os.getenv("TWILIO_ACCOUNT_SID"), os.getenv("TWILIO_AUTH_TOKEN"))
            client.messages.create(
                body=summary,
                from_=os.getenv("TWILIO_WHATSAPP_FROM"),
                to=os.getenv("MANAGER_PHONE"),
            )
        except Exception as e:
            print(f"[Günlük Özet Bildirim Hatası] {e}")

        return summary
    finally:
        db.close()


# ─────────────────────────────────────────────
# ANA AGENT FONKSİYONU
# ─────────────────────────────────────────────

def run_agent(message: str, sender: str, media_url: str = None) -> str:
    llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash", temperature=0.1)
    message_lower = message.strip().lower()
    state = USER_STATES.get(sender, {"step": "idle", "data": None})

    # 1. FOTOĞRAF ANALİZİ – HASARLI ÜRÜN TESPİTİ VE YÖNETİCİ BİLDİRİMİ
    if media_url:
        try:
            response = requests.get(
                media_url,
                auth=(os.getenv("TWILIO_ACCOUNT_SID"), os.getenv("TWILIO_AUTH_TOKEN")),
            )
            print(f"[DEBUG] Görsel indirme status: {response.status_code}")

            if response.status_code == 200:
                image_b64 = base64.b64encode(response.content).decode("utf-8")

                # Gemini için doğru format: inline_data
                image_part = {
                    "type": "image_url",
                    "image_url": {"url": f"data:image/jpeg;base64,{image_b64}"},
                }

                prompt = (
                   "Sen bir müşteri hizmetleri uzmanısın. "
                   "Görseldeki hasarı analiz et. "
                   "Sadece müşteriye gidecek kısa bir mesaj yaz, markdown kullanma, yıldız işareti koyma. "
                   "Mutlaka özür dile vesipariş kodunu iste mişteriden ürün değişimi veya iade yapılacağını belirt. Maksimum 2 cümle. "
                   "Sonra [YÖNETİCİ RAPORU] yaz ve hasarı 2 cümlede özetle."
                )

                ai_response = llm.invoke(
                    [HumanMessage(content=[{"type": "text", "text": prompt}, image_part])]
                ).content

                print(f"[DEBUG] AI Response: {ai_response}")

                if "[YÖNETİCİ RAPORU]" in ai_response:
                    parts = ai_response.split("[YÖNETİCİ RAPORU]")
                    customer_message = parts[0].strip()
                    manager_report = parts[1].strip()
                    notify_manager(manager_report, sender, media_url)
                    return customer_message

                return ai_response
            else:
                print(f"[DEBUG] Görsel indirilemedi, status: {response.status_code}")
                return "📸 Görseliniz sistemimize ulaştı, incelenmektedir."

        except Exception as e:
            print(f"[Görsel Analiz Hatası] {e}")
            return "📸 Görseliniz sistemimize ulaştı, incelenmektedir."

    # 2. SABAH GÜNLÜK ÖZET – MANUEL TETİKLEYİCİ (WhatsApp'tan)
    if "özet" in message_lower or "günaydın" in message_lower:
        return send_daily_summary_to_manager()

    # 3. TEDARİKÇİ ONAY MEKANİZMASI
    if state["step"] == "awaiting_approval" and "onayla" in message_lower:
        success = send_supplier_email(state["data"])
        USER_STATES[sender] = {"step": "idle", "data": None}
        if success:
            return "✅ Sipariş onaylandı! Tedarikçiye resmi mail başarıyla iletildi."
        return "⚠️ Mail gönderilemedi, lütfen e-posta ayarlarını kontrol edin."

    # 4. STOK SORGULAMA VE KRİTİK ÜRÜN TESPİTİ
    if "stok" in message_lower:
        db = SessionLocal()
        try:
            products = db.query(models.Product).all()
            msg = "📦 *Güncel Stok Durumu:*\n\n"
            critical_items = ""
            for p in products:
                status = "🔴" if p.stock <= p.critical_limit else "🟢"
                msg += f"{status} {p.name}: {p.stock} adet\n"
                if p.stock <= p.critical_limit:
                    critical_items += f"- {p.name} (Sipariş Miktarı: {p.order_amount} adet)\n"

            if critical_items:
                USER_STATES[sender] = {"step": "awaiting_approval", "data": critical_items}
                msg += (
                    "\n⚠️ *Kritik stok seviyesinde ürünler tespit edildi!*\n"
                    "Tedarikçiye sipariş maili göndermek için *ONAYLA* yazın."
                )
            return msg
        finally:
            db.close()

    # 5. SİPARİŞ TAKİBİ – KOD BEKLEME
    if state["step"] == "awaiting_order_code":
        db = SessionLocal()
        try:
            order = db.query(models.Order).filter(
                models.Order.order_code == message.strip().upper()
            ).first()
            USER_STATES[sender] = {"step": "idle", "data": None}
            if order:
                return (
                    f"🔍 *Sipariş Detayı – {order.order_code}*\n\n"
                    f"✅ Durum: {order.status}\n"
                    f"🚛 Kargo Firması: {order.cargo_company or 'Henüz atanmadı'}"
                )
            return "❌ Bu koda ait sipariş bulunamadı. Lütfen kodu kontrol edip tekrar deneyin."
        finally:
            db.close()

    if "sipariş" in message_lower and "nerede" in message_lower:
        USER_STATES[sender] = {"step": "awaiting_order_code", "data": None}
        return "📬 Sipariş kodunuzu paylaşır mısınız? (Örn: ORD-101)"

    # 6. STANDART GEMİNİ SOHBETİ
    return llm.invoke(
        f"Sen AgentSync adlı bir e-ticaret destek asistanısın. "
        f"Müşterilere nazik, çözüm odaklı ve kısa cevaplar veriyorsun. "
        f"Kullanıcı mesajı: {message}"
    ).content