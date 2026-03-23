import os
import requests
from dotenv import load_dotenv

def send_message(chat_id: str, message: str) -> dict:
    load_dotenv()

    WAHA_API_KEY = os.getenv("WAHA_API_KEY", "")
    WAHA_API_URL = os.getenv("WAHA_API_URL", "")
    WAHA_SESSION_NAME = os.getenv("WAHA_SESSION_NAME", "")

    headers = {
        "X-Api-Key": WAHA_API_KEY,
    }

    payload = {
        "session": WAHA_SESSION_NAME,
        "chatId": chat_id,
        "text": message
    }

    response = requests.post(
        url=f"{WAHA_API_URL}/sendText",
        headers=headers,
        json=payload
    )

    return response.json()