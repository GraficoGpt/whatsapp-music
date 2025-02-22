from fastapi import FastAPI
from app.api import router

app = FastAPI(
    title="WhatsApp API",
    description="API para recibir y enviar mensajes de WhatsApp con FastAPI",
    version="1.0.0",
)

app.include_router(router)