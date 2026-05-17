import os
import time
import requests
import hmac
import hashlib
from telegram import Bot
import asyncio

# --- ΡΥΘΜΙΣΕΙΣ ---
API_KEY = os.getenv("BITGET_API_KEY")
API_SECRET = os.getenv("BITGET_API_SECRET")
API_PASSPHRASE = os.getenv("BITGET_PASSPHRASE")
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

BASE_URL = "https://api.bitget.com"
bot = Bot(token=TELEGRAM_TOKEN)

def get_timestamp():
    return str(int(time.time() * 1000))

def generate_signature(timestamp, method, request_path, body=""):
    message = timestamp + method + request_path + body
    mac = hmac.new(bytes(API_SECRET, encoding='utf-8'), bytes(message, encoding='utf-8'), digestmod=hashlib.sha256)
    return mac.hexdigest()

def get_headers(method, request_path, body=""):
    timestamp = get_timestamp()
    sign = generate_signature(timestamp, method, request_path, body)
    return {
        "ACCESS-KEY": API_KEY,
        "ACCESS-SIGN": sign,
        "ACCESS-PASSPHRASE": API_PASSPHRASE,
        "ACCESS-TIMESTAMP": timestamp,
        "Content-Type": "application/json"
    }

async def send_telegram_message(text):
    try:
        await bot.send_message(chat_id=TELEGRAM_CHAT_ID, text=text)
    except Exception as e:
        print(f"Telegram error: {e}")
        
