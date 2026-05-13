def run_agent(message: str, sender: str):
    """
    WhatsApp / müşteri mesajları için hafif yönlendirme (ekip pipeline).
    İleride CrewAI veya gerçek ajan buraya bağlanır.
    """
    text = (message or "").lower()

    if "şikayet" in text:
        return {
            "priority": "HIGH",
            "response": "Şikayetiniz alındı. Öncelikli olarak inceleniyor.",
        }

    if "iade" in text:
        return {
            "priority": "MEDIUM",
            "response": "İade süreciniz başlatıldı.",
        }

    return {
        "priority": "LOW",
        "response": "Mesajınız alındı.",
    }
