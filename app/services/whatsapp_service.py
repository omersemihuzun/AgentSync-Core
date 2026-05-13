from typing import Optional

def parse_twilio_message(form_data: dict) -> dict:
    """
    Twilio'dan gelen form_data'yı analiz eder.
    Mesaj tipini (text, audio, image) belirler.
    """
    result = {
        "type": None,
        "content": None,
        "media_url": None,
        "sender": form_data.get("From", ""),
        "body": form_data.get("Body", "").strip()
    }

    num_media = int(form_data.get("NumMedia", 0))

    if num_media > 0:
        media_type = form_data.get("MediaContentType0", "")
        media_url = form_data.get("MediaUrl0", "")

        if "audio" in media_type:
            result["type"] = "audio"
            result["media_url"] = media_url

        elif "image" in media_type:
            result["type"] = "image"
            result["media_url"] = media_url

    elif result["body"]:
        result["type"] = "text"
        result["content"] = result["body"]

    return result