from fastapi import APIRouter
from pydantic import BaseModel
from app.whatsapp import check_whatsapp_connection, process_message, verify_webhook, send_whatsapp_message

router = APIRouter()

class MessageRequest(BaseModel):
    """Modelo para enviar mensajes de WhatsApp."""
    recipient_id: str
    text: str

@router.get("/", tags=["WhatsApp"])
async def health_check():
    """Verifica la conexión con la API de WhatsApp."""
    return check_whatsapp_connection()

@router.get("/webhook", tags=["WhatsApp"])
async def verify(request: dict):
    """Verifica el webhook de WhatsApp."""
    return verify_webhook(request)

@router.post("/webhook", tags=["WhatsApp"])
async def webhook_handler(request: dict):
    """Procesa mensajes entrantes de WhatsApp."""
    return await process_message(request)

@router.post("/send-message", tags=["WhatsApp"], response_model=dict)
async def send_message(request: MessageRequest):
    """
    Envía un mensaje de WhatsApp.

    - **recipient_id**: Número de WhatsApp con código de país (ej. `573028336170`) El número al que se le enviará el mensaje.
    - **text**: Mensaje que se enviará.

    **Ejemplo de JSON de entrada:**
    ```json
    {
        "recipient_id": "573028336170",
        "text": "Hola, esto es un mensaje desde la API"
    }
    ```
    """
    response = send_whatsapp_message(request.recipient_id, request.text)
    return response
