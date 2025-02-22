import requests
import os
from fastapi.responses import JSONResponse
from app.config import WHATSAPP_API_TOKEN, WHATSAPP_BUSINESS_ID

WHATSAPP_URL = f"https://graph.facebook.com/v21.0/{WHATSAPP_BUSINESS_ID}/messages"

async def process_message(request: dict):
    """Procesa los mensajes entrantes de WhatsApp y los imprime en consola."""
    try:
        entry = request["entry"][0]
        changes = entry["changes"][0]
        message = changes["value"]
        sender_id = message["messages"][0]["from"]
        text = message["messages"][0]["text"]["body"]

        # 📌 Imprimir mensaje en la consola
        print(f"📩 Nuevo mensaje recibido de {sender_id}: {text}")

        response_text = f"Recibido: {text}"
        send_whatsapp_message(sender_id, response_text)

        return JSONResponse(content={"status": "success", "received": text}, status_code=200)
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)

def send_whatsapp_message(recipient_id: str, text: str):
    """Envía un mensaje de WhatsApp."""
    headers = {
        "Authorization": f"Bearer {WHATSAPP_API_TOKEN}",
        "Content-Type": "application/json"
    }
    payload = {
        "messaging_product": "whatsapp",
        "to": recipient_id,
        "text": {"body": text}
    }

    response = requests.post(WHATSAPP_URL, json=payload, headers=headers)
    return response.json()
