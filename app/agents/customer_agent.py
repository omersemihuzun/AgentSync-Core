def run_agent(message, sender):

    if "şikayet" in message.lower():
        return {
            "priority": "HIGH",
            "response": "Şikayetiniz alındı. Öncelikli olarak inceleniyor."
        }

    elif "iade" in message.lower():
        return {
            "priority": "MEDIUM",
            "response": "İade süreciniz başlatıldı."
        }

    else:
        return {
            "priority": "LOW",
            "response": "Mesajınız alındı."
        }