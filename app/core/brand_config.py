"""YZTA / demo — marka; WhatsApp numarasi .env ile (repoda gercek numara tutulmaz)."""

import os

BOUTIQUE_NAME = os.getenv("BOUTIQUE_NAME", "Linen Atölye Butik")
BOUTIQUE_SECTOR_TR = "Butik giyim (kadın / sezon koleksiyonu)"
# Demo varsayilan: gercek is hatti icin .env → BOUTIQUE_WHATSAPP_E164 ve BOUTIQUE_WHATSAPP_DISPLAY
WHATSAPP_E164 = os.getenv("BOUTIQUE_WHATSAPP_E164", "whatsapp:+905551112233")
WHATSAPP_DISPLAY = os.getenv("BOUTIQUE_WHATSAPP_DISPLAY", "+90 555 111 22 33")
TAGLINE_TR = "Butik giyim: iade kontrolu, siparis ve WhatsApp musteri mesajlari tek merkezde."
