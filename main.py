from fastapi import FastAPI, Request
import requests
import os

app = FastAPI()

# Configuración de credenciales
WHATSAPP_API_URL = "https://graph.facebook.com/v21.0/"
ACCESS_TOKEN = "EAATLiZB6FZBnwBO317yNiPm2ZBYCI83yUvcB5EZBwRl2z1egPSyofn0nAQ2eBnHAI1zZCA4ZCCfgDrL4hTBXxyTZAtOpUlKxhhVfnOVO7vgDjBAPtPZA6EZAfDBl9Yzi9HyOI9xYVTyoHRkBJntnn0LxmaHszA4UEXqEeSf87BiqKymD5ff1A7J0KghgHi67XkdKnOXNc8hT8qTRmnxgYn17aUfPRwmOlVmktGK6aNJ0ZD"
PHONE_NUMBER_ID = "613073168545315"
VERIFY_TOKEN = "1234567890"

@app.get("/")
async def root():
    return {"message": "Hello World"}

# 1. Verificación del Webhook
@app.get("/webhook", summary="Verificar Webhook", description="Verifica el webhook de WhatsApp.")
async def verify_webhook(request: Request):
    mode = request.query_params.get("hub.mode")
    token = request.query_params.get("hub.verify_token")
    challenge = request.query_params.get("hub.challenge")

    if mode == "subscribe" and token == VERIFY_TOKEN:
        return int(challenge)

    return {"error": "Token de verificación incorrecto"}, 403

# 2. Recibir mensajes de WhatsApp
@app.post("/webhook")
async def receive_message(request: Request):
    data = await request.json()

    # Procesar mensaje recibido
    if "entry" in data and "changes" in data["entry"][0]:
        message = data["entry"][0]["changes"][0]["value"]
        if "messages" in message:
            sender = message["messages"][0]["from"]
            text = message["messages"][0]["text"]["body"]
            print(f"Mensaje recibido de {sender}: {text}")

            # Responder al mensaje
            send_whatsapp_message(sender, f"Recibido: {text}")

    return {"status": "ok"}

# 3. Enviar mensajes a WhatsApp
@app.post("/send", summary="Enviar Mensaje", description="Envía un mensaje a un número de WhatsApp.")
async def send_message(to: str, text: str):
    response = send_whatsapp_message(to, text)
    return response

# Función para enviar mensajes a WhatsApp
def send_whatsapp_message(to, text):
    url = f"{WHATSAPP_API_URL}{PHONE_NUMBER_ID}/messages"
    headers = {
        "Authorization": f"Bearer {ACCESS_TOKEN}",
        "Content-Type": "application/json"
    }
    payload = {
        "messaging_product": "whatsapp",
        "to": to,
        "text": {"body": text}
    }
    response = requests.post(url, json=payload, headers=headers)
    return response.json()
