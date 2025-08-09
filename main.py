from fastapi import FastAPI, Request
import httpx
import os

app = FastAPI()

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

TELEGRAM_API_URL = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"

@app.get("/")
async def root():
    return {"message": "Bot Webhook is running."}

@app.post("/webhook")
async def telegram_webhook(req: Request):
    data = await req.json()
    message = data.get("message", {}).get("text", "")
    sender = data.get("message", {}).get("chat", {}).get("id", "")

    if message.lower() in ["/start", "hi"]:
        await send_message(sender, "👋 Hello! The bot is running and ready to push alerts.")
    
    return {"ok": True}

async def send_message(chat_id, text):
    payload = {"chat_id": chat_id, "text": text}
    async with httpx.AsyncClient() as client:
        await client.post(TELEGRAM_API_URL, json=payload)
