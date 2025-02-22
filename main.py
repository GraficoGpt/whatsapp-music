from fastapi import FastAPI, Request
import requests

app = FastAPI()

# Configuración de credenciales
WHATSAPP_API_URL = "https://graph.facebook.com/v21.0/"
ACCESS_TOKEN = "EAATLiZB6FZBnwBOxGmFDF2R9KezJNd3uTaendPZA3ZCg38gWmy51gqZCrFzBkPSLBaDWsSh0oYNGa4gxUdKAgLzDWT5QYAIlZBSnYo9anIivIDJeFyC1nESMJuUrhre1vaURJ2kUO2kWbiEV9TbZBisfDDeTB3gWWnLF1uv24TCuomKq0aBNvysG4QXHqY7cE454wZDZD"
PHONE_NUMBER_ID = "613073168545315"
VERIFY_TOKEN = "1234567890"

@app.get("/")
async def root():
    return {"message": "Hello World"}

# 1. Verificación del Webhook
@app.get("/webhook")
async def verify_webhook(request: Request):
    mode = request.query_params.get("hub.mode")
    token = request.query_params.get("hub.verify_token")
    challenge = request.query_params.get("hub.challenge")

    if mode == "subscribe" and token == VERIFY_TOKEN:
        return int(challenge)

    return {"error": "Token de verificación incorrecto"}, 403

# 2. Recibir y reenviar mensajes de WhatsApp
@app.post("/webhook")
async def receive_message(request: Request):
    data = await request.json()

    try:
        if "entry" in data:
            for entry in data["entry"]:
                if "changes" in entry:
                    for change in entry["changes"]:
                        value = change.get("value", {})
                        if "messages" in value:
                            for message in value["messages"]:
                                sender = message["from"]
                                text = message["text"]["body"]

                                print(f"Mensaje recibido de {sender}: {text}")

                                # Enviar el mismo mensaje de vuelta al remitente
                                send_whatsapp_message(sender, f"Recibido: {text}")
    except Exception as e:
        print(f"Error procesando mensaje: {e}")

    return {"status": "ok"}

# 3. Enviar mensajes a WhatsApp
@app.post("/send")
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
        "recipient_type": "individual",
        "to": to,
        "type": "text",
        "text": {"body": text}
    }
    response = requests.post(url, json=payload, headers=headers)

    # Depuración: Imprimir la respuesta de WhatsApp API
    print(f"Respuesta de WhatsApp API: {response.json()}")

    return response.json()
