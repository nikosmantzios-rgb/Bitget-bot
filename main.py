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

BASE_URL = "https://vapi.bitget.com"
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

def check_balance():
    request_path = "/api/v2/mix/account/accounts?productType=USDT-FUTURES"
    headers = get_headers("GET", request_path)
    try:
        response = requests.get(BASE_URL + request_path, headers=headers)
        if response.status_code == 200:
            data = response.json()
            if data.get("code") == "00000":
                for acc in data.get("data", []):
                    if acc.get("marginCoin") == "USDT":
                        return float(acc.get("available", 0))
        return None
    except Exception as e:
        print(f"Error checking balance: {e}")
        return None

async def main():
    print("Bot started...")
    await send_telegram_message("🚀 Το Bitget Bot ξεκίνησε τη λειτουργία του!")
    
    while True:
        balance = check_balance()
        if balance is not None:
            print(f"Available Balance: {balance} USDT")
        else:
            print("Failed to fetch balance.")
        
        await asyncio.sleep(60)

if __name__ == "__main__":
    asyncio.run(main())
    
