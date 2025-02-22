# app/config.py
import os
from dotenv import load_dotenv

load_dotenv()

WHATSAPP_API_URL = os.getenv("WHATSAPP_API_URL")
ACCESS_TOKEN = os.getenv("ACCESS_TOKEN")
PHONE_NUMBER_ID = os.getenv("PHONE_NUMBER_ID")
VERIFY_TOKEN = os.getenv("VERIFY_TOKEN")

WHATSAPP_API_TOKEN = os.getenv("WHATSAPP_API_TOKEN")
TEST_PHONE_NUMBER = os.getenv("TEST_PHONE_NUMBER")
WHATSAPP_BUSINESS_ID = os.getenv("WHATSAPP_BUSINESS_ID")
